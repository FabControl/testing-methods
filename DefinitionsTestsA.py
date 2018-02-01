import Definitions
from TestSetupA import TestSetupA
import slicing_functionality as sf
from Definitions import *
from Globals import machine, material

# PRINTING RAFT
def print_raft(ts: TestSetupA):

    test_structure_size = ts.test_structure_size
    coef_w_raft = ts.coef_w_raft
    coef_h_raft = ts.coef_h_raft
    g = ts.g

    g.home()
    g.feed(2 * machine.settings.speed_printing)  # respect the units: mm/min
    g.abs_move(x=-6 * test_structure_size / 10,
               y=-6 * test_structure_size / 10,
               z=+2 * coef_h_raft * machine.nozzle.size_id,
               extrude=False, extrusion_multiplier=0)

    if machine.settings.temperature_printbed is not None:
        g.set_printbed_temperature(machine.settings.temperature_printbed)

    g.write("; --- start to clean the nozzle ---")
    g.set_extruder_temperature(machine.settings.temperature_extruder_raft)
    g.dwell(5)
    output = "G1 F1000 E5; extrude 5 mm of material"
    g.write(output)
    g.dwell(5)
    g.feed(machine.settings.speed_printing_raft)  # print the raft
    g.abs_move(x=+6 * test_structure_size / 10,
               y=-6 * test_structure_size / 10,
               z=0,
               extrude=True, extrusion_multiplier=2.25, coef_h=coef_h_raft, coef_w=coef_w_raft)
    g.move(x=0,
           y=+test_structure_size / 10,
           z=+coef_h_raft * machine.nozzle.size_id,
           extrude=False, extrusion_multiplier=0)
    g.move(x=-test_structure_size / 10,
           y=0,
           z=0,
           extrude=False, extrusion_multiplier=0)
    g.write("; --- end to clean the nozzle ---")

    g.write("; --- start to print the raft ---")
    g.set_extruder_temperature(machine.settings.temperature_extruder_raft)

    g.write("; --- print the outer perimeter ---")
    g.feed(machine.settings.speed_printing_raft)  # print the outer perimeter of the raft
    g.move(x=0,
           y=+test_structure_size,
           z=0,
           extrude=True, extrusion_multiplier=1.25, coef_h=coef_h_raft, coef_w=coef_w_raft)
    g.move(x=-test_structure_size,
           y=0,
           z=0,
           extrude=True, extrusion_multiplier=1.25, coef_h=coef_h_raft, coef_w=coef_w_raft)
    g.move(x=0,
           y=-test_structure_size,
           z=0,
           extrude=True, extrusion_multiplier=1.25, coef_h=coef_h_raft, coef_w=coef_w_raft)
    g.move(x=+test_structure_size,
           y=0,
           z=0,
           extrude=True, extrusion_multiplier=1.25, coef_h=coef_h_raft, coef_w=coef_w_raft)

    output = ("; --- print the infill with the fill density of %.f %% ---" % (machine.settings.raft_density))

    g.feed(machine.settings.speed_printing_raft)  # print the raft
    g.write(output)

    g.feed(machine.settings.speed_printing_raft)  # print the filling of the raft

    raft_density = machine.settings.raft_density / 100
    step = coef_w_raft * machine.nozzle.size_id / raft_density  # step size

    step_number = test_structure_size/(coef_w_raft * machine.nozzle.size_id / raft_density)

    overlap = 1.1*(coef_w_raft * machine.nozzle.size_id)/(2*step_number**2 - step_number)

    step_modified = (1-overlap)*step

    g.move(x=-coef_w_raft * machine.nozzle.size_id/2,
           y=0,
           z=0,
           extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)

    for dummy in range(0, int(step_number)):
        g.move(x=0,
               y=+step_modified,
               z=0,
               extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)
        g.move(x=(-1)**(dummy+1)*(test_structure_size-coef_w_raft * machine.nozzle.size_id),
               y=0,
               z=0,
               extrude=True, extrusion_multiplier=machine.settings.extrusion_multiplier_raft, coef_h=coef_h_raft, coef_w=coef_w_raft)

    g.write("; --- finish to print the raft ---")

    g.move(x=+20,
           y=0,
           z=0,
           extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)

    g.set_extruder_temperature(machine.settings.temperature_extruder)
    g.dwell(30)  # to unload the nozzle

    g.move(x=0,
           y=+20,
           z=0,
           extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)

    if machine.settings.part_cooling is not None:
        g.set_part_cooling(machine.settings.part_cooling)

    return


def print_raft_new(ts: TestSetupA):
    test_structure_size = ts.test_structure_size
    coef_w_raft = ts.coef_w_raft
    coef_h_raft = ts.coef_h_raft
    g = ts.g

    g.home()
    g.feed(2 * machine.settings.speed_printing)  # respect the units: mm/min

    if machine.settings.temperature_printbed is not None:
        g.set_printbed_temperature(machine.settings.temperature_printbed)
    g.abs_move(x=0,
               y=0,
               z=coef_h_raft * machine.nozzle.size_id,
               extrude=False)
    g.write("; --- start to clean the nozzle ---")
    g.set_extruder_temperature(machine.settings.temperature_extruder_raft)
    g.dwell(5)
    output = "G1 F1000 E5; extrude 5 mm of material"
    g.write(output)
    g.dwell(5)
    g.feed(machine.settings.speed_printing_raft)  # print the raft
    sf.infill(sf.raft_structure(test_structure_size/2, structure="square"), outlines=2, g= g, coef_w= coef_w_raft, coef_h= coef_h_raft)
    g.write("; --- finish to print the raft ---")


# GENERIC TEST ROUTINE: SINGLE TESTING PARAMETER
def flat_test_single_parameter(ts: TestSetupA):
    g = ts.g

    g.write(ts.title)
    g.write(ts.comment1)

    if ts.test_name == 'printing speed':
        flat_test_single_parameter(ts)
    else:
        if ts.raft:
            print_raft(ts)  # print the raft to support the test structure
        elif ts.raft == True and ts.test_name != 'first layer height':
            print_raft(ts)  # print the raft to support the test structure
        else:
            pass

    g.write("; --- start to print the test structure ---")
    g.feed(machine.settings.speed_printing)  # respect the units: mm/min

    for dummy1 in range(0, ts.number_of_test_structures):
        g.set_extruder_temperature(ts.temperature_extruder[dummy1])
        g.write(ts.comment2[dummy1])
        g.abs_move(x=+ts.test_structure_size / 2 - (2 * dummy1 + 1) * ts.test_structure_size / (2 * ts.number_of_test_structures + 1),
                   y=+ts.test_structure_size / 2,
                   z=+ts.abs_z[dummy1],
                   extrude=False, extrusion_multiplier=0)

        g.feed(ts.speed_printing[dummy1])  # respect the units: mm/min

        for dummy2 in range(0, ts.number_of_lines):
            step_x = ts.step_x[dummy1]

            g.move(x=-step_x,
                   y=0,
                   z=0,
                   extrude=False, extrusion_multiplier=0)
            g.move(x=0,
                   y=((-1)**(dummy2+1))*ts.step_y,
                   z=0,
                   extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy1], coef_h=ts.coef_h[dummy1], coef_w=ts.coef_w[dummy1])

        if ts.test_name == 'extrusion temperature':
            g.move(x=0,
                   y=+ts.test_structure_size / 5,
                   z=0,
                   extrude=False, extrusion_multiplier=0)

            try:
                g.set_extruder_temperature(ts.temperature_extruder[dummy1 + 1])
                g.dwell(30)
                output = "G1 F500 E" + str(round(2 * ts.temperature_extruder[dummy1] / ts.temperature_extruder[0], 2)) + "; extrude " + str(round(2 * ts.temperature_extruder[dummy1] / ts.temperature_extruder[0], 2)) + " mm of material"
                g.write(output)
                g.move(x=0,
                       y=-ts.test_structure_size / 5,
                       z=0,
                       extrude=False, extrusion_multiplier=0)
            except IndexError:
                g.set_extruder_temperature(ts.temperature_extruder[-1])

    g.write("; --- finish to print the test structure ---")
    g.teardown()
    return


# GENERIC TEST ROUTINE: SINGLE TESTING PARAMETER vs. PRINTING SPEED
def flat_test_single_parameter_vs_speed_printing(ts: TestSetupA):
    g = ts.g

    g.write(ts.title)
    g.write(ts.comment1)

    if ts.test_name == 'printing speed':
        flat_test_single_parameter(ts)
    else:
        if ts.raft:
            print_raft(ts)  # print the raft to support the test structure
        elif ts.raft == True and ts.test_name != 'first layer height':
            print_raft(ts)  # print the raft to support the test structure
        else:
            pass

        g.write("; --- start to print the test structure ---")
        g.feed(machine.settings.speed_printing)  # respect the units: mm/min

        for dummy1 in range(0, ts.number_of_test_structures):

            g.write(ts.comment2[dummy1])

            g.abs_travel(x=+ts.test_structure_size / 2 - (2 * dummy1 + 1) * ts.test_structure_size / (2 * ts.number_of_test_structures + 1),
                         y=+ts.test_structure_size / 2,
                         z=+ts.abs_z[dummy1],
                         lift=1)

            if ts.test_name == 'extrusion temperature':  # TODO! Fix the movement, time, extra restart distance
                g.travel(x=0,
                         y=+ts.test_structure_size / 5,
                         z=+ts.abs_z[dummy1], retraction_speed=ts.retraction_speed, retraction_distance=ts.retraction_distance[dummy1])
                g.set_extruder_temperature(ts.temperature_extruder[dummy1])
                g.dwell(30)
                output = "G1 F500 E" + str(round(2 * ts.temperature_extruder[dummy1] / ts.temperature_extruder[0],2)) + "; extrude " + str(round(2 * ts.temperature_extruder[dummy1] / ts.temperature_extruder[0],2)) + " mm of material"
                g.write(output)
                g.move(x=0,
                       y=-ts.test_structure_size / 5,
                       z=-ts.abs_z[dummy1], extrude=False)

            g.feed(ts.speed_printing[dummy1])  # respect the units: mm/min

            step_x = ts.step_x[dummy1]

            for dummy2 in range(0, 4):
                current_printing_speed = ts.min_max_speed_printing[dummy2]  # TODO
                g.write('; --- testing the following printing speed value: %.3f mm/s' % (current_printing_speed))
                g.feed(current_printing_speed)

                dummy3_range = range(0, int(ts.number_of_lines/2))
                for dummy3 in dummy3_range:
                        g.move(x=(-1)**(dummy2 + 1) * step_x,
                           y=0,
                           z=0,
                           extrude=False)
                        g.move(x=0,
                               y=-ts.step_y/4,
                               z=0,
                               extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy1], coef_h=ts.coef_h[dummy1], coef_w=ts.coef_w[dummy1])
                        if dummy3 != len(dummy3_range)-1:
                            g.move(x=(-1)**(dummy2 + 1) * step_x,
                                   y=0,
                                   z=0,
                                   extrude=False)
                            g.move(x=0,
                                   y=+ts.step_y/4,
                                   z=0,
                                   extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy1], coef_h=ts.coef_h[dummy1], coef_w=ts.coef_w[dummy1])

        g.write("; --- finish to print the test structure ---")
        g.teardown()

    return


# RETRACTION DISTANCE at maximum RETRACTION SPEED
def retraction_distance(ts: TestSetupA):
    g = ts.g

    g.write(ts.title)
    g.write(ts.comment1)

    print_raft(ts)  # print the raft to support the test structure

    g.write("; --- start to print the test structure ---")
    g.feed(machine.settings.speed_printing)  # respect the units: mm/min

    output = str("; --- testing the retraction speed value of %.3f mm/s ---" % (ts.retraction_speed))
    g.write(output)

    for dummy2 in range(0, ts.number_of_test_structures):
        g.set_extruder_temperature(ts.temperature_extruder[dummy2])
        g.write(ts.comment2[dummy2])

        for dummy3 in range(0, 4): # layers

            g.abs_move(x=+ts.test_structure_size / 2 - (2 * dummy2 + 1) * ts.test_structure_size / (2 * ts.number_of_test_structures + 1),
                       y=+ts.test_structure_size / 2,
                       z=+(dummy3 + 1) * ts.coef_h[dummy2] * machine.nozzle.size_id + ts.coef_h_raft * machine.nozzle.size_id,
                       extrude=False, extrusion_multiplier=0)

            for dummy4 in range(0, ts.number_of_lines):

                step_x = ts.step_x[dummy2]

                g.move(x=-step_x,
                       y=0,
                       z=0,
                       extrude=False, extrusion_multiplier=0)

                g.feed(ts.speed_printing[dummy2])

                g.move(x=0,
                       y=((-1)**(dummy4+1))*ts.step_y / 3,
                       z=0,
                       extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy2], coef_h=ts.coef_h[dummy2], coef_w=ts.coef_w[dummy2])

                output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(-ts.retraction_distance[dummy2]) + "; retract the filament"
                g.write(output)

                g.feed(ts.speed_printing[dummy2])

                g.move(x=0,
                       y=((-1)**(dummy4+1))*ts.step_y / 3,
                       z=0,
                       extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)

                output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(+ts.retraction_distance[dummy2]) + "; restart the filament"
                g.write(output)

                g.feed(ts.speed_printing[dummy2])

                g.move(x=0,
                       y=((-1)**(dummy4+1))*ts.step_y / 3,
                       z=0,
                       extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy2], coef_h=ts.coef_h[dummy2], coef_w=ts.coef_w[dummy2])

    g.write("; --- finish to print the test structure ---")
    g.teardown()

    return


# RETRACTION RESTART DISTANCE and COASTING DISTANCE
def retraction_restart_distance_vs_coasting_distance(ts: TestSetupA):
    g = ts.g

    g.write(ts.title)
    g.write(ts.comment1)

    print_raft(ts)  # print the raft to support the test structure

    g.write("; --- start to print the test structure ---")
    g.feed(machine.settings.speed_printing)  # respect the units: mm/min

    for dummy2 in range(0, ts.number_of_test_structures):
        g.set_extruder_temperature(ts.temperature_extruder[dummy2])
        g.write(ts.comment2[dummy2])

        for dummy3 in range(0, 4): # layers
                g.abs_move(x=+ts.test_structure_size / 2 - (2 * dummy2 + 1) * ts.test_structure_size / (2 * ts.number_of_test_structures + 1),
                           y=+ts.test_structure_size / 2,
                           z=+(dummy3 + 1) * ts.coef_h[dummy2] * machine.nozzle.size_id + ts.coef_h_raft * machine.nozzle.size_id,
                           extrude=False, extrusion_multiplier=0)

                dummy5 = 0

                for dummy4 in range(0, ts.number_of_lines):

                    step_x = ts.step_x[dummy2]

                    output = str("; --- testing the coasting distance value of %.3f mm ---" % (ts.coasting_distance[dummy5]))
                    g.write(output)

                    g.feed(ts.speed_printing[dummy2])

                    g.move(x=-step_x,
                           y=0,
                           z=0,
                           extrude=False, extrusion_multiplier=0)

                    g.move(x=0,
                           y=-(ts.step_y / 7 - ts.coasting_distance[dummy5]),
                           z=0,
                           extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy2], coef_h=ts.coef_h[dummy2], coef_w=ts.coef_w[dummy2])

                    g.move(x=0,
                           y=-(ts.coasting_distance[dummy5]),
                           z=0,
                           extrude=False, extrusion_multiplier=0)

                    output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(-ts.retraction_distance[dummy2]) + "; retract the filament"
                    g.write(output)

                    dummy5 = dummy5 + 1
                    output = str("; --- testing the coasting distance value of %.3f mm ---" % (ts.coasting_distance[dummy5]))
                    g.write(output)

                    g.feed(ts.speed_printing[dummy2])

                    g.move(x=0,
                           y=-ts.step_y / 7,
                           z=0,
                           extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)

                    output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(+ts.retraction_distance[dummy2]+ts.retraction_restart_distance[dummy2]) + "; restart the filament"
                    g.write(output)

                    g.feed(ts.speed_printing[dummy2])

                    g.move(x=0,
                           y=-(ts.step_y / 7 - ts.coasting_distance[dummy5]),
                           z=0,
                           extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy2], coef_h=ts.coef_h[dummy2], coef_w=ts.coef_w[dummy2])

                    g.move(x=0,
                           y=-(ts.coasting_distance[dummy5]),
                           z=0,
                           extrude=False, extrusion_multiplier=0)

                    output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(-ts.retraction_distance[dummy2]) + "; retract the filament"
                    g.write(output)

                    dummy5 = dummy5 + 1
                    output = str("; --- testing the coasting distance value of %.3f mm ---" % (ts.coasting_distance[dummy5]))
                    g.write(output)

                    g.feed(ts.speed_printing[dummy2])

                    g.move(x=0,
                           y=-ts.step_y / 7,
                           z=0,
                           extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)

                    output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(+ts.retraction_distance[dummy2] + ts.retraction_restart_distance[dummy2]) + "; restart the filament"
                    g.write(output)

                    g.feed(ts.speed_printing[dummy2])

                    g.move(x=0,
                           y=-(ts.step_y / 7 - ts.coasting_distance[dummy5]),
                           z=0,
                           extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy2], coef_h=ts.coef_h[dummy2], coef_w=ts.coef_w[dummy2])

                    g.move(x=0,
                           y=-ts.coasting_distance[dummy5],
                           z=0,
                           extrude=False, extrusion_multiplier=0)

                    output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(-ts.retraction_distance[dummy2]) + "; retract the filament"
                    g.write(output)

                    dummy5 = dummy5 + 1
                    output = str("; --- testing the coasting distance value of %.3f mm ---" % (ts.coasting_distance[dummy5]))
                    g.write(output)

                    g.feed(ts.speed_printing[dummy2])

                    g.move(x=0,
                           y=-ts.step_y / 7,
                           z=0,
                           extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)

                    output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(+ts.retraction_distance[dummy2] + ts.retraction_restart_distance[dummy2]) + "; restart the filament"
                    g.write(output)

                    g.feed(ts.speed_printing[dummy2])

                    g.move(x=0,
                           y=-(ts.step_y / 7 - ts.coasting_distance[dummy5]),
                           z=0,
                           extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy2], coef_h=ts.coef_h[dummy2], coef_w=ts.coef_w[dummy2])

                    g.move(x=0,
                           y=-ts.coasting_distance[dummy5],
                           z=0,
                           extrude=False, extrusion_multiplier=0)

                    output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(-ts.retraction_distance[dummy2]) + "; retract the filament"
                    g.write(output)

                    dummy5 = 0

                    g.feed(ts.speed_printing[dummy2])

                    g.move(x=0,
                           y=+ts.step_y,
                           z=0,
                           extrude=False, extrusion_multiplier=0)

                    output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(+ts.retraction_distance[dummy2] + ts.retraction_restart_distance[dummy2]) + "; restart the filament"
                    g.write(output)


    g.write("; --- finish to print the test structure ---")
    g.teardown()

    return


# # BRIDGING TEST TODO
# def test9(material: Material, path: str):
#     coef_h_raft, coef_h_min_raft, coef_h_max_raft, coef_w_raft, coef_h_raft_all = minmax_path_width_height_raft(machine)
#
#     g = Gplus(material, machine, outfile=path, layer_height=coef_h_raft * machine.nozzle.size_id,
#               extrusion_width=coef_w_raft * machine.nozzle.size_id,
#               aerotech_include=False, footer=footer, header=header, extrude=True,
#               extrusion_multiplier=machine.settings.extrusion_multiplier)
#
#     test_structure_size = get_test_structure_size(machine)
#
#     # The gcode actions go here:
#     output = str("; --- Bridging test of %s from %s (ID: %s) ---" % (material.name, material.manufacturer, material.id))
#     g.write(output)
#
#     print_raft(machine, test_structure_size, coef_w_raft, coef_h_raft, g)
#
#     # these data should come from the optimized values
#     coef_h = machine.settings.path_height / machine.nozzle.size_id
#     coef_w = machine.settings.path_width / machine.nozzle.size_id
#
#     retraction_distance = -3.5
#
#     speed_printing_all = np.linspace(machine.settings.speed_printing / 4, 2 * machine.settings.speed_printing, ts.number_of_test_structures)
#
#     g.write("; --- start to print the test structure ---")
#     g.feed(machine.settings.speed_printing)  # respect the units: mm/min
#
#     g.move(x=+test_structure_size / 10,
#            y=0,
#            z=0,
#            extrude=False, extrusion_multiplier=0, coef_h=coef_h, coef_w=coef_w)
#
#     if machine.settings.temperature_printbed_raft is not None:
#         g.set_printbed_temperature(machine.settings.temperature_printbed_raft)
#
#     g.set_extruder_temperature(machine.settings.temperature_extruder)
#     g.dwell(30)
#
#     g.move(x=-test_structure_size / 10,
#            y=0,
#            z=0,
#            extrude=False, extrusion_multiplier=0, coef_h=coef_h, coef_w=coef_w)
#
#     for dummy1 in range(0, ts.number_of_test_structures):
#
#         g.set_extruder_temperature(machine.settings.temperature_extruder)
#
#         for dummy2 in range(0, 5):
#
#             output = str("; --- creating a support structure with the path height of %.3f mm and the path width of %.3f mm ---" % (
#                     round(coef_h * machine.nozzle.size_id, 3),
#                     round(coef_w * machine.nozzle.size_id, 3)))
#             g.write(output)
#
#             g.abs_move(x=-test_structure_size / 2,
#                        y=-test_structure_size / 2 + (2 * dummy1 + 1) * test_structure_size / (2 * ts.number_of_test_structures + 1),
#                        z=(dummy2 + 1) * coef_h * machine.nozzle.size_id + coef_h_raft * machine.nozzle.size_id,
#                        extrude=False, extrusion_multiplier=0)
#
#             for dummy3 in range(0, int(int(round(test_structure_size / coef_w * machine.nozzle.size_id / 2, 0)) / (2 * machine.settings.number_of_test_structures + 1))):
#                 g.move(x=0,
#                        y=coef_w * machine.nozzle.size_id,
#                        z=0,
#                        extrude=False, extrusion_multiplier=0)
#
#                 g.move(x=(+test_structure_size - coef_w * machine.nozzle.size_id) / 3,
#                        y=0,
#                        z=0,
#                        extrude=True, extrusion_multiplier=1, coef_h=coef_h, coef_w=coef_w)
#
#                 output = "G1 F" + str(machine.settings.speed_printing * 60) + " E" + str(+retraction_distance) + "; retract the filament"
#                 g.write(output)
#
#                 g.move(x=(+test_structure_size - coef_w * machine.nozzle.size_id) / 3,
#                        y=0,
#                        z=0,
#                        extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)
#
#                 output = "G1 F" + str(machine.settings.speed_printing * 60) + " E" + str(-retraction_distance) + "; feed the filament"
#                 g.write(output)
#
#                 g.move(x=(+test_structure_size - coef_w * machine.nozzle.size_id) / 3,
#                        y=0,
#                        z=0,
#                        extrude=True, extrusion_multiplier=1, coef_h=coef_h, coef_w=coef_w)
#
#                 g.move(x=0,
#                        y=coef_w * machine.nozzle.size_id,
#                        z=0,
#                        extrude=False, extrusion_multiplier=0)
#
#                 g.move(x=(-test_structure_size + coef_w * machine.nozzle.size_id) / 3,
#                        y=0,
#                        z=0,
#                        extrude=True, extrusion_multiplier=1, coef_h=coef_h, coef_w=coef_w)
#
#                 output = "G1 F" + str(machine.settings.speed_printing * 60) + " E" + str(+retraction_distance) + "; retract the filament"
#                 g.write(output)
#
#                 g.move(x=(-test_structure_size + coef_w * machine.nozzle.size_id) / 3,
#                        y=0,
#                        z=0,
#                        extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)
#
#                 output = "G1 F" + str(machine.settings.speed_printing * 60) + " E" + str(-retraction_distance) + "; feed the filament"
#                 g.write(output)
#
#                 g.move(x=(-test_structure_size + coef_w * machine.nozzle.size_id) / 3,
#                        y=0,
#                        z=0,
#                        extrude=True, extrusion_multiplier=1, coef_h=coef_h, coef_w=coef_w)
#
#         for dummy4 in range(0, 1):
#
#             output = str("; --- testing the bridging performance at %.3f mm/s at the height of %.3f mm with the path height of %.3f mm and the path width of %.3f mm ---" % (
#                     round(speed_printing_all[dummy1], 3),
#                     round((dummy2 + 2) * coef_h * machine.nozzle.size_id + coef_h_raft * machine.nozzle.size_id, 3),
#                     round(coef_h * machine.nozzle.size_id, 3), round(coef_w * machine.nozzle.size_id, 3)))
#             g.write(output)
#
#             g.set_part_cooling(100)
#
#             output = "G1 F" + str(speed_printing_all[dummy1] * 60) + "; set a different printing speed"
#             g.write(output)
#
#             g.abs_move(x=-test_structure_size / 2,
#                        y=-test_structure_size / 2 + (2 * dummy1 + 1) * test_structure_size / (2 * machine.settings.number_of_test_structures + 1),
#                        z=(dummy2 + 2) * coef_h * machine.nozzle.size_id + coef_h_raft * machine.nozzle.size_id,
#                        extrude=False, extrusion_multiplier=0)
#
#             for dummy5 in range(0, int(int(round(test_structure_size / coef_w * machine.nozzle.size_id / 2, 0)) / (2 * machine.settings.number_of_test_structures + 1))):
#                 g.move(x=0,
#                        y=coef_w * machine.nozzle.size_id,
#                        z=0,
#                        extrude=False, extrusion_multiplier=0)
#
#                 g.move(x=+test_structure_size - coef_w * machine.nozzle.size_id,
#                        y=0,
#                        z=0,
#                        extrude=True, extrusion_multiplier=machine.settings.extrusion_multiplier, coef_h=coef_h, coef_w=coef_w)
#
#                 g.move(x=0,
#                        y=coef_w * machine.nozzle.size_id,
#                        z=0,
#                        extrude=False, extrusion_multiplier=0)
#
#                 g.move(x=-test_structure_size + coef_w * machine.nozzle.size_id,
#                        y=0,
#                        z=0,
#                        extrude=True, extrusion_multiplier=machine.settings.extrusion_multiplier, coef_h=coef_h, coef_w=coef_w)
#
#             g.set_part_cooling(0)
#
#     g.write("; --- finish to print the test structure ---")
#     g.teardown()
