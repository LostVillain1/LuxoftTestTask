import logging
import os
import subprocess
import sys
from pathlib import Path
from lib.blender_exep import BlenderTestException

def main():
    params_len = len(sys.argv) - 1
    if params_len != 4:
        raise BlenderTestException("Incorrect number of input parameters. Got " + str(params_len) + " instead of 4")

    blender_path = sys.argv[1]
    x_resolution = sys.argv[2]
    y_resolution = sys.argv[3]
    output_path = sys.argv[4]

    try:
        tests_directory_path = Path("tests").resolve()
        tests = set()
        for path, _, files in os.walk(tests_directory_path):
            for name in files:
                tests.add(os.path.join(path, name))
    except:
        raise BlenderTestException("Something went wrong while trying to get tests files. Check that /tests directory exists.")

    if len(tests) == 0:
        raise BlenderTestException("No tests found in /tests directory")

    for test_path in tests:
        try:
            run_task(blender_path, test_path, x_resolution, y_resolution, output_path)
            print(f'Test {test_path} successfully executed')
        except Exception as e:
            logging.error(e)


def run_task(blender_path, test_path, x_resolution, y_resolution, output_path):
    cmd = [f"{blender_path}", "--python", f"{test_path}", "--", x_resolution, y_resolution, output_path]
    blender_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='UTF-8')
    (_, err) = blender_proc.communicate()
    if err and err.strip():
        raise BlenderTestException(f"Test {test_path} returned not empty stderr. Details: \n" + err)
        

if __name__ == "__main__":
    main()