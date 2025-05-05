import sys
import fileoperators
import helpers

#def _ffsolver(ffsolver_base_directory, dedicated_run_directory, header, ender):
#    base_directory = "~/software/ffsolver/base"

def _ffprepare_config_file(pupulation_memebr_vector, core_map_array, dedicated_run_directory,
                           templates_directory, config_file_name, boundary_conditions, file_header, file_ender, verbosity):
    config_file = dedicated_run_directory + "/" + config_file_name
    fileoperators._remove_file(config_file, verbosity)
    header_path_and_file = templates_directory + "/" + boundary_conditions + "/" + file_header
    ender_path_and_file = templates_directory + "/" + boundary_conditions + "/" + file_ender
    fileoperators._copy_file_to_file(header_path_and_file, config_file, verbosity)
    #print(pupulation_memebr_vector)
    #print(core_map_array)
    #print(config_file)
    #sys.exit()
    #print("pre")
    fileoperators._append_vector_by_core_map_to_file(pupulation_memebr_vector, core_map_array, config_file, verbosity)
    #print("post")
    fileoperators._append_file_to_file(ender_path_and_file, config_file, verbosity)
    #print("post22")
#def _ffscore(ffsolver_exec_command, pupulation_memebr_vector, core_map_array, dedicated_run_directory,
#                           templates_directory, config_file_name, file_header, file_ender, verbosity):
#    _ffprepare_config_file(pupulation_memebr_vector, core_map_array, dedicated_run_directory,
#                           templates_directory, config_file_name, file_header, file_ender, verbosity)
#    system_command = "cd " + dedicated_run_directory + "; " + ffsolver_exec_command
##    if verbosity == 'y':
#        helpers._print_norm_blue("Trying to run FF solver - ", system_command)
#    command_output = helpers._system_executor(system_command)
#    results_file = dedicated_run_directory + "/results.log"
#    fileoperators._write_input_to_file(command_output, results_file, verbosity)
#    score = _ffscore_from_input(command_output)
#    return score

def _ffscore_command_and_resultsfile(ffsolver_exec_command, dedicated_run_directory):
    system_command = "cd " + dedicated_run_directory + "; " + ffsolver_exec_command
    results_file = dedicated_run_directory + "/results.log"
    return system_command, results_file

#def _ffscore_by_id(ffsolver_exec_comman, pupulation_memebr_vector, core_map_array, dedicated_run_directory,
#                           templates_directory, config_file_name, file_header, file_ender, verbosity):
#    score = _ffscore(ffsolver_exec_comman, pupulation_memebr_vector, core_map_array, dedicated_run_directory,
#                           templates_directory, config_file_name, file_header, file_ender, verbosity)
#    print("_ffscore_by_id - " + score)
#    return id, score

#def _ffscore_from_input(input):
#    score = -1
#    for line in input.split("\n"):
#        if line.startswith(" ITOU"):
#            score = line.split()[3]
#    return score

#def _ffruntime_from_input(input):
#    runtime = -1
#    for line in input.split("\n"):
#        if line.startswith(" TIME"):
#            runtime = line.split()[2]
#            runtime = runtime.split("E")[0]
#    return runtime

def _ffscore_and_runtime_from_input(input, number_of_reactor_core_rows):
    runtime = -1
    keff_score = -1
    ppf_score = -1
    #line_number = 0
    #keff_line_number = 99999999
    for line in input:#.split("\n"):
        ###print(line)
        #line_number += 1
        ###if line.startswith(" ITOU"):
        ###    score = line.split()[3]
        if line.startswith(' FXY:'):
            ppf_score = line.split()[1]
            #sys.exit("ppf found - " + str(ppf_score))
        if line.startswith(' keff ='):
            #print(line)
            keff_score = line.split()[2]
        #    keff_line_number = line_number
        #if (line_number > keff_line_number) and (line_number < (keff_line_number+(2*number_of_reactor_core_rows))):
        #    #print(line)
        #    if (not line.isspace()):
        #        split_line = line.split()
        #        #print(split_line)
        #        for element in split_line:
        #            float_flag = True
        #            try:
        #                float(element)
        #            except:
        #                float_flag = False
        #                #print(element)
        #            if float_flag:
        #                if(float(element) > float(ppf_score)):
        #                    ppf_score = element
        #####optimization_type == 'ppf':
        if "TIME =" in line:
            runtime = line.split()[2]
            runtime = runtime.split("E")[0]
    #sys.exit(str(keff_score) +","+ str(ppf_score)+ "," + str(runtime))
    return keff_score, ppf_score, runtime