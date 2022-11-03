import bpy
import sys
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

camera_coords = (7.86373, -12.966, 3.40269)
camera_radians = (1.40, -0.0159, 0.42)

try:
    blender.delete_default_figures('Cube')
    sphere = blender.create_sphere()
    material = bpy.data.materials.new(name='Material')
    sphere_material = blender.edit_object(sphere, material, Metallic = 10, Base_Color = (0.113597, 0.113597, 0.8, 0.5), Roughness = 0) 
    cube = blender.create_cube(vertices, faces)  
    blender.change_figure_location(cube, (3.99972, 0, 0))
    blender.change_figure_rotation(cube, (0.156, -0.10833, 0.601))
    second_material =  sphere_material.copy()
    blender.edit_object(cube, second_material, Metallic = 100, Base_Color = (0.049977, 0.78762, 0.8, 1), Roughness = 1, Anisotropic = 0.7)
    camera = bpy.context.scene.camera
    blender.change_camera_location(camera, camera_coords, camera_radians)
    scene = bpy.context.scene
    blender.get_rendered_image(scene, 2, x_resolution, y_resolution, output_path)
    stop_time = datetime.datetime.now()
    dict = blender.create_dict('second_test', start_time, stop_time, CPU, RAM)
    blender.write_json_in_file(dict, 2, output_path)    
except:
    stop_time = datetime.datetime.now()
    dict = blender.create_dict('second_test', start_time, stop_time, CPU, RAM)
    dict['status'] = 'Failed'
    blender.write_json_in_file(dict, 2, output_path)    
    raise BlenderTestException('Something went wrong during test execution')
finally:
    bpy.ops.wm.quit_blender()