from CLI_helpers import separator
from paths import cwd
import patoolib
import tempfile as tf
import re
import os
import io
import zipfile as zf
from configparser import ConfigParser


def numeral_eval(value):
    """
    Attempts to parse int and float values. Leaves the other values as they are
    :param value:
    :return:
    """
    try:
        return float(value) if not float(value).is_integer() else int(value)
    except ValueError:
        return value
    except TypeError:
        return value


def decode_cura(path: str):
    """
    Decodes a .curaprofile file into a single list of [parameter, value, conainer index] lists.
    First a list of Cura specific defaults is loaded, then the values, specified in the Cura file are overwritten.
    :param path:
    :return:
    """

    def format_check(path: str, extension: str = "curaprofile", override: str = "zip"):
        """
        Checks whether a file extension is :param extension. Changes to :param override if it is and returns path.
        :param path:
        :param extension:
        :param override:
        :return:
        """
        if os.path.isfile(path):
            if path.endswith(extension):
                path_override = path.rstrip(extension) + override
                os.rename(path, path_override)
                return path_override
            else:
                raise TypeError("'{}' is not a '.{}' file.".format(path, extension))
        else:
            raise ValueError("'{}' does not exist or is not a file.".format(path))

    output = []
    tempdir = tf.TemporaryDirectory()
    renamed_path = format_check(path=path)
    patoolib.extract_archive(renamed_path, outdir=tempdir.name)
    for i, container in enumerate(os.listdir(tempdir.name)):
        container_abs = tempdir.name + separator() + container
        with open(container_abs) as container_file:
            value_cutoff = container_file.read().split("[values]")[-1]  # Parse only the actual values, not metadata
            active_values = [list(re.findall(r"(.+) = (.+)", value_cutoff))][0]
            for j, parameter in enumerate(active_values):
                active_values[j] = list(parameter)
                active_values[j].append(i)
            output.extend(active_values)
    del tempdir
    format_check(renamed_path, "zip", "curaprofile")
    for i, parameter in enumerate(output):
        output[i] = numeral_eval(parameter)
    return output


def encode_cura(parameters: list, name: str, quality: str):
    """
    Takes a single list of [parameter, value, container index] lists and packs them as a .curaprofile file.
    :param parameters:
    :param name:
    :return:
    """

    def position_counter(input_string: str, position: int):
        """
        Takes in a blank cura profile template and sets the position meta tag to
        :param input_string:
        :param position:
        :return:
        """
        if position == 0:
            return input_string.replace("position = 0\n", "")
        else:
            return input_string.replace("position = 0", "position = {}".format(str(position)))

    def get_container_params(container_index: int, parameters=parameters):
        """
        Helper function for selecting all the parameters from a respective container
        :param container_index:
        :param parameters:
        :return:
        """
        output = []
        for parameter in parameters:
            if parameter[-1] == container_index:
                output.append(parameter)
        return output

    tempdir = tf.TemporaryDirectory()
    outpath = tempdir.name + separator() + 'temp.zip'
    # Get the base template for a container, containing Meta and General data
    with open(cwd + "/resources/cura_configuration_template/custom_extruder_") as file:
        sample_lines = ['quality_type = ' + quality if 'quality_type ' in x else x for x in file.readlines()]

    empty_cura_container = '\n'.join(sample_lines)
    # Write each of the new containers in a temporary directory
    zip_archive = zf.ZipFile(outpath, mode="a")
    for container in range(9):
        meta = position_counter(empty_cura_container, container)
        zip_archive.writestr("custom_extruder_{}_{}".format(container, name) if container != 0 else "custom_{}".format(name),
                             meta + "\n".join([" = ".join([str(b) for b in a][0:2]) for a in get_container_params(container)]))
    zip_archive.close()
    curaprofile_path = outpath.rstrip(".zip") + ".curaprofile"
    os.rename(outpath, curaprofile_path)
    with open(curaprofile_path, 'rb') as file:
        return file.read()

def update_cura_3(parameters: list, config_file):
    """
    Updates existing curaprofile file with provided parameters.
    """
    archive = zf.ZipFile(config_file, mode='r')
    # make sure we did not receive zipbomb
    sum_file_size = sum([data.file_size for data in archive.filelist])
    sum_compress_size = sum([data.compress_size for data in archive.filelist])
    ratio = sum_file_size / sum_compress_size
    # Cura usually exports with ratio = 1 (stored, not compressed)
    if (ratio > 20):
        raise zf.BadZipFile("Zip Bomb Detected")

    result = io.BytesIO()
    resulting_config = zf.ZipFile(result, 'w')

    for config_entry in archive.filelist:
        with archive.open(config_entry, 'r') as binary_entry:
            if config_entry.filename.startswith('base/'):
                resulting_config.writestr(config_entry, binary_entry.read())
                continue

            entry = io.TextIOWrapper(binary_entry)
            cfg = ConfigParser()
            cfg.read_file(entry)
        # write parameters
        for param in parameters:
            cfg.set('values', param[0], str(param[1]))
        entry = io.StringIO()
        cfg.write(entry)
        resulting_config.writestr(config_entry, entry.getvalue())

    archive.close()
    resulting_config.close()
    return result.getvalue()
