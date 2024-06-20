# flyte-conformance
A repository running the Flyte conformance tests

## Summary
The Flyte conformance test suite is a series of tests
that are run against a Flyte deployment to ensure that it is functioning correctly.


## Running the integration tests

### FlyteSnacks
Make sure all the flytesnacks are working correctly.
```bash
make flytesnacks
```

### FlytePlugins
- Test backend plugin, such as Tensorflow, Pytorch, Spark, etc.
- Test flytekit plugin, such as flyteinteractive, mlflow, pandera, etc.
```bash
make flyteplugins
```

### FlyteAgents
Test all the agents in flytekit, including BigQuery, Airflow, sensor, OpenAI, etc.
```bash
make flyteagents
```

### FlyteConformance Integration Tests
Any tests that cannot be added to Flytesnacks will be included in the flyte-conformance tests.
- Failure node, pod template, array node, image spec, etc
```bash
make flyte-conformance
```

### Functional Tests

It uses flytekit remote to run the tasks/workflows to test the functionality of Flyte. For example,
- Verify whether the outputs are being cached
- Verify whether the cache can be overridden
- Verify whether Flyte deck is working
- Verify whether flytekit remote is functioning properly.

```bash
make functional_tests
```