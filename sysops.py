import fileoperators
import helpers
import os
def _screen_exec_command_prep(screen_name, screen_config_file, screen_log_file, exec_command):
    log_string = "logfile " + screen_log_file
    command_string = "Executed Command : \n" + exec_command + "\n\n"
    fileoperators._write_to_file(screen_config_file, log_string)
    fileoperators._write_to_file(screen_log_file, command_string)
    screen_exec_command =  ("screen -S " + screen_name + " -L -c " + screen_config_file + " -d -m bash -c \"" +
                            exec_command + "\"")
    del log_string, command_string
    return screen_exec_command

def _spawn_screen_with_executable_inside_in_detached_mode(executable_command_for_screen, verbosity):
    if verbosity == 'y':
        helpers._print_norm_blue("Spawning Screen & Executing : ", executable_command_for_screen)
    _system_executor(executable_command_for_screen)


def _system_executor(exec_command):
    stream = os.popen(exec_command)
    output = stream.read()
    return (output)

def _get_number_of_open_screens(screen_header):
    screen_list_command = "screen -ls | grep -i " + str(screen_header) + " | wc -l"
    #print("Screen -list command - " + str(screen_list_command))
    number_of_listed_screens = _system_executor(screen_list_command)
    #print("Command output - " + number_of_listed_screens)
    try:
        number_of_listed_screens = int(number_of_listed_screens)
    except:
        number_of_listed_screens = 0
    return number_of_listed_screens

def _check_is_screen_already_spawned(screen_name, verbosity):
    screen_name.rstrip()
    sys_command_for_execution = "screen -ls | grep \""+screen_name+"\""
    screen_session_is_alive = False
    screen_list_output = _system_executor(sys_command_for_execution)
    if screen_name in screen_list_output:
        screen_session_is_alive = True
        if verbosity =='y':
            helpers._print_norm_red("Screen under same name is running !!!!  : ", screen_list_output)
    return screen_session_is_alive