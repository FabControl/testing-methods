import os

cwd = os.getcwd()

if os.name == "nt":
    blender_path = "C:\Program Files\Blender Foundation\Blender\\blender.exe"
    slic3r_path = "C:\Program Files\Prusa3D\Slic3rPE\\slic3r-console.exe"

    font_path = cwd + "\\resources\\fonts\\Roboto-Thin.ttf"
    font_bold_path = cwd + "\\resources\\fonts\\Roboto-Bold.ttf"

    config_folder = cwd + "\\configs"
    gcode_folder = cwd + "\\gcodes"
    json_folder = cwd + "\\jsons"
    pdf_folder = cwd + "\\pdfs"
    png_folder = cwd + "\\pngs"
    stl_folder = cwd + "\\stls"

    logo_path = cwd + "\\resources\\logos\\FabControl_Optimizer_Left_bw.png"

    header = cwd + "\\resources\\header"
    footer = cwd + "\\resources\\footer"
    config_ini = cwd + "\\resources\\config.ini"
    simplify_config_fff = cwd + "\\resources\\simplify_config.fff"

    conversion_json = cwd + "\\resources\\conversion.json"
    relational_dict_json = cwd + "\\resources\\relational_dict.json"
    target_overrides_json = cwd + "\\resources\\target_overrides.json"

else:
    blender_path = "blender"
    font_path = "/usr/share/fonts"
    slic3r_path = "slic3r"
    config_folder = "configs"
    gcode_folder = "gcodes"
    json_folder = "jsons"
    pdf_folder = "pdfs"
    png_folder = "pngs"
    stl_folder = "stls"
    header = "resources/header"
    footer = "resources/footer"
    blank_persistance = cwd + "/resources/blank_persistence.json"
    blank_test_info = cwd + "/resources/blank_test_info.json"
    config_ini = cwd + "/resources/config.ini"
    simplify_config_fff = cwd + "/resources/simplify_config.fff"
    conversion_json = cwd + "/resources/conversion.json"
    relational_dict_json = cwd + "/resources/relational_dict.json"
    target_overrides_json = cwd + "/resources/target_overrides.json"
    logo_path = cwd + "/resources/logos/FabControl_Optimizer_Left_bw.png"
