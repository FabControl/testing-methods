import Definitions
from TestSetupA import TestSetupA
from TestSetupB import TestSetupB
import slicing_functionality as sf
from Definitions import *
from Globals import machine


# WIPE
def wipe(ts: TestSetupA or TestSetupB, full = True):
    ts.g.home()
    ts.g.feed(2 * machine.settings.speed_printing)  # respect the units: mm/min
    ts.g.abs_move(x=-6 * ts.test_structure_size / 10,
                  y=-6 * ts.test_structure_size / 10,
                  z=+2 * ts.coef_h_raft * machine.nozzle.size_id,
                  extrude=False, extrusion_multiplier=0)

    ts.g.set_printbed_temperature(machine.settings.temperature_printbed) if machine.settings.temperature_printbed is not None else ts.g.set_printbed_temperature(40)

    ts.g.write("; --- start to clean the nozzle ---")
    ts.g.set_extruder_temperature(machine.settings.temperature_extruder_raft)
    ts.g.dwell(5)
    if machine.nozzle.size_id <= 0.4:
        output = "G1 F1000 E2.5; extrude 2.5 mm of material"
    elif 0.4 < machine.nozzle.size_id <= 0.6:
        output = "G1 F1000 E5; extrude 5 mm of material"
    elif machine.nozzle.size_id > 0.6:
        output = "G1 F1000 E7.5; extrude 7.5 mm of material"

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
    ts.g.feed(ts.speed_printing_raft) # print the raft
    ts.g.write("; --- start to print the raft ---")
    ts.g.set_extruder_temperature(ts.temperature_extruder_raft)
    raft_perimeter(ts)
    output = ("; --- print the infill with the fill density of {} % ---".format(machine.settings.raft_density))
    ts.g.write(output)
    ts.g.feed(ts.speed_printing_raft)  # print the filling of the raft
    raft_density = machine.settings.raft_density / 100
    step = ts.coef_w_raft * machine.nozzle.size_id / raft_density  # step size
    step_number = ts.test_structure_size/(ts.coef_w_raft * machine.nozzle.size_id / raft_density)
    #overlap = ts.coef_w_raft * machine.nozzle.size_id/(2*step_number**2 - step_number)
    step_modified = step
    ts.g.move(x=-ts.coef_w_raft * machine.nozzle.size_id/2,
              y=0,
              z=0,
              extrude=False, extrusion_multiplier=0)

    for dummy in range(0, int(step_number)):
        ts.g.move(x=0,
                  y=+step_modified,
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

    if machine.settings.temperature_printbed is not None:
        ts.g.set_printbed_temperature(machine.settings.temperature_printbed)
        ts.g.abs_move(x=0,
                      y=0,
                      z=ts.coef_h_raft * machine.nozzle.size_id,
                      extrude=False, extrusion_multiplier=0)
    ts.g.write("; --- start to clean the nozzle ---")
    ts.g.set_extruder_temperature(ts.temperature_extruder_raft)
    ts.g.dwell(5)
    output = "G1 F1000 E5; extrude 5 mm of material"
    ts.g.write(output)
    ts.g.dwell(5)
    ts.g.feed(machine.settings.speed_printing_raft)  # print the raft
    sf.infill(sf.raft_structure(ts.test_structure_size / 2, structure="square"), outlines=2, g=ts.g,
              coef_w_raft=ts.coef_w_raft, coef_h_raft=ts.coef_h_raft)
    ts.g.write("; --- finish to print the raft ---")


# GENERIC TEST ROUTINE: SINGLE TESTING PARAMETER vs. PRINTING SPEED
def flat_test_single_parameter_vs_speed_printing(ts: TestSetupA):
    ts.g.write(ts.title)
    ts.g.write(ts.comment1)
    wipe(ts)

    print_raft(ts) if ts.raft and ts.test_name != "first layer height" else raft_perimeter(ts) # print the raft to support the test structure

    ts.g.write("; --- start to print the test structure ---")
    ts.g.feed(machine.settings.speed_printing)  # respect the units: mm/min

    for current_test_structure in range(0, ts.number_of_test_structures):
        ts.g.write(ts.comment2[current_test_structure])
        ts.g.feed(ts.speed_printing[current_test_structure])  # respect the units: mm/min

        ts.g.abs_travel(x=+ts.test_structure_size / 2 - (2 * current_test_structure + 1) * ts.test_structure_size / (2 * ts.number_of_test_structures + 1),
                        y=+ts.test_structure_size / 2,
                        z=+ts.abs_z[current_test_structure],
                        lift=1)

        if ts.test_name == 'extrusion temperature':
            ts.g.travel(x=0,
                        y=+ts.test_structure_size / 5,
                        z=+ts.abs_z[current_test_structure], retraction_speed=ts.retraction_speed, retraction_distance=ts.retraction_distance[current_test_structure])
            ts.g.set_extruder_temperature(ts.temperature_extruder[current_test_structure])
            ts.g.dwell(30)
            output = "G1 F500 E" + str(round(4 * ts.temperature_extruder[current_test_structure] / ts.temperature_extruder[0],2)) + \
                     "; extrude " + str(round(4 * ts.temperature_extruder[current_test_structure] / ts.temperature_extruder[0],2)) + " mm of material"
            ts.g.write(output)
            ts.g.move(x=0,
                      y=-ts.test_structure_size / 5,
                      z=-ts.abs_z[current_test_structure],
                      extrude=True)

        step_x = ts.step_x[current_test_structure]

        for current_substructure in range(ts.number_of_substructures):
            current_printing_speed = ts.min_max_speed_printing[(current_substructure if ts.number_of_substructures > 1 else current_test_structure)] if ts.min_max_speed_printing is not None else ts.speed_printing[current_test_structure]
            ts.g.write('; --- testing the following printing speed value: {:.3f} mm/s'.format(current_printing_speed))
            ts.g.feed(current_printing_speed)

            for current_layer in range(ts.number_of_layers): # layers
                if current_layer != 0:
                    ts.g.move(z=ts.coef_h[current_test_structure] * machine.nozzle.size_id)  # move to the next floor

                for current_line in range(0, ts.number_of_lines):
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

            ts.g.move(x=0,
                      y=-ts.step_y/ts.number_of_substructures,
                      z=0,
                      extrude=False, extrusion_multiplier=0)  # Y step after substructure. Y and Z should be separated and staged

            if ts.number_of_layers % 2 != 0:  # check if even layer number
                ts.g.move(x=step_x * ts.number_of_lines,
                          y=0,
                          z=0,
                          extrude=False, extrusion_multiplier=0)

            ts.g.move(x=0,
                      y=0,
                      z=-ts.coef_h[current_test_structure] * machine.nozzle.size_id * (ts.number_of_layers-1),
                      extrude=False)

            if current_substructure != ts.number_of_substructures-1:
                ts.g.move(x=-step_x,
                          y=0,
                          z=0,
                          extrude=False, extrusion_multiplier=0)  # small X step

    ts.g.write("; --- finish to print the test structure ---")
    ts.g.teardown()


# RETRACTION DISTANCE at maximum RETRACTION SPEED
def retraction_distance(ts: TestSetupA):
    ts.g.write(ts.title)
    ts.g.write(ts.comment1)
    wipe(ts) # perform wipe of the nozzle
    print_raft(ts) # print the raft to support the test structure

    ts.g.write("; --- start to print the test structure ---")
    ts.g.feed(machine.settings.speed_printing)  # respect the units: mm/min

    output = str("; --- testing the retraction speed value of {:.3f} mm/s ---".format(ts.retraction_speed))
    ts.g.write(output)

    for current_test_structure in range(0, ts.number_of_test_structures):
        ts.g.set_extruder_temperature(ts.temperature_extruder[current_test_structure])
        ts.g.write(ts.comment2[current_test_structure])

        for current_layer in range(0, ts.number_of_layers): # layers
            ts.g.abs_move(x=+ts.test_structure_size / 2 - (2 * current_test_structure + 1) * ts.test_structure_size / (2 * ts.number_of_test_structures + 1),
                          y=+ts.test_structure_size / 2,
                          z=+(current_layer + 1) * ts.coef_h[current_test_structure] * machine.nozzle.size_id + ts.coef_h_raft * machine.nozzle.size_id,
                          extrude=False, extrusion_multiplier=0)

            for current_line in range(0, ts.number_of_lines):
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
                output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(-ts.retraction_distance[current_test_structure]) + "; retract the filament"
                ts.g.write(output)

                ts.g.feed(ts.speed_printing[current_test_structure])
                ts.g.move(x=0,
                       y=((-1)**(current_line+1))*ts.step_y/3,
                       z=0,
                       extrude=False, extrusion_multiplier=0)
                output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(+ts.retraction_distance[current_test_structure]) + "; restart the filament"
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
    number_of_layers = range(1) # TODO: more layers needed?
    ts.g.write(ts.title)
    ts.g.write(ts.comment1)
    wipe(ts) # perform wipe of the nozzle
    print_raft(ts) # print the raft to support the test structure
    ts.g.write("; --- start to print the test structure ---")
    ts.g.feed(machine.settings.speed_printing)  # respect the units: mm/min

    for current_test_structure in range(0, ts.number_of_test_structures):
        ts.g.write(ts.comment2[current_test_structure])
        ts.g.feed(ts.speed_printing[current_test_structure])  # respect the units: mm/min

        ts.g.abs_travel(x=+ts.test_structure_size / 2 - (2 * current_test_structure + 1) * ts.test_structure_size / (2 * ts.number_of_test_structures + 1),
                        y=+ts.test_structure_size / 2,
                        z=+ts.abs_z[current_test_structure],
                        lift=1)

        step_x = ts.step_x[current_test_structure]

        for current_substructure in range(ts.number_of_substructures):
            current_printing_speed = ts.min_max_speed_printing[(current_substructure if ts.number_of_substructures > 1 else current_test_structure)] if ts.min_max_speed_printing is not None else ts.speed_printing[current_test_structure]
            ts.g.write('; --- testing the following printing speed value: {:.3f} mm/s'.format(current_printing_speed))
            ts.g.feed(current_printing_speed)
            coasting_distance = np.linspace(0, ts.coasting_distance, ts.number_of_lines)

            for current_line in range(0, ts.number_of_lines):
                ts.g.move(x=0,
                          y=-(ts.step_y/(2*ts.number_of_substructures) - coasting_distance[current_line]),
                          z=0,
                          extrude=True, extrusion_multiplier=ts.extrusion_multiplier[current_test_structure], coef_h=ts.coef_h[current_test_structure], coef_w=ts.coef_w[current_test_structure])
                ts.g.move(x=0,
                          y=-coasting_distance[current_line],
                          z=0,
                          extrude=False)

                output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(-ts.retraction_distance[current_substructure]) + "; retract the filament"
                ts.g.write(output)

                ts.g.move(x=0,
                          y=-ts.step_y/(2*ts.number_of_substructures),
                          z=0,
                          extrude=False)
                ts.g.move(x=-step_x,
                          y=0,
                          z=0,
                          extrude=False)

                if current_line != ts.number_of_lines:
                    ts.g.move(x=0,
                              y=+ts.step_y/ts.number_of_substructures,
                              z=0,
                              extrude=False)
                else:
                    ts.g.move(x=step_x * ts.number_of_lines,
                              y=0,
                              z=0,
                              extrude=False)

                output = "G1 F" + str(ts.retraction_speed * 60) + " E" + str(+ts.retraction_distance[current_test_structure]+ ts.retraction_restart_distance[current_test_structure]) + "; deretract the filament"
                ts.g.write(output)

    ts.g.write("; --- finish to print the test structure ---")
    ts.g.teardown()


    return