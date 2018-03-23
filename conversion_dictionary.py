from pprint import pprint
import pickle
import json
import gc
from CLI_helpers import clear
import jsonpickle
from Globals import import_json_dict as values

gc.enable()  # Enable garbage collection
with open("relational_dict.json") as file:
    relational_dict = json.load(file)
    del file

flat_values = dict(values["settings"], **values["machine"]["nozzle"])  # Needed to unify all relevant values in a single list for convenience


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


def numeral_input(text: str):
    return numeral_eval(input(text))


def generate_reverse_modifier(input_obj):
    if input_obj.modifier is not None:
        print("Working parameter: %s" % input_obj.root.parameter)
        input_obj.reverse_modifier = numeral_input("reverse modifier for '%s': " % input_obj.modifier)


def generate_dict_entry():
    """
    Generate a dict entry for each value in settings
    """
    new_dictionary = []
    for key, value in values["settings"]:
        values[key] = {"prusa": input("%s in %s: " % (key, "prusa")),
                       "slic3r": "",
                       "simplify3d": input("%s in %s: " % (key, "simplify3d")),
                       "kissslicer": ""}
        with open("relational_dict.json", mode="w") as file:
            output = json.dumps(new_dictionary, indent=4, sort_keys=True)
            file.write(output)


def assign_modifiers():
    """
    Assign modifiers and parent parameters
    """
    with open("relational_dict.json", mode="r") as file:
        input_json = json.load(file)

    for param in input_json:
        for slicer in input_json[param]:
            if input_json[param][slicer] != "":
                parameter = input_json[param][slicer]
                input_json[param][slicer] = {
                    "parameter": input_json[param][slicer],
                    "modifier": input("%s modifier for %s to derive from %s: " % (param, parameter, values["settings"][param]))}
                if input_json[param][slicer]["modifier"] != "":
                    if "y" in input_json[param][slicer]["modifier"]:
                        input_json[param][slicer]["parent_parameter"] = input("Key of the parent parameter: ")
                    input_json[param][slicer]["units"] = input("Select units: ")
        with open("relational_dict2.json", mode="w") as file:
            output = json.dumps(input_json, indent=4, sort_keys=True)
            file.write(output)




class Slicer(object):
    """
    Stores slicer specific information and value getter and setter methods
    """

    def __init__(self, name=None, parameter=None, parent_parameter=None, modifier=None, units=None, root=None, **kwargs):
        self.name = name
        self.parameter = parameter
        self.parent_parameter = parent_parameter
        self.modifier = modifier
        self.units = units
        self.root = root

    def _slicer_modifier(self):
        """
        Helper function for returning a modified value, depending on the slicer type.
        :return:
        """

        if self.modifier is not None:
            x = self.root.value
            if self.parent_parameter is not None:
                y = self.root.params.get(self.parent_parameter).value
            result = eval(self.modifier)
            return result
        else:
            return self.root.value

    def _reverse_modifier(self, value):
        return value  # TODO

    @property
    def value(self):
        return self._slicer_modifier()

    @value.setter
    def value(self, new_value):
        self.root.value = self._reverse_modifier(new_value)


class Params(object):
    def __init__(self):
        with open("conversion.json", mode="r") as file:
            self._tests = jsonpickle.loads(file.read())

        # for x in self._tests:
        #     slicers = []
        #     for attr in x.__dir__():
        #         if isinstance(x.__getattribute__(attr), Slicer):
        #             slicers.append(x.__getattribute__(attr))
        #
        #     print(slicers)
        #     for slicer in slicers:
        #         slicer.value = None

        # for x in self._tests:
        #     del x.value
        # with open("conversion.json", mode="w") as file:
        #     file.write(jsonpickle.dumps(self._tests))

    def get(self, keyword: str, mode: str = "parameter"):
        """
        Returns a Param object if keyword is found in Param.name
        :param keyword: a string to look for
        :param mode: attribute in which to look for the keyword
        :return: Param object matching a keyword
        """
        for x in self._tests:
            if mode == "name":
                if keyword in x.name:
                    return x
            elif mode == "parameter":
                if keyword in x.parameter:
                    return x
            else:

                raise ValueError("%s is not a valid mode" % mode)
        return None


class Param(object):
    """
    Stores all information related to a single parameter
    """
    def __init__(self, parameter, params: Params, **kwargs):
        self.name = None
        self.parameter = parameter
        self.units = None
        self.test = None
        self.params = params

    @property
    def value(self):
        return flat_values[self.parameter]


if __name__ == "__main__":  # For testing
    params = Params()
    print(params.get("size_id").simplify3d.value)
    pass
