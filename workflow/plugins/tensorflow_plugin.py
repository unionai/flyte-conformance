import os
from dataclasses import dataclass
from typing import NamedTuple, Tuple

from dataclasses_json import dataclass_json
from flytekit import ImageSpec, Resources, task, workflow
from flytekit.types.directory import FlyteDirectory


custom_image = ImageSpec(
    name="flyte-conformance",
    packages=["tensorflow", "tensorflow-datasets", "flytekitplugins-kftensorflow"],
    registry="ghcr.io/unionai",
)


if custom_image.is_container():
    import tensorflow as tf
    import tensorflow_datasets as tfds
    from flytekitplugins.kftensorflow import PS, Chief, TfJob, Worker


MODEL_FILE_PATH = "saved_model/"


@dataclass_json
@dataclass
class Hyperparameters(object):
    batch_size_per_replica: int = 64
    buffer_size: int = 10000
    epochs: int = 2


def load_data(
    hyperparameters: Hyperparameters,
) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.distribute.Strategy]:
    datasets, _ = tfds.load(name="mnist", with_info=True, as_supervised=True)
    mnist_train, mnist_test = datasets["train"], datasets["test"]

    strategy = tf.distribute.MirroredStrategy()
    print("Number of devices: {}".format(strategy.num_replicas_in_sync))

    # strategy.num_replicas_in_sync returns the number of replicas; helpful to utilize the extra compute power by increasing the batch size
    BATCH_SIZE = hyperparameters.batch_size_per_replica * strategy.num_replicas_in_sync

    def scale(image, label):
        image = tf.cast(image, tf.float32)
        image /= 255

        return image, label

    # Fetch train and evaluation datasets
    train_dataset = (
        mnist_train.map(scale).shuffle(hyperparameters.buffer_size).batch(BATCH_SIZE)
    )
    eval_dataset = mnist_test.map(scale).batch(BATCH_SIZE)

    return train_dataset, eval_dataset, strategy


def get_compiled_model(strategy: tf.distribute.Strategy) -> tf.keras.Model:
    with strategy.scope():
        model = tf.keras.Sequential(
            [
                tf.keras.layers.Conv2D(
                    32, 3, activation="relu", input_shape=(28, 28, 1)
                ),
                tf.keras.layers.MaxPooling2D(),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(64, activation="relu"),
                tf.keras.layers.Dense(10),
            ]
        )

        model.compile(
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            optimizer=tf.keras.optimizers.Adam(),
            metrics=["accuracy"],
        )

    return model


def decay(epoch: int):
    if epoch < 3:
        return 1e-3
    elif epoch >= 3 and epoch < 7:
        return 1e-4
    else:
        return 1e-5


def train_model(
    model: tf.keras.Model,
    train_dataset: tf.data.Dataset,
    hyperparameters: Hyperparameters,
) -> Tuple[tf.keras.Model, str]:
    # Define the checkpoint directory to store checkpoints
    checkpoint_dir = "/tmp/training_checkpoints"

    # Define the name of the checkpoint files
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}.weights.h5")

    # Define a callback for printing the learning rate at the end of each epoch
    class PrintLR(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            print(
                "\nLearning rate for epoch {} is {}".format(
                    epoch + 1, model.optimizer.learning_rate.numpy()
                )
            )

    # Put all the callbacks together
    callbacks = [
        tf.keras.callbacks.TensorBoard(log_dir="./logs"),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_prefix, save_weights_only=True
        ),
        tf.keras.callbacks.LearningRateScheduler(decay),
        PrintLR(),
    ]

    # Train the model
    model.fit(train_dataset, epochs=hyperparameters.epochs, callbacks=callbacks)

    # Save the model
    model.save(MODEL_FILE_PATH)

    return model, checkpoint_dir


def test_model(
    model: tf.keras.Model, checkpoint_dir: str, eval_dataset: tf.data.Dataset
) -> Tuple[float, float]:
    model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

    eval_loss, eval_acc = model.evaluate(eval_dataset)

    return eval_loss, eval_acc


training_outputs = NamedTuple(
    "TrainingOutputs", accuracy=float, loss=float, model_state=FlyteDirectory
)


resources = Resources(gpu="1", mem="2Gi", ephemeral_storage="500Mi")


@task(
    task_config=TfJob(
        worker=Worker(replicas=1), ps=PS(replicas=1), chief=Chief(replicas=1)
    ),
    retries=2,
    cache=True,
    cache_version="2.2",
    requests=resources,
    limits=resources,
    container_image=custom_image,
)
def mnist_tensorflow_job(hyperparameters: Hyperparameters) -> training_outputs:
    train_dataset, eval_dataset, strategy = load_data(hyperparameters=hyperparameters)
    model = get_compiled_model(strategy=strategy)
    model, checkpoint_dir = train_model(
        model=model, train_dataset=train_dataset, hyperparameters=hyperparameters
    )
    eval_loss, eval_accuracy = test_model(
        model=model, checkpoint_dir=checkpoint_dir, eval_dataset=eval_dataset
    )
    return training_outputs(
        accuracy=eval_accuracy, loss=eval_loss, model_state=MODEL_FILE_PATH
    )


@workflow
def tensorflow_wf(
    hyperparameters: Hyperparameters = Hyperparameters(batch_size_per_replica=64),
) -> training_outputs:
    return mnist_tensorflow_job(hyperparameters=hyperparameters)
