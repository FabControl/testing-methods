from ast import literal_eval
from os import system, name, listdir, devnull
from paths import blender_path, slic3r_path, cwd, stl_folder, gcode_folder
import re
import subprocess
import warnings
import traceback
import sys
from datetime import timedelta


def evaluate(input):
    """
    Evaluates a given input string and outputs either an int, float, list or tuple.
    :param input:
    :return:
    """
    try:
        output = literal_eval(input)
    except:
        output = input

    if output == "":
        return None
    else:
        return output


def clear():
    """
    Clears the terminal screen. OS aware.
    :return:
    """
    system('cls' if name == 'nt' else 'clear')


def extruded_filament(gcode: str):
    """
    Takes a path to a gcode and returns a sum of all E values.
    :param gcode:
    :return:
    """
    extrusion_values = re.findall(r'(?<=E)[0-9.-]+(?=\s)', gcode)

    total_extrusion = 0
    for value in extrusion_values:
        try:
            total_extrusion = total_extrusion + float(value)
        except:
            total_extrusion = total_extrusion + literal_eval(value)

    return round(total_extrusion)


def printing_time(gcode: str, as_datetime: bool = False):
    """
    Takes a gcode as string and returns estimated print time.
    :param gcode:
    :param as_datetime:
    :return:
    """
    dwell_matcher = re.compile(r'(P(?P<milliseconds>\d+)|S(?P<seconds>\d+))')
    moves_matcher = re.compile(r'(?:G(?:0|1|92)'
                               r' X(?P<X>(?:[-+]?[0-9]+\.?[0-9]*))|'
                               r' Y(?P<Y>(?:[-+]?[0-9]+\.?[0-9]*))|'
                               r' Z(?P<Z>(?:[-+]?[0-9]+\.?[0-9]*))|'
                               r' E(?P<E>(?:[-+]?[0-9]+\.?[0-9]*))|'
                               r' F(?:(?P<F>[0-9]+)\.?[0-9]*)'
                               r'){1,5}', re.IGNORECASE)
    relative_extrusion = False
    relative_moves = False
    estimated_time = timedelta()
    # should be a sane value to start with
    feedrate = 10 # mm/sec
    x = y = z = e = 0

    for line in (x.split(';')[0].strip() for x in gcode.split('\n')):
        if len(line) < 3:
            continue

        if line == 'G28':
            x = y = z = 0
            # educated guess
            estimated_time += timedelta(seconds=3)
        elif line == 'G90':
            relative_moves = False
        elif line == 'G91':
            relative_moves = True
        elif line == 'M82':
            relative_extrusion = False
        elif line == 'M83':
            relative_extrusion = True

        elif line.startswith('G4 '):
            dwell = dwell_matcher.search(line)
            if dwell:
                ms, s = dwell.group('milliseconds', 'seconds')
                if ms is not None:
                    period = int(ms) / 1000
                elif s is not None:
                    period = int(s)
                estimated_time += timedelta(seconds=period)

        elif line.startswith('G92 '):
            X,Y,Z,E,F = moves_matcher.search(line).group('X','Y','Z','E','F')
            if X is not None:
                x = float(X)
            if Y is not None:
                y = float(Y)
            if Z is not None:
                z = float(Z)
            if E is not None:
                e = float(E)

        elif line.startswith('G1 ') or line.startswith('G0 '):
            X,Y,Z,E,F = moves_matcher.search(line).group('X','Y','Z','E','F')

            frate = feedrate
            if F is not None:
                if X is not None or Y is not None or Z is not None:
                    frate = (int(F)/60 + feedrate) / 2
                feedrate = int(F)/60

            dx = dy = dz = de = 0
            if X is not None:
                X = float(X)
                if relative_moves:
                    dx = X
                    x += X
                else:
                    dx = X - x
                    x = X
            if Y is not None:
                Y = float(Y)
                if relative_moves:
                    dy = Y
                    y += Y
                else:
                    dy = Y - y
                    y = Y
            if Z is not None:
                Z = float(Z)
                if relative_moves:
                    dz = Z
                    z += Z
                else:
                    dz = Z - z
                    z = Z
            if E is not None:
                E = float(E)
                if relative_moves:
                    de = E
                    e += E
                else:
                    de = E - e
                    e = E

            dxyz = (dx**2 + dy**2 + dz**2)**(0.5)
            if dxyz > 0.001:
                estimated_time += timedelta(seconds=dxyz/frate)
            else:
                estimated_time += timedelta(seconds=de/frate)

    return str(estimated_time).split('.')[0] if not as_datetime else estimated_time


def exclusive_write(path: str, output, limit=True):
    """
    Takes a path and output stream, attempts to write the stream to the path,
    if it exists, alters the path to either have a 3x zero padded number before the extension,
    or add padding and increase an existing number by 1.
    A boolean limit argument is used to prevent the file writing from overflowing and writing
    too many instances of a file.

    Used to prevent file overwriting.

    split[0] is the save_session_file_as,
    split[1] is either a number or NoneType
    split[2] is a file extension
    :param path:
    :param output:
    :param limit:
    :return:
    """
    try:
        with open(path, "x") as file:
            file.write(output)
        print("{} successfully saved.".format(path))

    except:
        split = re.split(r'(\d{3}(?=\.))*(\.[0-9a-zA-Z]+?$)', path)
        path = list(filter(lambda x: str(x).startswith(split[0]), listdir()))[-1]
        split = re.split(r'(\d{3}(?=\.))*(\.[0-9a-zA-Z]+?$)', path)
        if split[1] is not None and int(split[1]) > 999 and limit:
            raise ValueError(
                '%s%s is likely overflowing and has reached 1000 or more instances.' % (split[0], split[2]))
        underscore = "_" if not split[0].endswith("_") else ""
        path = split[0] + underscore + str(int(split[1] if split[1] is not None else 0) + 1).zfill(3) + split[2]
        with open(path, "x") as file:
            file.write(output)
        print("{} successfully saved.".format(path))


def generate_gcode(orientation: str, count: int, rotation: float or int, file: str, config: str, max_dim_y: int):
    """
    Creates a subprocesses of Blender and Slic3r in order to generate an ISO527 test specimen geometry and slice it with an appropriate
    Slic3r configuration file.
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


def separator(input=None):
    """
    Takes an input value and separates it with an OS aware directory separator. Returns a separator if no input is given.
    :param input:
    :return:
    """
    if input is None:
        if name == "nt":
            return "\\"
        else:
            return "/"
    else:
        if name == "nt":
            return "\\{}\\".format(input)
        else:
            return "/{}/".format(input)


builtins_round = round


def round(input: float, depth: int = 3):
    """
    A wrapper for the built-in round function which handles the datatype casting in a more intuitive fashion.
    :param input:
    :param depth:
    :return:
    """
    return float(str(builtins_round(input, depth)))


def exception_handler(message, fatal: bool = False):

    traceback.print_exc()
    print("FCException: " + message)
    if fatal:
        sys.exit(15)


if __name__ == "__main__":
    exception_handler("Session not loaded", True)
