from src.systems import LocalSystem, LOCAL_SYSTEM_DATABASE
import models


def test_LocalSystem_create_order_error():
    tested_object = LocalSystem()
    results = tested_object.create_order(models.Order(company_name="Customer_a"))
    assert results == models.SystemOrderResults(status_code=501, error='Somesing is no yes')
    assert len(LOCAL_SYSTEM_DATABASE) == 0


def test_LocalSystem_create_order():
    test_order = models.Order()
    tested_object = LocalSystem()
    results = tested_object.create_order(test_order)
    assert results == models.SystemOrderResults(status_code=201)
    expected_result = {
        'id': 1,
        'details': test_order.dict()
    }
    assert LOCAL_SYSTEM_DATABASE == [expected_result]
