from mecode import G
from Definitions import *
from paths import gcode_folder
from CLI_helpers import exception_handler
import io

track_list = []


class Gplus(G):
    # Build on the G class from mecode. Gplus class redefines some of the commands, creates new commands
    def __init__(self, material: Material, machine: Machine, *args, **kwargs):

        self.filament_diameter = material.size_od
        self.nozzle_diameter = machine.temperaturecontrollers.extruder.nozzle.size_id
        self.nozzle_od = machine.temperaturecontrollers.extruder.nozzle.size_od
        self.extrusion_multiplier = machine.settings.extrusion_multiplier
        self.track_height = machine.settings.track_height
        self.track_width = machine.settings.track_width
        self.form = machine.form
        self.tool = machine.temperaturecontrollers.extruder.tool
        self.buildarea_maxdim1 = machine.buildarea_maxdim1
        self.buildarea_maxdim2 = machine.buildarea_maxdim2
        self.coef_w = machine.settings.track_width / machine.temperaturecontrollers.extruder.nozzle.size_id
        self.speed_printing = machine.settings.speed_printing
        self._gcode = []
        super(Gplus, self).__init__(*args, **kwargs)
        with open(self.header) as hd:
            [self._gcode.append(statement) for statement in hd.readlines()]


    def set_extruder_temperature(self, temperature: int, extruder: Extruder, immediate: bool=None):
        """Set the liquefier temperature in degC"""
        if immediate:
            if extruder.gcode_command_immediate != "":
                self.write(extruder.gcode_command_immediate.format(temperature, extruder.tool) + "; set the extruder temperature")
        else:
            self.write(extruder.gcode_command.format(temperature, extruder.tool) + "; set the extruder temperature and wait")

    def set_printbed_temperature(self, temperature: float, printbed: Printbed, immediate: bool=None):
        """Set the printbed temperature in degC"""
        if immediate:
            if printbed.gcode_command_immediate != "":
                if printbed.tool:
                    self.write(str(printbed.gcode_command_immediate+" {1}").format(temperature, printbed.tool) + "; set the print bed temperature")
                else:
                    self.write(printbed.gcode_command_immediate.format(temperature) + "; set the print bed temperature")
        else:
            if printbed.tool:
                self.write(str(printbed.gcode_command+" {1}").format(temperature, printbed.tool) + "; set the print bed temperature and wait")
            else:
                self.write(printbed.gcode_command.format(temperature) + "; set the print bed temperature and wait")

    def set_chamber_temperature(self, temperature: int, chamber: Chamber):
        """Set the printbed temperature in degC"""
        self.write(chamber.gcode_command.format(temperature, chamber.tool) + "; set the chamber temperature")

    def set_part_cooling(self, cooling_power: float, extruder: Extruder):
        """Set the cooler power in percent"""
        if cooling_power >= 100:
            cooling_power = 100
        elif cooling_power <= 0:
            pass
        # get a fraction of 255 (max intensity of the cooler)corresponding to the fan percentage
        self.write(extruder.part_cooling_gcode_command.format(int(255 * (cooling_power / 100))) + "; set the cooler speed for part cooling")

    def set_ventilator_exit(self, cooling_power: float, chamber: Chamber):
        """Set the cooler power in percent"""
        if cooling_power >= 100:
            cooling_power = 100
        elif cooling_power < 0:
            pass
        # get a fraction of 255 (max intensity of the cooler)corresponding to the fan percentage
        self.write(chamber.ventilator_exit_gcode_command.format(chamber.ventilator_exit_tool, int(255 * (cooling_power / 100))) + "; set the speed for exit ventilator")

    def set_ventilator_entry(self, cooling_power: float, chamber: Chamber):
        """Set the cooler power in percent"""
        if cooling_power >= 100:
            cooling_power = 100
        elif cooling_power < 0:
            pass
        # get a fraction of 255 (max intensity of the cooler)corresponding to the fan percentage
        self.write(chamber.ventilator_entry_gcode_command.format(chamber.ventilator_entry_tool, int(255 * (cooling_power / 100)) + "; set the speed for entry ventilator"))

    def dwell(self, time: int):
        """ Pause code executions for the given amount of time """
        self.write("G4 P{0:.0f} ".format(time) + "; set the waiting time in ms")

    def home(self):
        """ Move the tool head to the home position (as defined in firmware).
        """
        self.write("G28; move to the home position")

    def retract(self, retraction_speed, retraction_distance, printing_speed):
        """ Retracts the filament """
        self.write("G1 F{:.0f}".format(retraction_speed*60) + " E{:.3f}".format(-retraction_distance) + "; retract the filament")
        self.write("G1 F{:.0f}".format(printing_speed*60))

    def deretract(self, retraction_speed, retraction_distance, printing_speed, retraction_restart_distance=None):
        """ Deretracts the filament """
        if retraction_restart_distance is None:
            retraction_restart_distance = 0
        self.write("G1 F{:.0f}".format(retraction_speed*60) + " E{:.3f}".format(+retraction_distance+retraction_restart_distance) + "; deretract the filament")
        self.write("G1 F{:.0f}".format(printing_speed*60))

    def move(self, x=None, y=None, z=None, rapid=False, extrude=None, extrusion_multiplier=None, coef_w=None, coef_h=None, **kwargs):
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
                exception_handler("path height of {:.3f} mm is too thin".format(self.coef_h * self.nozzle_diameter))
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
        if self.form != "elliptic":
            offset_x = self.buildarea_maxdim1/2
            offset_y = self.buildarea_maxdim2/2
        else:
            offset_x = 0
            offset_y = 0

        x_offset = x + offset_x if x is not None else x
        y_offset = y + offset_y if y is not None else y

        if extrude is not None:
            self.extrude = extrude
        if extrusion_multiplier is not None:
            self.extrusion_multiplier = extrusion_multiplier

        if self.is_relative:
            self.absolute()
            self.move(x=x_offset, y=y_offset, z=z, rapid=rapid, extrude=extrude, extrusion_multiplier=extrusion_multiplier, **kwargs)
            self.relative()
        else:
            self.move(x=x_offset, y=y_offset, z=z, rapid=rapid, extrude=extrude, extrusion_multiplier=extrusion_multiplier, **kwargs)

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
        self.write("G1 F{}".format(int(rate * 60)))
        self.speed = int(rate * 60)
    
    def write(self, statement_in, resp_needed=False):
        self._gcode.append(statement_in)

    def teardown(self, wait=True):
        """ Close the outfile file after writing the footer if opened. This
        method must be called once after all commands.

        Parameters
        ----------
        wait : Bool (default: True)
            Only used if direct_write_model == 'serial'. If True, this method
            waits to return until all buffered lines have been acknowledged.

        """
        if self.footer is not None:
            with open(self.footer) as fd:
                [self._gcode.append(statement) for statement in fd.readlines()]

        # self.buffer.write("\n".join(self._gcode))

    @property
    def gcode(self):
        return "\n".join(self._gcode)
