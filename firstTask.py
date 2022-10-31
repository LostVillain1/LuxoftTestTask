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
    #Deleting default Cube
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete() 

    #Creating Cube
    vertices = [(0, 0, 0), (0, 3, 0), (3, 3, 0), (3, 0, 0), (0, 0, 3), (0, 3, 3), (3, 3, 3), (3, 0, 3)]
    faces = [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]

    mesh = bpy.data.meshes.new('Cube') # Метод позволяет создавать объект определенного типа из коллекции, убираются объекты через remove()
    cube = bpy.data.objects.new("Cube", mesh)

    cube.location = bpy.context.scene.cursor.location
    bpy.context.collection.objects.link(cube)

    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)

    camera = bpy.context.scene.camera
    camera_location = camera.location
    camera_location[0] = 6.998
    camera_location[1] = -9.2825
    camera_location[2] = 3.2315

    camera.rotation_euler = (1.41, -0.016, 0.42)

    #Getting rendered image
    scene = bpy.context.scene
    scene.render.resolution_x = x_res
    scene.render.resolution_y = y_res
    scene.render.resolution_percentage = 100
    scene.render.use_border = False
    scene.render.image_settings.file_format='PNG'
    scene.render.filepath= f'{output_path}\\image.png' 
    bpy.ops.render.render(write_still=1)

    stop_time = datetime.datetime.now()
    #Creating JSON file
    output_dict = {'test_name': 'Test1',
                    'test_start_time': str(start_time),
                    'test_end_time': str(stop_time),
                    'test duration' : str(stop_time - start_time),
                    'CPU': CPU,
                    'RAM': RAM,
                    'OS_name': f'{os.name}'}

    json_object = json.dumps(output_dict, indent=4)

    with open(f"{output_path}\\sample.json", "w") as outfile:
        outfile.write(json_object)
    
   
createFigure(x_resolution, y_resolution, output_dir)

