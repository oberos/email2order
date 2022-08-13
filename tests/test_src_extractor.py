from unittest.mock import patch, MagicMock

from src.extractor import read_exporter, Converter
from src.systems import System
import models


class MockedCustomer:
    pass


class MockedCustomer2:
    pass


class MockedSystem(System):
    def __init__(self, is_error: bool = False) -> None:
        self.__is_error = is_error

    def create_order(self, order_info: models.Order, customer_name: str) -> models.SystemOrderResults:
        if self.__is_error is True:
            return models.SystemOrderResults(status_code=500, error='Mocked_error')
        return models.SystemOrderResults(status_code=201)


MockedMAPPING = {
    'Mocked_customer_1': MockedCustomer(),
    'Mocked_customer_2': MockedCustomer2()
}

CUSTOMER_DATA = models.CustomerData(
        name='Customer1',
        filename='SomeFile.txt',
        contentBytes='File_in_base64_format'
    )


@patch("src.extractor.MAPPING", MockedMAPPING)
def test_read_exporter():
    result = read_exporter('Mocked_customer_1')
    assert isinstance(result, MockedCustomer)


@patch("src.extractor.MAPPING", MockedMAPPING)
def test_read_exporter_customer_not_found():
    result = read_exporter('Mocked_customer_not_exists')
    assert result is None


def test_Converter_init():
    system = MockedSystem()
    tested_object = Converter(CUSTOMER_DATA, system)
    assert tested_object.customer_data_model == CUSTOMER_DATA
    assert tested_object.temp_file_name == ''
    assert tested_object.system == system


@patch("src.extractor.read_exporter")
def test_Converter_process_order_no_exporter(mocked_exporter: MagicMock):
    mocked_exporter.return_value = None
    tested_object = Converter(CUSTOMER_DATA, MockedSystem())
    assert tested_object.process_order() == models.ConversionResults(message="Customer not supported.")
    mocked_exporter.assert_called_once_with(CUSTOMER_DATA.name)


@patch("src.extractor.FileHandler")
@patch("src.extractor.read_exporter")
def test_Converter_process_order_file_error(mocked_exporter: MagicMock, mocked_FileHandler: MagicMock):
    mocked_FileHandler.return_value.save_base64_file.return_value = 'Error on file'
    tested_object = Converter(CUSTOMER_DATA, MockedSystem())
    assert tested_object.process_order() == models.ConversionResults(message="Error on file")
    mocked_FileHandler.assert_called_once_with(CUSTOMER_DATA.contentBytes, CUSTOMER_DATA.filename)
    mocked_FileHandler.return_value.save_base64_file.assert_called_once()


@patch("src.extractor.FileHandler")
@patch("src.extractor.read_exporter")
def test_Converter_process_order_etractor_error(mocked_exporter: MagicMock, mocked_FileHandler: MagicMock):
    mocked_FileHandler.return_value.save_base64_file.return_value = 'Some/path/to_file.txt'
    mocked_exporter.return_value.extract_data.return_value = models.Order(error='Mocked Error', error_description='Mocked error desc')
    tested_object = Converter(CUSTOMER_DATA, MockedSystem())
    assert tested_object.process_order() == models.ConversionResults(message="Problem with extracting data from file.\n Details: Mocked error desc")
    mocked_exporter.return_value.initialize_config.assert_called_once_with('Some/path/to_file.txt')
    mocked_FileHandler.return_value.delete_old_files.assert_called_once()


@patch("src.extractor.FileHandler")
@patch("src.extractor.read_exporter")
def test_Converter_process_order_order_creation_error(mocked_exporter: MagicMock, mocked_FileHandler: MagicMock):
    mocked_FileHandler.return_value.save_base64_file.return_value = 'Some/path/to_file.txt'
    mocked_exporter.return_value.extract_data.return_value = models.Order()
    tested_object = Converter(CUSTOMER_DATA, MockedSystem(is_error=True))
    assert tested_object.process_order() == models.ConversionResults(message="Order not created due to error: Mocked_error")


@patch("src.extractor.FileHandler")
@patch("src.extractor.read_exporter")
def test_Converter_process_order(mocked_exporter: MagicMock, mocked_FileHandler: MagicMock):
    mocked_FileHandler.return_value.save_base64_file.return_value = 'Some/path/to_file.txt'
    mocked_exporter.return_value.extract_data.return_value = models.Order()
    tested_object = Converter(CUSTOMER_DATA, MockedSystem())
    assert tested_object.process_order() == models.ConversionResults(message="Order created", success=True)
