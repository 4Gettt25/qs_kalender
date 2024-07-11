from django.test import TestCase

# Create your tests here.

import os


def get_current_venv():
    return os.environ.get('VIRTUAL_ENV', None)


print(get_current_venv())