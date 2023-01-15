from unittest.mock import patch, MagicMock

from src.file_handler import FileHandler


FILE_CONTENT = 'VGhpcyBpcyB0ZXN0IGZpbGU='


def test_FileHandler_init():
    tested_object = FileHandler(FILE_CONTENT, 'test_file.txt')
    assert tested_object.contentBytes == FILE_CONTENT
    assert tested_object.filename == 'test_file.txt'
    assert tested_object.temp_file_name == ''


def test_FileHandler_save_base64_file_conversion_error():
    tested_object = FileHandler(FILE_CONTENT[:-1], 'test_file.txt')
    expected_result = 'Error - Problem with conversion from base64 to file.'
    assert tested_object.save_base64_file() == expected_result


def test_FileHandler_save_base64_file_extension_not_found():
    tested_object = FileHandler(FILE_CONTENT, 'test_file')
    assert tested_object.save_base64_file() == 'Error - Extension not found in filename'


@patch('src.file_handler.uuid.uuid1')
def test_FileHandler_save_base64_file(mocked_uuid1: MagicMock):
    mocked_uuid1.return_value = 'mocked_hash'
    tested_object = FileHandler(FILE_CONTENT, 'test_file.txt')
    assert tested_object.save_base64_file() == 'temp/mocked_hash.txt'
    tested_object.delete_old_files()


@patch('src.file_handler.uuid.uuid1')
def test_FileHandler_delete_old_files(mocked_uuid1: MagicMock):
    mocked_uuid1.return_value = 'mocked_hash'
    tested_object = FileHandler(FILE_CONTENT, 'test_file.txt')
    tested_object.save_base64_file()
    assert tested_object.delete_old_files() is True


def test_FileHandler_delete_old_file_error():
    tested_object = FileHandler(FILE_CONTENT, 'test_file.txt')
    assert tested_object.delete_old_files() is False
