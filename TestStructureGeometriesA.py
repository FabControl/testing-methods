from Definitions import *
from get_values_A import get_values_A
from GetValuesB import TestSetupB


class TestStructure(object):
    def __init__(self, persistence):
        self.persistence = persistence
        self.machine = self.persistence.machine
        self.gcode = None

    # WIPE
    def wipe(self, gv: get_values_A or TestSetupB, length_multiplier=1):
        wipe_length_initial = 6 * gv.test_structure_size / 10
        wipe_length = wipe_length_initial * length_multiplier

        if self.machine.temperaturecontrollers.chamber.chamber_heatable:
            gv.g.set_chamber_temperature(gv.temperature_chamber_setpoint, gv.chamber)

        if self.machine.temperaturecontrollers.printbed.printbed_heatable:
            gv.g.set_printbed_temperature(gv.temperature_printbed_setpoint, gv.printbed, immediate=True)
            if gv.temperature_printbed_setpoint >= 30:
                gv.g.set_printbed_temperature(gv.temperature_printbed_setpoint, gv.printbed)

        gv.g.set_extruder_temperature(self.machine.settings.temperature_extruder_raft, gv.extruder, immediate=True)
        gv.g.set_extruder_temperature(self.machine.settings.temperature_extruder_raft, gv.extruder)
        gv.g.home()
        gv.g.write("G21; unit in mm")
        gv.g.write("G92 E0; reset extruder")
        gv.g.write("M83; set extruder to relative mode")
        gv.g.feed(self.machine.settings.speed_travel) # respect the units: mm/min
        self.initial_position = {'x': -wipe_length + gv.offset_x,
                            'y': -6 * gv.test_structure_size / 10 + gv.offset_y,
                            'z': +2 * np.mean(gv.coef_h_raft) * gv.extruder.nozzle.size_id + 0.001}
        gv.g.abs_move(**self.initial_position,
                      extrude=False, extrusion_multiplier=0)

        gv.g.write("; --- start to clean the nozzle ---")

        gv.g.dwell(5000)
        if self.machine.temperaturecontrollers.extruder.nozzle.size_id <= 0.4:
            output = "G1 F1000 E2.5; extrude 2.5 mm of material"
        else:
            output = "G1 F1000 E5.0; extrude 5.0 mm of material"

        gv.g.write(output)
        gv.g.dwell(5000)
        gv.g.feed(self.machine.settings.speed_printing_raft)  # print the raft

        if isinstance(gv, get_values_A):
            # The long movement along X axis to Z=0
            gv.g.abs_move(x=self.initial_position['x']+2 * wipe_length,
                          z=0.01, extrude=True, extrusion_multiplier=2.25, coef_h=np.mean(gv.coef_h_raft), coef_w=np.mean(gv.coef_w_raft))
            # Short movement on Y axis to nominal Z coordinates
            gv.g.abs_move(y=self.initial_position['y']+gv.test_structure_size / 10,
                          z=self.persistence.dict['settings']['track_height_raft'])
            gv.g.move(x=-wipe_length_initial / 6 + (1 - length_multiplier) * wipe_length_initial,
                      y=0,
                      z=0,
                      extrude=False, extrusion_multiplier=0)

        gv.g.write("; --- end to clean the nozzle ---")

        return

    # RAFT PERIMETER
    # prints the outer perimeter of the raft
    def raft_perimeter(self, values: get_values_A):
        values.g.write("; --- print the outer perimeter ---")
        values.g.feed(self.machine.settings.speed_printing_raft / 3)
        for dummy in range(2):
            for _ in range(20):
                values.g.move(x=0,
                              y=(-1) ** dummy * values.test_structure_size / 20,
                              z=0,
                              extrude=True, extrusion_multiplier=1.5, coef_h=np.mean(values.coef_h_raft), coef_w=np.mean(values.coef_w_raft))
            for _ in range(20):
                values.g.move(x=(-1) ** (dummy + 1) * values.test_structure_size / 20,
                              y=0,
                              z=0,
                              extrude=True, extrusion_multiplier=1.5, coef_h=np.mean(values.coef_h_raft), coef_w=np.mean(values.coef_w_raft))

        return

    # PRINTING RAFT
    # prints the filling of the raft
    def print_raft(self, values: get_values_A):
        values.g.write("; --- start to print the raft ---")
        self.raft_perimeter(values)
        values.g.write("; --- print the infill with the density of {0} % ---".format(self.machine.settings.raft_density))
        values.g.feed(values.speed_printing_raft)
        raft_density = self.machine.settings.raft_density/100
        step = self.persistence.dict['settings']['track_width_raft'] / raft_density  # step size
        step_number = int(values.test_structure_size / step) if (int(values.test_structure_size / step) % 2) == 0 else int(values.test_structure_size / step) + 1

        values.g.move(x=-np.mean(values.coef_w_raft) * self.machine.temperaturecontrollers.extruder.nozzle.size_id / 2,
                      y=0,
                      z=0,
                      extrude=False, extrusion_multiplier=0)

        for dummy in range(0, step_number):
            values.g.move(x=0,
                          y=+step,
                          z=0,
                          extrude=False, extrusion_multiplier=0)
            for _ in range(20):
                values.g.move(x=(-1) ** (dummy + 1) * (values.test_structure_size - np.mean(values.coef_w_raft) * self.machine.temperaturecontrollers.extruder.nozzle.size_id) / 20,
                              y=0,
                              z=0,
                              extrude=True, extrusion_multiplier=self.persistence.dict['settings']['extrusion_multiplier'], coef_h=np.mean(values.coef_h_raft), coef_w=np.mean(values.coef_w_raft))

        values.g.write("; --- finish to print the raft ---")

        if not values.raft:
            values.g.move(x=0,
                          y=20,
                          z=0,
                          extrude=False, extrusion_multiplier=0)

        if values.test_number not in ["01", "02", "03"]:
            values.g.abs_move(z=self.initial_position['z'] + 3, extrude=False)
            values.g.set_extruder_temperature(self.machine.settings.temperature_extruder, values.extruder, immediate=True)
            values.g.set_extruder_temperature(self.machine.settings.temperature_extruder, values.extruder, dwell=15000, use_safe_spot=True)
            values.g.abs_move(z=self.initial_position['z'], extrude=False)

        if values.part_cooling:
            values.g.set_part_cooling(values.part_cooling_setpoint, values.extruder)

        return

    # GENERIC TEST ROUTINE: SINGLE TESTING PARAMETER vs. PRINTING SPEED
    def flat_test_parameter_one_vs_parameter_two(self, values: get_values_A):
        values.g.write(values.title)
        values.g.write(values.comment_all_values_of_variable_parameters)
        self.wipe(values, length_multiplier=1 if self.machine.temperaturecontrollers.extruder.nozzle.size_id < 0.59 else 0.85)
        # print the raft to support the test structure
        self.print_raft(values) if values.raft else self.raft_perimeter(values)

        if self.persistence.dict['session']['test_number'] == '14':
            values.g.toolchange(1)

        values.g.write("; --- start to print the test structure ---")
        if self.machine.settings.speed_printing > 0:
            values.g.feed(self.machine.settings.speed_printing)

        for current_test_structure in range(values.number_of_test_structures):
            values.g.write(values.comment_all_values_of_constant_parameters)
            values.g.write(values.comment_current_values_of_variable_parameter[current_test_structure])

            if values.test_name == "extrusion temperature vs printing speed":
                values.g.travel(x=-values.test_structure_width[current_test_structure] - values.test_structure_separation,
                                y=+values.step_y if current_test_structure != 0 else 0,
                                lift=1,
                                retraction_speed=np.mean(values.retraction_speed))
                values.g.travel(x=0,
                                y=+values.test_structure_size / 7,
                                retraction_speed=np.mean(values.retraction_speed),
                                retraction_distance=values.retraction_distance[current_test_structure])

                values.g.absolute()
                values.g.abs_move(z=+values.abs_z[current_test_structure]+2)
                values.g.set_extruder_temperature(values.temperature_extruder[current_test_structure],
                                                  values.extruder,
                                                  dwell=30000,
                                                  use_safe_spot=True,
                                                  prime_after_heating=4 * values.temperature_extruder[current_test_structure] / values.temperature_extruder[0])
                values.g.abs_move(z=+values.abs_z[current_test_structure])
                values.g.move(x=0,
                              y=-values.test_structure_size / 7,
                              extrude=True, extrusion_multiplier=0)

            else:
                values.g.travel(x=-values.test_structure_width[current_test_structure] - values.test_structure_separation,
                                y=0 if (current_test_structure == 0 and values.raft) else +values.step_y,
                                lift=1,
                                retraction_speed=np.mean(values.retraction_speed))
                values.g.abs_move(z=+values.abs_z[current_test_structure])

            for current_substructure in range(values.number_of_substructures):
                current_printing_speed = values.speed_printing[current_test_structure] if values.test_info.parameter_two.values == [] else values.parameter_two.values[current_substructure]

                values.g.write("; --- testing the following printing speed value: {:.3f} mm/s".format(current_printing_speed))
                values.g.feed(current_printing_speed)

                values.g.abs_move(z=values.abs_z[current_test_structure],
                                  extrude=False, extrusion_multiplier=0)

                for current_layer in range(values.number_of_layers):  # layers
                    for current_line in range(values.number_of_lines):
                        values.g.move(x=0,
                                      y=(-1) ** (current_line+1) * values.step_y / values.number_of_substructures,
                                      z=0,
                                      extrude=True, extrusion_multiplier=values.extrusion_multiplier[current_test_structure],
                                      coef_h=values.coef_h[current_test_structure], coef_w=values.coef_w[current_test_structure])
                        values.g.move(x=(-1) ** (current_layer + 1) * values.step_x[current_test_structure],
                                      y=0,
                                      z=0,
                                      extrude=False, extrusion_multiplier=0)

                        if current_line == values.number_of_lines - 1:
                            values.g.move(x=0,
                                          y=(-1) ** (current_line+2) * values.step_y / values.number_of_substructures,
                                          z=0,
                                          extrude=True, extrusion_multiplier=values.extrusion_multiplier[current_test_structure],
                                          coef_h=values.coef_h[current_test_structure], coef_w=values.coef_w[current_test_structure])

                    if current_layer == values.number_of_layers - 1:
                            values.g.travel(x=+values.test_structure_width[current_test_structure + 1] if values.number_of_layers % 2 != 0 else 0,
                                            y=0,
                                            lift=1,
                                            retraction_speed=np.mean(values.retraction_speed))
                    else:
                        values.g.abs_move(z=values.abs_z[current_test_structure] + (current_layer + 1) * values.track_height[current_test_structure],
                                          extrude=False, extrusion_multiplier=0)
                        values.g.move(x=0,
                                      y=(-1) ** (current_line + 1) * values.step_y / values.number_of_substructures,
                                      z=0,
                                      extrude=False, extrusion_multiplier=0)

        values.g.write("; --- finish to print the test structure ---")
        self.write_footer(values)
        values.g.teardown()

        return

    # RETRACTION RESTART DISTANCE and COASTING DISTANCE
    def retraction_restart_distance_vs_coasting_distance(self, values: get_values_A):
        values.g.write(values.title)
        values.g.write(values.comment_all_values_of_variable_parameters)
        self.wipe(values, length_multiplier=1 if self.machine.temperaturecontrollers.extruder.nozzle.size_id < 0.59 else 0.85)
        # print the raft to support the test structure
        self.print_raft(values) if values.raft else self.raft_perimeter(values)

        values.g.write("; --- start to print the test structure ---")

        for current_test_structure in range(values.number_of_test_structures):
            values.g.write(values.comment_all_values_of_constant_parameters)
            values.g.write(values.comment_current_values_of_variable_parameter[current_test_structure])
            current_printing_speed = values.speed_printing[0]
            values.g.feed(current_printing_speed)

            values.g.travel(x=-values.test_structure_width[current_test_structure] - values.test_structure_separation,
                            y=0 if (current_test_structure == 0 and values.raft) else +values.step_y,
                            lift=1,
                            retraction_speed=np.mean(values.retraction_speed))

            values.g.abs_move(z=+values.abs_z[current_test_structure])
            step_x = values.step_x[current_test_structure]

            for current_substructure in range(values.number_of_substructures):
                current_printing_speed = values.speed_printing[current_substructure]
                values.g.write("; --- testing the following printing speed value: {:.1f} mm/s".format(current_printing_speed))

                coasting_distance = values.coasting_distance

                for current_line in range(values.number_of_lines):
                    values.g.move(x=0,
                                  y=-(values.step_y / (2 * values.number_of_substructures) - coasting_distance[current_line]),
                                  z=0,
                                  extrude=True, extrusion_multiplier=values.extrusion_multiplier[current_test_structure], coef_h=values.coef_h[current_test_structure], coef_w=values.coef_w[current_test_structure])
                    values.g.move(x=0,
                                  y=-coasting_distance[current_line],
                                  z=0,
                                  extrude=False, extrusion_multiplier=0)

                    values.g.retract(values.retraction_speed, values.retraction_distance[current_substructure], current_printing_speed)
                    values.g.move(x=0,
                                  y=-values.step_y / (2 * values.number_of_substructures),
                                  z=0,
                                  extrude=False, extrusion_multiplier=0)
                    values.g.move(x=-step_x,
                                  y=0,
                                  z=0,
                                  extrude=False, extrusion_multiplier=0)

                    if current_line != values.number_of_lines - 1:
                        values.g.move(x=0,
                                      y=+values.step_y / values.number_of_substructures,
                                      z=0,
                                      extrude=False, extrusion_multiplier=0)
                    else:
                        values.g.move(x=step_x * values.number_of_lines,
                                      y=0,
                                      z=0,
                                      extrude=False, extrusion_multiplier=0)
                    values.g.deretract(values.retraction_speed, values.retraction_distance[current_test_structure], current_printing_speed, values.retraction_restart_distance[current_test_structure])

        values.g.write("; --- finish to print the test structure ---")
        self.write_footer(values)
        values.g.teardown()

        return

    # BRIDGING EXTRUSION MULTIPLIER vs. BRIDGING PRINTING SPEED
    def bridging_test(self, values: get_values_A):
        values.g.write(values.title)
        values.g.write(values.comment_all_values_of_variable_parameters)
        values.g.write(values.comment_all_values_of_constant_parameters)

        self.wipe(values, length_multiplier=1 if self.machine.temperaturecontrollers.extruder.nozzle.size_id < 0.59 else 0.85)

        if values.raft:
            self.print_raft(values)  # print the raft to support the test structure

        values.g.write("; --- start to print the support structure ---")

        values.g.feed(self.machine.settings.speed_printing)

        angle = 45
        number_of_perimeters = 4

        step_x = values.test_structure_size / ((values.number_of_test_structures + 1) / 2) / 2
        step_y = (values.test_structure_size - (values.number_of_substructures + 1) * number_of_perimeters * np.mean(values.track_width) / np.sin(np.deg2rad(angle))) // values.number_of_substructures

        values.g.travel(x=0,
                        y=-step_y - number_of_perimeters * np.mean(values.track_width) / np.sin(np.deg2rad(angle)),
                        lift=1, retraction_speed=np.mean(values.retraction_speed))

        # Building support structures
        for current_layer in range(values.number_of_layers):
            values.g.abs_move(z=+np.mean(values.abs_z) + current_layer * np.mean(values.track_height))

            for current_substructure in range(values.number_of_substructures):
                for current_perimeter_line in range(number_of_perimeters):
                    for current_l_structure in range(int((values.number_of_test_structures + 1) / 2)):
                        values.g.move(x=(-1) ** (current_perimeter_line + 1) * step_x,
                                      y=+step_y,
                                      z=0,
                                      extrude=True, extrusion_multiplier=np.mean(values.extrusion_multiplier))
                        values.g.move(x=(-1) ** (current_perimeter_line + 1) * step_x,
                                      y=-step_y,
                                      z=0,
                                      extrude=True, extrusion_multiplier=np.mean(values.extrusion_multiplier))

                    if current_perimeter_line != range(number_of_perimeters)[-1]:
                        values.g.move(x=0,
                                      y=+np.mean(values.track_width) / np.sin(np.deg2rad(angle)),
                                      z=0,
                                      extrude=False, extrusion_multiplier=0)

                if current_substructure != values.number_of_substructures-1:
                    values.g.travel(x=0,
                                    y=-step_y - 2 * number_of_perimeters * np.mean(values.track_width) / np.sin(np.deg2rad(angle)),
                                    z=0,
                                    lift=1,
                                    retraction_speed=np.mean(values.retraction_speed),
                                    retraction_distance=np.mean(values.retraction_distance))

            values.g.travel(x=0,
                            y=+(values.number_of_substructures - 1) * step_y + (values.number_of_substructures - 1) * number_of_perimeters * np.mean(values.track_width) / np.sin(np.deg2rad(angle)),
                            z=0,
                            lift=1,
                            retraction_speed=np.mean(values.retraction_speed),
                            retraction_distance=np.mean(values.retraction_distance))

        values.g.write("; --- finish to print the support structure ---")
        values.g.move(z=+np.mean(values.track_height))
        values.g.write("; --- start to print the bridges ---")

        # Printing bridges
        if values.part_cooling:
            values.g.set_part_cooling(values.bridging_part_cooling, values.extruder)

        for index_current_speed, current_speed_value in enumerate(values.parameter_two.values):
            values.g.write("; --- testing the following bridging speed value: {:.1f} mm/s ---".format(current_speed_value))
            values.g.feed(current_speed_value)

            for index_current_extrusion_multiplier, current_extrusion_multiplier_value in enumerate(values.extrusion_multiplier_bridging):
                values.g.write(values.comment_all_values_of_constant_parameters)
                values.g.write(values.comment_current_values_of_variable_parameter[index_current_extrusion_multiplier])

                for step in range(int(step_y/np.mean(values.track_width))):
                    values.g.move(x=(-1) ** (step + 1) * 2 * (step_y - step * np.mean(values.track_width)) * step_x / step_y,
                                  y=0,
                                  z=0,
                                  extrude=True, extrusion_multiplier=current_extrusion_multiplier_value)
                    if step != range(int(step_y/np.mean(values.track_width)))[-1]:
                        values.g.move(x=0,
                                      y=(-1)**index_current_extrusion_multiplier*np.mean(values.track_width),
                                      z=0,
                                      extrude=False, extrusion_multiplier=0)
                        values.g.move(x=(-1) ** step * np.mean(values.track_width) * step_x / step_y,
                                      y=0,
                                      z=0,
                                      extrude=False, extrusion_multiplier=0)
                    else:
                        values.g.move(x=(-1) ** step * (step_y - step * np.mean(values.track_width)) * step_x / step_y,
                                      y=0,
                                      z=0,
                                      extrude=False, extrusion_multiplier=0)
            values.g.travel(x=+values.number_of_test_structures * step_x,
                            y=-2 * step_y - number_of_perimeters * np.mean(values.track_width) / np.sin(np.deg2rad(angle)),
                            z=0,
                            lift=1,
                            retraction_speed=np.mean(values.retraction_speed),
                            retraction_distance=np.mean(values.retraction_distance))

        values.g.write("; --- finish to print the test structure ---")
        self.write_footer(values)
        values.g.teardown()

        return

    # FIXED RETRACTION DISTANCE vs VARIABLE PRINTING SPEED
    # FIXED RETRACTION DISTANCE vs VARIABLE RETRACTION SPEED
    # VARIABLE RETRACTION DISTANCE at FIXED PRINTING SPEED and FIXED RETRACTION SPEED
    # VARIABLE EXTRUSION TEMPERATURE vs VARIABLE RETRACTION DISTANCE

    def retraction_distance(self, values: get_values_A):
        values.g.write(values.title)
        values.g.write(values.comment_all_values_of_variable_parameters)
        self.wipe(values, length_multiplier=1 if self.machine.temperaturecontrollers.extruder.nozzle.size_id < 0.59 else 0.85)  # perform wipe of the nozzle
        self.print_raft(values)  # print the raft to support the test structure
        values.g.write("; --- start to print the test structure ---")
        values.g.travel(x=-values.test_structure_width[0] - values.test_structure_separation,
                        y=0,
                        lift=1,
                        retraction_speed=np.mean(values.retraction_speed))

        values.g.abs_move(z=+values.abs_z[0])

        current_temperature = -1
        for current_test_structure in range(values.number_of_test_structures):
            output = str("; --- testing the {0} of {1} {2} ---".format(values.parameter_one.name, values.parameter_one.precision, values.parameter_one.units))
            output = str(output.format(values.parameter_one.values[current_test_structure]))
            values.g.write(output)
            values.g.write(values.comment_all_values_of_constant_parameters)

            for current_substructure in range(values.number_of_substructures): # TODO comments

                if values.test_number in ("09", "10", "11"):
                    current_speed_printing = values.speed_printing[current_substructure]
                    current_retraction_distance = values.retraction_distance[current_test_structure]
                elif values.test_number == "08":
                    current_speed_printing = np.mean(values.speed_printing)
                    current_retraction_distance = values.retraction_distance[current_substructure]
                    output = str("; --- testing the {0} of {1} {2} ---".format(values.parameter_two.name, values.parameter_two.precision, values.parameter_two.units))
                    output = str(output.format(values.parameter_two.values[current_substructure]))
                    values.g.write(output)

                if current_substructure == 0 and current_temperature != values.temperature_extruder[current_test_structure]:
                    values.g.travel(x=0,
                                    y=+values.test_structure_size / 7,
                                    z=+values.abs_z[current_test_structure],
                                    retraction_speed=values.retraction_speed[0],
                                    retraction_distance=np.mean(values.retraction_distance))
                    values.g.abs_move(z=values.abs_z[current_test_structure]+3, extrude=False)
                    values.g.set_extruder_temperature(values.temperature_extruder[current_test_structure],
                                                      values.extruder,
                                                      dwell=30000,
                                                      use_safe_spot=True,
                                                      prime_after_heating=1.5 * values.temperature_extruder[current_test_structure] / values.temperature_extruder[0])

                    values.g.abs_move(z=values.abs_z[current_test_structure], extrude=False)
                    values.g.move(x=0,
                                  y=-values.test_structure_size / 7,
                                  extrude=True, extrusion_multiplier=0)
                    current_temperature = values.temperature_extruder[current_test_structure]

                for current_layer in range(0, values.number_of_layers):  # layers
                    for current_line in range(values.number_of_lines):
                        current_retraction_speed = values.retraction_speed[current_substructure] if values.test_number in ("11") else values.retraction_speed[current_line]

                        step_x = values.step_x[current_test_structure]

                        values.g.move(x=-step_x,
                                      y=0,
                                      z=0,
                                      extrude=False, extrusion_multiplier=0)

                        values.g.feed(current_speed_printing)

                        values.g.move(x=0,
                                      y=((-1)**(current_line+1)) * values.step_y / (3 * values.number_of_substructures),
                                      z=0,
                                      extrude=True, extrusion_multiplier=values.extrusion_multiplier[current_test_structure],
                                      coef_h=values.coef_h[current_test_structure], coef_w=values.coef_w[current_test_structure])

                        values.g.retract(current_retraction_speed, current_retraction_distance, current_speed_printing)

                        values.g.move(x=0,
                                      y=((-1)**(current_line+1)) * values.step_y / (3 * values.number_of_substructures),
                                      z=0,
                                      extrude=False, extrusion_multiplier=0)

                        values.g.deretract(current_retraction_speed, current_retraction_distance, current_speed_printing)

                        values.g.move(x=0,
                                      y=((-1)**(current_line+1)) * values.step_y / (3 * values.number_of_substructures),
                                      z=0,
                                      extrude=True, extrusion_multiplier=values.extrusion_multiplier[current_test_structure], coef_h=values.coef_h[current_test_structure], coef_w=values.coef_w[current_test_structure])

                    if current_layer == values.number_of_layers - 1:
                        if current_substructure == values.number_of_substructures - 1:
                            values.g.travel(x=-values.test_structure_separation,
                                            y=+(values.number_of_substructures - 1) * values.step_y / values.number_of_substructures,
                                            lift=1,
                                            retraction_speed=np.mean(values.retraction_speed))
                        else:
                            values.g.travel(x=+step_x * values.number_of_lines,
                                            y=-values.step_y / values.number_of_substructures,
                                            lift=1,
                                            retraction_speed=np.mean(values.retraction_speed))
                        values.g.abs_move(z=+values.abs_z[current_test_structure],
                                          extrude=False, extrusion_multiplier=0)
                    else:
                        values.g.travel(x=+step_x * values.number_of_lines,
                                        lift=1,
                                        retraction_speed=np.mean(values.retraction_speed))
                        values.g.move(z=+values.track_height[current_test_structure],
                                      extrude=False, extrusion_multiplier=0)

        values.g.write("; --- finish to print the test structure ---")
        self.write_footer(values)
        values.g.teardown()

        return

    def offset_z(self, gv: get_values_A or TestSetupB):
        wipe_length = 100
        offset_z = gv.offset_z[::-1]
        notch_depth = 10

        if self.machine.temperaturecontrollers.printbed.printbed_heatable:
            gv.g.set_printbed_temperature(gv.temperature_printbed_setpoint, gv.printbed, immediate=True)
            if gv.temperature_printbed_setpoint >= 30:
                gv.g.set_printbed_temperature(gv.temperature_printbed_setpoint, gv.printbed)

        gv.g.set_extruder_temperature(self.machine.settings.temperature_extruder_raft, gv.extruder, immediate=True)
        gv.g.set_extruder_temperature(self.machine.settings.temperature_extruder_raft, gv.extruder)
        gv.g.home()
        gv.g.write("G21; unit in mm")
        gv.g.write("G92 E0; reset extruder")
        gv.g.write("M83; set extruder to relative mode")
        gv.g.feed(self.machine.settings.speed_travel)  # respect the units: mm/s
        initial_position = {'x': wipe_length/2 + gv.offset_x,
                            'y': gv.offset_y,
                            'z': offset_z[0] + self.machine.settings.track_height_raft}
        gv.g.abs_move(**initial_position,
                      extrude=False, extrusion_multiplier=0)
        gv.g.write(gv.title)
        gv.g.write(gv.comment_all_values_of_variable_parameters)
        gv.g.write("; --- starting z-offset test ---")

        gv.g.dwell(5000)
        if self.machine.temperaturecontrollers.extruder.nozzle.size_id <= 0.4:
            output = "G1 F1000 E2.5; purge 2.5 mm of material"
        else:
            output = "G1 F1000 E5.0; purge 5.0 mm of material"

        gv.g.write(output)
        gv.g.dwell(5000)
        gv.g.feed(self.machine.settings.speed_printing_raft/2)

        if isinstance(gv, get_values_A):
            gv.g.extrude = True
            lateral_step = wipe_length / (gv.number_of_test_structures-1)
            vertical_step = (max(gv.offset_z) - min(gv.offset_z)) / (gv.number_of_test_structures-1)
            track_width = self.machine.settings.track_width

            gv.g.write(f'; Starting to print a measuring notch at the initial height of {gv.offset_z[0]} mm.')
            gv.g.move(y=notch_depth, extrude=True, extrusion_multiplier=1)
            gv.g.move(x=-track_width)
            gv.g.move(y=-notch_depth)
            for offset in offset_z[:-1]:
                # Offset change
                gv.g.move(x=-lateral_step-track_width, z=-vertical_step)
                gv.g.write(f'; Reached Z height of {offset} mm, printing a measuring notch.')
                # Measuring notch
                gv.g.move(y=notch_depth)
                gv.g.move(x=-track_width)
                gv.g.move(y=-notch_depth)
            gv.g.move(z=10, extrude=False)
            gv.g.write("; --- finish to print the test structure ---")
            self.write_footer(gv)
            gv.g.teardown()

        return

    def detachable_support(self, v: get_values_A or TestSetupB):
        def direction(num: int):
            """
            Checks in which direction should a line be printed, depending on line index.
            Returns either 1 or -1.
            :param num:
            :return:
            """
            # this works correctly, even if num == 0
            if num % 2 == 0:
                return -1
            else:
                return 1

        #  Convenience variables
        g = v.g
        size = v.test_structure_size
        width = np.mean(v.test_structure_width)
        gap = v.test_structure_separation
        num_x = v.number_of_test_structures
        num_y = v.number_of_substructures
        track_width = v.track_width[0]
        tile_length = (size / num_y - gap / 2)  # Tile size on Y minus the gap between structures

        #  Fallback variables
        num_lines_y = 0
        lines_y_excess = 0
        num_lines_x = 0
        lines_x_excess = 0

        g.write(v.title)
        g.write(v.comment_all_values_of_variable_parameters)
        g.write(v.comment_all_values_of_constant_parameters)

        self.wipe(v, length_multiplier=1 if self.machine.temperaturecontrollers.extruder.nozzle.size_id < 0.59 else 0.85)

        if v.raft:
            self.print_raft(v)  # print the raft to support the test structure

        g.write("; --- start to print the support structure ---")
        g.feed(self.machine.settings.speed_printing)
        for layer in range(v.number_of_layers + 14):
            # LAYER SCOPE
            # Return to init X, Y advance on Z
            if layer == 0:
                # Step into position to start the first column of test tiles
                g.travel(x=-gap, y=-2 * v.track_width[0])
            else:
                g.travel(x=(width + gap)*(num_x-1), y=size-gap/2, z=v.track_height[0])
            for x in range(num_x):
                # COLUMN SCOPE
                # Return to init Y, advance on -X
                if x != 0:
                    g.travel(x=-(width + gap), y=size-gap/2)
                track_width = v.track_width[x]

                # calculate length of horizontal and vertical lines
                num_lines_y = int(tile_length / track_width)
                lines_y_excess = tile_length % track_width
                num_lines_x = int(width / track_width)
                lines_x_excess = width % track_width

                spacing = v.support_pattern_spacing[x]
                advance = spacing + track_width
                for y in range(num_y):
                    # TILE SCOPE
                    # Check whether to print support or breakaway structure
                    if layer < v.number_of_layers:
                        # Advance on -Y
                        line_count = int(tile_length / advance)
                        # Calculate how much excess length is left over after spacing out lines
                        excess_length = tile_length - line_count * advance
                        for line in range(line_count):
                            # direction(line) will alter direction by returning -1 or 1 multiplier.
                            g.move(width * direction(line), extrude=True)
                            g.move(y=-advance, extrude=True)

                        # move to end of tile
                        g.move(y=-excess_length, extrude=True)
                        # Extrude anyways, to complete tile
                        g.move(width * direction(line_count), extrude=True)

                        if direction(line_count) < 0:  # Are we on the right side of the tile?
                            # move back to left and keep all tiles aligned
                            g.move(-(width * direction(line_count)), extrude=False)

                        # Calculate how large the gap should be between the substructures
                        if y < num_y-1:  # Making sure that no gap is made after the last tile
                            g.travel(y=-(gap/2))

                    else:  # Print breakaway structure
                        # No idea, at what height previous structure was printed
                        g.abs_move(z=v.support_contact_distance[y] + (layer + 2) * v.track_height[0])
                        # Meander direction
                        g.extrude = True
                        if direction(layer) > 0:
                            # Meander on X direction
                            for line in range(num_lines_x):
                                g.move(y=tile_length*direction(line))
                                g.move(x=-track_width)
                            # move to the corner of tile
                            g.move(x=-(width - num_lines_x * track_width))
                            # we should have enough space for one more pass
                            line += 1
                            g.move(y=tile_length*direction(line))

                            g.travel(y=-tile_length *(line % 2) - (gap / 2.0 if y < num_y - 1 else 0), x=width)

                        else:
                            # Meander on Y direction
                            for line in range(num_lines_y):
                                g.move(x=width*direction(line))
                                g.move(y=-track_width)

                            # move to the end of tile
                            g.move(y=-(tile_length - num_lines_y * track_width))
                            # we should have enough space for one more pass
                            line += 1
                            g.move(x=width*direction(line))

                            # pass to right side of tiles, if we are on the left
                            g.travel(x=width if direction(line) < 0 else 0,
                                    y=-(gap / 2 if y < num_y - 1 else 0))

        g.write("; --- finish to print the test structure ---")
        self.write_footer(v)
        g.teardown()

    @staticmethod
    def write_footer(values: get_values_A):
        values.g.write(";--- start footer ---\n; end of the test routine")
        values.g.write("G91\nG0 Z5.0; Lift the nozzle to avoid hitting printed structure")
        if values.chamber_heatable:
            values.g.set_chamber_temperature(0, values.chamber, immediate=False)
        if values.printbed_heatable:
            values.g.set_printbed_temperature(0, values.printbed, immediate=True)
        values.g.set_extruder_temperature(0, values.extruder, immediate=True)
        if values.part_cooling:
            values.g.set_part_cooling(0, values.extruder)
        values.g.write(";--- end footer ---")
