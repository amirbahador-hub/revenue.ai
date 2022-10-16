import pytest
from run import read_file, validate_dataset

@pytest.fixture
def dataset_errors():
    with open("test.csv", 'rb') as file:
        return validate_dataset(read_file(file))
 
def test_region_name(dataset_errors) -> None:
    assert dataset_errors[0] == "order 292494523 -> region Sub-Saharan Africa is incorrect"

def test_priority_value(dataset_errors) -> None:
    assert dataset_errors[1] == "order 292494523 -> priority code L is incorrect"

def test_total_profit(dataset_errors) -> None:
    assert dataset_errors[2] == "order 292494523 -> total profit should not be less than 1000"

def test_total_cost_limit(dataset_errors) -> None:
    assert dataset_errors[3] == "order 292494523 -> total cost should not be greater than 5000000"

def test_order_date(dataset_errors) -> None:
    assert dataset_errors[4] == "order 292494523 -> order date 1/27/2013 should not be greater than 2/28/2012"

def test_total_revenue(dataset_errors) -> None:
    assert dataset_errors[5] == "order 292494523 -> total revenue 29200252.64 is not equal to 2920025.64"

def test_total_cost(dataset_errors) -> None:
    assert dataset_errors[6] == "order 292494523 -> total cost 23539202.64 is not equal to 2353920.64"
