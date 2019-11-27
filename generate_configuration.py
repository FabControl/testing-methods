#!/usr/local/bin/python
import datetime
import json
import re
from collections import OrderedDict
from paths import *
from persistence import Persistence
from io import BytesIO
from conversion_dictionary import Params
import math


class Converter(Persistence):
    def __init__(self, persistence):
        super(Converter, self).__init__(persistence)
        with open(config_ini) as ini:
            self.default_ini = ini.read()
        self.conversion_json = conversion_json
        self.target_overrides_path = target_overrides_json
        self.params = self.load_defaults()
        self.initialize_all_parameters()

    @staticmethod
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

    def read_ini(self, ini_string: str, output_type: object = OrderedDict):
        """
        Parses an ini file and returns an ordered dictionary with parameters as keys.
        Dict item contains a value and a percentage flag.
        :rtype: OrderedDict
        :param ini_string: ini file to parse, as string
        :param output_type:
        :return: returns an ordered dict
        """
        config = re.findall(r'(.+) = ([^%\n]*)(%)?', ini_string)

        dictionary = OrderedDict() if output_type == OrderedDict else {}
        for x in config:
            dictionary[x[0]] = {"value": self.numeral_eval(x[1])}
            dictionary[x[0]]["percentage"] = True if "%" in x else False
        return dictionary

    @staticmethod
    def assemble_ini(dictionary: OrderedDict):
        """
        Accepts an OrderedDict object, and writes it line by line by iterating through the OrderedDict.
        :param dictionary: read_ini()
        :return:
        :rtype: str
        """
        outstring = ""
        outstring += "# Created with FabControl Optimizer\n"

        for key, values in dictionary.items():
            value = values["value"]
            percentage = values["percentage"]
            line_start = "{0} = {1}".format(key, str(value) if value is not None else "")
            line_end = "%\n" if percentage else "\n"
            outstring += line_start + line_end

        return outstring

    def load_defaults(self):
        """
        Conversion dictionary PARAMS init
        """
        params = Params(self.conversion_json)
        defaults = self.read_ini(self.default_ini, output_type=dict)
        for key, value in defaults.items():
            defaults[key] = value["value"]
            del key, value
        params.populate(defaults, auto=True)
        return params

    def initialize_all_parameters(self):
        """
        Persistence pre-load block
        """
        self.load_defaults()
        persistence = self.dict
        persistence_flat = dict(persistence["settings"], **persistence["machine"]["temperature_controllers"]["extruder"]["nozzle"])
        persistence_flat["material_name"] = persistence["material"]["name"]
        self.params.populate(persistence_flat, auto=True)
        # Apply target overrides
        with open(self.target_overrides_path) as overrides:
            target_overrides = json.load(overrides)
        self.params.populate(target_overrides[persistence["session"]["target"]])

    def load_raw_config(self, config: dict):
        self.params.populate(config)

    def to_prusa(self):
        """
        Writes a Prusa Slic3r config
        """
        def generate_coordinates(form: str, **kwargs) -> str:
            """
            Generates build plate size coordinates to comply with Prusa Slicer
            Takes buildarea_maxdim1, buildarea_maxdim2 as numerals, origin as tuple of numerals
            :param form: Either 'elliptic' or 'cartesian'
            :return: A prusa format polygon coordinates as a str.
            """
            class Point:
                # Kernel for storing a point in 2D plane, where {x} is coords on X axis and {y} on Y
                kernel = "{x}x{y}"

                def __init__(self, x, y):
                    self.x = x
                    self.y = y

                def raster(self):
                    return self.kernel.format(x=self.x, y=self.y)

            points = []
            buildarea_maxdim1 = kwargs['buildarea_maxdim1']
            buildarea_maxdim2 = kwargs['buildarea_maxdim2']
            radius = buildarea_maxdim1
            if 'origin' in kwargs:
                origin = kwargs['origin']
            else:
                origin = (0, 0)
            if form == "cartesian":
                # Generate a square polygon
                for point in [(origin[0], origin[1]),
                              (buildarea_maxdim1, origin[1]),
                              (buildarea_maxdim1, buildarea_maxdim2),
                              (origin[0], buildarea_maxdim2)]:
                    points.append(Point(*point).raster())
            elif form == "elliptic":
                pi = math.pi
                n = 64
                circle_coordinates = [(round(math.cos(2 * pi / n * x) * radius, 2),
                                       round(math.sin(2 * pi / n * x) * radius, 2)) for x in range(0, n + 1)]
                for point in circle_coordinates:
                    points.append(Point(*point).raster())
            return ",".join(points)

        # Prusa slicer takes a polygon (in a proprietary format) to define the build volume shape
        # The buildarea polygon is created here
        buildarea_polygon = generate_coordinates(self.dict["machine"]["form"],
                                                 buildarea_maxdim1=self.dict["machine"]["buildarea_maxdim1"],
                                                 buildarea_maxdim2=self.dict["machine"]["buildarea_maxdim2"])

        # Configuration assembly
        configuration = self.read_ini(self.default_ini)
        for item in configuration:
            param = self.params.get(item, mode="prusa")
            if param is not None:
                configuration[item]["value"] = param.prusa.value
        configuration["bed_shape"]["value"] = buildarea_polygon
        return self.assemble_ini(configuration)

    def to_simplify(self):
        """
        Writes a Simplify3D config
        """
        import xml.etree.ElementTree as ET

        tree = ET.parse(simplify_config_fff)
        root = tree.getroot()
        root.attrib["name"] = str(self.id)
        root.attrib["version"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for param in self.params.parameters:
            if param.simplify3d.parameter is not None:
                element = root.find(param.simplify3d.parameter)
                if element is None:
                    element = root.find("extruder").find(param.simplify3d.parameter)
                if "temperature" in param.parameter:
                    temp_controllers = root.findall("temperatureController")
                    for controller in temp_controllers:
                        if controller.attrib["name"] == param.simplify3d.parameter:
                            setpoints = controller.findall("setpoint")
                            if len(setpoints) > 1:
                                if param.parameter == "temperature_extruder":
                                    element = setpoints[-1]
                                else:
                                    element = setpoints[0]
                            else:
                                element = controller.find("setpoint")
                            element.attrib["temperature"] = str(param.simplify3d.value)
                    continue
                if param.parameter == "ventilator_part_cooling":
                    element = root.find("fanSpeed").findall("setpoint")[-1]
                    element.attrib["speed"] = str(param.simplify3d.value)
                    continue
                if element is not None:
                    if element.text is not None:
                        element.text = str(self.numeral_eval(param.simplify3d.value))
                    elif param.parameter == "":
                        element.attrib = str(self.numeral_eval(param.simplify3d.value))
        f = BytesIO()
        tree.write(f, xml_declaration=True, encoding="utf-8")
        return f.getvalue()

    def to_cura(self):
        from cura_ops import decode_cura, encode_cura
        cura_params = []

        for param in self.params.parameters:
            if param.cura.parameter is not None:
                if param.cura.value is not None:
                    cura_params.append([param.cura.parameter, param.cura.value, 0])

        return encode_cura(cura_params, 'somename')

    # def to_raw(self):
    #     output_dictionary = {"raw": {},
    #                          "prusa": {},
    #                          "simplify3d": {},
    #                          "cura": {}}
    #
    #     for parameter in params.parameters:
    #         if parameter.value is not None:
    #             output_dictionary["raw"][parameter.parameter] = parameter.value
    #         if parameter.simplify3d.value is not None:
    #             output_dictionary["simplify3d"][parameter.simplify3d.parameter] = parameter.simplify3d.value
    #         if parameter.prusa.value is not None:
    #             output_dictionary["prusa"][parameter.prusa.parameter] = parameter.prusa.value
    #     with open(raw_config_folder + separator() + session_id + ".json", mode="w") as file:
    #         json.dump(output_dictionary, file)


if __name__ == "__main__":
    with open("debug.json") as file:
        import json
        per = json.load(file)
    c = Converter(per)
