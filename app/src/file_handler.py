import base64
import binascii
import uuid
import os


class FileHandler:
    def __init__(self, content_bytes: str, filename: str) -> None:
        """Class used to save base64 string to file

        Args:
            contentBytes (str): base64 string
            filename (str): name of the file
        """
        self.contentBytes = content_bytes
        self.filename = filename
        self.temp_file_name = ''

    def save_base64_file(self) -> str:
        """Method used for saving base64 string to file in temp folder.

        Returns:
            str: path for file after conversion from base64 string or error description.
        """
        try:
            file_as_bytes = base64.b64decode(self.contentBytes)
            self.temp_file_name = "temp/{0}.{1}".format(
                str(uuid.uuid1()), self.filename.split(".", 1)[1])
            os.makedirs(os.path.dirname(self.temp_file_name), exist_ok=True)
            with open(self.temp_file_name, 'wb') as file_temp:
                file_temp.write(file_as_bytes)
            return self.temp_file_name
        except binascii.Error:
            return 'Error - Problem with conversion from base64 to file.'
        except IndexError:
            return 'Error - Extension not found in filename'

    def delete_old_files(self) -> bool:
        """Method used for deleting already processed files."""
        try:
            os.remove(self.temp_file_name)
            return True
        except (IndexError, FileNotFoundError) as _:  # noqa: F841
            return False
