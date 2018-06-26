#!/usr/local/bin/python
"""
Mass Portal Feedstock Testing Suite
Test Report Generator

Usage:
    generate_report.py <session_id>
"""

import json
import os
from datetime import datetime

from docopt import docopt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image

from CLI_helpers import *
from Globals import filename
from paths import *

arguments = docopt(__doc__)
session_id = str(arguments["<session_id>"])

json_path = filename(cwd, session_id, "json")

with open(json_path, mode="r") as file:
    import_json_dict = json.load(file)

report_name = "Test report for " + import_json_dict["material"]["manufacturer"] + " " + import_json_dict["material"]["name"] + " Ø" + str(import_json_dict["material"]["size_od"]) + " mm"

doc = SimpleDocTemplate(filename(cwd, session_id, "pdf"),
                        pagesize=landscape(A4),
                        rightMargin=30,
                        leftMargin=25,
                        topMargin=30,
                        bottomMargin=18)

style_heading = ParagraphStyle(name="Bold",
                               fontName="Times",
                               fontSize=24)

style_text = ParagraphStyle(name="Normal",
                            fontName="Times",
                            fontSize=11)

elements = []
cwd = os.getcwd()

elements.append(Paragraph(report_name, style=style_heading))
im = Image(logo_path, 4.28*inch, 0.7*inch)
im.hAlign = "RIGHT"
elements.append(im)
elements.append(Spacer(1, 0.5*inch))

datetime_info = "Report generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
elements.append(Paragraph(datetime_info, style=style_text))
main_info = "Target: " + import_json_dict["session"]["target"]
elements.append(Paragraph(main_info, style=style_text))
main_info = "Material: " + import_json_dict["material"]["name"] + ", ID:" + import_json_dict["material"]["id"] if import_json_dict["material"]["id"] is not None else "Material: " + import_json_dict["material"]["name"]
elements.append(Paragraph(main_info, style=style_text))
main_info = "Manufacturer: " + import_json_dict["material"]["manufacturer"]
elements.append(Paragraph(main_info, style=style_text))
main_info = "Machine: " + import_json_dict["machine"]["manufacturer"] + " " + import_json_dict["machine"]["model"]+ ", SN: " + str(import_json_dict["machine"]["sn"])
elements.append(Paragraph(main_info, style=style_text))
main_info = "Nozzle: " + str(import_json_dict["machine"]["nozzle"]["size_id"]) + " mm, " + str(import_json_dict["machine"]["nozzle"]["type"])
elements.append(Paragraph(main_info, style=style_text))
main_info = "Part cooling: " + str(import_json_dict["settings"]["ventilator_part_cooling"]) + " %"
elements.append(Paragraph(main_info, style=style_text))
main_info = "Retraction distance: " + str(import_json_dict["settings"]["retraction_distance"]) + " mm"
elements.append(Paragraph(main_info, style=style_text))
main_info = "Retraction speed: " + str(import_json_dict["settings"]["retraction_speed"]) + " mm/s"
elements.append(Paragraph(main_info, style=style_text))
main_info = "Critical overhang angle: " + str(import_json_dict["settings"]["critical_overhang_angle"]) + " deg"
elements.append(Paragraph(main_info, style=style_text))
main_info = "Extruder temperature (raft): " + str(import_json_dict["settings"]["temperature_extruder_raft"]) + " degC"
elements.append(Paragraph(main_info, style=style_text))
main_info = "Track width (raft): " + str(import_json_dict["settings"]["track_width_raft"]) + " mm"
elements.append(Paragraph(main_info, style=style_text))
main_info = "Printbed temperature: " + str(import_json_dict["settings"]["temperature_printbed"]) + " degC"
elements.append(Paragraph(main_info, style=style_text))

consumed_filament = 0
for dummy in import_json_dict["session"]["previous_tests"]:
    consumed_filament = consumed_filament + round(float(dummy["extruded_filament"]), 3)
main_info = "Consumed filament: " + "{:.1f}".format(consumed_filament) + " mm"
elements.append(Paragraph(main_info, style=style_text))
elements.append(Spacer(1, 0.5*inch))

performed_tests = import_json_dict["session"]["previous_tests"]
data = [" ", "Test name", "Units"]
for dummy in range(import_json_dict["session"]["number_of_test_structures"]):
    data.append("Tested values")
data.append("Selected parameter value")
data.append("Selected printing-speed value (mm/s)")
data.append("Selected volumetric flow-rate value (mm3/s)")
data = [data]

i = 1

for single_test in performed_tests:
    new_line = [str(i), single_test["test_name"], single_test["units"]]
    for dummy in single_test["tested_parameter_values"]:
        new_line.append(single_test["parameter_precision"].format(dummy))

    new_line.append(single_test["parameter_precision"].format(single_test["selected_parameter_value"]))
    new_line.append("{:.1f}".format(single_test["selected_printing-speed_value"]))

    try:
        new_line.append("{:.3f}".format(single_test["selected_volumetric_flow-rate_value"]))
    except KeyError:
        pass
    data.append(new_line)
    i += 1

style = TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ("SPAN", (3, 0), (-4, 0))
                    ])

colwidths = [20, 110, 50]
for dummy in range(import_json_dict["session"]["number_of_test_structures"]):
    colwidths.append(45)
colwidths.append(80)
colwidths.append(80)
colwidths.append(80)

data2 = [[Paragraph(cell, style_text) for cell in row] for row in data]
t = Table(data2, colwidths)
t.setStyle(style)

# Send the data and build the file
elements.append(t)
doc.build(elements)
