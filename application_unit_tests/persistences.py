import json

BASE_PERSISTENCE_STRENGTH = '''
{
  "machine": {
    "model": "with offset",
    "buildarea_maxdim1": 0,
    "buildarea_maxdim2": 0,
    "form": "cartesian",
    "extruder_type": "bowden",
    "gcode_header": "This is header",
    "gcode_footer": "This is footer",
    "temperature_controllers": {
      "extruder": {
        "tool": "T0",
        "temperature_max": 350,
        "part_cooling": true,
        "nozzle": {
          "size_id": 0.4
        }
      },
      "chamber": {
        "tool": "",
        "gcode_command": "M141 S$temp",
        "temperature_max": 80,
        "chamber_heatable": false
      },
      "printbed": {
        "printbed_heatable": true,
        "temperature_max": 120
      }
    }
  },
  "material": {
    "size_od": 1.75,
    "name": "Mat"
  },
  "session": {
    "uid": 25,
    "target": "mechanical_strength",
    "test_number": "01",
    "min_max_parameter_one": [
      0.12,
      0.22
    ],
    "min_max_parameter_two": [
      5.0,
      20.0
    ],
    "min_max_parameter_three": [
      0,
      0
    ],
    "test_type": "A",
    "user_id": "Some One",
    "offset": [
      -500.00,
      50.00
    ],
    "slicer": "Prusa",
    "previous_tests": [
      {
        "comments": 0,
        "datetime_info": "2020-02-10 17:11:06",
        "executed": true,
        "extruded_filament_mm": 260.923,
        "parameter_one_name": "first-layer track height",
        "parameter_one_precision": "{:.2f}",
        "parameter_one_units": "mm",
        "parameter_three_name": null,
        "parameter_two_name": "first-layer printing speed",
        "parameter_two_precision": "{:.0f}",
        "parameter_two_units": "mm/s",
        "selected_parameter_one_value": 0,
        "selected_parameter_two_value": 0,
        "selected_volumetric_flow-rate_value": 0,
        "test_name": "first-layer track height vs first-layer printing speed",
        "test_number": "01",
        "tested_parameter_one_values": [
          0.12,
          0.14,
          0.15,
          0.17,
          0.19,
          0.2,
          0.22
        ],
        "tested_parameter_two_values": [
          5.0,
          10.0,
          15.0,
          20.0
        ],
        "tested_parameters": [
          {
            "active": true,
            "hint_active": "These seven values will be tested at four different <b>First-layer printing speeds</b> (see below). You can change the limiting values",
            "min_max": [
              0.04000000000000001,
              0.4
            ],
            "name": "first-layer track height",
            "precision": "{:.2f}",
            "programmatic_name": "track_height_raft",
            "units": "mm",
            "values": [
              0.12,
              0.13666666666666666,
              0.15333333333333332,
              0.16999999999999998,
              0.18666666666666665,
              0.2033333333333333,
              0.22
            ]
          },
          {
            "active": true,
            "hint_active": "Set the range to 5-15 mm/s for printing flexible materials, or to 10-30 mm/s for printing harder materials",
            "min_max": [
              1,
              140
            ],
            "name": "first-layer printing speed",
            "precision": "{:.0f}",
            "programmatic_name": "speed_printing_raft",
            "units": "mm/s",
            "values": [
              5.0,
              10.0,
              15.0,
              20.0
            ]
          }
        ],
        "tested_volumetric_flow-rate_values": [
          [
            0.225,
            0.253,
            0.281,
            0.309,
            0.336,
            0.362,
            0.388
          ],
          [
            0.449,
            0.507,
            0.563,
            0.618,
            0.672,
            0.725,
            0.776
          ],
          [
            0.674,
            0.76,
            0.844,
            0.927,
            1.008,
            1.087,
            1.164
          ],
          [
            0.898,
            1.013,
            1.126,
            1.236,
            1.344,
            1.449,
            1.552
          ]
        ],
        "validated": false
      }
    ]
  },
  "settings": {
    "speed_travel": 140,
    "raft_density": 100,
    "speed_printing_raft": 15,
    "track_height": 0.00,
    "track_height_raft": 0.24,
    "track_width": 0.40,
    "track_width_raft": 0.40,
    "extrusion_multiplier": 1.00,
    "temperature_extruder": 30,
    "temperature_extruder_raft": 30,
    "retraction_restart_distance": 0.00,
    "retraction_speed": 100,
    "retraction_distance": 0.00,
    "bridging_extrusion_multiplier": 1.0,
    "bridging_part_cooling": 0,
    "bridging_speed_printing": 0,
    "speed_printing": 0,
    "coasting_distance": 0.00,
    "critical_overhang_angle": 0,
    "temperature_printbed_setpoint": 30,
    "temperature_chamber_setpoint": 0,
    "part_cooling_setpoint": 0
  }
}
'''

PERSISTENCE_MIGRATIONS_STRENGTH = [
        # base persistence is used for first test
    {
      "deleted": [
      ],
      "overrides": [
      ]
    },
    {
      "deleted": [
        [
          "session",
          "min_max_parameter_two",
          1
        ]
      ],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 0.36
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 0.56
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "02"
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        }
      ]
    },
    {
      "deleted": [],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 30
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 51
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            1
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.39,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            2
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:14:47",
            "executed": True,
            "extruded_filament_mm": 1273.065,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0,
            "selected_parameter_two_value": 0,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion temperature vs printing speed",
            "test_number": "03",
            "tested_parameter_one_values": [
              30,
              34,
              37,
              40,
              44,
              48,
              51
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  30,
                  34,
                  37,
                  40,
                  44,
                  48,
                  51
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ]
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "03"
        },
        {
          "path": [
            "settings",
            "critical_overhang_angle"
          ],
          "value": 45
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "track_height"
          ],
          "value": 0.2
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        },
        {
          "path": [
            "settings",
            "track_width_raft"
          ],
          "value": 0.39
        }
      ]
    },
    {
      "deleted": [],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 0.07
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 0.29
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            1
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.39,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            2
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:14:47",
            "executed": True,
            "extruded_filament_mm": 1273.065,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 44,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion temperature vs printing speed",
            "test_number": "03",
            "tested_parameter_one_values": [
              30,
              34,
              37,
              40,
              44,
              48,
              51
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  30,
                  34,
                  37,
                  40,
                  44,
                  48,
                  51
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            3
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:15:28",
            "executed": True,
            "extruded_filament_mm": 1183.955,
            "parameter_one_name": "track height",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0,
            "selected_parameter_two_value": 0,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track height vs printing speed",
            "test_number": "04",
            "tested_parameter_one_values": [
              0.07,
              0.11,
              0.14,
              0.18,
              0.22,
              0.25,
              0.29
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four <b>Printing speeds</b>. You can change the limiting values",
                "min_max": [
                  0.04000000000000001,
                  0.4
                ],
                "name": "track height",
                "precision": "{:.2f}",
                "programmatic_name": "track_height",
                "units": "mm",
                "values": [
                  0.07,
                  0.10666666666666667,
                  0.1433333333333333,
                  0.18,
                  0.21666666666666662,
                  0.2533333333333333,
                  0.29
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ]
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "04"
        },
        {
          "path": [
            "settings",
            "critical_overhang_angle"
          ],
          "value": 45
        },
        {
          "path": [
            "settings",
            "speed_printing"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "temperature_extruder"
          ],
          "value": 44
        },
        {
          "path": [
            "settings",
            "track_height"
          ],
          "value": 0.2
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        },
        {
          "path": [
            "settings",
            "track_width_raft"
          ],
          "value": 0.39
        }
      ]
    },
    {
      "deleted": [
        [
          "session",
          "min_max_parameter_two",
          1
        ]
      ],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 0.36
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 0.44
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.39,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            2
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:14:47",
            "executed": True,
            "extruded_filament_mm": 1273.065,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 44,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion temperature vs printing speed",
            "test_number": "03",
            "tested_parameter_one_values": [
              30,
              34,
              37,
              40,
              44,
              48,
              51
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  30,
                  34,
                  37,
                  40,
                  44,
                  48,
                  51
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            3
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:15:28",
            "executed": True,
            "extruded_filament_mm": 1183.955,
            "parameter_one_name": "track height",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.11,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track height vs printing speed",
            "test_number": "04",
            "tested_parameter_one_values": [
              0.07,
              0.11,
              0.14,
              0.18,
              0.22,
              0.25,
              0.29
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four <b>Printing speeds</b>. You can change the limiting values",
                "min_max": [
                  0.04000000000000001,
                  0.4
                ],
                "name": "track height",
                "precision": "{:.2f}",
                "programmatic_name": "track_height",
                "units": "mm",
                "values": [
                  0.07,
                  0.10666666666666667,
                  0.1433333333333333,
                  0.18,
                  0.21666666666666662,
                  0.2533333333333333,
                  0.29
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            4
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:16:09",
            "executed": True,
            "extruded_filament_mm": 917.568,
            "parameter_one_name": "track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track width",
            "test_number": "05",
            "tested_parameter_one_values": [
              0.36,
              0.37,
              0.39,
              0.4,
              0.41,
              0.43,
              0.44
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width",
                "units": "mm",
                "values": [
                  0.36,
                  0.3733333333333333,
                  0.38666666666666666,
                  0.4,
                  0.41333333333333333,
                  0.42666666666666664,
                  0.44
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.37,
                0.385,
                0.399,
                0.414,
                0.429,
                0.443,
                0.458
              ]
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "05"
        },
        {
          "path": [
            "settings",
            "critical_overhang_angle"
          ],
          "value": 29
        },
        {
          "path": [
            "settings",
            "speed_printing"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "temperature_extruder"
          ],
          "value": 44
        },
        {
          "path": [
            "settings",
            "track_height"
          ],
          "value": 0.11
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        },
        {
          "path": [
            "settings",
            "track_width_raft"
          ],
          "value": 0.39
        }
      ]
    },
    {
      "deleted": [
        [
          "session",
          "min_max_parameter_two",
          1
        ]
      ],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 0.8
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 1.4
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.39,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            2
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:14:47",
            "executed": True,
            "extruded_filament_mm": 1273.065,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 44,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion temperature vs printing speed",
            "test_number": "03",
            "tested_parameter_one_values": [
              30,
              34,
              37,
              40,
              44,
              48,
              51
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  30,
                  34,
                  37,
                  40,
                  44,
                  48,
                  51
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            3
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:15:28",
            "executed": True,
            "extruded_filament_mm": 1183.955,
            "parameter_one_name": "track height",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.11,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track height vs printing speed",
            "test_number": "04",
            "tested_parameter_one_values": [
              0.07,
              0.11,
              0.14,
              0.18,
              0.22,
              0.25,
              0.29
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four <b>Printing speeds</b>. You can change the limiting values",
                "min_max": [
                  0.04000000000000001,
                  0.4
                ],
                "name": "track height",
                "precision": "{:.2f}",
                "programmatic_name": "track_height",
                "units": "mm",
                "values": [
                  0.07,
                  0.10666666666666667,
                  0.1433333333333333,
                  0.18,
                  0.21666666666666662,
                  0.2533333333333333,
                  0.29
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            4
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:16:09",
            "executed": True,
            "extruded_filament_mm": 917.568,
            "parameter_one_name": "track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.43,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track width",
            "test_number": "05",
            "tested_parameter_one_values": [
              0.36,
              0.37,
              0.39,
              0.4,
              0.41,
              0.43,
              0.44
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width",
                "units": "mm",
                "values": [
                  0.36,
                  0.3733333333333333,
                  0.38666666666666666,
                  0.4,
                  0.41333333333333333,
                  0.42666666666666664,
                  0.44
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.37,
                0.385,
                0.399,
                0.414,
                0.429,
                0.443,
                0.458
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            5
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:17:56",
            "executed": True,
            "extruded_filament_mm": 1009.607,
            "parameter_one_name": "extrusion multiplier",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "-",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion multiplier vs printing speed",
            "test_number": "06",
            "tested_parameter_one_values": [
              0.8,
              0.9,
              1,
              1.1,
              1.2,
              1.3,
              1.4
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.01,
                  2
                ],
                "name": "extrusion multiplier",
                "precision": "{:.3f}",
                "programmatic_name": "extrusion_multiplier",
                "units": "-",
                "values": [
                  0.8,
                  0.9,
                  1,
                  1.1,
                  1.2,
                  1.2999999999999998,
                  1.4
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.358,
                0.402,
                0.447,
                0.492,
                0.536,
                0.581,
                0.626
              ]
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "06"
        },
        {
          "path": [
            "settings",
            "critical_overhang_angle"
          ],
          "value": 27
        },
        {
          "path": [
            "settings",
            "retraction_distance"
          ],
          "value": 4
        },
        {
          "path": [
            "settings",
            "speed_printing"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "temperature_extruder"
          ],
          "value": 44
        },
        {
          "path": [
            "settings",
            "track_height"
          ],
          "value": 0.11
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        },
        {
          "path": [
            "settings",
            "track_width"
          ],
          "value": 0.43
        },
        {
          "path": [
            "settings",
            "track_width_raft"
          ],
          "value": 0.39
        }
      ]
    },
    {
      "deleted": [
        [
          "session",
          "min_max_parameter_two",
          1
        ]
      ],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.39,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            2
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:14:47",
            "executed": True,
            "extruded_filament_mm": 1273.065,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 44,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion temperature vs printing speed",
            "test_number": "03",
            "tested_parameter_one_values": [
              30,
              34,
              37,
              40,
              44,
              48,
              51
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  30,
                  34,
                  37,
                  40,
                  44,
                  48,
                  51
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            3
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:15:28",
            "executed": True,
            "extruded_filament_mm": 1183.955,
            "parameter_one_name": "track height",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.11,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track height vs printing speed",
            "test_number": "04",
            "tested_parameter_one_values": [
              0.07,
              0.11,
              0.14,
              0.18,
              0.22,
              0.25,
              0.29
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four <b>Printing speeds</b>. You can change the limiting values",
                "min_max": [
                  0.04000000000000001,
                  0.4
                ],
                "name": "track height",
                "precision": "{:.2f}",
                "programmatic_name": "track_height",
                "units": "mm",
                "values": [
                  0.07,
                  0.10666666666666667,
                  0.1433333333333333,
                  0.18,
                  0.21666666666666662,
                  0.2533333333333333,
                  0.29
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            4
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:16:09",
            "executed": True,
            "extruded_filament_mm": 917.568,
            "parameter_one_name": "track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.43,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track width",
            "test_number": "05",
            "tested_parameter_one_values": [
              0.36,
              0.37,
              0.39,
              0.4,
              0.41,
              0.43,
              0.44
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width",
                "units": "mm",
                "values": [
                  0.36,
                  0.3733333333333333,
                  0.38666666666666666,
                  0.4,
                  0.41333333333333333,
                  0.42666666666666664,
                  0.44
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.37,
                0.385,
                0.399,
                0.414,
                0.429,
                0.443,
                0.458
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            5
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:17:56",
            "executed": True,
            "extruded_filament_mm": 1009.607,
            "parameter_one_name": "extrusion multiplier",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "-",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.9,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion multiplier vs printing speed",
            "test_number": "06",
            "tested_parameter_one_values": [
              0.8,
              0.9,
              1,
              1.1,
              1.2,
              1.3,
              1.4
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.01,
                  2
                ],
                "name": "extrusion multiplier",
                "precision": "{:.3f}",
                "programmatic_name": "extrusion_multiplier",
                "units": "-",
                "values": [
                  0.8,
                  0.9,
                  1,
                  1.1,
                  1.2,
                  1.2999999999999998,
                  1.4
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.358,
                0.402,
                0.447,
                0.492,
                0.536,
                0.581,
                0.626
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            6
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:18:33",
            "executed": True,
            "extruded_filament_mm": 862.732,
            "parameter_one_name": "printing speed",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "mm/s",
            "parameter_three_name": None,
            "parameter_two_name": None,
            "parameter_two_precision": None,
            "parameter_two_units": None,
            "selected_parameter_one_value": 0,
            "selected_parameter_two_value": None,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "printing speed",
            "test_number": "07",
            "tested_parameter_one_values": [
              10,
              10,
              10,
              10,
              10,
              10,
              10
            ],
            "tested_parameter_two_values": None,
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested while all other processing parameters are constant. You can change the limiting values",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10,
                  10,
                  10,
                  10
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": None,
                "name": None,
                "precision": None,
                "programmatic_name": None,
                "units": None,
                "values": []
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "07"
        },
        {
          "path": [
            "settings",
            "critical_overhang_angle"
          ],
          "value": 27
        },
        {
          "path": [
            "settings",
            "extrusion_multiplier"
          ],
          "value": 0.9
        },
        {
          "path": [
            "settings",
            "retraction_distance"
          ],
          "value": 4
        },
        {
          "path": [
            "settings",
            "speed_printing"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "temperature_extruder"
          ],
          "value": 44
        },
        {
          "path": [
            "settings",
            "track_height"
          ],
          "value": 0.11
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        },
        {
          "path": [
            "settings",
            "track_width"
          ],
          "value": 0.43
        },
        {
          "path": [
            "settings",
            "track_width_raft"
          ],
          "value": 0.39
        }
      ]
    },
    {
      "deleted": [],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 39
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 49
        },
        {
          "path": [
            "session",
            "min_max_parameter_three",
            0
          ],
          "value": 60
        },
        {
          "path": [
            "session",
            "min_max_parameter_three",
            1
          ],
          "value": 120
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 0
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            1
          ],
          "value": 6
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.39,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            2
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:14:47",
            "executed": True,
            "extruded_filament_mm": 1273.065,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 44,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion temperature vs printing speed",
            "test_number": "03",
            "tested_parameter_one_values": [
              30,
              34,
              37,
              40,
              44,
              48,
              51
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  30,
                  34,
                  37,
                  40,
                  44,
                  48,
                  51
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            3
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:15:28",
            "executed": True,
            "extruded_filament_mm": 1183.955,
            "parameter_one_name": "track height",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.11,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track height vs printing speed",
            "test_number": "04",
            "tested_parameter_one_values": [
              0.07,
              0.11,
              0.14,
              0.18,
              0.22,
              0.25,
              0.29
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four <b>Printing speeds</b>. You can change the limiting values",
                "min_max": [
                  0.04000000000000001,
                  0.4
                ],
                "name": "track height",
                "precision": "{:.2f}",
                "programmatic_name": "track_height",
                "units": "mm",
                "values": [
                  0.07,
                  0.10666666666666667,
                  0.1433333333333333,
                  0.18,
                  0.21666666666666662,
                  0.2533333333333333,
                  0.29
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            4
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:16:09",
            "executed": True,
            "extruded_filament_mm": 917.568,
            "parameter_one_name": "track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.43,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track width",
            "test_number": "05",
            "tested_parameter_one_values": [
              0.36,
              0.37,
              0.39,
              0.4,
              0.41,
              0.43,
              0.44
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width",
                "units": "mm",
                "values": [
                  0.36,
                  0.3733333333333333,
                  0.38666666666666666,
                  0.4,
                  0.41333333333333333,
                  0.42666666666666664,
                  0.44
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.37,
                0.385,
                0.399,
                0.414,
                0.429,
                0.443,
                0.458
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            5
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:17:56",
            "executed": True,
            "extruded_filament_mm": 1009.607,
            "parameter_one_name": "extrusion multiplier",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "-",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.9,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion multiplier vs printing speed",
            "test_number": "06",
            "tested_parameter_one_values": [
              0.8,
              0.9,
              1,
              1.1,
              1.2,
              1.3,
              1.4
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.01,
                  2
                ],
                "name": "extrusion multiplier",
                "precision": "{:.3f}",
                "programmatic_name": "extrusion_multiplier",
                "units": "-",
                "values": [
                  0.8,
                  0.9,
                  1,
                  1.1,
                  1.2,
                  1.2999999999999998,
                  1.4
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.358,
                0.402,
                0.447,
                0.492,
                0.536,
                0.581,
                0.626
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            6
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:18:33",
            "executed": True,
            "extruded_filament_mm": 862.732,
            "parameter_one_name": "printing speed",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "mm/s",
            "parameter_three_name": None,
            "parameter_two_name": None,
            "parameter_two_precision": None,
            "parameter_two_units": None,
            "selected_parameter_one_value": 10,
            "selected_parameter_two_value": None,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "printing speed",
            "test_number": "07",
            "tested_parameter_one_values": [
              10,
              10,
              10,
              10,
              10,
              10,
              10
            ],
            "tested_parameter_two_values": None,
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested while all other processing parameters are constant. You can change the limiting values",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10,
                  10,
                  10,
                  10
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": None,
                "name": None,
                "precision": None,
                "programmatic_name": None,
                "units": None,
                "values": []
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            7
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:04",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": "retraction speed",
            "parameter_three_precision": "{:.0f}",
            "parameter_three_units": "mm/s",
            "parameter_two_name": "retraction distance",
            "parameter_two_precision": "{:.3f}",
            "parameter_two_units": "mm",
            "selected_parameter_one_value": 0,
            "selected_parameter_three_value": 0,
            "selected_parameter_two_value": 0,
            "selected_volumetric_flow-rate_value": 0.447,
            "test_name": "extrusion temperature vs retraction distance",
            "test_number": "08",
            "tested_parameter_one_values": [
              39,
              41,
              42,
              44,
              46,
              47,
              49
            ],
            "tested_parameter_three_values": [
              60,
              120
            ],
            "tested_parameter_two_values": [
              0,
              2,
              4,
              6
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Retraction distances</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  39,
                  40.666666666666664,
                  42.333333333333336,
                  44,
                  45.666666666666664,
                  47.333333333333336,
                  49
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range of <b>Retraction distances</b> to be tested",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  2,
                  4,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "retraction speed",
                "precision": "{:.0f}",
                "programmatic_name": "retraction_speed",
                "units": "mm/s",
                "values": [
                  60,
                  120
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.447
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "08"
        },
        {
          "path": [
            "settings",
            "critical_overhang_angle"
          ],
          "value": 27
        },
        {
          "path": [
            "settings",
            "extrusion_multiplier"
          ],
          "value": 0.9
        },
        {
          "path": [
            "settings",
            "retraction_distance"
          ],
          "value": 4
        },
        {
          "path": [
            "settings",
            "speed_printing"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "temperature_extruder"
          ],
          "value": 44
        },
        {
          "path": [
            "settings",
            "track_height"
          ],
          "value": 0.11
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        },
        {
          "path": [
            "settings",
            "track_width"
          ],
          "value": 0.43
        },
        {
          "path": [
            "settings",
            "track_width_raft"
          ],
          "value": 0.39
        }
      ]
    },
    {
      "deleted": [],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 0
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 6
        },
        {
          "path": [
            "session",
            "min_max_parameter_three",
            0
          ],
          "value": 60
        },
        {
          "path": [
            "session",
            "min_max_parameter_three",
            1
          ],
          "value": 120
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            1
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.39,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            2
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:14:47",
            "executed": True,
            "extruded_filament_mm": 1273.065,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 44,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion temperature vs printing speed",
            "test_number": "03",
            "tested_parameter_one_values": [
              30,
              34,
              37,
              40,
              44,
              48,
              51
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  30,
                  34,
                  37,
                  40,
                  44,
                  48,
                  51
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            3
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:15:28",
            "executed": True,
            "extruded_filament_mm": 1183.955,
            "parameter_one_name": "track height",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.11,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track height vs printing speed",
            "test_number": "04",
            "tested_parameter_one_values": [
              0.07,
              0.11,
              0.14,
              0.18,
              0.22,
              0.25,
              0.29
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four <b>Printing speeds</b>. You can change the limiting values",
                "min_max": [
                  0.04000000000000001,
                  0.4
                ],
                "name": "track height",
                "precision": "{:.2f}",
                "programmatic_name": "track_height",
                "units": "mm",
                "values": [
                  0.07,
                  0.10666666666666667,
                  0.1433333333333333,
                  0.18,
                  0.21666666666666662,
                  0.2533333333333333,
                  0.29
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            4
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:16:09",
            "executed": True,
            "extruded_filament_mm": 917.568,
            "parameter_one_name": "track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.43,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track width",
            "test_number": "05",
            "tested_parameter_one_values": [
              0.36,
              0.37,
              0.39,
              0.4,
              0.41,
              0.43,
              0.44
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width",
                "units": "mm",
                "values": [
                  0.36,
                  0.3733333333333333,
                  0.38666666666666666,
                  0.4,
                  0.41333333333333333,
                  0.42666666666666664,
                  0.44
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.37,
                0.385,
                0.399,
                0.414,
                0.429,
                0.443,
                0.458
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            5
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:17:56",
            "executed": True,
            "extruded_filament_mm": 1009.607,
            "parameter_one_name": "extrusion multiplier",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "-",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.9,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion multiplier vs printing speed",
            "test_number": "06",
            "tested_parameter_one_values": [
              0.8,
              0.9,
              1,
              1.1,
              1.2,
              1.3,
              1.4
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.01,
                  2
                ],
                "name": "extrusion multiplier",
                "precision": "{:.3f}",
                "programmatic_name": "extrusion_multiplier",
                "units": "-",
                "values": [
                  0.8,
                  0.9,
                  1,
                  1.1,
                  1.2,
                  1.2999999999999998,
                  1.4
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.358,
                0.402,
                0.447,
                0.492,
                0.536,
                0.581,
                0.626
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            6
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:18:33",
            "executed": True,
            "extruded_filament_mm": 862.732,
            "parameter_one_name": "printing speed",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "mm/s",
            "parameter_three_name": None,
            "parameter_two_name": None,
            "parameter_two_precision": None,
            "parameter_two_units": None,
            "selected_parameter_one_value": 10,
            "selected_parameter_two_value": None,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "printing speed",
            "test_number": "07",
            "tested_parameter_one_values": [
              10,
              10,
              10,
              10,
              10,
              10,
              10
            ],
            "tested_parameter_two_values": None,
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested while all other processing parameters are constant. You can change the limiting values",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10,
                  10,
                  10,
                  10
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": None,
                "name": None,
                "precision": None,
                "programmatic_name": None,
                "units": None,
                "values": []
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            7
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:04",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": "retraction speed",
            "parameter_three_precision": "{:.0f}",
            "parameter_three_units": "mm/s",
            "parameter_two_name": "retraction distance",
            "parameter_two_precision": "{:.3f}",
            "parameter_two_units": "mm",
            "selected_parameter_one_value": 47,
            "selected_parameter_three_value": 103,
            "selected_parameter_two_value": 2,
            "selected_volumetric_flow-rate_value": 0.447,
            "test_name": "extrusion temperature vs retraction distance",
            "test_number": "08",
            "tested_parameter_one_values": [
              39,
              41,
              42,
              44,
              46,
              47,
              49
            ],
            "tested_parameter_three_values": [
              60,
              120
            ],
            "tested_parameter_two_values": [
              0,
              2,
              4,
              6
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Retraction distances</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  39,
                  40.666666666666664,
                  42.333333333333336,
                  44,
                  45.666666666666664,
                  47.333333333333336,
                  49
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range of <b>Retraction distances</b> to be tested",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  2,
                  4,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "retraction speed",
                "precision": "{:.0f}",
                "programmatic_name": "retraction_speed",
                "units": "mm/s",
                "values": [
                  60,
                  120
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.447
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            8
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:34",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "retraction distance",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0,
            "selected_parameter_two_value": 0,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "retraction distance vs printing speed",
            "test_number": "09",
            "tested_parameter_one_values": [
              0,
              1,
              2,
              3,
              4,
              5,
              6
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ]
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "09"
        },
        {
          "path": [
            "settings",
            "critical_overhang_angle"
          ],
          "value": 27
        },
        {
          "path": [
            "settings",
            "extrusion_multiplier"
          ],
          "value": 0.9
        },
        {
          "path": [
            "settings",
            "retraction_distance"
          ],
          "value": 2
        },
        {
          "path": [
            "settings",
            "retraction_speed"
          ],
          "value": 103
        },
        {
          "path": [
            "settings",
            "speed_printing"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "temperature_extruder"
          ],
          "value": 47
        },
        {
          "path": [
            "settings",
            "track_height"
          ],
          "value": 0.11
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        },
        {
          "path": [
            "settings",
            "track_width"
          ],
          "value": 0.43
        },
        {
          "path": [
            "settings",
            "track_width_raft"
          ],
          "value": 0.39
        }
      ]
    },
    {
      "deleted": [],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 0
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 6
        },
        {
          "path": [
            "session",
            "min_max_parameter_three",
            0
          ],
          "value": 60
        },
        {
          "path": [
            "session",
            "min_max_parameter_three",
            1
          ],
          "value": 120
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            1
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.39,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            2
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:14:47",
            "executed": True,
            "extruded_filament_mm": 1273.065,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 44,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion temperature vs printing speed",
            "test_number": "03",
            "tested_parameter_one_values": [
              30,
              34,
              37,
              40,
              44,
              48,
              51
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  30,
                  34,
                  37,
                  40,
                  44,
                  48,
                  51
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            3
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:15:28",
            "executed": True,
            "extruded_filament_mm": 1183.955,
            "parameter_one_name": "track height",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.11,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track height vs printing speed",
            "test_number": "04",
            "tested_parameter_one_values": [
              0.07,
              0.11,
              0.14,
              0.18,
              0.22,
              0.25,
              0.29
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four <b>Printing speeds</b>. You can change the limiting values",
                "min_max": [
                  0.04000000000000001,
                  0.4
                ],
                "name": "track height",
                "precision": "{:.2f}",
                "programmatic_name": "track_height",
                "units": "mm",
                "values": [
                  0.07,
                  0.10666666666666667,
                  0.1433333333333333,
                  0.18,
                  0.21666666666666662,
                  0.2533333333333333,
                  0.29
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            4
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:16:09",
            "executed": True,
            "extruded_filament_mm": 917.568,
            "parameter_one_name": "track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.43,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track width",
            "test_number": "05",
            "tested_parameter_one_values": [
              0.36,
              0.37,
              0.39,
              0.4,
              0.41,
              0.43,
              0.44
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width",
                "units": "mm",
                "values": [
                  0.36,
                  0.3733333333333333,
                  0.38666666666666666,
                  0.4,
                  0.41333333333333333,
                  0.42666666666666664,
                  0.44
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.37,
                0.385,
                0.399,
                0.414,
                0.429,
                0.443,
                0.458
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            5
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:17:56",
            "executed": True,
            "extruded_filament_mm": 1009.607,
            "parameter_one_name": "extrusion multiplier",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "-",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.9,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion multiplier vs printing speed",
            "test_number": "06",
            "tested_parameter_one_values": [
              0.8,
              0.9,
              1,
              1.1,
              1.2,
              1.3,
              1.4
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.01,
                  2
                ],
                "name": "extrusion multiplier",
                "precision": "{:.3f}",
                "programmatic_name": "extrusion_multiplier",
                "units": "-",
                "values": [
                  0.8,
                  0.9,
                  1,
                  1.1,
                  1.2,
                  1.2999999999999998,
                  1.4
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.358,
                0.402,
                0.447,
                0.492,
                0.536,
                0.581,
                0.626
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            6
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:18:33",
            "executed": True,
            "extruded_filament_mm": 862.732,
            "parameter_one_name": "printing speed",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "mm/s",
            "parameter_three_name": None,
            "parameter_two_name": None,
            "parameter_two_precision": None,
            "parameter_two_units": None,
            "selected_parameter_one_value": 10,
            "selected_parameter_two_value": None,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "printing speed",
            "test_number": "07",
            "tested_parameter_one_values": [
              10,
              10,
              10,
              10,
              10,
              10,
              10
            ],
            "tested_parameter_two_values": None,
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested while all other processing parameters are constant. You can change the limiting values",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10,
                  10,
                  10,
                  10
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": None,
                "name": None,
                "precision": None,
                "programmatic_name": None,
                "units": None,
                "values": []
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            7
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:04",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": "retraction speed",
            "parameter_three_precision": "{:.0f}",
            "parameter_three_units": "mm/s",
            "parameter_two_name": "retraction distance",
            "parameter_two_precision": "{:.3f}",
            "parameter_two_units": "mm",
            "selected_parameter_one_value": 47,
            "selected_parameter_three_value": 103,
            "selected_parameter_two_value": 2,
            "selected_volumetric_flow-rate_value": 0.447,
            "test_name": "extrusion temperature vs retraction distance",
            "test_number": "08",
            "tested_parameter_one_values": [
              39,
              41,
              42,
              44,
              46,
              47,
              49
            ],
            "tested_parameter_three_values": [
              60,
              120
            ],
            "tested_parameter_two_values": [
              0,
              2,
              4,
              6
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Retraction distances</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  39,
                  40.666666666666664,
                  42.333333333333336,
                  44,
                  45.666666666666664,
                  47.333333333333336,
                  49
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range of <b>Retraction distances</b> to be tested",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  2,
                  4,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "retraction speed",
                "precision": "{:.0f}",
                "programmatic_name": "retraction_speed",
                "units": "mm/s",
                "values": [
                  60,
                  120
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.447
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            8
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:34",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "retraction distance",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 1,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "retraction distance vs printing speed",
            "test_number": "09",
            "tested_parameter_one_values": [
              0,
              1,
              2,
              3,
              4,
              5,
              6
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            9
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:56",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "retraction distance",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": None,
            "parameter_two_precision": None,
            "parameter_two_units": None,
            "selected_parameter_one_value": 0,
            "selected_parameter_two_value": None,
            "selected_volumetric_flow-rate_value": 0.447,
            "test_name": "retraction distance",
            "test_number": "10",
            "tested_parameter_one_values": [
              0,
              1,
              2,
              3,
              4,
              5,
              6
            ],
            "tested_parameter_two_values": None,
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested. You can change the limiting values",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": None,
                "name": None,
                "precision": None,
                "programmatic_name": None,
                "units": None,
                "values": None
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.447
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "10"
        },
        {
          "path": [
            "settings",
            "critical_overhang_angle"
          ],
          "value": 27
        },
        {
          "path": [
            "settings",
            "extrusion_multiplier"
          ],
          "value": 0.9
        },
        {
          "path": [
            "settings",
            "retraction_distance"
          ],
          "value": 1
        },
        {
          "path": [
            "settings",
            "retraction_speed"
          ],
          "value": 103
        },
        {
          "path": [
            "settings",
            "speed_printing"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "temperature_extruder"
          ],
          "value": 47
        },
        {
          "path": [
            "settings",
            "track_height"
          ],
          "value": 0.11
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        },
        {
          "path": [
            "settings",
            "track_width"
          ],
          "value": 0.43
        },
        {
          "path": [
            "settings",
            "track_width_raft"
          ],
          "value": 0.39
        }
      ]
    },
    {
      "deleted": [],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 0
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 6
        },
        {
          "path": [
            "session",
            "min_max_parameter_three",
            0
          ],
          "value": 60
        },
        {
          "path": [
            "session",
            "min_max_parameter_three",
            1
          ],
          "value": 120
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 60
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            1
          ],
          "value": 120
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.39,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            2
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:14:47",
            "executed": True,
            "extruded_filament_mm": 1273.065,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 44,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion temperature vs printing speed",
            "test_number": "03",
            "tested_parameter_one_values": [
              30,
              34,
              37,
              40,
              44,
              48,
              51
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  30,
                  34,
                  37,
                  40,
                  44,
                  48,
                  51
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            3
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:15:28",
            "executed": True,
            "extruded_filament_mm": 1183.955,
            "parameter_one_name": "track height",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.11,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track height vs printing speed",
            "test_number": "04",
            "tested_parameter_one_values": [
              0.07,
              0.11,
              0.14,
              0.18,
              0.22,
              0.25,
              0.29
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four <b>Printing speeds</b>. You can change the limiting values",
                "min_max": [
                  0.04000000000000001,
                  0.4
                ],
                "name": "track height",
                "precision": "{:.2f}",
                "programmatic_name": "track_height",
                "units": "mm",
                "values": [
                  0.07,
                  0.10666666666666667,
                  0.1433333333333333,
                  0.18,
                  0.21666666666666662,
                  0.2533333333333333,
                  0.29
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            4
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:16:09",
            "executed": True,
            "extruded_filament_mm": 917.568,
            "parameter_one_name": "track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.43,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track width",
            "test_number": "05",
            "tested_parameter_one_values": [
              0.36,
              0.37,
              0.39,
              0.4,
              0.41,
              0.43,
              0.44
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width",
                "units": "mm",
                "values": [
                  0.36,
                  0.3733333333333333,
                  0.38666666666666666,
                  0.4,
                  0.41333333333333333,
                  0.42666666666666664,
                  0.44
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.37,
                0.385,
                0.399,
                0.414,
                0.429,
                0.443,
                0.458
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            5
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:17:56",
            "executed": True,
            "extruded_filament_mm": 1009.607,
            "parameter_one_name": "extrusion multiplier",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "-",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.9,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion multiplier vs printing speed",
            "test_number": "06",
            "tested_parameter_one_values": [
              0.8,
              0.9,
              1,
              1.1,
              1.2,
              1.3,
              1.4
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.01,
                  2
                ],
                "name": "extrusion multiplier",
                "precision": "{:.3f}",
                "programmatic_name": "extrusion_multiplier",
                "units": "-",
                "values": [
                  0.8,
                  0.9,
                  1,
                  1.1,
                  1.2,
                  1.2999999999999998,
                  1.4
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.358,
                0.402,
                0.447,
                0.492,
                0.536,
                0.581,
                0.626
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            6
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:18:33",
            "executed": True,
            "extruded_filament_mm": 862.732,
            "parameter_one_name": "printing speed",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "mm/s",
            "parameter_three_name": None,
            "parameter_two_name": None,
            "parameter_two_precision": None,
            "parameter_two_units": None,
            "selected_parameter_one_value": 10,
            "selected_parameter_two_value": None,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "printing speed",
            "test_number": "07",
            "tested_parameter_one_values": [
              10,
              10,
              10,
              10,
              10,
              10,
              10
            ],
            "tested_parameter_two_values": None,
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested while all other processing parameters are constant. You can change the limiting values",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10,
                  10,
                  10,
                  10
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": None,
                "name": None,
                "precision": None,
                "programmatic_name": None,
                "units": None,
                "values": []
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            7
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:04",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": "retraction speed",
            "parameter_three_precision": "{:.0f}",
            "parameter_three_units": "mm/s",
            "parameter_two_name": "retraction distance",
            "parameter_two_precision": "{:.3f}",
            "parameter_two_units": "mm",
            "selected_parameter_one_value": 47,
            "selected_parameter_three_value": 103,
            "selected_parameter_two_value": 2,
            "selected_volumetric_flow-rate_value": 0.447,
            "test_name": "extrusion temperature vs retraction distance",
            "test_number": "08",
            "tested_parameter_one_values": [
              39,
              41,
              42,
              44,
              46,
              47,
              49
            ],
            "tested_parameter_three_values": [
              60,
              120
            ],
            "tested_parameter_two_values": [
              0,
              2,
              4,
              6
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Retraction distances</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  39,
                  40.666666666666664,
                  42.333333333333336,
                  44,
                  45.666666666666664,
                  47.333333333333336,
                  49
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range of <b>Retraction distances</b> to be tested",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  2,
                  4,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "retraction speed",
                "precision": "{:.0f}",
                "programmatic_name": "retraction_speed",
                "units": "mm/s",
                "values": [
                  60,
                  120
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.447
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            8
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:34",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "retraction distance",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 1,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "retraction distance vs printing speed",
            "test_number": "09",
            "tested_parameter_one_values": [
              0,
              1,
              2,
              3,
              4,
              5,
              6
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            9
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:56",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "retraction distance",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": None,
            "parameter_two_precision": None,
            "parameter_two_units": None,
            "selected_parameter_one_value": 4,
            "selected_parameter_two_value": None,
            "selected_volumetric_flow-rate_value": 0.447,
            "test_name": "retraction distance",
            "test_number": "10",
            "tested_parameter_one_values": [
              0,
              1,
              2,
              3,
              4,
              5,
              6
            ],
            "tested_parameter_two_values": None,
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested. You can change the limiting values",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": None,
                "name": None,
                "precision": None,
                "programmatic_name": None,
                "units": None,
                "values": None
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.447
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            10
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:20:34",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "retraction distance",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "retraction speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0,
            "selected_parameter_two_value": 0,
            "selected_volumetric_flow-rate_value": 0.447,
            "test_name": "retraction distance vs retraction speed",
            "test_number": "11",
            "tested_parameter_one_values": [
              0,
              1,
              2,
              3,
              4,
              5,
              6
            ],
            "tested_parameter_two_values": [
              60,
              80,
              100,
              120
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Retraction speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "retraction speed",
                "precision": "{:.0f}",
                "programmatic_name": "retraction_speed",
                "units": "mm/s",
                "values": [
                  60,
                  80,
                  100,
                  120
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.447
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "11"
        },
        {
          "path": [
            "settings",
            "critical_overhang_angle"
          ],
          "value": 27
        },
        {
          "path": [
            "settings",
            "extrusion_multiplier"
          ],
          "value": 0.9
        },
        {
          "path": [
            "settings",
            "retraction_distance"
          ],
          "value": 4
        },
        {
          "path": [
            "settings",
            "retraction_speed"
          ],
          "value": 103
        },
        {
          "path": [
            "settings",
            "speed_printing"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "temperature_extruder"
          ],
          "value": 47
        },
        {
          "path": [
            "settings",
            "track_height"
          ],
          "value": 0.11
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        },
        {
          "path": [
            "settings",
            "track_width"
          ],
          "value": 0.43
        },
        {
          "path": [
            "settings",
            "track_width_raft"
          ],
          "value": 0.39
        }
      ]
    },
    {
      "deleted": [],
      "overrides": [
        {
          "path": [
            "session",
            "min_max_parameter_one",
            0
          ],
          "value": 1
        },
        {
          "path": [
            "session",
            "min_max_parameter_one",
            1
          ],
          "value": 2
        },
        {
          "path": [
            "session",
            "min_max_parameter_three",
            0
          ],
          "value": 60
        },
        {
          "path": [
            "session",
            "min_max_parameter_three",
            1
          ],
          "value": 120
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            0
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "min_max_parameter_two",
            1
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_one_value"
          ],
          "value": 0.17
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "selected_parameter_two_value"
          ],
          "value": 10
        },
        {
          "path": [
            "session",
            "previous_tests",
            0,
            "validated"
          ],
          "value": True
        },
        {
          "path": [
            "session",
            "previous_tests",
            1
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:13:48",
            "executed": True,
            "extruded_filament_mm": 238.203,
            "parameter_one_name": "first-layer track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "first-layer printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.39,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "first-layer track width",
            "test_number": "02",
            "tested_parameter_one_values": [
              0.36,
              0.39,
              0.43,
              0.46,
              0.49,
              0.53,
              0.56
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>First-layer printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "first-layer track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width_raft",
                "units": "mm",
                "values": [
                  0.36,
                  0.3933333333333333,
                  0.4266666666666667,
                  0.46,
                  0.4933333333333334,
                  0.5266666666666667,
                  0.56
                ]
              },
              {
                "active": False,
                "hint_active": "This value was determined in the previous test(s) and cannot be changed",
                "min_max": [
                  1,
                  140
                ],
                "name": "first-layer printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing_raft",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.55,
                0.607,
                0.663,
                0.72,
                0.777,
                0.833,
                0.89
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            2
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:14:47",
            "executed": True,
            "extruded_filament_mm": 1273.065,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 44,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion temperature vs printing speed",
            "test_number": "03",
            "tested_parameter_one_values": [
              30,
              34,
              37,
              40,
              44,
              48,
              51
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  30,
                  34,
                  37,
                  40,
                  44,
                  48,
                  51
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ],
              [
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714,
                0.714
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            3
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:15:28",
            "executed": True,
            "extruded_filament_mm": 1183.955,
            "parameter_one_name": "track height",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.11,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track height vs printing speed",
            "test_number": "04",
            "tested_parameter_one_values": [
              0.07,
              0.11,
              0.14,
              0.18,
              0.22,
              0.25,
              0.29
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four <b>Printing speeds</b>. You can change the limiting values",
                "min_max": [
                  0.04000000000000001,
                  0.4
                ],
                "name": "track height",
                "precision": "{:.2f}",
                "programmatic_name": "track_height",
                "units": "mm",
                "values": [
                  0.07,
                  0.10666666666666667,
                  0.1433333333333333,
                  0.18,
                  0.21666666666666662,
                  0.2533333333333333,
                  0.29
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 20-50 mm/s for printing flexible materials, or to 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ],
              [
                0.269,
                0.402,
                0.529,
                0.65,
                0.766,
                0.876,
                0.98
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            4
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:16:09",
            "executed": True,
            "extruded_filament_mm": 917.568,
            "parameter_one_name": "track width",
            "parameter_one_precision": "{:.2f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.43,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "track width",
            "test_number": "05",
            "tested_parameter_one_values": [
              0.36,
              0.37,
              0.39,
              0.4,
              0.41,
              0.43,
              0.44
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.2,
                  0.8
                ],
                "name": "track width",
                "precision": "{:.2f}",
                "programmatic_name": "track_width",
                "units": "mm",
                "values": [
                  0.36,
                  0.3733333333333333,
                  0.38666666666666666,
                  0.4,
                  0.41333333333333333,
                  0.42666666666666664,
                  0.44
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.37,
                0.385,
                0.399,
                0.414,
                0.429,
                0.443,
                0.458
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            5
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:17:56",
            "executed": True,
            "extruded_filament_mm": 1009.607,
            "parameter_one_name": "extrusion multiplier",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "-",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0.9,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "extrusion multiplier vs printing speed",
            "test_number": "06",
            "tested_parameter_one_values": [
              0.8,
              0.9,
              1,
              1.1,
              1.2,
              1.3,
              1.4
            ],
            "tested_parameter_two_values": [
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at one <b>Printing speed</b>. You can change the limiting values",
                "min_max": [
                  0.01,
                  2
                ],
                "name": "extrusion multiplier",
                "precision": "{:.3f}",
                "programmatic_name": "extrusion_multiplier",
                "units": "-",
                "values": [
                  0.8,
                  0.9,
                  1,
                  1.1,
                  1.2,
                  1.2999999999999998,
                  1.4
                ]
              },
              {
                "active": False,
                "hint_active": "Set a value from the range 20-50 mm/s for printing flexible materials, or 30-70 mm/s for printing harder materials",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.358,
                0.402,
                0.447,
                0.492,
                0.536,
                0.581,
                0.626
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            6
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:18:33",
            "executed": True,
            "extruded_filament_mm": 862.732,
            "parameter_one_name": "printing speed",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "mm/s",
            "parameter_three_name": None,
            "parameter_two_name": None,
            "parameter_two_precision": None,
            "parameter_two_units": None,
            "selected_parameter_one_value": 10,
            "selected_parameter_two_value": None,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "printing speed",
            "test_number": "07",
            "tested_parameter_one_values": [
              10,
              10,
              10,
              10,
              10,
              10,
              10
            ],
            "tested_parameter_two_values": None,
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested while all other processing parameters are constant. You can change the limiting values",
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10,
                  10,
                  10,
                  10
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": None,
                "name": None,
                "precision": None,
                "programmatic_name": None,
                "units": None,
                "values": []
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402,
              0.402
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            7
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:04",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "extrusion temperature",
            "parameter_one_precision": "{:.0f}",
            "parameter_one_units": "degC",
            "parameter_three_name": "retraction speed",
            "parameter_three_precision": "{:.0f}",
            "parameter_three_units": "mm/s",
            "parameter_two_name": "retraction distance",
            "parameter_two_precision": "{:.3f}",
            "parameter_two_units": "mm",
            "selected_parameter_one_value": 47,
            "selected_parameter_three_value": 103,
            "selected_parameter_two_value": 2,
            "selected_volumetric_flow-rate_value": 0.447,
            "test_name": "extrusion temperature vs retraction distance",
            "test_number": "08",
            "tested_parameter_one_values": [
              39,
              41,
              42,
              44,
              46,
              47,
              49
            ],
            "tested_parameter_three_values": [
              60,
              120
            ],
            "tested_parameter_two_values": [
              0,
              2,
              4,
              6
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Retraction distances</b> (see below). You can change the limiting values",
                "min_max": [
                  30,
                  350
                ],
                "name": "extrusion temperature",
                "precision": "{:.0f}",
                "programmatic_name": "temperature_extruder",
                "units": "degC",
                "values": [
                  39,
                  40.666666666666664,
                  42.333333333333336,
                  44,
                  45.666666666666664,
                  47.333333333333336,
                  49
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range of <b>Retraction distances</b> to be tested",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  2,
                  4,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "retraction speed",
                "precision": "{:.0f}",
                "programmatic_name": "retraction_speed",
                "units": "mm/s",
                "values": [
                  60,
                  120
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.447
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            8
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:34",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "retraction distance",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 1,
            "selected_parameter_two_value": 10,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "retraction distance vs printing speed",
            "test_number": "09",
            "tested_parameter_one_values": [
              0,
              1,
              2,
              3,
              4,
              5,
              6
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ],
              [
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402,
                0.402
              ]
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            9
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:19:56",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "retraction distance",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": None,
            "parameter_two_precision": None,
            "parameter_two_units": None,
            "selected_parameter_one_value": 4,
            "selected_parameter_two_value": None,
            "selected_volumetric_flow-rate_value": 0.447,
            "test_name": "retraction distance",
            "test_number": "10",
            "tested_parameter_one_values": [
              0,
              1,
              2,
              3,
              4,
              5,
              6
            ],
            "tested_parameter_two_values": None,
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested. You can change the limiting values",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": None,
                "name": None,
                "precision": None,
                "programmatic_name": None,
                "units": None,
                "values": None
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.447
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            10
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:20:34",
            "executed": True,
            "extruded_filament_mm": 685.191,
            "parameter_one_name": "retraction distance",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "mm",
            "parameter_three_name": None,
            "parameter_two_name": "retraction speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 1,
            "selected_parameter_two_value": 80,
            "selected_volumetric_flow-rate_value": 0.447,
            "test_name": "retraction distance vs retraction speed",
            "test_number": "11",
            "tested_parameter_one_values": [
              0,
              1,
              2,
              3,
              4,
              5,
              6
            ],
            "tested_parameter_two_values": [
              60,
              80,
              100,
              120
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Retraction speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  0,
                  20
                ],
                "name": "retraction distance",
                "precision": "{:.3f}",
                "programmatic_name": "retraction_distance",
                "units": "mm",
                "values": [
                  0,
                  1,
                  2,
                  3,
                  4,
                  5,
                  6
                ]
              },
              {
                "active": True,
                "hint_active": None,
                "min_max": [
                  1,
                  140
                ],
                "name": "retraction speed",
                "precision": "{:.0f}",
                "programmatic_name": "retraction_speed",
                "units": "mm/s",
                "values": [
                  60,
                  80,
                  100,
                  120
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              0.447
            ],
            "validated": True
          }
        },
        {
          "path": [
            "session",
            "previous_tests",
            11
          ],
          "value": {
            "comments": 0,
            "datetime_info": "2020-02-10 17:20:58",
            "executed": True,
            "extruded_filament_mm": 1007.558,
            "parameter_one_name": "bridging extrusion multiplier",
            "parameter_one_precision": "{:.3f}",
            "parameter_one_units": "-",
            "parameter_three_name": None,
            "parameter_two_name": "bridging printing speed",
            "parameter_two_precision": "{:.0f}",
            "parameter_two_units": "mm/s",
            "selected_parameter_one_value": 0,
            "selected_parameter_two_value": 0,
            "selected_volumetric_flow-rate_value": 0,
            "test_name": "bridging extrusion multiplier vs bridging printing speed",
            "test_number": "13",
            "tested_parameter_one_values": [
              1,
              1.167,
              1.333,
              1.5,
              1.667,
              1.833,
              2
            ],
            "tested_parameter_two_values": [
              10,
              10,
              10,
              10
            ],
            "tested_parameters": [
              {
                "active": True,
                "hint_active": "These seven values will be tested at four different <b>Bridging printing speeds</b> (see below). You can change the limiting values",
                "min_max": [
                  0.01,
                  2
                ],
                "name": "bridging extrusion multiplier",
                "precision": "{:.3f}",
                "programmatic_name": "bridging_extrusion_multiplier",
                "units": "-",
                "values": [
                  1,
                  1.1666666666666667,
                  1.3333333333333333,
                  1.5,
                  1.6666666666666665,
                  1.8333333333333333,
                  2
                ]
              },
              {
                "active": True,
                "hint_active": "Set the range to 10-25 mm/s for printing flexible materials, or 15-35 mm/s for harder materials",
                "min_max": [
                  1,
                  280
                ],
                "name": "bridging printing speed",
                "precision": "{:.0f}",
                "programmatic_name": "bridging_speed_printing",
                "units": "mm/s",
                "values": [
                  10,
                  10,
                  10,
                  10
                ]
              }
            ],
            "tested_volumetric_flow-rate_values": [
              [
                0.447,
                0.522,
                0.596,
                0.671,
                0.745,
                0.82,
                0.894
              ],
              [
                0.447,
                0.522,
                0.596,
                0.671,
                0.745,
                0.82,
                0.894
              ],
              [
                0.447,
                0.522,
                0.596,
                0.671,
                0.745,
                0.82,
                0.894
              ],
              [
                0.447,
                0.522,
                0.596,
                0.671,
                0.745,
                0.82,
                0.894
              ],
              [
                0.447,
                0.522,
                0.596,
                0.671,
                0.745,
                0.82,
                0.894
              ],
              [
                0.447,
                0.522,
                0.596,
                0.671,
                0.745,
                0.82,
                0.894
              ],
              [
                0.447,
                0.522,
                0.596,
                0.671,
                0.745,
                0.82,
                0.894
              ]
            ],
            "validated": False
          }
        },
        {
          "path": [
            "session",
            "test_number"
          ],
          "value": "13"
        },
        {
          "path": [
            "settings",
            "critical_overhang_angle"
          ],
          "value": 27
        },
        {
          "path": [
            "settings",
            "extrusion_multiplier"
          ],
          "value": 0.9
        },
        {
          "path": [
            "settings",
            "retraction_distance"
          ],
          "value": 1
        },
        {
          "path": [
            "settings",
            "retraction_speed"
          ],
          "value": 80
        },
        {
          "path": [
            "settings",
            "speed_printing"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "speed_printing_raft"
          ],
          "value": 10
        },
        {
          "path": [
            "settings",
            "temperature_extruder"
          ],
          "value": 47
        },
        {
          "path": [
            "settings",
            "track_height"
          ],
          "value": 0.11
        },
        {
          "path": [
            "settings",
            "track_height_raft"
          ],
          "value": 0.17
        },
        {
          "path": [
            "settings",
            "track_width"
          ],
          "value": 0.43
        },
        {
          "path": [
            "settings",
            "track_width_raft"
          ],
          "value": 0.39
        }
      ]
    },
]


def _execute_on_path(parent, path, do_delete:bool=True, val=None):
    p = parent
    k = path.pop()
    for i in path:
        parent = parent[i]
    if do_delete:
        del parent[k]
    else:
        try:
            parent[k] = val
        except IndexError:
            parent.append(val)


def _migrate_dict(base, migration):
    for path in migration['deleted']:
        _execute_on_path(base, path)

    for i in migration['overrides']:
        _execute_on_path(base, i['path'], False, i['value'])


class PersistencesIterator:
    def __init__(self, strength_persistence=True):
        persistences = []
        if strength_persistence:
            persistences.append(('Mechanical strength',
                                BASE_PERSISTENCE_STRENGTH,
                                PERSISTENCE_MIGRATIONS_STRENGTH))

        self._p = persistences
        self._last = None


    def __iter__(self):
        return self

    def __next__(self):
        if self._last is None:
            pers_type = 0
            pers_num = 0
        else:
            pers_type, pers_num = self._last
            pers_num +=1

        while True:
            if pers_type >= len(self._p):
                raise StopIteration
            elif pers_num >= len(self._p[pers_type][-1]):
                pers_type +=1
                pers_num = 0
                continue
            else:
                name, base, migrations = self._p[pers_type]
                p = json.loads(base)
                _migrate_dict(p, migrations[pers_num])
                result = ('{0} test {1}'.format(name, pers_num +1), p)
                self._last = (pers_type, pers_num)
                return result
            # should never actually get to here
            raise StopIteration

