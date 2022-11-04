import logging
import os
import subprocess
import sys
from pathlib import Path
from lib.blender_exep import BlenderTestException

def main():
    logging.basicConfig(level='INFO')
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

    any_task_failed = False
    for test_path in tests:
        try:
            test_name = get_test_name(test_path)
            logging.info(f'Starting test {test_name}')
            run_task(blender_path, test_path, x_resolution, y_resolution, output_path)
            logging.info(f'Test {test_name} successfully executed')
        except Exception as e:
            any_task_failed = True
            logging.error(e)

    if any_task_failed:
        exit(1)

def get_test_name(test_path: str):
    return test_path[test_path.rindex('\\') + 1:]

def run_task(blender_path, test_path, x_resolution, y_resolution, output_path):
    cmd = [f"{blender_path}", "--python-exit-code", "1", "-b", "--python", f"{test_path}", "--", x_resolution, y_resolution, output_path]
    blender_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='UTF-8')
    (out, _) = blender_proc.communicate()
    if blender_proc.returncode != 0:
        raise BlenderTestException(f"Test {get_test_name(test_path)} returned non zero exit code. Details: \n" + out)


if __name__ == "__main__":
    main()