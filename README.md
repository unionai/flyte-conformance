# flyte-conformance
A repository running the Flyte conformance tests

## Summary
The Flyte conformance test suite is a series of tests
that are run against a Flyte deployment to ensure that it is functioning correctly.

## Integration Tests
It contains a bunch of subworkflows that are used to test various features of Flyte, including:
- The examples in flytesnacks.
- Flyte agents. (BigQuery, Airflow, sensor, etc.)
- Flyte plugins. (Tensorflow, Pytorch, Pandera, etc.)
- Others (e.g. Failure node, pod template, array node, etc.)


## Functional Tests
It uses flytekit remote to run the tasks/workflows to test the functionality of Flyte. For example,
- Verify whether the outputs are being cached
- Verify whether the cache can be overridden
- Verify whether Flyte deck is working
- Verify whether flytekit remote is functioning properly.

## Running the tests

### FlyteSnacks Integration Tests
```bash
pyflyte run --remote --project flyte-conformance --domain development integration_tests.py flytesnacks_wf
```

### FlytePlugins Integration Tests
```bash
pyflyte run --remote integration_tests.py flyte_plugin_wf
```

### FlyteAgents Integration Tests
```bash
pyflyte run --remote integration_tests.py flyte_agent_wf
```

### FlyteSnacks Integration Tests
```bash
pyflyte run --remote integration_tests.py flytesnacks_wf
```

### FlyteConformance Integration Tests
Any tests that cannot be added to Flytesnacks will be included in the flyte-conformance tests.
```bash
pyflyte run --remote integration_tests.py flyte_conformance_wf
```

### Functional Tests
```bash
python functional_tests.py
```