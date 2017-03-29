import pytest


def something(duration=0.000001):
    """
    Function that needs some serious benchmarking.
    """
    import time
    time.sleep(duration)
    # You may return anything you want, like the result of a computation
    return 123


@pytest.mark.benchmark(
    group="group-name",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    disable_gc=True,
    warmup=False
)
def test_my_stuff(benchmark):
    # benchmark something
    result = benchmark(something)

    # Extra code, to verify that the run completed correctly.
    # Sometimes you may want to check the result, fast functions
    # are no good if they return incorrect results :-)
    assert result == 123


def test_micro_benchmark(self):
    import cProfile
    cProfile.run('re.compile("foo|bar")')
