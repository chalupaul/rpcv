__version__ = "0.1.0"
import os
import sys

# This hacks in the correct directory so that
# it's usable in local flask and in lambda.
app_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_base)

# Import controllers for flask_rebar
from api.controllers import hypervisor, cluster  # noqa: F401

from api.app import run_app  # noqa: F401
