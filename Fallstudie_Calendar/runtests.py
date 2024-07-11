import os
import sys
import django
from django.test.utils import get_runner
from django.conf import settings

# Fügen Sie Ihr Projektverzeichnis zum sys.path hinzu
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ['DJANGO_SETTINGS_MODULE'] = 'Fallstudie_Calendar.settings'  # Passen Sie den Namen Ihres Projekts an
django.setup()

TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(["account", "mycalendar"])  # Fügen Sie hier den Namen Ihrer App hinzu
sys.exit(bool(failures))
