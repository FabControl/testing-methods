import Definitions
from TestSetupA import TestSetupA
from TestSetupB import TestSetupB
import slicing_functionality as sf
from Definitions import *
from Globals import machine, material


# WIPE
def wipe(ts: TestSetupA or TestSetupB, full = True):
    ts.g.home()
    ts.g.feed(2 * machine.settings.speed_printing)  # respect the units: mm/min
    ts.g.abs_move(x=-6 * ts.test_structure_size / 10,
               y=-6 * ts.test_structure_size / 10,
               z=+2 * ts.coef_h_raft * machine.nozzle.size_id,
               extrude=False, extrusion_multiplier=0)

    if machine.settings.temperature_printbed is not None:
        ts.g.set_printbed_temperature(machine.settings.temperature_printbed)

    ts.g.write("; --- start to clean the nozzle ---")
    ts.g.set_extruder_temperature(machine.settings.temperature_extruder_raft)
    ts.g.dwell(5)
    output = "G1 F1000 E5; extrude 5 mm of material"
    ts.g.write(output)
    ts.g.dwell(5)
    ts.g.feed(machine.settings.speed_printing_raft)  # print the raft
    if isinstance(ts, TestSetupA):
        ts.g.abs_move(x=+6 * ts.test_structure_size / 10,
                      y=-6 * ts.test_structure_size / 10,
                      z=0,
                      extrude=True, extrusion_multiplier=2.25, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)
        ts.g.move(x=0,
                  y=+ts.test_structure_size / 10,
                  z=+ts.coef_h_raft * machine.nozzle.size_id,
                  extrude=False, extrusion_multiplier=0)
        ts.g.move(x=-ts.test_structure_size / 10,
                  y=0,
                  z=0,
                  extrude=False, extrusion_multiplier=0)
    elif isinstance(ts, TestSetupB):
        ts.g.abs_move(x=+6 * ts.test_structure_size / 10,
                      y=-6 * ts.test_structure_size / 10,
                      z=0,
                      extrude=True, extrusion_multiplier=2.25, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)
        ts.g.move(x=0,
                  y=-ts.test_structure_size / 10,
                  z=+ts.coef_h_raft * machine.nozzle.size_id,
                  extrude=False, extrusion_multiplier=0)
        ts.g.move(x=-ts.test_structure_size / 10,
                  y=0,
                  z=0,
                  extrude=False, extrusion_multiplier=0)
    ts.g.write("; --- end to clean the nozzle ---")


# RAFT PERIMETER
def raft_perimeter(ts: TestSetupA):
    ts.g.feed(machine.settings.speed_printing_raft)  # print the raft
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


# PRINTING RAFT
def print_raft(ts: TestSetupA):
    ts.g.feed(machine.settings.speed_printing_raft)  # print the raft
    ts.g.write("; --- start to print the raft ---")
    ts.g.set_extruder_temperature(machine.settings.temperature_extruder_raft)

    raft_perimeter(ts)

    output = ("; --- print the infill with the fill density of %.f %% ---" % (machine.settings.raft_density))

    ts.g.feed(machine.settings.speed_printing_raft)  # print the raft
    ts.g.write(output)

    ts.g.feed(machine.settings.speed_printing_raft)  # print the filling of the raft

    raft_density = machine.settings.raft_density / 100
    step = ts.coef_w_raft * machine.nozzle.size_id / raft_density  # step size

    step_number = ts.test_structure_size/(ts.coef_w_raft * machine.nozzle.size_id / raft_density)

    overlap = 1.1*(ts.coef_w_raft * machine.nozzle.size_id)/(2*step_number**2 - step_number)

    step_modified = (1-overlap)*step

    ts.g.move(x=-ts.coef_w_raft * machine.nozzle.size_id/2,
              y=0,
              z=0,
              extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)

    for dummy in range(0, int(step_number)):
        ts.g.move(x=0,
                  y=+step_modified,
                  z=0,
                  extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)
        ts.g.move(x=(-1)**(dummy+1)*(ts.test_structure_size-ts.coef_w_raft * machine.nozzle.size_id),
                  y=0,
                  z=0,
                  extrude=True, extrusion_multiplier=machine.settings.extrusion_multiplier_raft, coef_h=ts.coef_h_raft, coef_w=ts.coef_w_raft)

    ts.g.write("; --- finish to print the raft ---")

    ts.g.move(x=0,
              y=20,
              z=0,
              extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)

    ts.g.set_extruder_temperature(ts.temperature_extruder[0])
    ts.g.dwell(30)  # to unload the nozzle

    if machine.settings.part_cooling is not None:
        ts.g.set_part_cooling(machine.settings.part_cooling)

    return


def print_raft_new(ts: TestSetupA):
    ts.g.home()
    ts.g.feed(2 * machine.settings.speed_printing)  # respect the units: mm/min

    if machine.settings.temperature_printbed is not None:
        ts.g.set_printbed_temperature(machine.settings.temperature_printbed)
        ts.g.abs_move(x=0,
                      y=0,
                      z=ts.coef_h_raft * machine.nozzle.size_id,
                      extrude=False)
    ts.g.write("; --- start to clean the nozzle ---")
    ts.g.set_extruder_temperature(machine.settings.temperature_extruder_raft)
    ts.g.dwell(5)
    output = "G1 F1000 E5; extrude 5 mm of material"
    ts.g.write(output)
    ts.g.dwell(5)
    ts.g.feed(machine.settings.speed_printing_raft)  # print the raft
    sf.infill(sf.raft_structure(ts.test_structure_size/2, structure="square"), outlines=2, g= ts.g, coef_w= ts.coef_w_raft, coef_h= ts.coef_h_raft) # TODO
    ts.g.write("; --- finish to print the raft ---")


# GENERIC TEST ROUTINE: SINGLE TESTING PARAMETER vs. PRINTING SPEED
def flat_test_single_parameter_vs_speed_printing(ts: TestSetupA):
    g = ts.g

    number_of_substructures = 1 if ts.test_name == "printing speed" else 4

    ts.g.write(ts.title)
    ts.g.write(ts.comment1)
    wipe(ts)

    if ts.raft and ts.test_name != "first layer height":
        print_raft(ts)  # print the raft to support the test structure
    else:
        raft_perimeter(ts)
    ts.g.write("; --- start to print the test structure ---")
    ts.g.feed(machine.settings.speed_printing)  # respect the units: mm/min

    for dummy1 in range(0, ts.number_of_test_structures):
        ts.g.write(ts.comment2[dummy1])
        ts.g.feed(ts.speed_printing[dummy1])  # respect the units: mm/min

        ts.g.abs_travel(x=+ts.test_structure_size / 2 - (2 * dummy1 + 1) * ts.test_structure_size / (2 * ts.number_of_test_structures + 1),
                        y=+ts.test_structure_size / 2,
                        z=+ts.abs_z[dummy1],
                        lift=1)

        if ts.test_name == 'extrusion temperature':  # TODO! Fix the movement, time, extra restart distance
            ts.g.travel(x=0,
                     y=+ts.test_structure_size / 5,
                     z=+ts.abs_z[dummy1], retraction_speed=ts.retraction_speed, retraction_distance=ts.retraction_distance[dummy1]) #  TODO disable retractions
            ts.g.set_extruder_temperature(ts.temperature_extruder[dummy1])
            ts.g.dwell(30)
            output = "G1 F500 E" + str(round(4 * ts.temperature_extruder[dummy1] / ts.temperature_extruder[0],2)) + \
                     "; extrude " + str(round(4 * ts.temperature_extruder[dummy1] / ts.temperature_extruder[0],2)) + " mm of material"
            ts.g.write(output)
            ts.g.move(x=0,
                      y=-ts.test_structure_size / 5,
                      z=-ts.abs_z[dummy1],
                      extrude=True)

        step_x = ts.step_x[dummy1]

        dummy2_range = range(number_of_substructures)
        for dummy2 in dummy2_range:
            if ts.min_max_speed_printing is not None:
                current_printing_speed = ts.min_max_speed_printing[dummy2]
            else:
                current_printing_speed = ts.speed_printing[dummy1]
            ts.g.write('; --- testing the following printing speed value: %.3f mm/s' % (current_printing_speed))
            ts.g.feed(current_printing_speed)

            number_of_layers = range(1 if ts.test_name == "first layer height" else 2)
            for dummy0 in number_of_layers: # layers
                dummy3_range = range(0, ts.number_of_lines)
                if dummy0 != 0:
                    ts.g.move(z=ts.coef_h[dummy1] * machine.nozzle.size_id)  # move to the next floor

                for dummy3 in dummy3_range:
                    if dummy0 % 2 != 0:
                        ts.g.move(x=(-1)**(dummy0 + 1) * step_x,
                                  y=0,
                                  z=0,
                                  extrude=False)
                        ts.g.move(x=0,
                                  y=(-1)**(dummy3 + 1) * ts.step_y/number_of_substructures,
                                  z=0,
                                  extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy1], coef_h=ts.coef_h[dummy1], coef_w=ts.coef_w[dummy1])
                    else:
                        ts.g.move(x=0,
                               y=(-1) ** (dummy3 + 1) * ts.step_y / number_of_substructures,
                               z=0,
                               extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy1],
                               coef_h=ts.coef_h[dummy1], coef_w=ts.coef_w[dummy1])
                        ts.g.move(x=(-1) ** (dummy0 + 1) * step_x,
                               y=0,
                               z=0,
                               extrude=False)
            ts.g.move(x=0,
                      y=-ts.step_y/number_of_substructures,
                      extrude=False)  # Y step after substructure. Y and Z should be separated and staged

            if len(number_of_layers) % 2 != 0:  # check if even layer number
                ts.g.move(x=step_x * ts.number_of_lines,
                          y=0,
                          z=0,
                          extrude=False)

            ts.g.move(x=0,
                      y=0,
                      z=-ts.coef_h[dummy1] * machine.nozzle.size_id * (len(number_of_layers)-1),
                      extrude=False)
            if dummy2 != len(dummy2_range)-1:
                ts.g.move(x=-step_x,
                          y=0,
                          z=0,
                          extrude=False)  # small X step
                # g.move(z=+ts.coef_h[dummy1]*machine.nozzle.size_id,)

    g.write("; --- finish to print the test structure ---")
    g.teardown()


# RETRACTION DISTANCE at maximum RETRACTION SPEED
def retraction_distance(ts: TestSetupA):
    g = ts.g

    g.write(ts.title)
    g.write(ts.comment1)
    wipe(ts) # perform wipe of the nozzle
    print_raft(ts) # print the raft to support the test structure

    g.write("; --- start to print the test structure ---")
    g.feed(machine.settings.speed_printing)  # respect the units: mm/min

    output = str("; --- testing the retraction speed value of %.3f mm/s ---" % (ts.retraction_speed))
    g.write(output)

    for dummy2 in range(0, ts.number_of_test_structures):
        g.set_extruder_temperature(ts.temperature_extruder[dummy2])
        g.write(ts.comment2[dummy2])

        for dummy3 in range(0, 2): # layers
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
                       y=((-1)**(dummy4+1))*ts.step_y/3,
                       z=0,
                       extrude=True, extrusion_multiplier=ts.extrusion_multiplier[dummy2], coef_h=ts.coef_h[dummy2], coef_w=ts.coef_w[dummy2])
                output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(-ts.retraction_distance[dummy2]) + "; retract the filament"
                g.write(output)

                g.feed(ts.speed_printing[dummy2])
                g.move(x=0,
                       y=((-1)**(dummy4+1))*ts.step_y/3,
                       z=0,
                       extrude=False, extrusion_multiplier=0, coef_h=0, coef_w=0)
                output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(+ts.retraction_distance[dummy2]) + "; restart the filament"
                g.write(output)

                g.feed(ts.speed_printing[dummy2])
                g.move(x=0,
                       y=((-1)**(dummy4+1))*ts.step_y/3,
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
    wipe(ts)

    print_raft(ts)  # print the raft to support the test structure

    g.write("; --- start to print the test structure ---")
    g.feed(machine.settings.speed_printing)  # respect the units: mm/min

    for dummy2 in range(0, ts.number_of_test_structures):
        g.set_extruder_temperature(ts.temperature_extruder[dummy2])
        g.write(ts.comment2[dummy2])

        for dummy3 in range(0, 1): # layers
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


# # BRIDGING TEST overhang test TODO
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
