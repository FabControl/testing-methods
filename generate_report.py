#!/usr/local/bin/python
"""
FabControl Optimizer: Test Report Generator

Usage:
    generate_report.py <session_id>
"""
from io import BytesIO
import json
from datetime import *

import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, Frame, PageBreak, PageTemplate

from CLI_helpers import *
from Definitions import save_session_file_as
from paths import *
from get_test_info import get_test_info


def generate_report(import_json_dict: dict):
    session_id = import_json_dict["session"]["uid"]
    parameter_values_for_comments = get_test_info(import_json_dict)
    list_of_other_parameters = parameter_values_for_comments.other_parameters
    dict_of_other_parameters = dict()

    for other_parameter in list_of_other_parameters:
        dict_of_other_parameters[other_parameter.name] = ("{0} ".format(other_parameter.precision)+other_parameter.units).format(other_parameter.values)

    try:
        material_manufacturer = str(import_json_dict["material"]["manufacturer"]).strip() + " "
    except KeyError:
        material_manufacturer = str()
    try:
        material_id = " (batch: " + str(import_json_dict["material"]["id"]).strip() + ")"
    except KeyError:
        material_id = str()
    try:
        machine_sn = " (SN: " + str(import_json_dict["machine"]["sn"]).strip() + ")"
    except KeyError:
        machine_sn = str()
    try:
        machine_manufacturer = str(import_json_dict["machine"]["manufacturer"]).strip() + " "
    except KeyError:
        machine_manufacturer = str()
    try:
        nozzle_type = str(import_json_dict["machine"]["temperature_controllers"]["extruder"]["nozzle"]["type"]).strip() + "nozzle "
    except KeyError:
        nozzle_type = str()

    # Generate the title
    report_head = "Test report for " + str(import_json_dict["material"]["name"]) + ("from " + material_manufacturer if material_manufacturer else str()) + " Ø" + str(import_json_dict["material"]["size_od"]) + " mm"

    f = BytesIO()
    # get document template
    doc = SimpleDocTemplate(f,
                            pagesize=landscape(A4),
                            rightMargin=20,
                            leftMargin=20,
                            topMargin=30,
                            bottomMargin=20)

    font_small = 7

    # Define two styles
    style_heading = ParagraphStyle(name="Bold",
                                   fontName="Helvetica",
                                   fontSize=3*font_small)

    style_text = ParagraphStyle(name="Normal",
                                fontName="Helvetica",
                                fontSize=font_small)

    # Create element list
    elements = []

    # Add logo
    im = Image(logo_path, 2.14*inch, 0.35*inch)
    im.hAlign = "RIGHT"

    elements.append(im)
    elements.append(Paragraph(report_head, style=style_heading))
    elements.append(Spacer(1, 0.5*inch))

    main_info = []
    main_info_entry = "Report generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    main_info.append(main_info_entry)
    main_info_entry = "Tests performed by: " + import_json_dict["session"]["user_id"]
    main_info.append(main_info_entry)
    main_info_entry = "Target: " + str(import_json_dict["session"]["target"]).replace("_", " ")
    main_info.append(main_info_entry)
    main_info_entry = "Material: " + material_manufacturer + import_json_dict["material"]["name"] + material_id
    main_info.append(main_info_entry)

    if machine_sn.strip():
        main_info_entry = "3D Printer: " + machine_manufacturer + import_json_dict["machine"]["model"] + machine_sn
    else:
        if import_json_dict["machine"]["model"].strip():
            main_info_entry = "3D Printer: " + machine_manufacturer + import_json_dict["machine"]["model"]
        else:
            main_info_entry = "3D Printer: " + machine_manufacturer

    main_info.append(main_info_entry)
    main_info_entry = "Nozzle inner diameter: {:.2f}".format(import_json_dict["machine"]["temperature_controllers"]["extruder"]["nozzle"]["size_id"]) +  " mm"
    main_info.append(main_info_entry)

    all_test_numbers = []
    all_tested_parameters = []

    for test in import_json_dict["session"]["previous_tests"]:
        all_test_numbers.append(test["test_number"])
        all_tested_parameters.append(test["parameter_one_name"])
        all_tested_parameters.append(test["parameter_two_name"])
        try:
            all_tested_parameters.append(test["parameter_three_name"])
        except KeyError:
            pass

    for parameter in all_tested_parameters:
        if parameter in dict_of_other_parameters:
            del dict_of_other_parameters[parameter]

    for parameter in dict_of_other_parameters:
        main_info_entry = parameter.capitalize() + ": " + dict_of_other_parameters[parameter]
        main_info.append(main_info_entry)

    main_info_entry = "Critical overhang angle: " + "{:.1f}".format(import_json_dict["settings"]["critical_overhang_angle"]) + " deg"
    main_info.append(main_info_entry)

    unique_test_numbers = np.unique(all_test_numbers)
    indexes_of_last_occurrence = []

    for element in unique_test_numbers:
        index_of_last_occurrence = len(all_test_numbers) - all_test_numbers[::-1].index(element) - 1
        indexes_of_last_occurrence.append(index_of_last_occurrence)

    unique_test_numbers_last_occurrence = [all_test_numbers[i] for i in indexes_of_last_occurrence]

    consumed_filament = 0
    list_of_estimated_printing_time = []
    for dummy in import_json_dict["session"]["previous_tests"]:
        if dummy["executed"]:
            consumed_filament = consumed_filament + round(float(dummy["extruded_filament_mm"] or 0), 3)
            list_of_estimated_printing_time.append("00:15:00")  # TODO append(dummy["estimated_printing_time"])

    total_estimated_printing_time = timedelta()
    for estimated_time in list_of_estimated_printing_time:
        (h, m, s) = estimated_time.split(':')
        d = timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        total_estimated_printing_time += d

    main_info_entry = "Consumed filament: " + "{:.1f}".format(consumed_filament/1000) + " m"
    main_info.append(main_info_entry)
    main_info_entry = "Total estimated printing time: " + str(total_estimated_printing_time)
    main_info.append(main_info_entry)

    styles = getSampleStyleSheet()
    styles = styles["BodyText"]
    styles.wordWrap = "CJK"
    style_text = ParagraphStyle(name="Normal",
                                fontName="Helvetica",
                                fontSize=font_small)

    # Splitting the not tested data into three rows, and putting them into table1
    if len(main_info)%3 == 0:
        number_of_rows = int(len(main_info)/3)
    elif len(main_info)%3 == 1:
        number_of_rows = int((len(main_info)+2)/3)
    else:
        number_of_rows = int((len(main_info)+1)/3)

    table_data_1 = []

    for i in range(number_of_rows):
        left_entry = Paragraph(main_info[i],style_text)
        centre_entry = Paragraph(main_info[number_of_rows+i],style_text)
        try:
            right_entry = Paragraph(main_info[2*number_of_rows+i], style_text)
        except IndexError:
            right_entry = Paragraph("", style_text)

        table_data_1_entry = [left_entry, centre_entry, right_entry]
        table_data_1.append(table_data_1_entry)

    colwidths_1 = [250, 250, 250]
    table1 = Table(data=table_data_1, colWidths=colwidths_1, rowHeights=0.1*inch)
    elements.append(table1)
    elements.append(Spacer(1, 0.15*inch))

    # Preparing the header and putting it into table2
    performed_tests = filter(lambda x: x["executed"] is True, import_json_dict["session"]["previous_tests"])
    table_data_2 = [" ", "<b>Test name</b>", "<b>Parameters</b>", "<b>Units</b>"]
    for dummy in range(7):
        table_data_2.append("<b>Tested values</b>")
    table_data_2.append("<b>Selected value</b>")
    table_data_2.append("<b>Comments</b>")
    table_data_2 = [table_data_2]

    colwidths_2 = [20, 110, 105, 40]
    for dummy in range(7):
        colwidths_2.append(40)
    colwidths_2.append(45)
    colwidths_2.append(160)

    test_sequence_number = 1
    row_number = 0

    table_2_style = [("ALIGN", (0, 0), (-1, -1), "CENTER"),
                   ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                   ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                   ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                   ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                   ("SPAN", (4, 0), (-3, 0)),
                   ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey)]

    style = TableStyle(table_2_style)

    table_data_2 = [[Paragraph(cell, style_text) for cell in row] for row in table_data_2]
    table2 = Table(table_data_2, colwidths_2, rowHeights=0.4*inch)
    table2.setStyle(style)
    elements.append(table2)

    # Preparing the data and putting them into table3
    table_data_3 = []
    table_3_style = [("ALIGN", (0, 0), (-1, -1), "CENTER"),
                     ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                     ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                     ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                     ("BOX", (0, 0), (-1, -1), 0.25, colors.black)]

    row_number = 0

    for single_test in performed_tests:
        new_line = [str(test_sequence_number), single_test["test_name"], single_test["parameter_one_name"], single_test["parameter_one_units"]]
        for dummy in single_test["tested_parameter_one_values"]:
            new_line.append(single_test["parameter_one_precision"].format(dummy))
        new_line.append(single_test["parameter_one_precision"].format(single_test["selected_parameter_one_value"]))
        table_data_3.append(new_line)
        if single_test["comments"]:
            new_line.append(single_test["comments"])

        if single_test["tested_parameter_two_values"] is not None:
            row_number += 1
            new_line = ["", "", single_test["parameter_two_name"], single_test["parameter_two_units"]]
            for dummy in single_test["tested_parameter_two_values"]:
                new_line.append(single_test["parameter_two_precision"].format(dummy))

            spaces_to_skip = len(single_test["tested_parameter_one_values"])-len(single_test["tested_parameter_two_values"])
            for _ in range(spaces_to_skip):
                new_line.append("-")
            new_line.append(single_test["parameter_two_precision"].format(single_test["selected_parameter_two_value"]))
            new_line.append("-")
            table_data_3.append(new_line)

            if single_test["test_number"] in ("01", "02", "03", "04", "05", "06", "07", "09", "11", "13"):
                table_3_style.append(("SPAN", (0, row_number-1), (0, row_number)))
                table_3_style.append(("SPAN", (1, row_number-1), (1, row_number)))
                table_3_style.append(("SPAN", (12, row_number-1), (12, row_number)))

        if single_test["test_number"] == "08":
            row_number += 1
            new_line = ["", "", single_test["parameter_three_name"], single_test["parameter_three_units"]]
            for dummy in single_test["tested_parameter_three_values"]:
                new_line.append(single_test["parameter_three_precision"].format(dummy))

            spaces_to_skip = len(single_test["tested_parameter_one_values"])-len(single_test["tested_parameter_three_values"])
            for _ in range(spaces_to_skip):
                new_line.append("-")
            new_line.append(single_test["parameter_three_precision"].format(single_test["selected_parameter_three_value"]))
            new_line.append("-")

            table_data_3.append(new_line)
            table_3_style.append(("SPAN", (0, row_number), (0, row_number-2)))
            table_3_style.append(("SPAN", (1, row_number), (1, row_number-2)))
            table_3_style.append(("SPAN", (12, row_number), (12, row_number-2)))

        test_sequence_number += 1
        row_number += 1

    table_data_3 = [[Paragraph(cell, style_text) for cell in row] for row in table_data_3]
    table3 = Table(table_data_3, colwidths_2, rowHeights=0.2*inch)
    style = TableStyle(table_3_style)
    table3.setStyle(style)
    elements.append(table3)

    if "notes" in import_json_dict["session"]:
        elements.append(Spacer(1, 0.5 * inch))
        main_info = "Notes: {0}".format(str(import_json_dict["session"]["notes"]))
        elements.append(Paragraph(main_info, style=style_text))

    doc.build(elements)
    return f.getvalue()
