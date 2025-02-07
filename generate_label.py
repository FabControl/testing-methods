#!/usr/local/bin/python
"""
FabControl Optimizer: Feedstock Material Testing
Label Generator
"""

from Definitions import save_session_file_as
from paths import *


from PIL import Image, ImageFont, ImageDraw
scale = 3

def add_logo(mfname, lfname, outfname):
    mimage = Image.open(mfname)
    limage = Image.open(lfname)
    limage = limage.rotate(angle=0, expand=True)

    wsize = int(min(mimage.size[0], mimage.size[1])*0.75)
    wpercent = (wsize/float(limage.size[0]))
    hsize = int((float(limage.size[1]) * float(wpercent)))

    simage = limage.resize((wsize, hsize))
    mbox = mimage.getbbox()
    sbox = simage.getbbox()

    box = (mbox[2] - scale*550, mbox[3] - scale*700)
    mimage.paste(simage, box)
    mimage.save(outfname)


def generate_label(import_json_dict):
    if import_json_dict["session"]["previous_tests"][-1]["executed"]:
        font_size = scale*20
        font_size_small = scale*15
        font = ImageFont.truetype(font_path, font_size)
        font_bold = ImageFont.truetype(font_bold_path, font_size)
        font_small_bold = ImageFont.truetype(font_bold_path, font_size_small)
        img = Image.new("RGBA", (scale*700, scale*550), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        try:
            material_name = str(import_json_dict["material"]["name"]).strip() + " "
        except KeyError:
            material_name = str()
        try:
            nozzle_size = str(import_json_dict["machine"]["temperature_controllers"]["extruder"]["nozzle"]["size_id"]).strip() + " mm"
        except KeyError:
            nozzle_size = str()
        try:
            nozzle_type = str(import_json_dict["machine"]["temperature_controllers"]["extruder"]["nozzle"]["type"]).strip() + "nozzle "
        except KeyError:
            nozzle_type = str()

        n = 0
        draw.text((0, n * font_size), "Session ID: {0}, User ID: {1}".format(import_json_dict["session"]["uid"],
                                                                             import_json_dict["session"]["user_id"]), (0, 0, 0), font=font_bold)
        n += 1
        draw.text((0, n * font_size), "G-code name: {0}".format(import_json_dict["session"]["previous_tests"][-1]["gcode_path"].split("gcodes")[-1].translate("\\//"), (0, 0, 0), font=font_bold))
        n += 1
        draw.text((0, n * font_size), "Feedstock material: {0}, {1} mm".format(material_name,
                                                                               import_json_dict["material"]["size_od"]), (0, 0, 0), font=font_bold)
        n += 1
        draw.text((0, n*font_size), "3D printer: {0}".format(str(import_json_dict["machine"]["model"])), (0, 0, 0), font=font_bold)
        n += 1
        if import_json_dict["machine"]["temperature_controllers"]["chamber"]["chamber_heatable"]:
            draw.text((0, n * font_size), "Build chamber temperature: {0} degC".format(import_json_dict["settings"]["temperature_chamber_setpoint"]), (0, 0, 0), font=font_bold)
            n += 1
        if import_json_dict["machine"]["temperature_controllers"]["extruder"]["part_cooling"]:
            draw.text((0, n * font_size), "Part cooling: {0} %".format(import_json_dict["settings"]["part_cooling_setpoint"]), (0, 0, 0), font=font_bold)
            n += 1

        draw.text((0, n*font_size), "Nozzle: {0}".format(nozzle_size+nozzle_type), (0, 0, 0), font=font_bold)
        n += 1
        draw.text((0, n*font_size), "Tested parameters: {0}".format(import_json_dict["session"]["previous_tests"][-1]["test_name"].replace("_", " ")), (0,0,0), font=font_bold)
        n += 1
        draw.text((0, n*font_size), "Target: {0}".format(import_json_dict["session"]["target"].replace("_", " ")), (0, 0, 0), font=font_bold)
        n += 2

        horizontal_offset = 130*scale
        square_size = 35*scale

        for ind, parameter_value in enumerate(import_json_dict["session"]["previous_tests"][-1]["tested_parameter_one_values"][::-1]):
            draw.text((5.25*ind*font_size_small+225, 1*n*font_size), str(import_json_dict["session"]["previous_tests"][-1]["parameter_one_precision"]+ " "+ import_json_dict["session"]["previous_tests"][-1]["parameter_one_units"]).format(parameter_value), (0, 0, 0), font=font_small_bold)
        n += 1

        if import_json_dict["session"]["previous_tests"][-1]["test_name"] == "printing speed":
            for parameter_ind in range(len(import_json_dict["session"]["previous_tests"][-1]["tested_parameter_one_values"])):
                draw.rectangle(((2*square_size*(1*parameter_ind+0)+4*font_size, 2*square_size + horizontal_offset),
                                (1*square_size*(2*parameter_ind+1)+4*font_size, 1*square_size + horizontal_offset)), fill="white", outline="black")
        else:
            if import_json_dict["session"]["previous_tests"][-1]["tested_parameter_two_values"]:
                for printing_speed_ind in range(len(import_json_dict["session"]["previous_tests"][-1]["tested_parameter_two_values"])):
                    parameter_value = import_json_dict["session"]["previous_tests"][-1]["tested_parameter_two_values"][printing_speed_ind]
                    draw.text((0, 2*printing_speed_ind*square_size+n*font_size), "{0} {1}".format(parameter_value, import_json_dict["session"]["previous_tests"][-1]["parameter_two_units"]), (0, 0, 0), font=font_small_bold)
                    for parameter_ind in range(len(import_json_dict["session"]["previous_tests"][-1]["tested_parameter_one_values"])):
                        draw.rectangle(((square_size*(2*parameter_ind+0)+6*font_size, square_size*(2*printing_speed_ind+2)+horizontal_offset),
                                        (square_size*(2*parameter_ind+1)+6*font_size, square_size*(2*printing_speed_ind+3)+horizontal_offset)), fill="white", outline="black")

        ImageDraw.Draw(img)

        label = img.rotate(angle=90, expand=True)
        label.save(save_session_file_as(str(import_json_dict["session"]["uid"]), ".png"))
        add_logo(save_session_file_as(str(import_json_dict["session"]["uid"]), ".png"), logo_path, save_session_file_as(str(import_json_dict["session"]["uid"]), ".png"))
