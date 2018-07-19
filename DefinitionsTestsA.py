from Definitions import *
from Globals import machine
import slicing_functionality as sf
from TestSetupA import TestSetupA
from TestSetupB import TestSetupB


# WIPE
def wipe(ts: TestSetupA or TestSetupB, full = True):
    ts.g.home()
    ts.g.feed(machine.settings.speed_travel)  # respect the units: mm/min
    ts.g.abs_move(x=-6 * ts.test_structure_size/10,
                  y=-6 * ts.test_structure_size/10,
                  z=+2 * ts.coef_h_raft * machine.nozzle.size_id,
                  extrude=False, extrusion_multiplier=0)

    if hasattr(ts, "temperature_printbed"):
        ts.g.set_printbed_temperature(ts.temperature_printbed)

    ts.g.write("; --- start to clean the nozzle ---")
    ts.g.set_extruder_temperature(machine.settings.temperature_extruder_raft)
    ts.g.dwell(5)
    if machine.nozzle.size_id <= 0.4:
        output = "G1 F1000 E2.5; extrude 2.5 mm of material"
    else:
        output = "G1 F1000 E5.0; extrude 5 mm of material"

    ts.g.write(output)
    ts.g.dwell(5)
    ts.g.feed(machine.settings.speed_printing_raft)  # print the raft

    if isinstance(ts, TestSetupA):
        ts.g.abs_move(x=+6 * ts.test_structure_size/10,
                      y=-6 * ts.test_structure_size/10,
                      z=0,
                      extrude=True, extrusion_multiplier=2.25, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)
        ts.g.move(x=0,
                  y=+ts.test_structure_size/10,
                  z=+ts.coef_h_raft * machine.nozzle.size_id,
                  extrude=False, extrusion_multiplier=0)
        ts.g.move(x=-ts.test_structure_size/10,
                  y=0,
                  z=0,
                  extrude=False, extrusion_multiplier=0)
    elif isinstance(ts, TestSetupB):
        ts.g.abs_move(x=+6 * ts.test_structure_size/10,
                      y=-6 * ts.test_structure_size/10,
                      z=0,
                      extrude=True, extrusion_multiplier=2.25, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)
        ts.g.move(x=0,
                  y=-ts.test_structure_size/10,
                  z=+ts.coef_h_raft * machine.nozzle.size_id,
                  extrude=False, extrusion_multiplier=0)
        ts.g.move(x=-ts.test_structure_size/10,
                  y=0,
                  z=0,
                  extrude=False, extrusion_multiplier=0)
    ts.g.write("; --- end to clean the nozzle ---")

    return


# RAFT PERIMETER
def raft_perimeter(ts: TestSetupA):
    ts.g.set_extruder_temperature(machine.settings.temperature_extruder_raft)
    ts.g.write("; --- print the outer perimeter ---")
    ts.g.feed(machine.settings.speed_printing_raft / 3)  # print the outer perimeter of the raft
    ts.g.move(x=0,
              y=+ts.test_structure_size,
              z=0,
              extrude=True, extrusion_multiplier=1.5, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)
    ts.g.move(x=-ts.test_structure_size,
              y=0,
              z=0,
              extrude=True, extrusion_multiplier=1.5, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)
    ts.g.move(x=0,
              y=-ts.test_structure_size,
              z=0,
              extrude=True, extrusion_multiplier=1.5, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)
    ts.g.move(x=+ts.test_structure_size,
              y=0,
              z=0,
              extrude=True, extrusion_multiplier=1.5, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)

    return


# PRINTING RAFT
def print_raft(ts: TestSetupA):
    ts.g.write("; --- start to print the raft ---")
    ts.g.set_extruder_temperature(ts.temperature_extruder_raft)
    raft_perimeter(ts)
    ts.g.write("; --- print the infill with the fill density of {} % ---".format(machine.settings.raft_density))
    ts.g.feed(ts.speed_printing_raft)  # print the filling of the raft
    raft_density = machine.settings.raft_density/100
    step = ts.coef_w_raft * machine.nozzle.size_id/raft_density  # step size
    step_number = ts.test_structure_size/step

    ts.g.move(x=-ts.coef_w_raft * machine.nozzle.size_id/2,
              y=0,
              z=0,
              extrude=False, extrusion_multiplier=0)

    for dummy in range(0, int(step_number)):
        ts.g.move(x=0,
                  y=+step,
                  z=0,
                  extrude=False, extrusion_multiplier=0)
        ts.g.move(x=(-1)**(dummy+1)*(ts.test_structure_size-ts.coef_w_raft * machine.nozzle.size_id),
                  y=0,
                  z=0,
                  extrude=True, extrusion_multiplier=ts.extrusion_multiplier_raft, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)

    ts.g.write("; --- finish to print the raft ---")
    ts.g.move(x=0,
              y=20,
              z=0,
              extrude=False, extrusion_multiplier=0)

    ts.g.set_extruder_temperature(ts.temperature_extruder[0])
    ts.g.dwell(30)  # to unload the nozzle

    if ts.ventilator_part_cooling:
        ts.g.set_ventilator_part_cooling(ts.set_ventilator_part_cooling)
    if ts.ventilator_entry:
        ts.g.set_ventilator_entry(ts.set_ventilator_entry)
    if ts.ventilator_exit:
        ts.g.set_ventilator_exit(ts.set_ventilator_exit)

    return


def print_raft_new(ts: TestSetupA):
    ts.g.home()
    ts.g.feed(2 * machine.settings.speed_printing)  # respect the units: mm/min

    if hasattr(ts, "temperature_printbed"):
        ts.g.set_printbed_temperature(ts.temperature_printbed)

    ts.g.abs_move(x=0,
                  y=0,
                  z=ts.coef_h_raft * machine.nozzle.size_id,
                  extrude=False, extrusion_multiplier=0)
    ts.g.write("; --- start to clean the nozzle ---")
    ts.g.set_extruder_temperature(ts.temperature_extruder_raft)
    ts.g.dwell(5)
    ts.g.write("G1 F1000 E5; extrude 5 mm of material")
    ts.g.dwell(5)
    ts.g.feed(machine.settings.speed_printing_raft)  # print the raft
    sf.infill(sf.raft_structure(ts.test_structure_size/2, structure="square"), outlines=2, g=ts.g, coef_w_raft=ts.coef_w_raft, coef_h_raft=ts.coef_h_raft)
    ts.g.write("; --- finish to print the raft ---")

    return


# GENERIC TEST ROUTINE: SINGLE TESTING PARAMETER vs. PRINTING SPEED
def flat_test_single_parameter_vs_speed_printing(ts: TestSetupA):
    ts.g.write(ts.title)
    ts.g.write(ts.comment1)
    wipe(ts)

    print_raft(ts) if ts.raft and ts.test_name != "first layer height" else raft_perimeter(ts) # print the raft to support the test structure

    ts.g.write("; --- start to print the test structure ---")
    ts.g.feed(machine.settings.speed_printing)

    test_structure_separation = (ts.test_structure_size - sum(map(lambda x, y: x*y, [ts.number_of_lines]*ts.number_of_test_structures, ts.step_x)))/(ts.number_of_test_structures+1)
    test_structure_width = [0.]
    test_structure_width.extend([ts.number_of_lines * k for k in ts.step_x])

    for current_test_structure in range(ts.number_of_test_structures):
        ts.g.write(ts.comment2[current_test_structure])
        ts.g.feed(ts.speed_printing[current_test_structure])

        ts.g.abs_travel(x=+ts.test_structure_size/2 - (sum_of_list_elements(test_structure_width, current_test_structure) + (current_test_structure + 1) * test_structure_separation),
                        y=+ts.test_structure_size/2,
                        z=+ts.abs_z[current_test_structure],
                        lift=1)

        if ts.test_name == "extrusion temperature":
            ts.g.travel(x=0,
                        y=+ts.test_structure_size/5,
                        z=+ts.abs_z[current_test_structure], retraction_speed=ts.retraction_speed, retraction_distance=ts.retraction_distance[current_test_structure])
            ts.g.set_extruder_temperature(ts.temperature_extruder[current_test_structure])
            ts.g.dwell(30)
            output = "G1 F500 E" + "{:.3f}".format(4 * ts.temperature_extruder[current_test_structure] / ts.temperature_extruder[0]) + \
                     "; extrude " + "{:.3f}".format(4 * ts.temperature_extruder[current_test_structure] / ts.temperature_extruder[0]) + " mm of material"
            ts.g.write(output)
            ts.g.move(x=0,
                      y=-ts.test_structure_size/5,
                      z=-ts.abs_z[current_test_structure],
                      extrude=True, extrusion_multiplier=0)

        step_x = ts.step_x[current_test_structure]

        for current_substructure in range(ts.number_of_substructures):
            if hasattr(ts, "min_max_speed_printing"):
                current_printing_speed = ts.min_max_speed_printing[(current_substructure)]
            else:
                current_printing_speed = ts.speed_printing[current_test_structure]

            ts.g.write("; --- testing the following printing speed value: {:.3f} mm/s".format(current_printing_speed))
            ts.g.feed(current_printing_speed)

            for current_layer in range(ts.number_of_layers): # layers
                if current_layer != 0:
                    ts.g.move(x=0,
                              y=0,
                              z=ts.coef_h[current_test_structure] * machine.nozzle.size_id,
                              extrude=False, extrusion_multiplier=0)  # move to the next floor

                for current_line in range(ts.number_of_lines):
                    if current_layer % 2 != 0:
                        ts.g.move(x=(-1)**(current_layer + 1) * step_x,
                                  y=0,
                                  z=0,
                                  extrude=False, extrusion_multiplier=0)
                        ts.g.move(x=0,
                                  y=(-1)**(current_line + 1) * ts.step_y/ts.number_of_substructures,
                                  z=0,
                                  extrude=True, extrusion_multiplier=ts.extrusion_multiplier[current_test_structure], coef_h=ts.coef_h[current_test_structure], coef_w=ts.coef_w[current_test_structure])
                    else:
                        ts.g.move(x=0,
                                  y=(-1)**(current_line + 1) * ts.step_y/ts.number_of_substructures,
                                  z=0,
                                  extrude=True, extrusion_multiplier=ts.extrusion_multiplier[current_test_structure], coef_h=ts.coef_h[current_test_structure], coef_w=ts.coef_w[current_test_structure])
                        ts.g.move(x=(-1)**(current_layer + 1) * step_x,
                                  y=0,
                                  z=0,
                                  extrude=False, extrusion_multiplier=0)

            ts.g.move(x=+step_x,
                      y=-ts.step_y/ts.number_of_substructures,
                      z=0,
                      extrude=False, extrusion_multiplier=0)  # Y step after substructure. Y and Z should be separated and staged

            if ts.number_of_layers % 2 != 0:  # check if even layer number
                ts.g.move(x=+step_x * ts.number_of_lines,
                          y=0,
                          z=0,
                          extrude=False, extrusion_multiplier=0)

            ts.g.move(x=0,
                      y=0,
                      z=-ts.coef_h[current_test_structure] * machine.nozzle.size_id * (ts.number_of_layers-1),
                      extrude=False, extrusion_multiplier=0)

            if current_substructure != ts.number_of_substructures-1:
                ts.g.move(x=-step_x,
                          y=0,
                          z=0,
                          extrude=False, extrusion_multiplier=0)  # small X step

    ts.g.write("; --- finish to print the test structure ---")
    ts.g.teardown()

    return


# RETRACTION DISTANCE at maximum RETRACTION SPEED
def retraction_distance(ts: TestSetupA):
    ts.g.write(ts.title)
    ts.g.write(ts.comment1)
    wipe(ts) # perform wipe of the nozzle
    print_raft(ts) # print the raft to support the test structure

    ts.g.write("; --- start to print the test structure ---")
    ts.g.feed(np.mean(ts.speed_printing))

    output = str("; --- testing the retraction speed value of {:.3f} mm/s ---".format(ts.retraction_speed))
    ts.g.write(output)

    test_structure_separation = (ts.test_structure_size - sum(map(lambda x, y: x * y, [ts.number_of_lines]*ts.number_of_test_structures, ts.step_x)))/(ts.number_of_test_structures+1)
    test_structure_width = [0.]
    test_structure_width.extend([ts.number_of_lines * k for k in ts.step_x])

    for current_test_structure in range(ts.number_of_test_structures):
        ts.g.set_extruder_temperature(ts.temperature_extruder[current_test_structure])
        ts.g.write(ts.comment2[current_test_structure])

        for current_layer in range(0, ts.number_of_layers): # layers
            ts.g.abs_travel(x=+ts.test_structure_size/2 - (sum_of_list_elements(test_structure_width, current_test_structure) + (current_test_structure + 1) * test_structure_separation),
                            y=+ts.test_structure_size/2,
                            z=+ts.abs_z[current_test_structure]+current_layer*ts.track_height[current_test_structure],
                            lift=1)

            for current_line in range(ts.number_of_lines):
                step_x = ts.step_x[current_test_structure]
                ts.g.move(x=-step_x,
                          y=0,
                          z=0,
                          extrude=False, extrusion_multiplier=0)

                ts.g.feed(ts.speed_printing[current_test_structure])
                ts.g.move(x=0,
                          y=((-1)**(current_line+1))*ts.step_y/3,
                          z=0,
                          extrude=True, extrusion_multiplier=ts.extrusion_multiplier[current_test_structure], coef_h=ts.coef_h[current_test_structure], coef_w=ts.coef_w[current_test_structure])
                output = "G1 F"+str(ts.retraction_speed * 60)+" E{:.3f}".format(-ts.retraction_distance[current_test_structure])+"; retract the filament"
                ts.g.write(output)

                ts.g.feed(ts.speed_printing[current_test_structure])
                ts.g.move(x=0,
                          y=((-1)**(current_line+1))*ts.step_y/3,
                          z=0,
                          extrude=False, extrusion_multiplier=0)
                output = "G1 F"+str(ts.retraction_speed * 60)+" E{:.3f}".format(+ts.retraction_distance[current_test_structure])+"; restart the filament"
                ts.g.write(output)

                ts.g.feed(ts.speed_printing[current_test_structure])
                ts.g.move(x=0,
                          y=((-1)**(current_line+1))*ts.step_y/3,
                          z=0,
                          extrude=True, extrusion_multiplier=ts.extrusion_multiplier[current_test_structure], coef_h=ts.coef_h[current_test_structure], coef_w=ts.coef_w[current_test_structure])

    ts.g.write("; --- finish to print the test structure ---")
    ts.g.teardown()

    return


# RETRACTION RESTART DISTANCE and COASTING DISTANCE
def retraction_restart_distance_vs_coasting_distance(ts: TestSetupA):
    ts.g.write(ts.title)
    ts.g.write(ts.comment1)
    wipe(ts) # perform wipe of the nozzle
    print_raft(ts) # print the raft to support the test structure
    ts.g.write("; --- start to print the test structure ---")
    ts.g.feed(machine.settings.speed_printing)

    test_structure_separation = (ts.test_structure_size - sum(map(lambda x, y: x * y, [ts.number_of_lines]*ts.number_of_test_structures, ts.step_x)))/(ts.number_of_test_structures+1)
    test_structure_width = [0.]
    test_structure_width.extend([ts.number_of_lines * k for k in ts.step_x])

    for current_test_structure in range(ts.number_of_test_structures):
        ts.g.write(ts.comment2[current_test_structure])
        ts.g.feed(ts.speed_printing[current_test_structure])

        ts.g.abs_travel(x=+ts.test_structure_size/2 - (sum_of_list_elements(test_structure_width, current_test_structure) + (current_test_structure + 1) * test_structure_separation),
                        y=+ts.test_structure_size/2,
                        z=+ts.abs_z[current_test_structure],
                        lift=1)

        step_x = ts.step_x[current_test_structure]

        for current_substructure in range(ts.number_of_substructures):
            if ts.min_max_speed_printing is not None:
                current_printing_speed = ts.min_max_speed_printing[(current_substructure if ts.number_of_substructures > 1 else current_test_structure)]
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

                output = "G1 F"+str(ts.retraction_speed * 60)+" E{:.3f}".format(-ts.retraction_distance[current_substructure])+"; retract the filament"
                ts.g.write(output)

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

                output = "G1 F"+str(ts.retraction_speed * 60)+" E{:.3f}".format(+ts.retraction_distance[current_test_structure]+ts.retraction_restart_distance[current_test_structure])+"; restart the filament"
                ts.g.write(output)

    ts.g.write("; --- finish to print the test structure ---")
    ts.g.teardown()

    return


# GENERIC TEST ROUTINE: SINGLE TESTING PARAMETER vs. PRINTING SPEED
def bridging_test(ts: TestSetupA):
    ts.g.write(ts.title)
    ts.g.write(ts.comment1)
    wipe(ts)

    if ts.raft:
        print_raft(ts)  # print the raft to support the test structure

    ts.g.write("; --- start to print the support structure ---")
    ts.g.feed(machine.settings.speed_printing)

    angle = 45
    perimeter = 4

    step_x = ts.test_structure_size/((ts.number_of_test_structures + 1)/2)/2
    step_y = ts.test_structure_size/ts.number_of_substructures - perimeter*np.mean(ts.track_width)/np.cos(np.deg2rad(angle))

    # Building support structures
    for current_layer in range(ts.number_of_layers):
        ts.g.abs_travel(x=+ts.test_structure_size/2,
                        y=-ts.test_structure_size/2,
                        z=+np.mean(ts.abs_z)+current_layer*np.mean(ts.track_height), lift=1)
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
            if current_substructure != range(ts.number_of_substructures)[-1]:
                ts.g.travel(x=0,
                            y=+step_y,
                            z=0,
                            lift=1,
                            retraction_speed=ts.retraction_speed,
                            retraction_distance=np.mean(ts.retraction_distance))

    ts.g.travel(x=0,
                y=-perimeter*np.mean(ts.track_width)/np.cos(np.deg2rad(angle))/4,
                z=np.mean(ts.track_height),
                lift=1,
                retraction_speed=ts.retraction_speed,
                retraction_distance=np.mean(ts.retraction_distance))

    ts.g.write("; --- starting to print bridges ---")

    # Printing bridges
    for current_speed_value in ts.min_max_speed_printing:
        ts.g.write("; --- testing the following bridging speed value: {:.1f} mm/s ---".format(current_speed_value))
        ts.g.feed(current_speed_value)
        for index, current_extrusion_multiplier_value in enumerate(ts.extrusion_multiplier_bridging):
            ts.g.write(ts.comment2[index])
            for step in range(int(step_y/np.mean(ts.track_width))):
                ts.g.move(x=(-1)**(step + 1)*2*(step_y - step*np.mean(ts.track_width))*step_x/step_y,
                          y=0,
                          z=0,
                          extrude=True, extrusion_multiplier=current_extrusion_multiplier_value)
                if step != range(int(step_y/np.mean(ts.track_width)))[-1]:
                    ts.g.move(x=0,
                              y=(-1)**index*np.mean(ts.track_width),
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
                    y=-2*step_y-perimeter*np.mean(ts.track_width)/np.cos(np.deg2rad(angle))/2,
                    z=0,
                    lift=1,
                    retraction_speed=ts.retraction_speed,
                    retraction_distance=np.mean(ts.retraction_distance))

    return
