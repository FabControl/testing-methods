#!/usr/local/bin/python
"""
Mass Portal Feedstock Testing Suite
Test Report Generator

Usage:
    generate_report.py [json_path]
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
import json, os
from datetime import datetime
from CLI_helpers import *
from docopt import docopt

arguments = docopt(__doc__)
if arguments["json_path"]:
    json_path = arguments["json_path"]
else:
    json_path = "persistence.json"

with open(json_path, mode="r") as file:
    import_json_dict = json.load(file)

file_name = 'Test report for ' + import_json_dict["material"]["manufacturer"]+' '+import_json_dict["material"]["name"] + ' ' + str(import_json_dict["material"]["size_od"]) + ' mm'
report_name = 'Test report for ' + import_json_dict["material"]["manufacturer"]+' '+import_json_dict["material"]["name"] + ' Ø' + str(import_json_dict["material"]["size_od"]) + ' mm'

doc = SimpleDocTemplate(file_name + '.pdf',
                        pagesize=landscape(A4),
                        rightMargin=30,
                        leftMargin=25,
                        topMargin=30,
                        bottomMargin=18)

style_heading = ParagraphStyle(
        name='Bold',
        fontName='Times',
        fontSize=24)

style_text = ParagraphStyle(
        name='Normal',
        fontName='Times',
        fontSize=11)

elements = []

cwd = os.getcwd()

logo = cwd + '/MP-Logo-horiz-black.png'
im = Image(logo, 2.14*inch, 0.35*inch)
im.hAlign = 'LEFT'
elements.append(im)

elements.append(Paragraph(report_name, style=style_heading))
elements.append(Spacer(1, 0.5*inch))

datetime_info = "Report generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
main_info = "Aim for: " + import_json_dict["settings"]["aim"]
elements.append(Paragraph(main_info, style=style_text))
elements.append(Paragraph(datetime_info, style=style_text))
main_info = "Material: " + import_json_dict["material"]["name"]
elements.append(Paragraph(main_info, style=style_text))
main_info = "Manufacturer: " + import_json_dict["material"]["manufacturer"]
elements.append(Paragraph(main_info, style=style_text))
main_info = "Machine: " + import_json_dict["machine"]["manufacturer"] + " " + import_json_dict["machine"]["model"]+ ", SN: " + str(import_json_dict["machine"]["sn"])
elements.append(Paragraph(main_info, style=style_text))
main_info = "Nozzle: " + str(import_json_dict["machine"]["nozzle"]["size_id"]) + " mm, " + str(import_json_dict["machine"]["nozzle"]["metal"])
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
main_info = "Printbed temperature (raft): " + str(import_json_dict["settings"]["temperature_printbed_raft"]) + " degC"
elements.append(Paragraph(main_info, style=style_text))
main_info = "Path width (raft): " + str(import_json_dict["settings"]["path_width_raft"]) + " mm"
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
for dummy in range(import_json_dict["settings"]["number_of_test_structures"]):
    data.append("Tested values")
data.append("Selected parameter value")
data.append("Selected printing speed value (mm/s)")
data.append("Selected volumetric flow rate value (mm3/s)")
data = [data]

i = 1

for k in performed_tests:
    new_line = [str(i), k["test_name"], k["units"]]
    for dummy in k["tested_parameter_values"]:
        new_line.append(k["parameter_precision"].format(dummy))

    new_line.append(k["parameter_precision"].format(k["selected_parameter_value"]))
    new_line.append("{:.1f}".format(k["selected_speed_value"]))

    try:
        new_line.append("{:.3f}".format(k["selected_volumetric_flow_rate_value"]))
    except KeyError:
        pass
    data.append(new_line)
    i += 1

style = TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),
                    ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                    ('VALIGN',(0, 0),(-1,-1),'MIDDLE'),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ('SPAN',(3,0),(-4,0))
                    ])

colwidths = [20, 110, 50]
for dummy in range(import_json_dict["settings"]["number_of_test_structures"]):
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
# TODO to foresee: fields for comments Reinis
exclusive_write(json_path, json.dumps(import_json_dict, indent=4, sort_keys=False))