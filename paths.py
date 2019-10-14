import os

cwd = "/var/www/fc-testing-methods/"
if os.name == "nt":
    blender_path = "C:\Program Files\Blender Foundation\Blender\\blender.exe"
    slic3r_path = "C:\Program Files\Prusa3D\Slic3rPE\\slic3r-console.exe"

    font_path = cwd + "\\resources\\fonts\\Roboto-Thin.ttf"
    font_bold_path = cwd + "\\resources\\fonts\\Roboto-Bold.ttf"

    config_folder = cwd + "\\configs"
    raw_config_folder = cwd + "\\raw_config"
    gcode_folder = cwd + "\\gcodes"
    json_folder = cwd + "\\jsons"
    pdf_folder = cwd + "\\pdfs"
    png_folder = cwd + "\\pngs"
    stl_folder = cwd + "\\stls"

    logo_path = cwd + "\\resources\\logos\\FabControl_Optimizer_Left_bw.png"

    header = cwd + "\\resources\\header"
    footer = cwd + "\\resources\\footer"
    config_ini = cwd + "\\resources\\config.ini"
    cura_configuration_template = cwd + "\\resources\\cura_configuration_template"
    cura_deserialized = cura_configuration_template + "\\deserialized"
    cura_temp_folder = cura_configuration_template + "\\temp"
    simplify_config_fff = cwd + "\\resources\\simplify_config.fff"

    conversion_json = cwd + "\\resources\\conversion_w_cura.json"
    relational_dict_json = cwd + "\\resources\\relational_dict.json"
    target_overrides_json = cwd + "\\resources\\target_overrides.json"

else:
    blender_path = "blender"
    font_path = "resources/fonts/Roboto-Regular.ttf"
    font_bold_path = "resources/fonts/Roboto-Bold.ttf"
    slic3r_path = "slic3r"
    config_folder = "configs"
    raw_config_folder = "raw_config"
    gcode_folder = "gcodes"
    json_folder = "jsons"
    pdf_folder = "pdfs"
    png_folder = "pngs"
    stl_folder = "stls"

    logo_path = cwd + "/resources/logos/FabControl_Optimizer_Left_bw.png"

    header = cwd + "resources/header"
    footer = cwd + "resources/footer"
    config_ini = cwd + "resources/config.ini"
    cura_configuration_template = cwd + "/resources/cura_configuration_template"
    cura_deserialized = cura_configuration_template + "/deserialized"
    cura_temp_folder = cura_configuration_template + "/temp"
    simplify_config_fff = cwd + "/resources/simplify_config.fff"
    blank_persistance = cwd + "/resources/blank_persistence.json"
    blank_test_info = cwd + "/resources/blank_test_info.json"

    conversion_json = cwd + "/resources/conversion.json"
    relational_dict_json = cwd + "/resources/relational_dict.json"
    target_overrides_json = cwd + "/resources/target_overrides.json"

