import sys
import bpy
import datetime
import logging

import blender_funcs as blender
from blender_exep import BlenderTestException
import system_utils as utils

start_time = datetime.datetime.now()
(x_resolution, y_resolution, output_path) = utils.parse_input_params(sys.argv)
(CPU, RAM) = utils.get_system_params()

vertices = [(0, 0, 0), (0, 3, 0), (3, 3, 0), (3, 0, 0), (0, 0, 3), (0, 3, 3), (3, 3, 3), (3, 0, 3)]
faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]

camera_coords = [6.998, -9.2825, 3.2315]
camera_rot_radians = [1.41, -0.016, 0.42]

try:    
    blender.delete_default_figures('Cube')
    blender.create_cube(vertices, faces)
    camera = bpy.context.scene.camera
    blender.change_camera_location(camera, camera_coords, camera_rot_radians)
    scene = bpy.context.scene
    blender.get_rendered_image(scene, 1, x_resolution, y_resolution, output_path)
    stop_time = datetime.datetime.now()
    dict = blender.create_dict('first_test', start_time, stop_time, CPU, RAM)
    blender.write_json_in_file(dict, 1, output_path)
    print('Test Passed')
except:
    stop_time = datetime.datetime.now()
    dict = blender.create_dict('first_test', start_time, stop_time, CPU, RAM)
    dict['status'] = 'Failed'
    blender.write_json_in_file(dict, 1, output_path)    
    raise BlenderTestException('Something went wrong during test execution')
finally:
    bpy.ops.wm.quit_blender()

