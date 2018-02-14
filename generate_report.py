#!/usr/local/bin/python

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, StyleSheet1
import json, os

with open("persistence.json", mode="r") as file:
    import_json_dict = json.load(file)


report_name = 'Test report for ' + import_json_dict["material"]["manufacturer"]+' '+import_json_dict["material"]["name"] + ' ' + str(import_json_dict["material"]["size_od"]) + 'mm'

doc = SimpleDocTemplate(report_name + '.pdf',
                        pagesize=A4,
                        rightMargin=30,
                        leftMargin=30,
                        topMargin=30,
                        bottomMargin=18)

heading_style = ParagraphStyle(
        name='Bold',
        fontName='Times',
        fontSize=24)

text_style = ParagraphStyle(
        name='Normal',
        fontName='Times',
        fontSize=11)

elements = []

cwd = os.getcwd()

logo = cwd + '/MP-Logo-horiz-black.png'
im = Image(logo, 1.5*inch, 0.35*inch)
im.hAlign = 'LEFT'
elements.append(im)

elements.append(Paragraph(report_name, style=heading_style))
elements.append(Spacer(1, 0.5*inch))

main_info = "Material: " + import_json_dict["material"]["name"]
elements.append(Paragraph(main_info, style=text_style))
main_info = "Manufacturer: " + import_json_dict["material"]["manufacturer"] + "\n"
elements.append(Paragraph(main_info, style=text_style))
elements.append(Spacer(1, 0.5*inch))

performed_tests = import_json_dict["session"]["previous_tests"]
data = [["Test number", "Test name", "Units", "Tested values", "Selected value"]]
i = 1

for k in performed_tests:
    new_line = [str(i), k["test_name"], k["units"], ", ".join("{:.3f}".format(dummy) for dummy in k["tested_values"]), str(k["selected_value"])]
    data.append(new_line)
    i += 1

style = TableStyle([
                       ('ALIGN',(0,0),(-1,-1),'CENTER'),
                       ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                       ('VALIGN',(0, 0),(-1,-1),'MIDDLE'),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])


# Configure style and word wrap
# s = getSampleStyleSheet()
# s = s["BodyText"]
# s.wordWrap = 'CJK'

colwidths = (75, 90, 60, 240, 60)
data2 = [[Paragraph(cell, text_style) for cell in row] for row in data]
t = Table(data2, colwidths)
t.setStyle(style)

# Send the data and build the file
elements.append(t)
doc.build(elements)