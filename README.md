## About
This project is a set of tests for testing Blender.

## Prerequisites

* Windows OS
* Installed or portable Blender version 3.3. Also, `psutil` package should be installed into built-in Python's interpreter. 
* To get access to the helper methods, you need to copy the files from **lib** directory to Blender python lib packages folder. For example: **\Blender Foundation\Blender 3.3\3.3\python\lib**


## Running

You need to run **main.py** file in cmd

```<Blender Home>\blender\3.3\python\bin\python.exe main.py <blender_path> <x_resolution> <y_resolution> <output_path>```

Where,

| **Parameter**      | **Description**                                                   |
|--------------------|-------------------------------------------------------------------|
| **blender_path**   | absolute path to blender.exe file                                 |
| **x_resolution**   | x-axis resolution                                                 |
| **y_resolution**   | y-axis resolution                                                 |
| **output_path**    | absolute path to output directory                                 |


