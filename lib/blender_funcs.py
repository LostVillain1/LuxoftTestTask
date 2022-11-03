import bpy
import os
import json

def delete_default_figures(*figures):
    bpy.ops.object.select_all(action='DESELECT')
    for figure in figures:
        bpy.data.objects[figure].select_set(True)
    bpy.ops.object.delete() 

def create_cube(vertices, faces):
    mesh = bpy.data.meshes.new('Cube') 
    cube = bpy.data.objects.new("Cube", mesh)

    cube.location = bpy.context.scene.cursor.location
    bpy.context.collection.objects.link(cube)

    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)

    return cube

def change_figure_location(figure, coords):
    figure.location = coords

def change_figure_rotation(figure, radians):
    figure.rotation_euler = radians

def create_sphere():
    bpy.ops.mesh.primitive_uv_sphere_add(radius = 2, enter_editmode = True, location = ( 0, 0, 0))
    sphere = bpy.context.collection.objects['Sphere']
    return sphere


def edit_object(object, material, **props):
    material.use_nodes = True
    object.data.materials.append(material)
    for prop in props:
        if prop == 'Base_Color':
            material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = props[prop]
        else:
            material.node_tree.nodes['Principled BSDF'].inputs[f'{prop}'].default_value = props[prop]
    return material    
        

def change_camera_location(camera, coords, rot_radians):
    camera.location = coords
    camera.rotation_euler = rot_radians

def get_rendered_image(scene, image_num, x_res, y_res, output_path):
    scene.render.resolution_x = x_res
    scene.render.resolution_y = y_res
    scene.render.resolution_percentage = 100
    scene.render.use_border = False
    scene.render.image_settings.file_format='PNG'
    scene.render.filepath= f'{output_path}\\image{image_num}.png' 
    bpy.ops.render.render(write_still=1)

def create_dict(test_name, start_time, stop_time, CPU, RAM):
    output_dict = { 'test_name': test_name,
                    'status': 'Done',
                    'test_start_time': str(start_time),
                    'test_end_time': str(stop_time),
                    'test duration' : str(stop_time - start_time),
                    'CPU': CPU,
                    'RAM': RAM,
                    'OS_name': f'{os.name}'}
    return output_dict

def setup_light(light_type, energy, coords):
    light_data = bpy.data.lights.new('light', type=light_type)
    light_data.energy = energy
    light_first = bpy.data.objects.new('light', light_data)
    bpy.context.collection.objects.link(light_first)
    bpy.context.view_layer.objects.active = light_first
    light_first.location = coords


def write_json_in_file(output_dict, test_index, output_path):
    json_object = json.dumps(output_dict, indent=4)
    
    with open(f"{output_path}\\sample{test_index}.json", "w") as outfile:
        outfile.write(json_object)