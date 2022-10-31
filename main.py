import subprocess

# Need to change the path to the tasks
blender_path = r"C:\\Program Files\\Blender Foundation\\Blender 3.3\blender-launcher.exe"
scripts = [r'C:\Users\User\Desktop\Lux\firstTask.py', r'C:\Users\User\Desktop\Lux\secondTask.py', r'C:\Users\User\Desktop\Lux\thirdTask.py']


def runTask(blender_path):
    for script in scripts:
        cmd = [f"{blender_path}", "--python", f"{script}"]    
        blender_proc = subprocess.Popen(cmd)   

runTask(blender_path)