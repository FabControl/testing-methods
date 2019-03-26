#!/usr/local/bin/python
"""
FabControl Optimizer: Test Report Generator

Usage:
    generate_report.py <session_id>
"""

import json
from datetime import datetime

from docopt import docopt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, Frame, PageBreak, PageTemplate

from CLI_helpers import *
from Definitions import save_session_file_as
from paths import *

arguments = docopt(__doc__)
session_id = str(arguments["<session_id>"])

# from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Frame, Paragraph, PageBreak, PageTemplate
# from reportlab.lib.styles import getSampleStyleSheet
# import random
#
# words = "lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore et".split()
#
# styles=getSampleStyleSheet()
# Elements=[]
#
# doc = BaseDocTemplate('basedoc.pdf',showBoundary=1)

json_path = save_session_file_as(session_id, "json")

with open(json_path, mode="r") as file:
    import_json_dict = json.load(file)

report_head = "Test report for " + str(import_json_dict["material"]["manufacturer"]) + " " + str(import_json_dict["material"]["name"]) + " Ø" + str(import_json_dict["material"]["size_od"]) + " mm"


doc = SimpleDocTemplate(save_session_file_as(session_id, "pdf"),
                        pagesize=landscape(A4),
                        rightMargin=30,
                        leftMargin=25,
                        topMargin=30,
                        bottomMargin=18)

style_heading = ParagraphStyle(name="Bold",
                               fontName="Helvetica",
                               fontSize=24)

style_text = ParagraphStyle(name="Normal",
                            fontName="Helvetica",
                            fontSize=9)

elements = []

im = Image(logo_path, 4.28*inch, 0.7*inch)
im.hAlign = "RIGHT"
elements.append(im)
elements.append(Paragraph(report_head, style=style_heading))
elements.append(Spacer(1, 0.5*inch))

main_info = []
main_info_entry = "Report generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
main_info.append(main_info_entry)
main_info_entry = "Target: " + str(import_json_dict["session"]["target"]).replace("_", " ")
main_info.append(main_info_entry)
if import_json_dict["material"]["drying"]["dried"]:
    main_info_entry = "Material: " + import_json_dict["material"]["manufacturer"] + " " + import_json_dict["material"]["name"] + " (batch: " + str(import_json_dict["material"]["id"]) + "), dried at: " + str(import_json_dict["material"]["drying"]["drying_temperature"]) + " degC for " + str(import_json_dict["material"]["drying"]["drying_time"]) + " min"
else:
    main_info_entry = "Material: " + import_json_dict["material"]["manufacturer"] + " " + import_json_dict["material"]["name"] + " (batch: " + str(import_json_dict["material"]["id"]) + ")"
main_info.append(main_info_entry)
main_info_entry = "3D Printer: " + import_json_dict["machine"]["manufacturer"] + " " + import_json_dict["machine"]["model"]+ " (SN: " + str(import_json_dict["machine"]["sn"]) + ")"
main_info.append(main_info_entry)
main_info_entry = "Nozzle: " + "{:.2f}".format(import_json_dict["machine"]["temperature_controllers"]["extruder"]["nozzle"]["size_id"]) + " mm, " + str(import_json_dict["machine"]["temperature_controllers"]["extruder"]["nozzle"]["type"])
main_info.append(main_info_entry)
main_info_entry = "Part cooling: " + str(import_json_dict["settings"]["part_cooling_setpoint"]) + " %"
main_info.append(main_info_entry)
main_info_entry = "Retraction distance: " + "{:.2f}".format(import_json_dict["settings"]["retraction_distance"]) + " mm"
main_info.append(main_info_entry)
main_info_entry = "Retraction speed: " + "{:.1f}".format(import_json_dict["settings"]["retraction_speed"]) + " mm/s"
main_info.append(main_info_entry)
main_info_entry = "Critical overhang angle: " + "{:.1f}".format(import_json_dict["settings"]["critical_overhang_angle"]) + " deg"
main_info.append(main_info_entry)
main_info_entry = "Extruder temperature (first layer): " + "{:.0f}".format(import_json_dict["settings"]["temperature_extruder_raft"]) + " degC"
main_info.append(main_info_entry)

if import_json_dict["machine"]["temperature_controllers"]["printbed"]["printbed_heatable"]:
    main_info_entry = "Printbed temperature: " + "{:.0f}".format(import_json_dict["settings"]["temperature_printbed_setpoint"]) + " degC"
    main_info.append(main_info_entry)
if "first-layer track width" not in import_json_dict["session"]["previous_tests"]:
    main_info_entry = "Track width (first layer): " + "{:.2f}".format(import_json_dict["settings"]["track_width_raft"]) + " mm"
    main_info.append(main_info_entry)
if "track height" not in import_json_dict["session"]["previous_tests"]:
    main_info_entry = "Track height: " + "{:.2f}".format(import_json_dict["settings"]["track_height"]) + " mm"
    main_info.append(main_info_entry)
if "track width" not in import_json_dict["session"]["previous_tests"]:
    main_info_entry = "Track width: " + "{:.2f}".format(import_json_dict["settings"]["track_width"]) + " mm"
    main_info.append(main_info_entry)
if "extrusion multiplier" not in import_json_dict["session"]["previous_tests"]:
    main_info_entry = "Extrusion multiplier: " + "{:.2f}".format(import_json_dict["settings"]["extrusion_multiplier"])
    main_info.append(main_info_entry)

consumed_filament = 0
for dummy in import_json_dict["session"]["previous_tests"]:
    if dummy["executed"]:
        consumed_filament = consumed_filament + round(float(dummy["extruded_filament_mm"]), 3)
main_info_entry = "Consumed filament: " + "{:.1f}".format(consumed_filament) + " mm"
main_info.append(main_info_entry)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT

styles = getSampleStyleSheet()

style_text = ParagraphStyle(name="Normal",
                            fontName="Helvetica",
                            fontSize=9)

style_right = ParagraphStyle(name="right",
                             parent=styles["Normal"],
                             alignment=TA_RIGHT)

if len(main_info)%2 == 0:
    number_of_rows = int(len(main_info)/2)
else:
    number_of_rows = int((len(main_info)+1)/2)

table_data_1 = []

for i in range(number_of_rows):
    left_entry = Paragraph(main_info[i],style_text)
    try:
        right_entry = Paragraph(main_info[number_of_rows+i], style_text)
    except IndexError:
        right_entry = Paragraph("", style_text)

    table_data_1_entry = [left_entry, right_entry]
    table_data_1.append(table_data_1_entry)

colwidths_1 = [250, 250]
table1 = Table(table_data_1, colwidths_1)
elements.append(table1)
elements.append(Spacer(1, 0.5*inch))

performed_tests = filter(lambda x: x["executed"] is True, import_json_dict["session"]["previous_tests"])
table_data_2 = [" ", "Test name", "Parameters", "Units"]
for dummy in range(import_json_dict["session"]["number_of_test_structures"]):
    table_data_2.append("Tested values")
table_data_2.append("Selected parameter value")
table_data_2.append("Comments")
table_data_2 = [table_data_2]

test_sequence_number = 1
row_number = 0

table_2_style = [("ALIGN", (0, 0), (-1, -1), "CENTER"),
               ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
               ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
               ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
               ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
               ("SPAN", (4, 0), (-3, 0))]

for single_test in performed_tests:
    new_line = [str(test_sequence_number), single_test["test_name"], single_test["parameter_one_name"], single_test["parameter_one_units"]]
    for dummy in single_test["tested_parameter_one_values"]:
        new_line.append(single_test["parameter_one_precision"].format(dummy))
    new_line.append(single_test["parameter_one_precision"].format(single_test["selected_parameter_one_value"]))

    table_data_2.append(new_line)
    test_sequence_number += 1
    row_number += 1

    if single_test["tested_parameter_two_values"] is not None:
        new_line = ["", "", single_test["parameter_two_name"], single_test["parameter_two_units"]]
        for dummy in single_test["tested_parameter_two_values"]:
            new_line.append(single_test["parameter_two_precision"].format(dummy))

        spaces_to_skip = len(single_test["tested_parameter_one_values"])-len(single_test["tested_parameter_two_values"])
        for _ in range(spaces_to_skip):
            new_line.append("")
        new_line.append(single_test["parameter_two_precision"].format(single_test["selected_parameter_two_value"]))
        new_line.append("")
        table_data_2.append(new_line)
        row_number += 1

    if single_test["test_number"] in ("01", "02", "03", "04", "08", "13"):
        table_2_style.append(("SPAN", (0, row_number-1), (0, row_number)))
        table_2_style.append(("SPAN", (1, row_number-1), (1, row_number)))
        table_2_style.append(("SPAN", (12, row_number-1), (12, row_number)))


style = TableStyle(table_2_style)

colwidths_2 = [20, 110, 80, 45]
for dummy in range(import_json_dict["session"]["number_of_test_structures"]):
    colwidths_2.append(45)

colwidths_2.append(60)
colwidths_2.append(80)

table_data_2 = [[Paragraph(cell, style_text) for cell in row] for row in table_data_2]
table2 = Table(table_data_2, colwidths_2)
table2.setStyle(style)
elements.append(table2)

if "notes" in import_json_dict["session"]:
    elements.append(Spacer(1, 0.5 * inch))
    main_info = "Notes: {0}".format(str(import_json_dict["session"]["notes"]))
    elements.append(Paragraph(main_info, style=style_text))

doc.build(elements)
