from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import os

@deconstructible
class ExcelFileValidator:
    def __init__(self, allowed_extensions=('.xls', '.xlsx')):
        self.allowed_extensions = allowed_extensions

    def __call__(self, value):
        # print(value)
        ext = os.path.splitext(value.name)[1]
        # print(ext)
        if not ext.lower() in self.allowed_extensions:
            raise ValidationError('Only Excel files with .xls or .xlsx extensions are allowed.')
