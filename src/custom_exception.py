import sys
import traceback

class CustomException(Exception):
    def __init__(self, error_message, error_detail=None):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail=None):
        if error_detail:
            _, _, exc_tb = error_detail.exc_info()
            if exc_tb:
                file_name = exc_tb.tb_frame.f_code.co_filename
                line_number = exc_tb.tb_lineno
                return f"Error in {file_name}, line {line_number}: {error_message}"
        return error_message  # If no traceback, return just the message

    def __str__(self):
        return self.error_message
