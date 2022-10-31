import bpy
import datetime
import platform
import os
import json
import psutil

x_resolution = 1920
y_resolution = 1080
# Need to change the path to output dir
output_dir = 'C:\\Users\\User\\Desktop\\LuxOutput'

start_time = datetime.datetime.now()
CPU = platform.processor(),
RAM = f"RAM memory % used: {psutil.virtual_memory()[3]/1000000000}"

def createFigure(x_res, y_res, output_path):
    #Deleting default Cube and Light
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Cube'].select_set(True)
    bpy.data.objects['Light'].select_set(True)
    bpy.ops.object.delete()

    #Creating and Editing Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius = 2, enter_editmode = True, location = ( 0, 0, 0))
    sphere = bpy.context.collection.objects['Sphere']
    material = bpy.data.materials.new(name='Material')
    material.use_nodes = True
    sphere.data.materials.append(material)
    material.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 0.3
    material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.66387, 0.937999, 0.099708, 0.5)
    material.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0
    material.node_tree.nodes['Principled BSDF'].inputs['Specular'].default_value = 0.9
    
    #Creating Cube
    
    vertices = [(0, 0, 0), (0, 3, 0), (3, 3, 0), (3, 0, 0), (0, 0, 3), (0, 3, 3), (3, 3, 3), (3, 0, 3)]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]

    mesh = bpy.data.meshes.new('Cube') # Метод позволяет создавать объект определенного типа из коллекции, убираются объекты через remove()
    cube = bpy.data.objects.new("Cube", mesh)

    cube.location = bpy.context.scene.cursor.location
    bpy.context.collection.objects.link(cube)

    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)
    
    cube.location = (3.99972, 0, 0)
    cube.rotation_euler = (0.156, -0.10833, 0.601)
    
    material2 = material.copy()
    cube.data.materials.append(material2)
    material2.node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 100
    material2.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.049977, 0.78762, 0.8, 1)
    material2.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1
    material2.node_tree.nodes['Principled BSDF'].inputs['Anisotropic'].default_value = 0.7
    
    
    #Setup camera
    camera = bpy.context.scene.camera
    camera_location = camera.location
    camera_location[0] = 7.86373
    camera_location[1] = -12.966 
    camera_location[2] = 3.40269

    camera.rotation_euler = (1.40, -0.0159, 0.42)

    #Setup first Light
    light_data = bpy.data.lights.new('light', type='POINT')
    light_data.energy = 800.0
    light_first = bpy.data.objects.new('light', light_data)
    bpy.context.collection.objects.link(light_first)
    bpy.context.view_layer.objects.active = light_first
    light_first.location = (4.49963 , -5.09817 , 1.91513)
    
    
    #Getting rendered image
    scene = bpy.context.scene
    scene.render.resolution_x = x_res
    scene.render.resolution_y = y_res
    scene.render.resolution_percentage = 100
    scene.render.use_border = False
    scene.render.image_settings.file_format='PNG'
    scene.render.filepath= f'{output_path}\\image3.png'
    bpy.ops.render.render(write_still=1)
    
    #Delete first light
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['light'].select_set(True)
    bpy.ops.object.delete()
    
    #Create Second Light
    light_data = bpy.data.lights.new('light', type='SUN')
    light_data.energy = 20.0
    light_second = bpy.data.objects.new('light', light_data)
    bpy.context.collection.objects.link(light_second)
    bpy.context.view_layer.objects.active = light_second
    light_second.location = (5.33554  , -16.4816  , 1.91513)
    
    scene.render.image_settings.file_format='PNG'
    scene.render.filepath= f'{output_path}\\image4.png' 
    bpy.ops.render.render(write_still=1)

    stop_time = datetime.datetime.now()
    #Creating JSON file
    output_dict = {'test_name': 'Test3',
                    'test_start_time': str(start_time),
                    'test_end_time': str(stop_time),
                    'test duration' : str(stop_time - start_time),
                    'CPU': CPU,
                    'RAM': RAM,
                    'OS_name': f'{os.name}'}

    json_object = json.dumps(output_dict, indent=4)

    with open(f"{output_path}\\sample3.json", "w") as outfile:
        outfile.write(json_object)
    

createFigure(x_resolution, y_resolution, output_dir)