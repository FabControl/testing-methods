import json
from Definitions import Material, Machine, Settings
from get_test_info import get_test_info, get_comment
from fill_values import fill_values as fv


class Persistence(object):
    def __init__(self, persistence: str or dict or None):
        # Load the persistence json
        # Assume request contains a persistence json
        request_empty = False
        if persistence is None:
            # No JSON loaded. Assume it's a new session, return a blank json.
            request_empty = True
            with open('resources/blank_persistence.json') as json_file:  # TODO Move blank_persistence path to paths.py
                self.dict = json.load(json_file)
        elif type(persistence) == str:
            try:
                # Check whether the input is a json in form of a string
                self.dict = json.loads(persistence)
            except json.JSONDecodeError:
                # It isn't.
                request_empty = True

        else:
            self.dict = persistence
        try:
            assert type(self.dict) == dict
        except AssertionError:
            raise TypeError("Loaded persistence does not yield a valid json dictionary")

        # Check if the loaded json yields a valid dictionary

        # Check if machine, material and session are in the loaded dictionary
        for block in ["machine", "material", "session"]:
            try:
                assert block in self.dict
            except AssertionError:
                raise KeyError("'{}' item not found in the loaded json.".format(block))

        # Loaded Json is a valid persistence dictionary.
        if not request_empty:
            self.session = self.dict["session"]

            self.machine = Machine(**self.dict["machine"])
            self.material = Material(**self.dict["material"])
            # Append settings to the machine object
            self.machine.settings = Settings(nozzle=self.machine.temperaturecontrollers.extruder.nozzle,
                                             material=self.material,
                                             machine=self.machine, **self.dict["settings"])

            self.id = self.dict["session"]["uid"]
            self.test_info = get_test_info(self.dict)
            self.test_comment = get_comment(self.test_info)

    def fill_values(self):
        pass
    #     fv(self)  TODO Fix fill_values.py
