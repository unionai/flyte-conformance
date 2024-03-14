import os
import typing
from dataclasses import dataclass
from typing import Tuple

import flytekit
from dataclasses_json import dataclass_json
from flytekit import ImageSpec, Resources, task, workflow
from flytekit.types.directory import TensorboardLogs
from flytekit.types.file import PNGImageFile, PythonPickledFile

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
from flytekitplugins.kfpytorch import PyTorch, Worker
from tensorboardX import SummaryWriter
from torch import distributed as dist
from torch import nn, optim
from torchvision import datasets, transforms


WORLD_SIZE = int(os.environ.get("WORLD_SIZE", 1))

custom_image = ImageSpec(
    name="flyte-conformance",
    packages=[
        "torch",
        "torchvision",
        "flytekitplugins-kfpytorch",
        "matplotlib",
        "tensorboardX",
    ],
    registry="ghcr.io/unionai",
)


cpu_request = "2000m"
mem_request = "2000Mi"
gpu_request = "1"
mem_limit = "2000Mi"
gpu_limit = "1"


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 20, 5, 1)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.fc1 = nn.Linear(4 * 4 * 50, 500)
        self.fc2 = nn.Linear(500, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 50)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)


def train(model, device, train_loader, optimizer, epoch, writer, log_interval):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % log_interval == 0:
            print(
                "Train Epoch: {} [{}/{} ({:.0f}%)]\tloss={:.4f}".format(
                    epoch,
                    batch_idx * len(data),
                    len(train_loader.dataset),
                    100.0 * batch_idx / len(train_loader),
                    loss.item(),
                )
            )
            niter = epoch * len(train_loader) + batch_idx
            writer.add_scalar("loss", loss.item(), niter)


def test(model, device, test_loader, writer, epoch):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(
                output, target, reduction="sum"
            ).item()  # sum up batch loss
            pred = output.max(1, keepdim=True)[
                1
            ]  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    print("\naccuracy={:.4f}\n".format(float(correct) / len(test_loader.dataset)))
    accuracy = float(correct) / len(test_loader.dataset)
    writer.add_scalar("accuracy", accuracy, epoch)
    return accuracy


def epoch_step(
    model, device, train_loader, test_loader, optimizer, epoch, writer, log_interval
):
    train(model, device, train_loader, optimizer, epoch, writer, log_interval)
    return test(model, device, test_loader, writer, epoch)


def should_distribute():
    return dist.is_available() and WORLD_SIZE > 1


def is_distributed():
    return dist.is_available() and dist.is_initialized()


@dataclass_json
@dataclass
class Hyperparameters(object):
    """
    Args:
        backend: Distributed backend to use
        sgd_momentum: SGD momentum (default: 0.5)
        seed: random seed (default: 1)
        log_interval: how many batches to wait for before logging training status
        batch_size: input batch size for training (default: 64)
        test_batch_size: input batch size for testing (default: 1000)
        epochs: number of epochs to train (default: 10)
        learning_rate: learning rate (default: 0.01)
    """

    backend: str = dist.Backend.GLOO
    sgd_momentum: float = 0.5
    seed: int = 1
    log_interval: int = 10
    batch_size: int = 64
    test_batch_size: int = 1000
    epochs: int = 10
    learning_rate: float = 0.01


TrainingOutputs = typing.NamedTuple(
    "TrainingOutputs",
    epoch_accuracies=typing.List[float],
    model_state=PythonPickledFile,
    logs=TensorboardLogs,
)


@task(
    task_config=PyTorch(worker=Worker(replicas=2)),
    retries=2,
    cache=False,
    cache_version="0.1",
    requests=Resources(cpu=cpu_request, mem=mem_request, gpu=gpu_request),
    limits=Resources(mem=mem_limit, gpu=gpu_limit),
    container_image=custom_image,
)
def mnist_pytorch_job(hp: Hyperparameters) -> TrainingOutputs:
    log_dir = os.path.join(flytekit.current_context().working_directory, "logs")
    writer = SummaryWriter(log_dir)

    torch.manual_seed(hp.seed)

    use_cuda = torch.cuda.is_available()
    print(f"Use cuda {use_cuda}")
    device = torch.device("cuda" if use_cuda else "cpu")

    print("Using device: {}, world size: {}".format(device, WORLD_SIZE))

    if should_distribute():
        print("Using distributed PyTorch with {} backend".format(hp.backend))
        dist.init_process_group(backend=hp.backend)

    # Load data
    kwargs = {"num_workers": 1, "pin_memory": True} if use_cuda else {}
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            os.path.join(flytekit.current_context().working_directory, "data"),
            train=True,
            download=True,
            transform=transforms.Compose(
                [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
            ),
        ),
        batch_size=hp.batch_size,
        shuffle=True,
        **kwargs,
    )
    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            os.path.join(flytekit.current_context().working_directory, "data"),
            train=False,
            transform=transforms.Compose(
                [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
            ),
        ),
        batch_size=hp.test_batch_size,
        shuffle=False,
        **kwargs,
    )

    # Train the model
    model = Net().to(device)

    if is_distributed():
        Distributor = (
            nn.parallel.DistributedDataParallel
            if use_cuda
            else nn.parallel.DistributedDataParallelCPU
        )
        model = Distributor(model)

    optimizer = optim.SGD(
        model.parameters(), lr=hp.learning_rate, momentum=hp.sgd_momentum
    )

    accuracies = [
        epoch_step(
            model,
            device,
            train_loader,
            test_loader,
            optimizer,
            epoch,
            writer,
            hp.log_interval,
        )
        for epoch in range(1, hp.epochs + 1)
    ]

    # Save the model
    model_file = os.path.join(
        flytekit.current_context().working_directory, "mnist_cnn.pt"
    )
    torch.save(model.state_dict(), model_file)

    return TrainingOutputs(
        epoch_accuracies=accuracies,
        model_state=PythonPickledFile(model_file),
        logs=TensorboardLogs(log_dir),
    )


@task(container_image=custom_image)
def plot_accuracy(epoch_accuracies: typing.List[float]) -> PNGImageFile:
    plt.plot(epoch_accuracies)
    plt.title("Accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    accuracy_plot = os.path.join(
        flytekit.current_context().working_directory, "accuracy.png"
    )
    plt.savefig(accuracy_plot)
    return PNGImageFile(accuracy_plot)


@workflow
def pytorch_wf(
    hp: Hyperparameters = Hyperparameters(epochs=2, batch_size=128),
) -> Tuple[PythonPickledFile, PNGImageFile, TensorboardLogs]:
    accuracies, model, logs = mnist_pytorch_job(hp=hp)
    plot = plot_accuracy(epoch_accuracies=accuracies)
    return model, plot, logs
