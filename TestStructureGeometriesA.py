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
        gv.g.home()
        gv.g.write("G21; unit in mm")
        gv.g.write("G92 E0; reset extruder")
        gv.g.write("M83; set extruder to relative mode")
        gv.g.feed(self.machine.settings.speed_travel) # respect the units: mm/min
        gv.g.abs_move(x=-wipe_length + gv.offset_x,
                      y=-6 * gv.test_structure_size / 10 + gv.offset_y,
                      z=+2 * np.mean(gv.coef_h_raft) * gv.extruder.nozzle.size_id,
                      extrude=False, extrusion_multiplier=0)

        if self.machine.temperaturecontrollers.chamber.chamber_heatable:
            gv.g.set_chamber_temperature(gv.temperature_chamber_setpoint, gv.chamber)

        if self.machine.temperaturecontrollers.printbed.printbed_heatable:
            gv.g.set_printbed_temperature(gv.temperature_printbed_setpoint, gv.printbed, immediate=True)
            gv.g.set_printbed_temperature(gv.temperature_printbed_setpoint, gv.printbed)

        gv.g.write("; --- start to clean the nozzle ---")

        gv.g.set_extruder_temperature(self.machine.settings.temperature_extruder_raft, gv.extruder, immediate=True)
        gv.g.set_extruder_temperature(self.machine.settings.temperature_extruder_raft, gv.extruder)
        gv.g.dwell(5000)
        if self.machine.temperaturecontrollers.extruder.nozzle.size_id <= 0.4:
            output = "G1 F1000 E2.5; extrude 2.5 mm of material"
        else:
            output = "G1 F1000 E5.0; extrude 5.0 mm of material"

        gv.g.write(output)
        gv.g.dwell(5000)
        gv.g.feed(self.machine.settings.speed_printing_raft)  # print the raft

        if isinstance(gv, get_values_A):
            gv.g.move(x=+2 * wipe_length,
                      y=0,
                      z=-2 * np.mean(gv.coef_h_raft) * self.machine.temperaturecontrollers.extruder.nozzle.size_id,
                      extrude=True, extrusion_multiplier=2.25, coef_h=np.mean(gv.coef_h_raft), coef_w=np.mean(gv.coef_w_raft))
            gv.g.move(x=0,
                      y=+gv.test_structure_size / 10,
                      z=+np.mean(gv.coef_h_raft) * self.machine.temperaturecontrollers.extruder.nozzle.size_id,
                      extrude=False, extrusion_multiplier=0)
            gv.g.move(x=-wipe_length_initial / 6 + (1 - length_multiplier) * wipe_length_initial,
                      y=0,
                      z=0,
                      extrude=False, extrusion_multiplier=0)

        gv.g.write("; --- end to clean the nozzle ---")

        return


    # RAFT PERIMETER
    # prints the outer perimeter of the raft
    def raft_perimeter(self, values: get_values_A):
        values.g.set_extruder_temperature(self.machine.settings.temperature_extruder_raft, self.machine.temperaturecontrollers.extruder, immediate=True)
        values.g.set_extruder_temperature(self.machine.settings.temperature_extruder_raft, self.machine.temperaturecontrollers.extruder)
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
        step = np.mean(values.coef_w_raft) * self.machine.temperaturecontrollers.extruder.nozzle.size_id / raft_density  # step size
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
                              extrude=True, extrusion_multiplier=values.extrusion_multiplier_raft, coef_h=np.mean(values.coef_h_raft), coef_w=np.mean(values.coef_w_raft))

        values.g.write("; --- finish to print the raft ---")

        if not values.raft:
            values.g.move(x=0,
                          y=20,
                          z=0,
                          extrude=False, extrusion_multiplier=0)

        if values.test_number not in ["01", "02", "03"]:
            values.g.set_extruder_temperature(self.machine.settings.temperature_extruder, values.extruder, immediate=True)
            values.g.set_extruder_temperature(self.machine.settings.temperature_extruder, values.extruder)
            values.g.dwell(15000)  # to unload the nozzle

        if values.part_cooling:
            values.g.set_part_cooling(values.part_cooling_setpoint, values.extruder)

        return


    # GENERIC TEST ROUTINE: SINGLE TESTING PARAMETER vs. PRINTING SPEED
    def flat_test_parameter_one_vs_parameter_two(self, values: get_values_A):
        values.g.write(values.title)
        values.g.write(values.comment_all_values_of_variable_parameters)
        self.wipe(values, length_multiplier=1 if self.machine.temperaturecontrollers.extruder.nozzle.size_id < 0.59 else 0.85)

        self.print_raft(values) if values.raft else self.raft_perimeter(values) # print the raft to support the test structure

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

                values.g.abs_move(z=+values.abs_z[current_test_structure])

                values.g.set_extruder_temperature(values.temperature_extruder[current_test_structure], values.extruder)
                values.g.dwell(30000)
                output = "G1 F500 E" + "{:.3f}".format(4 * values.temperature_extruder[current_test_structure] / values.temperature_extruder[0]) + \
                         "; extrude " + "{:.3f}".format(4 * values.temperature_extruder[current_test_structure] / values.temperature_extruder[0]) + " mm of material"
                values.g.write(output)
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

                for current_layer in range(values.number_of_layers): # layers
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

        self.print_raft(values) if values.raft else self.raft_perimeter(values) # print the raft to support the test structure

        values.g.write("; --- start to print the test structure ---")

        for current_test_structure in range(values.number_of_test_structures):
            values.g.write(values.comment_all_values_of_constant_parameters)
            values.g.write(values.comment_current_values_of_variable_parameter[current_test_structure])

            current_printing_speed = values.speed_printing[current_test_structure]
            values.g.feed(current_printing_speed)

            values.g.travel(x=-values.test_structure_width[current_test_structure] - values.test_structure_separation,
                            y=0 if (current_test_structure == 0 and values.raft) else +values.step_y,
                            lift=1,
                            retraction_speed=np.mean(values.retraction_speed))

            values.g.abs_move(z=+values.abs_z[current_test_structure])
            step_x = values.step_x[current_test_structure]

            for current_substructure in range(values.number_of_substructures):
                values.g.write("; --- testing the following printing speed value: {:.1f} mm/s".format(current_printing_speed))

                coasting_distance = np.linspace(0, values.coasting_distance, values.number_of_lines)

                for current_line in range(values.number_of_lines):
                    values.g.move(x=0,
                                  y=-(values.step_y / (2 * values.number_of_substructures) - coasting_distance[current_line]),
                                  z=0,
                                  extrude=True, extrusion_multiplier=values.extrusion_multiplier[current_test_structure], coef_h=values.coef_h[current_test_structure], coef_w=values.coef_w[current_test_structure])
                    values.g.move(x=0,
                                  y=-coasting_distance[current_line],
                                  z=0,
                                  extrude=False, extrusion_multiplier=0)

                    values.g.retract(values.retraction_speed, values.retraction_distance[current_substructure])

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

                    values.g.retract(values.retraction_speed, values.retraction_distance[current_test_structure], values.retraction_restart_distance[current_test_structure])

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
        self.wipe(values, length_multiplier=1 if self.machine.temperaturecontrollers.extruder.nozzle.size_id < 0.59 else 0.85) # perform wipe of the nozzle
        self.print_raft(values) # print the raft to support the test structure
        values.g.write("; --- start to print the test structure ---")
        values.g.travel(x=-values.test_structure_width[0] - values.test_structure_separation,
                        y=0,
                        lift=1,
                        retraction_speed=np.mean(values.retraction_speed))

        values.g.abs_move(z=+values.abs_z[0])

        for current_test_structure in range(values.number_of_test_structures):
            output = str("; --- testing the {0} of {1} {2} ---".format(values.parameter_one.name, values.parameter_one.precision, values.parameter_one.units))
            output = str(output.format(values.parameter_one.values[current_test_structure]))
            values.g.write(output)
            values.g.write(values.comment_all_values_of_constant_parameters)

            for current_substructure in range(values.number_of_substructures): # TODO comments
                current_temperature_extruder = values.temperature_extruder[current_test_structure]

                if values.test_number in ("09", "10", "11"):
                    current_speed_printing = values.speed_printing[current_substructure]
                    current_retraction_distance = values.retraction_distance[current_test_structure]
                elif values.test_number == "08":
                    current_speed_printing = np.mean(values.speed_printing)
                    current_retraction_distance = values.retraction_distance[current_substructure]

                    if current_substructure == 0:
                        values.g.travel(x=0,
                                        y=+values.test_structure_size / 7,
                                        z=+values.abs_z[current_test_structure],
                                        retraction_speed=values.retraction_speed[0],
                                        retraction_distance=np.mean(values.retraction_distance))

                        values.g.set_extruder_temperature(values.temperature_extruder[current_test_structure], values.extruder)

                        values.g.dwell(30000)
                        output = "G1 F500 E" + "{:.3f}".format(1.5 * values.temperature_extruder[current_test_structure] / values.temperature_extruder[0]) + \
                                 "; extrude " + "{:.3f}".format(1.5 * values.temperature_extruder[current_test_structure] / values.temperature_extruder[0]) + " mm of material"
                        values.g.write(output)

                        values.g.move(x=0,
                                      y=-values.test_structure_size / 7,
                                      z=-values.abs_z[current_test_structure],
                                      extrude=True, extrusion_multiplier=0)

                    output = str("; --- testing the {0} of {1} {2} ---".format(values.parameter_two.name, values.parameter_two.precision, values.parameter_two.units))
                    output = str(output.format(values.parameter_two.values[current_substructure]))
                    values.g.write(output)

                values.g.set_extruder_temperature(current_temperature_extruder, values.extruder)

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

    @staticmethod
    def write_footer(values: get_values_A):
        values.g.write(";--- start footer ---\n; end of the test routine")
        if values.chamber_heatable:
            values.g.set_chamber_temperature(0, values.chamber, immediate=False)
        if values.printbed_heatable:
            values.g.set_printbed_temperature(0, values.printbed, immediate=True)
        values.g.set_extruder_temperature(0, values.extruder, immediate=True)
        if values.part_cooling:
            values.g.set_part_cooling(0, values.extruder)
        values.g.home()
        values.g.write("M84; disable motors")
        values.g.write(";--- end footer ---")

