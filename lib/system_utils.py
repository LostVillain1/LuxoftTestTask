import platform
import psutil


def parse_input_params(sys_argv):
    argv = sys_argv
    argv = argv[argv.index("--") + 1:]
    return (int(argv[0]), int(argv[1]), argv[2])


def get_system_params():
    return (platform.processor(), psutil.virtual_memory()[3]/1000000000)