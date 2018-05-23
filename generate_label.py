#!/usr/local/bin/python
"""
Mass Portal Feedstock Testing Suite
Label Generator
"""

from Globals import filename
from paths import *

from PIL import Image, ImageFont, ImageDraw

def generate_label(import_json_dict):
    font_size = 25
    font_size_small = 20
    font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", font_size)
    font_bold = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", font_size)
    font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", font_size_small)
    img = Image.new("RGBA", (696,550), (255,255,255))
    draw = ImageDraw.Draw(img)

    draw.text((0,0), "Session ID: {}, User ID: {}".format(import_json_dict["session"]["uid"],
                                                          import_json_dict["session"]["user_id"]), (0,0,0), font=font_bold)

    draw.text((0,font_size), "Feedstock material: {} {} {} {}".format(import_json_dict["material"]["manufacturer"],
                                                                     import_json_dict["material"]["id"],
                                                                     import_json_dict["material"]["name"],
                                                                     import_json_dict["material"]["size_od"]), (0,0,0), font=font)

    draw.text((0,2*font_size), "3D printer: {} {} {}".format(import_json_dict["machine"]["manufacturer"],
                                                             import_json_dict["machine"]["model"],
                                                             import_json_dict["machine"]["sn"]), (0,0,0), font=font)

    draw.text((0,3*font_size), "Nozzle: {} mm {} nozzle".format(import_json_dict["machine"]["nozzle"]["size_id"],
                                                                import_json_dict["machine"]["nozzle"]["type"]), (0,0,0), font=font)

    draw.text((0,4*font_size), "Tested parameter (units): {} ({})".format(import_json_dict["session"]["previous_tests"][-1]["test_name"],
                                                                          import_json_dict["session"]["previous_tests"][-1]["units"],
                                                                          import_json_dict["machine"]["nozzle"]["type"]), (0,0,0), font=font)

    draw.text((0,5*font_size), "Target: {}".format(import_json_dict["session"]["target"]), (0,0,0), font=font)

    vertical_offset = 0
    horizontal_offset = 225
    square_size = 40

    for ind, parameter_value in enumerate(import_json_dict["session"]["previous_tests"][-1]["tested_parameter_values"]):
        draw.text((4*ind*font_size_small+125, 7*font_size), import_json_dict["session"]["previous_tests"][-1]["parameter_precision"].format(parameter_value), (0, 0, 0), font=font_small)

    for printing_speed_ind in range(len(import_json_dict["session"]["previous_tests"][-1]["tested_printing-speed_values"])):
        parameter_value = import_json_dict["session"]["previous_tests"][-1]["tested_printing-speed_values"][printing_speed_ind]
        draw.text((0, 2*printing_speed_ind*square_size+9*font_size), "{} mm/s".format(parameter_value), (0, 0, 0), font=font_small)

        for parameter_ind in range(len(import_json_dict["session"]["previous_tests"][-1]["tested_parameter_values"])):
            draw.rectangle(((2*square_size*parameter_ind+6*font_size, 2*square_size*printing_speed_ind+horizontal_offset),
                            (square_size*(2*parameter_ind+1)+6*font_size, square_size*(2*printing_speed_ind+1)+horizontal_offset)), fill="white", outline="black")

    ImageDraw.Draw(img)
    img.save(filename(cwd, str(import_json_dict["session"]["uid"]), ".png"))
