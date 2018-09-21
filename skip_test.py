"""
Usage:
    skip_test.py <session-id> <test-number>
"""

from docopt import docopt
from Globals import persistence, test_dict, filename
from session_loader import session_uid
from datetime import datetime
from paths import cwd
import json

arguments = docopt(__doc__)

current_test = {"test_name": test_dict[arguments["<test-number>"]].name,
                "executed": False,
                "comments": 0,
                "datetime_info": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

persistence["session"]["previous_tests"].append(current_test)

with open(filename(session_uid, "json"), mode="w") as file:
    output = json.dumps(persistence, indent=4, sort_keys=False)
    file.write(output)
