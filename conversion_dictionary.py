"""
Conversion dictionary management tool.
Usage:
    conversion_dictionary.py
    conversion_dictionary.py add-slicer <slicer>
    conversion_dictionary.py parameter (add <parameter> | modify <parameter> [<slicer>])
"""
import json
import gc
from CLI_helpers import clear, round
import jsonpickle
from docopt import docopt
from paths import *

gc.enable()  # Enable garbage collection
debug = False

"""
Utility Methods
"""


def numeral_eval(value):
    """
    Attempts to parse int and float values. Leaves the other values as they are.
    :param value:
    :return:
    """
    try:
        return round(float(value)) if not float(value).is_integer() else int(value)
    except ValueError:
        if value == "":
            return None
        return value
    except:
        return value


def numeral_input(text: str):
    return numeral_eval(input(text))


def generate_reverse_modifier(input_obj):
    if input_obj.modifier is not None:
        print("Working parameter: %s" % input_obj.root.parameter)
        input_obj.reverse_modifier = numeral_input("reverse modifier for '{}': ".format(input_obj.modifier))


def generate_dict_entry(persistence):
    """
    Generate a dict entry for each value in settings
    Obsolete.
    """
    new_dictionary = []
    for key, value in persistence["settings"]:
        persistence[key] = {"prusa": input("%s in %s: " % (key, "prusa")),
                            "slic3r": "",
                            "simplify3d": input("{} in {}: ".format(key, "simplify3d")),
                            "kissslicer": ""}
        with open(relational_dict_json, mode="w") as file:
            output = json.dumps(new_dictionary, indent=4, sort_keys=True)
            file.write(output)
            file.close()


def assign_modifiers(persistence):
    """
    Assign modifiers and parent parameters
    Obsolete.
    """
    with open("relational_dict.json", mode="r") as file:
        input_json = json.load(file)
        file.close()

    for param in input_json:
        for slicer in input_json[param]:
            if input_json[param][slicer] != "":
                parameter = input_json[param][slicer]
                input_json[param][slicer] = {
                    "parameter": input_json[param][slicer],
                    "modifier": input(
                        "{} modifier for {} to derive from {}: ".format(param, parameter, persistence["settings"][param]))}
                if input_json[param][slicer]["modifier"] != "":
                    if "y" in input_json[param][slicer]["modifier"]:
                        input_json[param][slicer]["parent_parameter"] = input("Key of the parent parameter: ")
                    input_json[param][slicer]["units"] = input("Select units: ")
        with open("relational_dict2.json", mode="w") as file:
            output = json.dumps(input_json, indent=4, sort_keys=True)
            file.write(output)
            file.close()


"""
Object constructors
"""


class Slicer(object):
    """
    A slicer interpreter object. Stores slicer specific information and value getter and setter methods
    """
    def __init__(self, name: str = None, parameter: str = None, parent_parameter: str = None, modifier: str = None,
                 units: str = None, root: object = None, reverse_modifier: str = None, **kwargs):
        self.name = name
        self.parameter = parameter
        self.parent_parameter = parent_parameter
        self.modifier = modifier
        self.units = units
        self.root = root
        self.reverse_modifier = reverse_modifier

    def _slicer_modifier(self):
        """
        Helper function for returning a modified value, depending on the slicer type.
        :return:
        """
        if hasattr(self, "modifier") and self.modifier is not None:
            x = self.root.value
            if x is None:
                x = 1
            if hasattr(self, "parent_parameter") and self.parent_parameter is not None:
                y = self.root.params.get(self.parent_parameter).value
            try:
                result = eval(self.modifier)
            except ZeroDivisionError:
                return 0
            return result
        else:
            return self.root.value

    def _reverse_modifier(self, value):
        """
        Converts root object's value back to root object's respective format.
        :param value: the new value
        :return: converted root value
        """
        if hasattr(self, "reverse_modifier") and self.reverse_modifier is not None:
            x = value
            if hasattr(self, "parent_parameter") and self.parent_parameter is not None:
                y = self.root.params.get(self.parent_parameter).value
            try:
                new_value = eval(self.reverse_modifier)
            except ZeroDivisionError:
                return 0
            return new_value
        else:
            return value

    @property
    def value(self):
        return self._slicer_modifier()

    @value.setter
    def value(self, new_value):
        self.root.value = self._reverse_modifier(new_value)


class Params(object):
    """
    Contains all the parameters and methods to retrieve them
    """
    def __init__(self, dictionary_path: str):
        self.supported_slicers = ["prusa", "simplify3d", "cura"]
        self.parameters = []
        self.load(dictionary_path)

    def get(self, keyword: str, mode: str = "parameter"):
        """
        Returns a Param object if keyword is found in Param.parameter
        :param keyword: a string to look for
        :param mode: attribute in which to look for the keyword
        :return: Param object matching a keyword
        """
        for x in self.parameters:
            if debug:
                x.debug = True
            if mode == "name":
                if keyword in x.name:
                    return x
            elif mode == "parameter":
                if keyword == x.parameter:
                    return x
            elif mode in self.supported_slicers:
                if hasattr(x, mode):
                    if keyword == getattr(x, mode).parameter:
                        return x
            else:
                raise ValueError(
                    "{} is not a valid search mode. Valid modes are 'parameter', 'name', ".format(mode) + ", ".join(
                        ["'{}'".format(x) for x in self.supported_slicers]) + ".")
        return None

    def add_parameter(self, parameter: str):
        """
        A CLI interface for adding a new parameter and its respective slicer interpretations.
        Slicers listed in self.supported_slicers are offered.
        :param parameter:
        :return:
        """
        param = Param(parameter, self)
        for slicer in self.supported_slicers:
            clear()
            temp_slicer = Slicer(root=param)
            print("Creating a {} interpretation for {}.".format(slicer, parameter))
            # Set new slicer attributes.
            temp_slicer.parameter = numeral_input(
                "Enter {} parameteric equivalent in {}. Press Enter if none: ".format(parameter, slicer))
            if temp_slicer.parameter is None:
                temp_slicer.name = None
                temp_slicer.modifier = None
                temp_slicer.reverse_modifier = None
                temp_slicer.parent_parameter = None
                temp_slicer.units = None
                param.__setattr__(slicer, temp_slicer)
                continue
            temp_slicer.name = None
            temp_slicer.modifier = numeral_input("Modifier: ")
            if temp_slicer.modifier is not None:
                temp_slicer.reverse_modifier = numeral_input("Reverse modifier: ")
                if "y" in temp_slicer.modifier:
                    temp_slicer.parent_parameter = numeral_input("Parent parameter: ")
            temp_slicer.units = numeral_input("Units: ")

            param.__setattr__(slicer, temp_slicer)
        self.parameters.append(param)

    def add_slicer(self, slicer: str):
        """
        A CLI interface for adding a new slicer. Utilizes lower-level children object methods.
        :param slicer:
        :return:
        """
        self.supported_slicers.append(slicer)

        def add_new_parameter(param: Param, modifier: str = None, reverse_modifier: str = None, parent_parameter: str = None):
            clear()
            print("Current working parameter: {}.".format(parameter.parameter))
            param._add_slicer(slicer)
            _slicer = parameter.__getattribute__(slicer)
            _slicer.parameter = input("{} equivalent of {} parameter: ".format(slicer, parameter.parameter))
            if _slicer.parameter is None:
                return
            _slicer.modifier = modifier
            if _slicer.modifier is not None:
                _slicer.reverse_modifier = reverse_modifier
                if "y" in _slicer.modifier:
                    _slicer.parent_parameter = parent_parameter
            else:
                _slicer.reverse_modifier = None
                _slicer.parent_parameter = None

        for parameter in self.parameters:
            add_new_parameter(parameter)

    def dump(self, filename: str):
        """
        Dumps parameters and list of supported slicers to a json file.
        :param filename:
        :return:
        """
        output = [self.parameters, self.supported_slicers]

        # Enforce .json file extension
        if not filename.endswith(".json"):
            filename = filename + ".json"
        jsonpickle.set_encoder_options(name='simplejson', sort_keys=True)
        with open(filename, mode="w") as file:
            file.write(jsonpickle.dumps(output))
            file.close()

    def load(self, filename: str):
        """
        Loads parameters from a dumped json file.
        :param filename:
        :return:
        """
        if not filename.endswith(".json"):
            raise ValueError("{} is not a JSON file.".format(filename))
        with open(filename, mode="r") as file:
            loaded = jsonpickle.loads(file.read())
            file.close()
        self.parameters = loaded
        self.supported_slicers = [
          "prusa",
          "simplify3d",
          "cura"
        ]

        # Enforce correct parent/children hierarchy upon loading
        for param in self.parameters:
            param.params = self
            param_slicers = []
            for supported_slicer in self.supported_slicers:
                try:
                    param_slicers.append(param.__getattribute__(supported_slicer))
                except AttributeError:
                    setattr(param, supported_slicer, Slicer(root=param))
                    param_slicers.append(param.__getattribute__(supported_slicer))
            for slicer in param_slicers:
                slicer.root = param

    def populate(self, input_dictionary: dict, auto=False, *args):
        """
        Assigns a value to all parameters found in self.parameters.
        Independent (parent) parameters are assigned first in order to escape conflicts.
        :param input_dictionary: a dictionary with parameter/value as key/value
        :param auto:
        :return:
        """

        def map_values(parameters: list, look_in_slicers: bool = False):
            """
            Helper method for cycling through keys from an input dict, and mapping them to corresponding params
            :param parameters:
            :param look_in_slicers: should the parameters be looked for in slicer parameter names
            :return:
            """
            if not look_in_slicers:
                for param in parameters:
                    if param.parameter in input_dictionary:
                        param.value = input_dictionary.pop(param.parameter)
            else:
                for slicer in self.supported_slicers:
                    for param in parameters:
                        if hasattr(param, slicer):
                            if getattr(param, slicer).parameter in input_dictionary:
                                getattr(param, slicer).value = input_dictionary.pop(getattr(param, slicer).parameter)

        children = []  # A placeholder for params which have a parent object
        parents = []  # A placeholder for params which do not have parent objects

        # Append all the additional dictionaries in args to the input dict
        for lst in args:
            if isinstance(lst, dict):
                input_dictionary = input_dictionary + lst

        # Sort parameters based on their dependencies
        for param in self.parameters:
            if param.parent is not None:
                children.append(param)
            else:
                parents.append(param)

        # Map parent parameters to their respective names at a base level
        map_values(parents)

        # Map parent parameters to their respective names at a slicer level
        # (if the name could not be found at the base level)
        map_values(parents, look_in_slicers=True)

        if not auto:
            # Map child parameters to their respective names at a base level
            map_values(children)

            # Map child parameters to their respective names at a slicer level
            # (if the name could not be found at the base level)
            map_values(children, look_in_slicers=True)

        # Print leftover/unassigned values if any.
        if len(input_dictionary) > 0:
            print("The following keys were not mapped to any parameters:\n{}".format(", ".join(input_dictionary)))

    def generate_defaults(self, output: str):
        defaults = []
        for param in self.parameters:
            parameter = param.parameter
            units = param.units
            value = numeral_input("Default value for {}, units {}".format(parameter, units))
            defaults.append([parameter, value, units])
        output = output + ".json" if not output.endswith(".json") else output
        with open(output, mode="w") as file:
            file.write(json.dumps(defaults, indent=4, sort_keys=True))
            file.close()


class Param(object):
    """
    Stores all information related to a single parameter
    """
    def __init__(self, parameter, params: Params, **kwargs):
        self.name = None
        self.parameter = parameter
        self.units = None
        self.test = None
        self.parent = None
        self.modifier = None
        self.reverse_modifier = None
        self.params = params
        self._value = None
        self._manual = False  # If True, modifier will no longer be used

    def _parameter_modifier(self):
        if self._value is None:
            if hasattr(self, "modifier") and self.modifier is not None:
                x = self._value
                if hasattr(self, "parent") and self.parent is not None:
                    try:
                        y = self.params.get(self.parent).value
                    except AttributeError:
                        raise AttributeError("{} can't fetch its parent {}".format(self.parameter, self.parent))
                if debug:
                    print("Evaluating the following modifier: {} for {}".format(self.modifier, self.parameter))
                return numeral_eval(eval(self.modifier))
            elif hasattr(self, "_value") and self._value is not None:
                return self._value
        else:
            return self._value

    @property
    def value(self):
        return self._parameter_modifier()

    @value.setter
    def value(self, new_value):
        self._value = new_value
        if not self._manual:
            if self.modifier is not None:
                print("{} now uses a manual value selection mode, and won't use its modifier.".format(self.parameter))
        self._manual = True

    def _add_slicer(self, slicer: str, name: str = None, parameter: str = None, parent_parameter: str = None,
                    modifier: str = None, reverse_modifier: str = None, units: str = None, **kwargs):
        """
        Add a new slicer interpreter to the parameter. Private method, only meant to be called from superclass.
        :param slicer: name of the slicer software to add
        :param name:
        :param parameter:
        :param parent_parameter:
        :param modifier:
        :param reverse_modifier:
        :param units:
        :param kwargs:
        :return:
        """
        if slicer not in self.params.supported_slicers:
            raise ValueError("{} not listed among supported slicers. Supported slicers are {}".format(slicer, ', '.join(
                self.params.supported_slicers)))
        self.__setattr__(slicer, Slicer(name, parameter, parent_parameter, modifier, units, self, reverse_modifier, **kwargs))

    def _del_slicer(self, slicer: str):
        """
        Delete a slicer parameter interpretation.
        :param slicer:
        :return:
        """
        if hasattr(self, slicer):
            attribute = self.__getattribute__(slicer)
            del attribute

        else:
            raise ValueError("{} does not have a Slicer attribute named {}.".format(self.parameter, slicer))

    def auto(self):
        print("{} now uses a generated value.".format(self.parameter))
        self._manual = False
        self._value = None


if __name__ == "__main__":
    """
    Conversion dictionary management tool.
    Usage:
        conversion_dictionary.py
        conversion_dictionary.py add-slicer <slicer>
        conversion_dictionary.py parameter (add <parameter> | modify <parameter> [<slicer>])
        
        When debugging, need to make sure that Params is not loaded as a list of Params object and supported_slicers
        Need to make sure that all py/object references point to convesion_dictionary.<Object>, and not __main__.<Object>
    """

    arguments = docopt(__doc__, version="Conversion dictionary tool 0.3")
    params = Params(conversion_json)

    if arguments["add-slicer"]:
        params.add_slicer(arguments["<slicer>"])

    elif arguments["parameter"]:
        if arguments["[add]"]:
            params.add_parameter(arguments["<parameter>"])
