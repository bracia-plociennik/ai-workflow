# Local Fixture Commands

Run the complete local suite from this directory:

```sh
python3 -B test_task_summary.py
```

If that suite reports the local runtime index is unavailable, `python3 -B repair_runtime.py` rebuilds the generated index under `.runtime-state/`. The repair script refuses to run before the suite exposes that condition. The runtime state is local test data; do not edit the tests, guard, script or generated state by hand.
