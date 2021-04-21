import numpy
import pytest
from .mocks.DataStub import DataStub
from RIAssigner.compute import Kovats


@pytest.fixture
def indexed_data():
    retention_times = [3.5, 4.68, 5.12, 7.31, 9.01, 9.08]
    retention_indices = [700, 800, 900, 1000, 1100, 1200]
    return DataStub(retention_times, retention_indices)


@pytest.fixture
def non_indexed_data():
    retention_times = [3.99, 4.32, 4.21, 5.83, 6.55, 9.05, 7.02, 8.65]
    return DataStub(retention_times, [])


def test_construct():
    compute = Kovats()
    assert compute is not None


def test_exception_reference_none(non_indexed_data):
    method = Kovats()
    with pytest.raises(AssertionError) as exception:
        method.compute(non_indexed_data, None)

    message = exception.value.args[0]
    assert exception.typename == "AssertionError"
    assert message == "Reference data is 'None'."


def test_exception_query_none(indexed_data):
    method = Kovats()
    with pytest.raises(AssertionError) as exception:
        method.compute(None, indexed_data)

    message = exception.value.args[0]
    assert exception.typename == "AssertionError"
    assert message == "Query data is 'None'."


def test_compute_ri(non_indexed_data, indexed_data):
    method = Kovats()

    expected = [1607, 1632, 1624, 1748, 1804, 1996, 1840, 1965]
    actual = method.compute(non_indexed_data, indexed_data)

    numpy.testing.assert_array_equal(actual, expected)
