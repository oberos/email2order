from src.customers.customer_b import CustomerBExporter


def test_Customer_aExporter_initialize_config():
    mocked_filepath = 'Some/path/to_file'
    tested_object = CustomerBExporter()
    tested_object.initialize_config(mocked_filepath)
    assert tested_object.file_path == mocked_filepath

# TODO add more UT