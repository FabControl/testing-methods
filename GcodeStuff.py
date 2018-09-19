from mecode import G
from Definitions import *
from paths import gcode_folder
from CLI_helpers import exception_handler

track_list = []

# TODO Second extruder support


class Gplus(G):
    # Build on the G class from mecode. Gplus class redefines some of the commands, creates new commands
    def __init__(self, material: Material, machine: Machine, *args, **kwargs):
        super(Gplus, self).__init__(*args, **kwargs)

        self.filament_diameter = material.size_od
        self.nozzle_diameter = machine.nozzle.size_id
        self.nozzle_od = machine.nozzle.size_od
        self.extrusion_multiplier = machine.settings.extrusion_multiplier
        self.track_height = machine.settings.track_height
        self.track_width = machine.settings.track_width

        self.coef_w = machine.settings.track_width / machine.nozzle.size_id
        self.speed_printing = machine.settings.speed_printing

        self.track_list = [] # TODO Is it used?

    def set_extruder_temperature(self, temperature: float):
        """Set the liquefier temperature in degC"""
        G.write(self, "M109 S{:.0f}".format(temperature) + " T0; set the extruder temperature and wait till it has been reached")

    def set_printbed_temperature(self, temperature: float):
        """Set the printbed temperature in degC"""
        G.write(self, "M190 S{:.0f}".format(temperature) + " T0; set the printbed temperature and wait till it has been reached")

    def set_ventilator_part_cooling(self, cooling_power: float):
        """Set the cooler power in percent"""
        if cooling_power > 100:
            cooling_power = 100
        elif cooling_power < 0:
            pass
        # get a fraction of 255 (max intensity of the cooler)corresponding to the fan percentage
        output = "M106 S{:.0f}".format(255 * (cooling_power / 100)) + "; set the cooler speed for part cooling"
        G.write(self, output)

    def set_ventilator_exit(self, cooling_power: float):
        """Set the cooler power in percent"""
        if cooling_power > 100:
            cooling_power = 100
        elif cooling_power < 0:
            pass
        # get a fraction of 255 (max intensity of the cooler)corresponding to the fan percentage
        output = "M106 P1 S{:.0f}".format(255 * (cooling_power / 100)) + "; set the speed for exit ventilator"
        G.write(self, output)

    def set_ventilator_entry(self, cooling_power: float):
        """Set the cooler power in percent"""
        if cooling_power > 100:
            cooling_power = 100
        elif cooling_power < 0:
            pass
        # get a fraction of 255 (max intensity of the cooler)corresponding to the fan percentage
        output = "M106 P2 S{:.0f}".format(255 * (cooling_power / 100)) + "; set the speed for entry ventilator"
        G.write(self, output)

    def dwell(self, time: int):
        """ Pause code executions for the given amount of time """
        self.write("G4 P{}".format(time * 1000) + " T0; set the waiting time in ms")

    def move(self, x=None, y=None, z=None, rapid=False, extrude=None, extrusion_multiplier=None, coef_w=None,
             coef_h=None, **kwargs):
        """ Move the tool head to the given position. This method operates in
        relative mode unless a manual call to `absolute` was given previously.
        If an absolute movement is desired, the `abs_move` method is
        recommended instead."""
        if extrude is not None: self.extrude = extrude
        self.extrusion_multiplier = 1 if extrusion_multiplier is None else extrusion_multiplier

        if coef_w is not None:
            self.coef_w = coef_w
        elif coef_w is None:
            self.coef_w = self.track_width / self.nozzle_diameter

        if coef_h is not None:
            self.coef_h = coef_h
        elif coef_h is None:
            self.coef_h = self.track_height / self.nozzle_diameter

        if self.extrude is True and "E" not in kwargs.keys():
            if self.is_relative is not True:
                x_move = self.current_position["x"] if x is None else x
                y_move = self.current_position["y"] if y is None else y
                x_distance = abs(x_move - self.current_position["x"])
                y_distance = abs(y_move - self.current_position["y"])
                current_extruder_position = self.current_position["E"]
            else:
                x_distance = 0 if x is None else x
                y_distance = 0 if y is None else y
                current_extruder_position = 0

            line_length = math.sqrt(x_distance ** 2 + y_distance ** 2)

            if self.coef_h < self.coef_w / (2 - math.pi / 2):
                filament_length = (4 / math.pi) * (self.nozzle_diameter / self.filament_diameter) ** 2 * ((self.coef_w - self.coef_h) * self.coef_h + (math.pi / 4) * (
                    self.coef_h) ** 2) * line_length * self.extrusion_multiplier
            else:
                exception_handler("path height of {:.3f} mm is too thin".format(self.coef_h * self.nozzle_diameter)) # TODO Reinis!!!
                filament_length = (4 / math.pi) * (self.nozzle_diameter / self.filament_diameter) ** 2 * (self.coef_w * self.coef_h) * line_length * self.extrusion_multiplier

            kwargs["E"] = filament_length + current_extruder_position
        elif self.extrude is False:
            if self.is_relative is not True:
                kwargs["E"] = 0
            else:
                current_extruder_position = 0
                kwargs["E"] = 0 + current_extruder_position

        self._update_current_position(x=x, y=y, z=z, **kwargs)
        track_list.append((self.current_position["x"], self.current_position["y"], self.current_position["z"]))
        args = self._format_args(x, y, z, **kwargs)
        cmd = "G0 " if rapid else "G1 "
        self.write(cmd + args)

    def abs_move(self, x=None, y=None, z=None, rapid=False, extrude=None, extrusion_multiplier=None, **kwargs):
        """ Same as `move` method, but positions are interpreted as absolute.
        """
        if extrude is not None:
            self.extrude = extrude
        if extrusion_multiplier is not None:
            self.extrusion_multiplier = extrusion_multiplier

        if self.is_relative:
            self.absolute()
            self.move(x=x, y=y, z=z, rapid=rapid, extrude=extrude, extrusion_multiplier=extrusion_multiplier, **kwargs)
            self.relative()
        else:
            self.move(x=x, y=y, z=z, rapid=rapid, extrude=extrude, extrusion_multiplier=extrusion_multiplier, **kwargs)

    def travel(self, x=None, y=None, z=None, speed=None, lift=0.2, retraction_speed=60, retraction_distance=3,  **kwargs):
        """
        Travel move method
        :param x:
        :param y:
        :param z:
        :param speed:
        :param lift:
        :param retraction_speed:
        :param retraction_distance:
        :param kwargs:
        :return:
        """
        temp_speed = self.speed/60 if speed is None else speed
        self.feed(temp_speed*2)
        self.write("G1 F" + str(retraction_speed * 60) + " E" + str(-retraction_distance))
        self.move(z=lift)
        self.move(x, y, z, extrude=False, **kwargs)
        self.move(z=-lift)
        self.write("G1 F" + str(retraction_speed * 60) + " E" + str(retraction_distance))
        self.feed(temp_speed)

    def abs_travel(self, x=None, y=None, z=None, speed=None, lift=0.2, retraction_speed=60, retraction_distance=3, **kwargs):
        """
        Travel absolute move method
        :param x:
        :param y:
        :param z:
        :param speed:
        :param lift:
        :param retraction_speed:
        :param retraction_distance:
        :param kwargs:
        :return:
        """
        temp_speed = self.speed / 60
        self.feed(temp_speed * 2 if speed is None else speed)
        self.write("G1 F" + str(retraction_speed * 60) + " E" + str(-retraction_distance))
        self.move(z=lift)
        self.abs_move(x, y, z+lift, extrude=False, **kwargs)
        self.move(z=-lift)
        self.write("G1 F" + str(retraction_speed * 60) + " E" + str(retraction_distance))
        self.feed(temp_speed)

    def feed(self, rate):
        """ Set the feed rate (tool head speed) in mm/s

        Parameters
        ----------
        rate : float
        The speed to move the tool head in mm/s.

        """
        self.write("G1 F{}".format(rate * 60))
        self.speed = rate * 60
