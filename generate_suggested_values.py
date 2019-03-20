"""
FabControl Optimizer: Feedstock Material Testing
Suggested Values Generator

Returns suggested values of the testing parameters, based on session specific get_test_info.py.

Usage:
   generate_suggested_values.py <session-id>
"""
from Definitions import *
from Globals import persistence
from get_test_info import get_test_info
from docopt import docopt

arguments = docopt(__doc__)

test_info = get_test_info(persistence)
suggested_values = test_info.parameter_one.values
suggested_values_min_max = border_values(suggested_values)

output = "[{}".format(test_info.parameter_one.precision).format(suggested_values_min_max[0]) + ",{}]".format(test_info.parameter_one.precision).format(suggested_values_min_max[-1])
print(output)

