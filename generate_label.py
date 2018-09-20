#!/usr/local/bin/python
"""
Mass Portal Feedstock Testing Suite
Label Generator
"""

from Globals import filename
from paths import *

from PIL import Image, ImageFont, ImageDraw


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

    box = (mbox[2] - 550, mbox[3] - 700)
    mimage.paste(simage, box)
    mimage.save(outfname)


def generate_label(import_json_dict):
    if import_json_dict["previous_tests"][-1]["executed"]:
        font_size = 25
        font_size_small = 20
        font = ImageFont.truetype(font_path, font_size)
        font_bold = ImageFont.truetype(font_bold_path, font_size)
        font_small = ImageFont.truetype(font_path, font_size_small)
        img = Image.new("RGBA", (696, 550), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        n = 0
        draw.text((0, n * font_size), "Session ID: {}, User ID: {}".format(import_json_dict["session"]["uid"],
                                                               import_json_dict["session"]["user_id"]), (0, 0, 0), font=font_bold)
        n += 1
        draw.text((0, n * font_size), "Feedstock material: {0} {1} (ID: {2}), {3} mm".format(import_json_dict["material"]["manufacturer"],
                                                                                             import_json_dict["material"]["name"],
                                                                                             import_json_dict["material"]["id"],
                                                                                             import_json_dict["material"]["size_od"]), (0, 0, 0), font=font)
        n += 1
        if import_json_dict["material"]["drying"]["dried"]:
            draw.text((0, n * font_size), "Feedstock material dried prior to printing: at {0} degC for {1} min".format(import_json_dict["material"]["drying"]["drying_temperature"],
                                                                                                    import_json_dict["material"]["drying"]["drying_time"]), (0, 0, 0), font=font)
        else:
            draw.text((0, n * font_size), "Feedstock material dried prior to printing: not dried", (0, 0, 0), font=font)
        n += 1
        draw.text((0, n*font_size), "3D printer: {} {} (SN: {})".format(import_json_dict["machine"]["manufacturer"],
                                                               import_json_dict["machine"]["model"],
                                                               import_json_dict["machine"]["sn"]), (0, 0, 0), font=font)
        n += 1
        draw.text((0, n*font_size), "Nozzle: {} mm {} nozzle".format(import_json_dict["machine"]["nozzle"]["size_id"],
                                                                    import_json_dict["machine"]["nozzle"]["type"]), (0, 0, 0), font=font)
        n += 1
        draw.text((0, n*font_size), "Tested parameter (units): {} ({})".format(import_json_dict["session"]["previous_tests"][-1]["test_name"],
                                                                              import_json_dict["session"]["previous_tests"][-1]["units"],
                                                                              import_json_dict["machine"]["nozzle"]["type"]), (0,0,0), font=font)
        n += 1
        draw.text((0, n*font_size), "Target: {}".format(import_json_dict["session"]["target"]), (0, 0, 0), font=font)
        n += 2

        horizontal_offset = 250
        square_size = 35

        for ind, parameter_value in enumerate(import_json_dict["session"]["previous_tests"][-1]["tested_parameter_values"]):
            draw.text((3.5*ind*font_size_small+150, n*font_size), import_json_dict["session"]["previous_tests"][-1]["parameter_precision"].format(parameter_value), (0, 0, 0), font=font_small)
        print(n)
        n += 2

        for printing_speed_ind in range(len(import_json_dict["session"]["previous_tests"][-1]["tested_printing-speed_values"])):
            parameter_value = import_json_dict["session"]["previous_tests"][-1]["tested_printing-speed_values"][printing_speed_ind]
            draw.text((10, 2*printing_speed_ind*square_size+n*font_size), "{} mm/s".format(parameter_value), (0, 0, 0), font=font_small)

            for parameter_ind in range(len(import_json_dict["session"]["previous_tests"][-1]["tested_parameter_values"])):
                draw.rectangle(((2*square_size*parameter_ind+6*font_size, 2*square_size*printing_speed_ind+horizontal_offset),
                                (square_size*(2*parameter_ind+1)+6*font_size, square_size*(2*printing_speed_ind+1)+horizontal_offset)), fill="white", outline="black")

        ImageDraw.Draw(img)

        label = img.rotate(angle=90, expand=True)
        label.save(filename(cwd, str(import_json_dict["session"]["uid"]), ".png"))
        add_logo(filename(cwd, str(import_json_dict["session"]["uid"]), ".png"), logo_path, filename(cwd, str(import_json_dict["session"]["uid"]), ".png"))
