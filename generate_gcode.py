"""
usage:

    generate_gcode.py <session-id> <config_path> <stl_path> <count> <rotation> <orientation>

"""


from Globals import persistence
from paths import *
from CLI_helpers import separator
import subprocess
from os import devnull
from docopt import docopt
from Globals import persistence

arguments = docopt(__doc__)


def generate_gcode(orientation: str, count: int, rotation: float or int, file: str, config: str, max_dim_y: int):
    """
    Creates a subprocesses of Blender and Slic3r in order to generate an ISO527 test specimen geometry and slice
    it with an appropriate Slic3r configuration file.
    :param orientation:
    :param count:
    :param rotation:
    :param file:
    :param config:
    :param max_dim_y:
    :return:
    """
    output = cwd + gcode_folder + separator() + file.replace(".stl", ".gcode")
    geometry = cwd + stl_folder + separator() + file
    subprocess.run([blender_path, "-b", "-P", str(cwd + "stl_modifier.py"), "--", orientation, str(count),
                    str(rotation), cwd + stl_folder + separator() + file, stl_folder, max_dim_y],
                   stderr=open(devnull, 'wb'))
    subprocess.run([slic3r_path, "--load", config, "-o", output, "--dont-arrange", geometry])


if __name__ == "__main__":
    output_path = gcode_folder + ""
    generate_gcode(arguments["<orientation>"], arguments["count"], arguments["rotation"], output_path,
                   arguments["<config>"], persistence["machine"]["buildarea_maxdim2"])
