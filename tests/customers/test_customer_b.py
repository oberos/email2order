from src.customers.customer_b import Customer_bExporter


def test_Customer_aExporter_initialize_config():
    mocked_filepath = 'Some/path/to_file'
    tested_object = Customer_bExporter()
    tested_object.initialize_config(mocked_filepath)
    assert tested_object.file_path == mocked_filepath

# TODO add more UT