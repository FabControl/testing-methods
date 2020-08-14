from mecode import G
from Definitions import *
from paths import gcode_folder
from CLI_helpers import exception_handler, printing_time, extruded_filament
from string import Template
import io
import re


class Gplus(G):
    # Build on the G class from mecode. Gplus class redefines some of the commands, creates new commands
    def __init__(self, material: Material, machine: Machine, *args, **kwargs):

        self.nozzle_diameter = machine.temperaturecontrollers.extruder.nozzle.size_id
        self.extrusion_multiplier = machine.settings.extrusion_multiplier
        self.track_height = machine.settings.track_height
        self.track_width = machine.settings.track_width
        self.form = machine.form
        self.tool = machine.temperaturecontrollers.extruder.tool
        self.buildarea_maxdim1 = machine.buildarea_maxdim1
        self.buildarea_maxdim2 = machine.buildarea_maxdim2
        self.coef_w = machine.settings.track_width / machine.temperaturecontrollers.extruder.nozzle.size_id
        self.speed_printing = machine.settings.speed_printing
        self.retraction_speed = machine.settings.retraction_speed
        self.offset_z = machine.settings.offset_z
        self.use_temperature_wait_cmd = 'flashforge' in machine.model.lower()
        self._machine = machine
        self._gcode = []

        super(Gplus, self).__init__(*args, **kwargs)

        self._gcode = [machine.gcode_header,
                    ";----- end of user defined header -----"]

        self.filament_diameter = material.size_od

    def set_extruder_temperature(self,
                                 temperature: int,
                                 extruder: Extruder,
                                 immediate: bool=None,
                                 return_string: bool=None):
        """Set the liquefier temperature in degC"""
        if immediate:
            if extruder.gcode_command_immediate != "":
                t = Template(extruder.gcode_command_immediate + "; set the extruder temperature and apply immediately")
        else:
            t = Template(extruder.gcode_command  + "; set the extruder temperature and wait till it has been reached")
        result = t.substitute(temp=f'{temperature:.0f}', tool=extruder.tool)
        self.write(result)
        # FlashForge specific wait for temperature to be reached
        if not immediate and self.use_temperature_wait_cmd:
            self.write('M6 {}'.format(extruder.tool))
        if return_string:
            return result

    def set_printbed_temperature(self,
                                 temperature: int,
                                 printbed: Printbed,
                                 immediate: bool=None,
                                 return_string: bool=None):
        """Set the printbed temperature in degC"""
        if immediate:
            gcode_command = printbed.gcode_command_immediate + "; set the print bed temperature and apply immediately"
        else:
            gcode_command = printbed.gcode_command + "; set the print bed temperature and wait till the temperature has been reached"

        t = Template(gcode_command)
        result = t.substitute(temp=f'{temperature:.0f}')
        self.write(result)
        # FlashForge specific wait for temperature to be reached
        if not immediate and self.use_temperature_wait_cmd:
            self.write('M7')
        if return_string:
            return result

    def set_chamber_temperature(self,
                                temperature: int,
                                chamber: Chamber,
                                immediate: bool=None,
                                return_string: bool=None):
        """Set the chamber temperature in degC"""
        if immediate:
            gcode_command = chamber.gcode_command_immediate + " $tool; set the chamber temperature and apply immediately"
        else:
            gcode_command = chamber.gcode_command + " $tool; set the chamber temperature and wait till the temperature has been reached"

        if "T" in chamber.tool:
            t = Template(gcode_command)
            self.write(t.substitute(temp=temperature, tool=chamber.tool))
            if return_string:
                return t.substitute(temp=temperature, tool=chamber.tool)
        else:
            t = Template(gcode_command.replace(" $tool",""))
            self.write(t.substitute(temp=temperature))
            if return_string:
                return t.substitute(temp=temperature)

    def set_part_cooling(self,
                         cooling_power: float,
                         extruder: Extruder,
                         return_string: bool=None):
        """Set the cooler power in percent"""
        if cooling_power >= 100:
            cooling_power = 100
        elif cooling_power <= 0:
            pass
        # get a fraction of 255 (max intensity of the cooler)corresponding to the fan percentage
        t = Template(extruder.part_cooling_gcode_command + "; set the cooler speed for part cooling")
        self.write(t.substitute(cool=int(255 * (cooling_power / 100))))
        if return_string:
            return t.substitute(cool=int(255 * (cooling_power / 100)))

    def set_ventilator_exit(self,
                            cooling_power: float,
                            chamber: Chamber):
        """Set the cooler power in percent"""
        if cooling_power >= 100:
            cooling_power = 100
        elif cooling_power < 0:
            pass
        # get a fraction of 255 (max intensity of the cooler)corresponding to the fan percentage
        t = Template(chamber.ventilator_exit_gcode_command + "; set the speed for exit ventilator")
        self.write(t.substitute(tool=chamber.ventilator_exit_tool,cool=int(255 * (cooling_power / 100))))

    def set_ventilator_entry(self,
                             cooling_power: float,
                             chamber: Chamber):
        """Set the cooler power in percent"""
        if cooling_power >= 100:
            cooling_power = 100
        elif cooling_power < 0:
            pass
        # get a fraction of 255 (max intensity of the cooler)corresponding to the fan percentage
        t = Template(chamber.ventilator_exit_gcode_command + "; set the speed for entry ventilator")
        self.write(t.substitute(tool=chamber.ventilator_exit_tool,cool=int(255 * (cooling_power / 100))))

    def dwell(self,
              time: int):
        """ Pause code executions for the given amount of time """
        self.write("G4 P{0:.0f} ".format(time) + "; set the waiting time in ms")

    def home(self):
        """ Move the tool head to the home position (as defined in firmware) """
        self.write(self._machine.home_command)

    def toolchange(self, tool_index):
        self.write(self._machine.toolchange_command.replace('$tool_index$', str(tool_index)))

    def retract(self,
                retraction_speed,
                retraction_distance,
                printing_speed):
        """ Retracts the filament """
        self.write(f"G1 F{retraction_speed * 60:.0f} E{-retraction_distance}; retract the filament")
        self.write(f"G1 F{printing_speed*60:.0f}")

    def deretract(self,
                  retraction_speed,
                  retraction_distance,
                  printing_speed,
                  retraction_restart_distance=None):
        """ Deretracts the filament """
        if retraction_restart_distance is None:
            retraction_restart_distance = 0
        self.write("G1 F{:.0f}".format(retraction_speed*60) + " E{:.3f}".format(+retraction_distance+retraction_restart_distance) + "; deretract the filament")
        self.write("G1 F{:.0f}".format(printing_speed*60))

    def move(self,
             x=None, y=None, z=None,
             rapid=False,
             extrude=None,
             extrusion_multiplier=None,
             coef_w=None, coef_h=None, **kwargs):
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
        args = self._format_args(x, y, z, **kwargs)
        cmd = "G0 " if rapid else "G1 "
        self.write(cmd + args)

    def abs_move(self,
                 x=None, y=None, z=None,
                 rapid=False,
                 extrude=None, extrusion_multiplier=None, use_offset_z=True, **kwargs):
        """ Same as `move` method, but positions are interpreted as absolute.
        """
        if use_offset_z:
            z = z + self.offset_z
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

    def travel(self,
               x=None, y=None, z=None,
               speed=None,
               retraction_speed=None,
               lift=0.2, retraction_distance=2,  **kwargs):
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
        self.retraction_speed = retraction_speed
        temp_speed = self.speed/60 if speed is None else speed
        self.feed(temp_speed*2)
        self.write(f"G1 F{self.retraction_speed * 60:.0f} E {-retraction_distance:.3f}")
        self.move(z=lift, rapid=True)
        self.move(x, y, z, extrude=False, rapid=True, **kwargs)
        self.move(z=-lift, rapid=True)
        self.write(f"G1 F{self.retraction_speed * 60:.0f} E {retraction_distance:.3f}")
        self.feed(temp_speed)

    def abs_travel(self,
                   x=None, y=None, z=None,
                   speed=None,
                   retraction_speed=None,
                   lift=0.2, retraction_distance=2, **kwargs):
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
        self.retraction_speed = retraction_speed
        temp_speed = self.speed / 60
        self.feed(temp_speed * 2 if speed is None else speed)
        self.write(f"G1 F{self.retraction_speed * 60:.0f} E {-retraction_distance:.3f}")
        self.move(z=lift)
        self.abs_move(x, y, z+lift, extrude=False, **kwargs)
        self.move(z=-lift)
        self.write(f"G1 F{self.retraction_speed * 60:.0f} E {retraction_distance:.3f}")
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
        # Ensure that E0.00000 is never passed to gcode
        statement_in = re.sub(r"E-{0,1}0\.0+([^0-9]|$)", r'\1', statement_in)
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
        self.write(";----- start of user defined footer -----")
        self.write(self._machine.gcode_footer)

        # self.buffer.write("\n".join(self._gcode))

    @property
    def gcode(self):
        return "\n".join(self._gcode)

    def gcode_post_process(self, persistence):
        """
        Substitutes variables following the convention of `$variable$`
        :param persistence:
        :return:
        """
        temp_gcode = self.gcode
        exposed_variables = {'nozzle_size': persistence.machine.temperaturecontrollers.extruder.nozzle.size_id,
                             'temperature_printbed': persistence.dict['settings']['temperature_printbed_setpoint'],
                             'extrusion_temperature_raft': persistence.dict['settings']['temperature_extruder_raft'],
                             'size_x': persistence.machine.buildarea_maxdim1,
                             'size_y': persistence.machine.buildarea_maxdim2,
                             '3dprinter_model': persistence.machine.model,
                             'print_time': printing_time(temp_gcode, as_datetime=True).seconds,
                             'extruded_filament': int(extruded_filament(temp_gcode)/10*(persistence.material.size_od*math.pi) ** 2)}  # Extruded filament in cm^3
        for parameter, value in exposed_variables.items():
            query = f'${parameter}$'
            temp_gcode = temp_gcode.replace(query, str(value))

        return temp_gcode
