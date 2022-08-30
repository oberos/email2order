from src.customers.customer_a import Customer_aExporter


def test_Customer_aExporter_initialize_config():
    mocked_filepath = 'Some/path/to_file'
    tested_object = Customer_aExporter()
    tested_object.initialize_config(mocked_filepath)
    assert tested_object.file_path == mocked_filepath


def test_Customer_aExporter_extract_data():
    mocked_filepath = 'tests/files/customer_a.csv'
    tested_object = Customer_aExporter()
    tested_object.initialize_config(mocked_filepath)
    result = tested_object.extract_data()
    expected_result = {
        'comments': '',
        'company_name': 'Customer_a',
        'company_number': '100001',
        'cust_ref': 'test customer reference',
        'customer_order_date': '21/02/2022',
        'error': '',
        'error_description': '',
        'order_number': 'test order number',
        'rows': [
            {'item': '200088', 'price': 15.0, 'qty': '10'},
            {'item': '200089', 'price': 21.0, 'qty': '20'}
        ]
    }
    assert result.dict() == expected_result
