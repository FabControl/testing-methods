import json
from Definitions import Material, Machine, Settings
from get_test_info import get_test_info, get_comment
from paths import blank_persistance
from fill_values import fill_values as fv


class Persistence(object):
    def __init__(self, persistence: str or dict or None):
        self.session = None

        self.machine = None
        self.material = None
        self.id = None
        self.test_info = None
        self.test_comment = None

        # Load the persistence json
        # Assume request contains a persistence json
        request_empty = False
        if persistence is None:
            # No JSON loaded. Assume it's a new session, return a blank json.
            request_empty = True
            with open(blank_persistance) as json_file:
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
            print("Received a valid persistence json. Processing...")
            self.populate()

        else:
            print("Did not receive a valid persistence json. Returning a blank template!")

    def populate(self):
        """
        Assign the json dictionary items to appropriate object attributes
        :return:
        """
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
        self.populate()
