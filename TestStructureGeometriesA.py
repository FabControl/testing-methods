from Definitions import *
from Globals import machine
from get_values_A import get_values_A
from GetValuesB import TestSetupB
from paths import footer

# WIPE
def wipe(ts: get_values_A or TestSetupB, length_multiplier=1):
    wipe_length_initial = 6 * ts.test_structure_size/10
    wipe_length = wipe_length_initial * length_multiplier
    ts.g.home()
    ts.g.feed(machine.settings.speed_travel) # respect the units: mm/min
    ts.g.abs_move(x=-wipe_length+ts.offset_x,
                  y=-6*ts.test_structure_size/10+ts.offset_y,
                  z=+2*ts.coef_h_raft*ts.extruder.nozzle.size_id,
                  extrude=False, extrusion_multiplier=0)

    if machine.temperaturecontrollers.chamber.chamber_heatable:
        ts.g.set_chamber_temperature(ts.temperature_chamber_setpoint, ts.chamber)

    if machine.temperaturecontrollers.printbed.printbed_heatable:
        ts.g.set_printbed_temperature(ts.temperature_printbed_setpoint, ts.printbed, immediate=True)
        ts.g.set_printbed_temperature(ts.temperature_printbed_setpoint, ts.printbed)

    ts.g.write("; --- start to clean the nozzle ---")

    ts.g.set_extruder_temperature(machine.settings.temperature_extruder_raft, ts.extruder, immediate=True)
    ts.g.set_extruder_temperature(machine.settings.temperature_extruder_raft, ts.extruder)
    ts.g.dwell(5000)
    if machine.temperaturecontrollers.extruder.nozzle.size_id <= 0.4:
        output = "G1 F1000 E2.5; extrude 2.5 mm of material"
    else:
        output = "G1 F1000 E5.0; extrude 5.0 mm of material"

    ts.g.write(output)
    ts.g.dwell(5000)
    ts.g.feed(machine.settings.speed_printing_raft)  # print the raft

    if isinstance(ts, get_values_A):
        ts.g.move(x=+2*wipe_length,
                  y=0,
                  z=-2*ts.coef_h_raft*machine.temperaturecontrollers.extruder.nozzle.size_id,
                  extrude=True, extrusion_multiplier=2.25, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)
        ts.g.move(x=0,
                  y=+ts.test_structure_size/10,
                  z=+ts.coef_h_raft * machine.temperaturecontrollers.extruder.nozzle.size_id,
                  extrude=False, extrusion_multiplier=0)
        ts.g.move(x=-wipe_length_initial/6+(1-length_multiplier)*wipe_length_initial,
                  y=0,
                  z=0,
                  extrude=False, extrusion_multiplier=0)

    ts.g.write("; --- end to clean the nozzle ---")

    return


# RAFT PERIMETER
# prints the outer perimeter of the raft
def raft_perimeter(ts: get_values_A):
    ts.g.set_extruder_temperature(machine.settings.temperature_extruder_raft, machine.temperaturecontrollers.extruder, immediate=True)
    ts.g.set_extruder_temperature(machine.settings.temperature_extruder_raft, machine.temperaturecontrollers.extruder)
    ts.g.write("; --- print the outer perimeter ---")
    ts.g.feed(machine.settings.speed_printing_raft/3)
    for dummy in range(2):
        for _ in range(100):
            ts.g.move(x=0,
                      y=(-1)**dummy*ts.test_structure_size/100,
                      z=0,
                      extrude=True, extrusion_multiplier=1.5, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)
        for _ in range(100):
            ts.g.move(x=(-1)**(dummy+1)*ts.test_structure_size/100,
                      y=0,
                      z=0,
                      extrude=True, extrusion_multiplier=1.5, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)

    return


# PRINTING RAFT
# prints the filling of the raft
def print_raft(gv: get_values_A):
    gv.g.write("; --- start to print the raft ---")
    raft_perimeter(gv)
    gv.g.write("; --- print the infill with the density of {0} % ---".format(machine.settings.raft_density))
    gv.g.feed(gv.speed_printing_raft)
    raft_density = machine.settings.raft_density/100
    step = gv.coef_w_raft * machine.temperaturecontrollers.extruder.nozzle.size_id / raft_density  # step size
    step_number = gv.test_structure_size / step

    gv.g.move(x=-gv.coef_w_raft * machine.temperaturecontrollers.extruder.nozzle.size_id / 2,
              y=0,
              z=0,
              extrude=False, extrusion_multiplier=0)

    for dummy in range(0, int(step_number)):
        gv.g.move(x=0,
                  y=+step,
                  z=0,
                  extrude=False, extrusion_multiplier=0)
        for _ in range(100):
            gv.g.move(x=(-1) ** (dummy + 1) * (gv.test_structure_size - gv.coef_w_raft * machine.temperaturecontrollers.extruder.nozzle.size_id)/100,
                      y=0,
                      z=0,
                      extrude=True, extrusion_multiplier=gv.extrusion_multiplier_raft, coef_h=gv.coef_h_raft, coef_w=gv.coef_w_raft)

    gv.g.write("; --- finish to print the raft ---")

    if not gv.raft:
        gv.g.move(x=0,
                  y=20,
                  z=0,
                  extrude=False, extrusion_multiplier=0)

    gv.g.set_extruder_temperature(machine.settings.temperature_extruder, gv.extruder, immediate=True)
    gv.g.set_extruder_temperature(machine.settings.temperature_extruder, gv.extruder)
    gv.g.dwell(20000)  # to unload the nozzle

    if gv.part_cooling:
        gv.g.set_part_cooling(gv.part_cooling_setpoint, gv.extruder)
    if gv.ventilator_entry:
        gv.g.set_ventilator_entry(gv.ventilator_entry_setpoint, gv.chamber)
    if gv.ventilator_exit:
        gv.g.set_ventilator_exit(gv.ventilator_exit_setpoint, gv.chamber)

    return


# def print_raft_new(values: get_values_A):
#     values.g.home()
#     values.g.feed(2 * machine.settings.speed_printing)  # respect the units: mm/min
#
#     if hasattr(values, "temperature_printbed"):
#         values.g.set_printbed_temperature(values.temperature_printbed)
#
#     values.g.abs_move(x=0,
#                   y=0,
#                   z=values.coef_h_raft * machine.nozzle.size_id,
#                   extrude=False, extrusion_multiplier=0)
#     values.g.write("; --- start to clean the nozzle ---")
#     values.g.set_extruder_temperature(values.temperature_extruder_raft)
#     values.g.dwell(5000)
#     values.g.write("G1 F1000 E5; extrude 5 mm of material")
#     values.g.dwell(5000)
#     values.g.feed(machine.settings.speed_printing_raft)  # print the raft
#     sf.infill(sf.raft_structure(values.test_structure_size/2, structure="square"), outlines=2, g=values.g, coef_w_raft=values.coef_w_raft, coef_h_raft=values.coef_h_raft)
#     values.g.write("; --- finish to print the raft ---")
#
#     return


# GENERIC TEST ROUTINE: SINGLE TESTING PARAMETER vs. PRINTING SPEED
def flat_test_parameter_one_vs_parameter_two(ts: get_values_A):
    ts.g.write(ts.title)
    ts.g.write(ts.comment_all_values_of_variable_parameters)
    wipe(ts, length_multiplier=1 if machine.temperaturecontrollers.extruder.nozzle.size_id < 0.59 else 0.85)

    print_raft(ts) if ts.raft else raft_perimeter(ts) # print the raft to support the test structure

    ts.g.write("; --- start to print the test structure ---")
    ts.g.feed(machine.settings.speed_printing)

    for current_test_structure in range(ts.number_of_test_structures):
        ts.g.write(ts.comment_all_values_of_constant_parameters)
        ts.g.write(ts.comment_current_values_of_variable_parameter[current_test_structure])

        if ts.test_name == "extrusion temperature vs printing speed":
            ts.g.travel(x=-ts.test_structure_width[current_test_structure]-ts.test_structure_separation,
                        y=+ts.step_y if current_test_structure !=0 else 0,
                        lift=1)
            ts.g.travel(x=0,
                        y=+ts.test_structure_size/7,
                        retraction_speed=ts.retraction_speed, retraction_distance=ts.retraction_distance[current_test_structure])

            ts.g.abs_move(z=+ts.abs_z[current_test_structure])

            ts.g.set_extruder_temperature(ts.temperature_extruder[current_test_structure], ts.extruder)
            ts.g.dwell(30000)
            output = "G1 F500 E" + "{:.3f}".format(4 * ts.temperature_extruder[current_test_structure] / ts.temperature_extruder[0]) + \
                     "; extrude " + "{:.3f}".format(4 * ts.temperature_extruder[current_test_structure] / ts.temperature_extruder[0]) + " mm of material" #TODO tool
            ts.g.write(output)
            ts.g.move(x=0,
                      y=-ts.test_structure_size/7,
                      extrude=True, extrusion_multiplier=0)

        else:
            ts.g.travel(x=-ts.test_structure_width[current_test_structure]-ts.test_structure_separation,
                        y=0 if (current_test_structure == 0 and ts.raft) else +ts.step_y,
                        lift=1)

            ts.g.abs_move(z=+ts.abs_z[current_test_structure])

        for current_substructure in range(ts.number_of_substructures):
            if ts.test_info.parameter_two.values == []:
                current_printing_speed = ts.speed_printing[current_test_structure]
            else:
                current_printing_speed = ts.parameter_two.values[current_substructure]

            ts.g.write("; --- testing the following printing speed value: {:.3f} mm/s".format(current_printing_speed))
            ts.g.feed(current_printing_speed)

            ts.g.abs_move(z=ts.abs_z[current_test_structure],
                          extrude=False, extrusion_multiplier=0)

            for current_layer in range(ts.number_of_layers): # layers
                for current_line in range(ts.number_of_lines):
                    ts.g.move(x=0,
                              y=(-1) ** (current_line+1) * ts.step_y / ts.number_of_substructures,
                              z=0,
                              extrude=True, extrusion_multiplier=ts.extrusion_multiplier[current_test_structure],
                              coef_h=ts.coef_h[current_test_structure], coef_w=ts.coef_w[current_test_structure])
                    ts.g.move(x=(-1) ** (current_layer+1) * ts.step_x[current_test_structure],
                              y=0,
                              z=0,
                              extrude=False, extrusion_multiplier=0)

                    if current_line == ts.number_of_lines - 1:
                        ts.g.move(x=0,
                                  y=(-1) ** (current_line+2) * ts.step_y / ts.number_of_substructures,
                                  z=0,
                                  extrude=True, extrusion_multiplier=ts.extrusion_multiplier[current_test_structure],
                                  coef_h=ts.coef_h[current_test_structure], coef_w=ts.coef_w[current_test_structure])

                if current_layer == ts.number_of_layers - 1:
                    if ts.number_of_layers == 1:
                        ts.g.travel(x=+ts.test_structure_width[current_test_structure+1],
                                    y=0,
                                    lift=1)
                    else:
                        ts.g.travel(x=0,
                                    y=0,
                                    lift=1)
                else:
                    ts.g.abs_move(z=ts.abs_z[current_test_structure] + (current_layer+1) * ts.track_height[current_test_structure],
                                  extrude=False, extrusion_multiplier=0)
                    ts.g.move(x=0,
                              y=(-1) ** (current_line + 1) * ts.step_y / ts.number_of_substructures,
                              z=0,
                              extrude=False, extrusion_multiplier=0)

    ts.g.write("; --- finish to print the test structure ---")
    generate_footer(ts)
    ts.g.teardown()

    return


# RETRACTION RESTART DISTANCE and COASTING DISTANCE
def retraction_restart_distance_vs_coasting_distance(ts: get_values_A):
    ts.g.write(ts.title)
    ts.g.write(ts.comment_all_values_of_variable_parameters)
    wipe(ts, length_multiplier=1 if machine.nozzle.size_id < 0.59 else 0.85) # perform wipe of the nozzle
    print_raft(ts) # print the raft to support the test structure
    ts.g.write("; --- start to print the test structure ---")
    ts.g.feed(machine.settings.speed_printing)

    test_structure_separation = (ts.test_structure_size - sum(map(lambda x, y: x * y, [ts.number_of_lines]*ts.number_of_test_structures, ts.step_x)))/(ts.number_of_test_structures+1)
    test_structure_width = [0.]
    test_structure_width.extend([ts.number_of_lines * k for k in ts.step_x])

    for current_test_structure in range(ts.number_of_test_structures):
        ts.g.write(ts.comment_all_values_of_constant_parameters)
        ts.g.feed(ts.speed_printing[current_test_structure])

        ts.g.abs_travel(x=+ts.test_structure_size/2 - (sum_of_list_elements(test_structure_width, current_test_structure) + (current_test_structure + 1) * test_structure_separation),
                        y=+ts.test_structure_size/2,
                        z=+ts.abs_z[current_test_structure],
                        lift=1)

        step_x = ts.step_x[current_test_structure]

        for current_substructure in range(ts.number_of_substructures):
            if ts.parameter_two_min_max is not None:
                current_printing_speed = ts.parameter_two_min_max[(current_substructure if ts.number_of_substructures > 1 else current_test_structure)]
            else:
                current_printing_speed = ts.speed_printing[current_test_structure]

            ts.g.write("; --- testing the following printing speed value: {:.1f} mm/s".format(current_printing_speed))
            ts.g.feed(current_printing_speed)
            coasting_distance = np.linspace(0, ts.coasting_distance, ts.number_of_lines)

            for current_line in range(ts.number_of_lines):
                ts.g.move(x=0,
                          y=-(ts.step_y/(2*ts.number_of_substructures) - coasting_distance[current_line]),
                          z=0,
                          extrude=True, extrusion_multiplier=ts.extrusion_multiplier[current_test_structure], coef_h=ts.coef_h[current_test_structure], coef_w=ts.coef_w[current_test_structure])
                ts.g.move(x=0,
                          y=-coasting_distance[current_line],
                          z=0,
                          extrude=False, extrusion_multiplier=0)

                ts.g.retract(ts.retraction_speed, ts.retraction_distance[current_substructure])

                ts.g.move(x=0,
                          y=-ts.step_y/(2*ts.number_of_substructures),
                          z=0,
                          extrude=False, extrusion_multiplier=0)
                ts.g.move(x=-step_x,
                          y=0,
                          z=0,
                          extrude=False, extrusion_multiplier=0)

                if current_line != ts.number_of_lines - 1:
                    ts.g.move(x=0,
                              y=+ts.step_y/ts.number_of_substructures,
                              z=0,
                              extrude=False, extrusion_multiplier=0)
                else:
                    ts.g.move(x=step_x * ts.number_of_lines,
                              y=0,
                              z=0,
                              extrude=False, extrusion_multiplier=0)

                ts.g.retract(ts.retraction_speed, ts.retraction_distance[current_test_structure], ts.retraction_restart_distance[current_test_structure])

    ts.g.write("; --- finish to print the test structure ---")
    ts.g.teardown()

    return


# BRIDGING EXTRUSION MULTIPLIER vs. BRIDGING PRINTING SPEED
def bridging_test(ts: get_values_A):
    ts.g.write(ts.title)
    ts.g.write(ts.comment_all_values_of_variable_parameters)
    ts.g.write(ts.comment_all_values_of_constant_parameters)

    wipe(ts, length_multiplier=1 if machine.temperaturecontrollers.extruder.nozzle.size_id < 0.59 else 0.85)

    if ts.raft:
        print_raft(ts)  # print the raft to support the test structure

    ts.g.write("; --- start to print the support structure ---")

    ts.g.feed(machine.settings.speed_printing)

    angle = 45
    perimeter = 4

    step_x = ts.test_structure_size/((ts.number_of_test_structures + 1)/2)/2
    step_y = (ts.test_structure_size - (ts.number_of_substructures + 1)*perimeter*np.mean(ts.track_width)/np.sin(np.deg2rad(angle)))//ts.number_of_substructures

    ts.g.travel(x=0,
                y=-step_y-perimeter*np.mean(ts.track_width)/np.sin(np.deg2rad(angle)), lift=1)

    # Building support structures
    for current_layer in range(ts.number_of_layers):
        ts.g.abs_move(z=+np.mean(ts.abs_z) + current_layer * np.mean(ts.track_height))

        for current_substructure in range(ts.number_of_substructures):
            for current_perimeter_line in range(perimeter):
                for current_l_structure in range(int((ts.number_of_test_structures + 1)/2)):
                    ts.g.move(x=(-1)**(current_perimeter_line + 1)*step_x,
                              y=+step_y,
                              z=0,
                              extrude=True, extrusion_multiplier=np.mean(ts.extrusion_multiplier))
                    ts.g.move(x=(-1)**(current_perimeter_line + 1)*step_x,
                              y=-step_y,
                              z=0,
                              extrude=True, extrusion_multiplier=np.mean(ts.extrusion_multiplier))

                if current_perimeter_line != range(perimeter)[-1]:
                    ts.g.move(x=0,
                              y=+np.mean(ts.track_width)/np.sin(np.deg2rad(angle)),
                              z=0,
                              extrude=False, extrusion_multiplier=0)

            if current_substructure != ts.number_of_substructures-1:
                ts.g.travel(x=0,
                            y=-step_y-2*perimeter*np.mean(ts.track_width)/np.sin(np.deg2rad(angle)),
                            z=0,
                            lift=1,
                            retraction_speed=ts.retraction_speed,
                            retraction_distance=np.mean(ts.retraction_distance))

        ts.g.travel(x=0,
                    y=+(ts.number_of_substructures-1)*step_y + (ts.number_of_substructures-1)*perimeter*np.mean(ts.track_width)/np.sin(np.deg2rad(angle)),
                    z=0,
                    lift=1,
                    retraction_speed=ts.retraction_speed,
                    retraction_distance=np.mean(ts.retraction_distance))

    ts.g.write("; --- finish to print the support structure ---")
    ts.g.move(z=+np.mean(ts.track_height))
    ts.g.write("; --- start to print the bridges ---")

    # Printing bridges
    for index_current_speed, current_speed_value in enumerate(ts.parameter_two.values):
        ts.g.write("; --- testing the following bridging speed value: {:.1f} mm/s ---".format(current_speed_value))
        ts.g.feed(current_speed_value)

        for index_current_extrusion_multiplier, current_extrusion_multiplier_value in enumerate(ts.extrusion_multiplier_bridging):
            ts.g.write(ts.comment_all_values_of_constant_parameters)
            ts.g.write(ts.comment_current_values_of_variable_parameter[index_current_extrusion_multiplier])

            for step in range(int(step_y/np.mean(ts.track_width))):
                ts.g.move(x=(-1)**(step + 1)*2*(step_y - step*np.mean(ts.track_width))*step_x/step_y,
                          y=0,
                          z=0,
                          extrude=True, extrusion_multiplier=current_extrusion_multiplier_value)
                if step != range(int(step_y/np.mean(ts.track_width)))[-1]:
                    ts.g.move(x=0,
                              y=(-1)**index_current_extrusion_multiplier*np.mean(ts.track_width),
                              z=0,
                              extrude=False, extrusion_multiplier=0)
                    ts.g.move(x=(-1)**step*np.mean(ts.track_width)*step_x/step_y,
                              y=0,
                              z=0,
                              extrude=False, extrusion_multiplier=0)
                else:
                    ts.g.move(x=(-1)**step*(step_y - step*np.mean(ts.track_width))*step_x/step_y,
                              y=0,
                              z=0,
                              extrude=False, extrusion_multiplier=0)
        ts.g.travel(x=+ts.number_of_test_structures*step_x,
                    y=-2*step_y-perimeter*np.mean(ts.track_width)/np.sin(np.deg2rad(angle)),
                    z=0,
                    lift=1,
                    retraction_speed=ts.retraction_speed,
                    retraction_distance=np.mean(ts.retraction_distance))

    ts.g.write("; --- finish to print the test structure ---")
    generate_footer(ts)
    ts.g.teardown()

    return


# FIXED RETRACTION DISTANCE vs VARIABLE PRINTING SPEED
# FIXED RETRACTION DISTANCE vs VARIABLE RETRACTION SPEED
# VARIABLE RETRACTION DISTANCE at FIXED PRINTING SPEED and FIXED RETRACTION SPEED
# VARIABLE EXTRUSION TEMPERATURE vs VARIABLE RETRACTION DISTANCE

def retraction_distance(ts: get_values_A):
    ts.g.write(ts.title)
    ts.g.write(ts.comment_all_values_of_variable_parameters)
    wipe(ts, length_multiplier=1 if machine.temperaturecontrollers.extruder.nozzle.size_id < 0.59 else 0.85) # perform wipe of the nozzle
    print_raft(ts) # print the raft to support the test structure
    ts.g.write("; --- start to print the test structure ---")
    ts.g.travel(x=-ts.test_structure_width[0] - ts.test_structure_separation,
                y=0,  # +values.step_y-values.test_structure_size/values.number_of_substructures if current_test_structure != 0 else
                lift=1)

    ts.g.abs_move(z=+ts.abs_z[0])

    for current_test_structure in range(ts.number_of_test_structures):
        output = str("; --- testing the {0} of {1} {2} ---".format(ts.parameter_one.name, ts.parameter_one.precision, ts.parameter_one.units))
        output = str(output.format(ts.parameter_one.values[current_test_structure]))
        ts.g.write(output)

        if ts.test_name == "extrusion temperature vs retraction distance":
            ts.g.feed(np.mean(ts.speed_printing))

        ts.g.write(ts.comment_all_values_of_constant_parameters)

        for current_substructure in range(ts.number_of_substructures):
            current_temperature_extruder = ts.temperature_extruder[current_test_structure]

            if ts.test_name == "retraction distance":
                current_retraction_distance = ts.retraction_distance[current_test_structure]

            if ts.test_name == "extrusion temperature vs retraction distance":
                if current_substructure == 0:
                    ts.g.travel(x=0,
                                y=+ts.test_structure_size/7,
                                z=+ts.abs_z[current_test_structure],
                                retraction_speed=ts.retraction_speed[0],
                                retraction_distance=np.mean(ts.retraction_distance))

                    ts.g.set_extruder_temperature(ts.temperature_extruder[current_test_structure], ts.extruder)

                    ts.g.dwell(30000)
                    output = "G1 F500 E" + "{:.3f}".format(1.5*ts.temperature_extruder[current_test_structure]/ts.temperature_extruder[0]) + \
                             "; extrude " + "{:.3f}".format(1.5*ts.temperature_extruder[current_test_structure]/ts.temperature_extruder[0]) + " mm of material"
                    ts.g.write(output)

                    ts.g.move(x=0,
                              y=-ts.test_structure_size/7,
                              z=-ts.abs_z[current_test_structure],
                              extrude=True, extrusion_multiplier=0)

                current_retraction_distance = ts.retraction_distance[current_substructure]
                output = str("; --- testing the {0} of {1} {2} ---".format(ts.parameter_two.name, ts.parameter_two.precision, ts.parameter_two.units))
                output = str(output.format(ts.parameter_two.values[current_substructure]))
                ts.g.write(output)

            ts.g.set_extruder_temperature(current_temperature_extruder, ts.extruder)

            for current_layer in range(0, ts.number_of_layers):  # layers
                for current_line in range(ts.number_of_lines):
                    if hasattr(ts, "parameter_three"):
                        current_retraction_speed = ts.retraction_speed[current_line]
                    else:
                        current_retraction_speed = np.linspace(ts.retraction_speed,ts.retraction_speed,ts.number_of_lines).tolist()[current_line]

                    step_x = ts.step_x[current_test_structure]
                    print("step in x = {:.3f}".format(step_x))

                    ts.g.move(x=-step_x,
                              y=0,
                              z=0,
                              extrude=False, extrusion_multiplier=0)

                    ts.g.feed(ts.speed_printing[current_test_structure])
                    ts.g.move(x=0,
                              y=((-1)**(current_line+1))*ts.step_y/(3*ts.number_of_substructures),
                              z=0,
                              extrude=True, extrusion_multiplier=ts.extrusion_multiplier[current_test_structure],
                              coef_h=ts.coef_h[current_test_structure], coef_w=ts.coef_w[current_test_structure])

                    ts.g.retract(current_retraction_speed, current_retraction_distance, ts.speed_printing[current_test_structure])

                    ts.g.move(x=0,
                              y=((-1)**(current_line+1))*ts.step_y/(3*ts.number_of_substructures),
                              z=0,
                              extrude=False, extrusion_multiplier=0)

                    ts.g.deretract(current_retraction_speed, current_retraction_distance, ts.speed_printing[current_test_structure])

                    ts.g.move(x=0,
                              y=((-1)**(current_line+1))*ts.step_y/(3*ts.number_of_substructures),
                              z=0,
                              extrude=True, extrusion_multiplier=ts.extrusion_multiplier[current_test_structure], coef_h=ts.coef_h[current_test_structure], coef_w=ts.coef_w[current_test_structure])

                if current_layer == ts.number_of_layers - 1:
                    if current_substructure == ts.number_of_substructures - 1:
                        ts.g.travel(x=-ts.test_structure_separation,
                                    y=+(ts.number_of_substructures - 1)*ts.step_y/ts.number_of_substructures,
                                    lift=1)
                        ts.g.abs_move(z=+ts.abs_z[current_test_structure],
                                      extrude=False, extrusion_multiplier=0)
                    else:
                        ts.g.travel(x=+step_x*ts.number_of_lines,
                                    y=-ts.step_y/ts.number_of_substructures,
                                    lift=1)
                        ts.g.abs_move(z=+ts.abs_z[current_test_structure],
                                      extrude=False, extrusion_multiplier=0)
                else:
                    ts.g.travel(x=+step_x*ts.number_of_lines,
                                lift=1)
                    ts.g.move(z=+ts.track_height[current_test_structure],
                              extrude=False, extrusion_multiplier=0)

    ts.g.write("; --- finish to print the test structure ---")
    generate_footer(ts)
    ts.g.teardown()

    return

def generate_footer(values: get_values_A): # TODO Rewrite!
    custom_footer = ";--- start footer ---\n; end of the test routine\n"

    if values.chamber_heatable:
        custom_footer = custom_footer + values.chamber.gcode_command.format(values.chamber.temperature_min, values.chamber.tool) + "; set the chamber temperature\n"

    if values.printbed_heatable:
        custom_footer = custom_footer + values.printbed.gcode_command.format(values.printbed.temperature_min, values.printbed.tool) + "; set the print bed temperature\n"

    custom_footer = custom_footer + values.extruder.gcode_command.format(0, values.extruder.tool) + "; set the extruder temperature\n"

    if values.part_cooling:
        custom_footer = custom_footer + values.part_cooling_gcode_command.format(0) + "; set the part cooling\n"

    custom_footer = custom_footer + "G28; move to the home position\nM84; disable motors\n;--- end footer ---"

    with open(footer, "w") as f:
        f.write(custom_footer)

    return custom_footer

