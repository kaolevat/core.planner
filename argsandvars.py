
import argparse
import helpers
import sys
import fileoperators
import numpy as np
#import re
# def _variable_list():
class _static_variables_set:
    base_directory  = "/home/kaolevat/PycharmProjects/core.planner"
    base_tmp_directory = "/dev/shm/tmp"
    logs_directory  = base_directory+"/logs"
    screen_conf_directory = base_directory+"/screenconfs"
    screen_logs_directory = base_directory+"/screenlogs"
    experimets_base_directory = base_directory+"/../../core.planner.experiments"
    #experimets_base_directory = "/coldstorage/kaolevat/core.planner.experiments"
    #binaries_directory = base_directory+"/binaries"
    templates_base_directory = base_directory+"/templates"
    ffsolver_directory_repo = base_directory + "/ffsolver/base"
    ffsolver_config_header_file_name = "header_kref_kin.dat"
    ffsolver_config_ender_file_name = "ender_kref_kin.dat"
    ffsolver_config_file_name = "kref_kin.dat"
    ffsolver_exec_command = "./DYN3D ./kref ./kref"
    tmp_directory = base_tmp_directory + "/core.planner"
    history_size = 360
    skip_chars = ('!!', '==', '**', '#')
    # ######## Hard limits ###########
    # It would be wise to rewrite this secion via a config file in the future
    number_of_iterations_limit = 100000
    number_of_parallel_threads_limit = 320
    minimal_viable_fuel_assembly_concentration = 0
    maximal_viable_fuel_assemply_concentration = 100
    population_size_minimal_limit = 2
    population_size_maximal_limit = 1000
    valid_map_chars = "0-1"

    # ######## Hard coded limits ###########
def _get_arguments():
        # define format and general descrtiption
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                         description="This core planner script strives to provide a reactor core optimization focusing on the following criteria" +
                                                     " a) Optimize reactivity (Keff)\n" +
                                                     " b) Optimize uniformity of activity (PPF) to minimize variations and extremes in the power distribution\n" +
                                                     " c) Optimize Keff and PPF under specific linear ratio")

        #parser.add_argument('-m', '--map',
        #        help="Path to a config file map of a core of a reactor.\n"
        #                "Default core map is based on 15x15 core with 257 Fuel Assemblies (FAs)",
        #        dest='core_map_file',
        #        default='./default.map',
        #        required=False)
        parser.add_argument('-m', '--map',
                    help="Path to reactor core map configuration file.\n"
                         "Default map is 17x17 core with 257 Fuel Assemblies (FAs).",
                    dest='core_map_file',
                    default='./default.map',
                    required=False)
        parser.add_argument('-fa', '--fa-types',
                #help='This flag provides the variance in percentrage numbers of the concentration of U235 within the fuel assembly \n in the reactor, '
                #            #'Specifies the variance in percentage concentrations of U235 within the fuel assemblies in the reactor. '
                #            #'Provide the values as percentages, delimited by %. '
                #            'Example: 1.6%%2.4%%3.1%%. Default is 1.6%%2.4%%3.1%%.',
                #            #and delimited as follows: FA1%FA2%FA3%FA4 , were in place of FA is a real number.\n Minimal number of FAs is 3 and maximal number of FAs is 5.\n Default is: 1.6%2.4%3.1%',
                help='Percentage concentrations of U235 in fuel assemblies.'
                         'Provide the values as percentages, delimited by %%. '  
                         'Example: 1.6%%2.4%%3.1%%. Default is 1.6%%2.4%%3.1%%.',
                dest='fuel_assembly_concentrations',
                default='1.6%2.4%3.1%',
        #        #default='1.6-2.4-3.1',
                required=False)
        parser.add_argument('-nfa', '--fa-amounts', '--number-of-fas',
                help='Number of fuel assemblies per type. '
                     'The definition is delimited as follows: NFA1-NFA2-NFA3-NFA4 , were in place of NFA is an integer that represents the number of fuel assemblies of the type in FA1,2,3,4 respectrully '
                     '(see -fa of FA types). The sum of the integers required to correlate to the number of active slots within the core (see -m map), or 193 in a 15x15 default map.',
                dest='fuel_assembly_amounts',
                default='86-86-85',
                required=False)
        parser.add_argument('-ps', '--population-size',
                help='Population size for evolution. ',
                dest='population_size',
                type=int,
                default=100,
                required=False)
        parser.add_argument('-pl', '--population-logic',
                help='Population logic: static or growing. ',
                choices=['static', 'growing'],
                dest='population_logic',
                default='static',
                required=False)
        parser.add_argument('-bc', '--boundary-conditions',
                help='Neutron boundary conditions: void(all neutrons escape) or reflective(all neutrons are reflected back). ',
                choices=['void', 'reflective'],
                dest='boundary_conditions',
                default='void',
                required=False)
        parser.add_argument('-ml', '--mutation-logic',
                help='Mutation logic - specifies the probability of mutation to occur in chromosome and the amount/type of mutations',
                dest='mutation_logic',
                choices=['constant', 'assured', 'proportional', 'none', 'progressing', 'min1proportional', 'min1progressing'],
                default='constant',
                required=False)
        parser.add_argument('-mt', '--mutation-type',
                help='Type of mutation.',
                dest='mutation_type',
                choices=['switch', 'shift', 'switchORshift', 'switchANDshift', 'switchORDIMshift'],
                default='switch',
                required=False)
        parser.add_argument('-ma', '--mating-algorithm',
                help='Mating algorithm. ',
                choices=['random', 'weighted-random', 'alpha-fe-male-by-generation'],# 'weighted-by-score'],
                dest='mating_algorithm',
                type=str,
                default='weighted-random',
                required=False)
        parser.add_argument('-mcl', '--mated-couple-logic',
                help='Mated couple logic - selects if a couple members can be mated with themselves',
                choices=['inclusive', 'exclusive', 'combination'],
                dest='mated_couple_logic',
                default='exclusive',
                required=False)
        parser.add_argument('-os', '--offspring-algorithm',
                help='Offspring algorithm - selects how the crossover of two members is performed. ',
                choices=['single-slice', 'random', 'double-slice', 'vertical-double-slice', '2-double-random',
                         '3random', 'quadrad', 'weighted-quadrat', 'square321', 'square321byG','square1x1'],#'mutation-only', 'multi-mutation-only'],
                dest='offspring_algorithm',
                default='square321',
                required=False)
        parser.add_argument('-i', '--iterations','-g', '--generations',
                help='Max number of generations/iterations',
                dest='number_of_iterations',
                type=int,
                default=100,
                required=False)
        parser.add_argument('-p', '--parallel',
                help='Max number of parallel threads. ',
                type=int,
                dest='number_of_parallel_threads',
                default=10)
        parser.add_argument('-sv', '--save-results',
                help='Save results: only the best or all.',
                dest='save_results_flag',
                choices=['only_the_best', 'all'],
                default='only_the_best')
        parser.add_argument('-ot', '--optimization-type',
                help='Optimization type: Keff, PPF, or alpha.',
                dest='optimization_type',
                choices=['keff', 'ppf', 'alpha'],
                default='keff')
        parser.add_argument('-v', '--verbose',
                help='Verbose output: y or n.',
                dest='verbosity',
                choices=['y', 'n'],
                default='n')
        parser.add_argument('-alpha',
                help='Combination ratio for Keff & PPF.',
                dest='alpha',
                type=float,
                default='0.5')
        args = parser.parse_args()
        return args
def _check_arguments(users_args_list, static_vars_list):
    check_flag = True
    parallel_check_flag = True
    iterations_check_flag = True
    population_check_flag = True
    core_map_check_flag = True
    fa_amounts_check_flag = True
    fa_concentrations_check_flag = True
    #print (users_args_list)
    #sys.exit("zzzz")
    # Checking # of parallel limit upheld - see hardcoded few lines above
    if not _check_parallelization_limit(users_args_list.number_of_parallel_threads,
                                        static_vars_list.number_of_parallel_threads_limit):
        check_flag = False
        parallel_check_flag = False
    if not _check_population_size(users_args_list.population_size, static_vars_list.population_size_minimal_limit,
                                  static_vars_list.population_size_maximal_limit):
        check_flag = False
        population_check_flag = False
    if not _check_iterations_limit(users_args_list.number_of_iterations,
                                   static_vars_list.number_of_iterations_limit):
        check_flag = False
        iterations_check_flag = False
    #print("-------------------------------")
    #print(static_vars_list.templates_base_directory +"/" + users_args_list.core_map_file)
    if not _check_map_file(static_vars_list.templates_base_directory +"/" + users_args_list.core_map_file, static_vars_list.valid_map_chars,
                           users_args_list.verbosity, static_vars_list.skip_chars):
        check_flag = False
        core_map_check_flag = False
    #print("-------------------------------")
    if not _check_valid_concentration_in_fuel_assembly(users_args_list.fuel_assembly_concentrations,
                                                       static_vars_list.minimal_viable_fuel_assembly_concentration,
                                                       static_vars_list.maximal_viable_fuel_assemply_concentration,
                                                       users_args_list.verbosity):
        check_flag = False
        fa_concentrations_check_flag = False
    #print("-------------------------------_check_valid_amount_of_fuel_assemblies")
    if not _check_valid_amount_of_fuel_assemblies(users_args_list.fuel_assembly_amounts,
                                                  users_args_list.fuel_assembly_concentrations,
                                                  static_vars_list.templates_base_directory +"/" +
                                                  users_args_list.core_map_file, users_args_list.verbosity):
        check_flag = False
        fa_amounts_check_flag = False
    #print("-------------------------------")
    if not check_flag or (users_args_list.verbosity == 'yes') or (users_args_list.verbosity == 'y'):
        print('Checking the following received arguments:')
        helpers._print_norm_blue_green("   Type of optimization to perform: ",
                                       "type_of_optimization=" + users_args_list.optimization_type,
                                       " - Parser Verified")
        # Verify Map Validity
        #print("-------------------------------Verify Map Validity")
        if core_map_check_flag:
            helpers._print_norm_blue_green("   Path to file of the core map: ",
                                           "core_map=" + users_args_list.core_map_file, " - Passed")
        else:
            helpers._print_norm_blue_red("   Path to file of the core map: ",
                                         "core_map=" + users_args_list.core_map_file, " - Failed !!!")
        # Verify FAs concentrations
        #print("-------------------------------Verify FAs concentrations")
        if fa_concentrations_check_flag:
            helpers._print_norm_blue_green("   Fuel assembly concentrations: ",
                                           "fuel_assembly_concentrations=" + users_args_list.fuel_assembly_concentrations,
                                           " - Passed")
        else:
            helpers._print_norm_blue_red("   Fuel assembly concentrations: ",
                                         "fuel_assembly_concentrations=" +
                                         users_args_list.fuel_assembly_concentrations,
                                         " - Failed!!!")
        if fa_amounts_check_flag:
            helpers._print_norm_blue_green("   Fuel assembly amount: ",
                                           "fuel_assembly_amount=" + users_args_list.fuel_assembly_amounts,
                                           " - Passed")
        else:
            helpers._print_norm_blue_red("   Fuel assembly amount: ",
                                         "fuel_assembly_amount=" + users_args_list.fuel_assembly_amounts,
                                         " - Failed!!!")
        if population_check_flag:
            helpers._print_norm_blue_green("   Population size: ",
                                           "population_size=" + str(users_args_list.population_size),
                                           " - Passed")
        else:
            helpers._print_norm_blue_red("   Population size: ",
                                         "population_size=" + str(users_args_list.population_size),
                                         " - Failed!!!")
        if iterations_check_flag:
            helpers._print_norm_blue_green("   Number of iteration cycles the scripts perform : ",
                                           "number_of_iterations=" +
                                           str(users_args_list.number_of_iterations),
                                           " - Passed - Limit(" +
                                           str(static_vars_list.number_of_iterations_limit)+")")
        else:
            helpers._print_norm_blue_red("   Number of iteration cycles the scripts perform : ",
                                         "number_of_iterations=" + str(users_args_list.number_of_iterations),
                                         " - Failed - Limit(" + str(static_vars_list.number_of_iterations_limit) + ")")
        if parallel_check_flag:
            helpers._print_norm_blue_green("   Number of parallel threads permitted : ",
                                           "number_of_parallel_threads=" + str(users_args_list.number_of_parallel_threads),
                                           " - Passed - Limit("+str(static_vars_list.number_of_parallel_threads_limit)+")")
        else:
            helpers._print_norm_blue_red("   Number of parallel threads permitted : ",
                                         "number_of_parallel_threads=" + str(
                                             users_args_list.number_of_parallel_threads),
                                         " - Failed - Limit(" +
                                         str(static_vars_list.number_of_parallel_threads_limit) + ")")
        helpers._print_norm_blue_green("   Verbosity level : ", "verbose=" + users_args_list.verbosity,
                                       " - Parser Verified")
    #print("-------------------------------end check")
    if not check_flag:
        sys.exit('Some Argument Errors occurred - see the list above - for more information use -v y flags')
class _merge_variables:
    def __init__(self, static_vars,  user_args):
        # Static Variables - exogenic ##################################################################################
        self.base_directory = static_vars.base_directory
        self.logs_directory = static_vars.logs_directory
        self.screen_conf_directory = static_vars.screen_conf_directory
        self.screen_logs_directory = static_vars.screen_logs_directory
        self.experimets_base_directory = static_vars.experimets_base_directory
        #self.binaries_directory = static_vars.binaries_directory
        self.templates_base_directory = static_vars.templates_base_directory
        self.tmp_directory = static_vars.tmp_directory
        self.ffsolver_directory_repo = static_vars.ffsolver_directory_repo

        self.ffsolver_config_header_file_name = static_vars.ffsolver_config_header_file_name
        self.ffsolver_config_ender_file_name = static_vars.ffsolver_config_ender_file_name
        self.ffsolver_config_file_name = static_vars.ffsolver_config_file_name
        self.ffsolver_exec_command = static_vars.ffsolver_exec_command
        self.history_size = static_vars.history_size
        self.skip_chars = static_vars.skip_chars
        self.number_of_iterations_limit = static_vars.number_of_iterations_limit
        self.number_of_parallel_threads_limit = static_vars.number_of_parallel_threads_limit
        self.minimal_viable_fuel_assembly_concentration = static_vars.minimal_viable_fuel_assembly_concentration
        self.maximal_viable_fuel_assemply_concentration = static_vars.maximal_viable_fuel_assemply_concentration
        self.population_size_minimal_limit = static_vars.population_size_minimal_limit
        self.population_size_maximal_limit = static_vars.population_size_maximal_limit
        # User/Experiment Variables - endogenic ########################################################################
        self.optimization_type = user_args.optimization_type
        self.alpha = user_args.alpha
        self.core_map_file = static_vars.templates_base_directory + "/" + user_args.core_map_file
        self.fuel_assembly_concentrations = user_args.fuel_assembly_concentrations
        self.fuel_assembly_number_of_concentration_varieties = _concentrations_in_fuel_assembly_to_number_of_variations(
            self.fuel_assembly_concentrations)
        self.fuel_assembly_amounts = user_args.fuel_assembly_amounts
        self.boundary_conditions = user_args.boundary_conditions
        self.population_size = user_args.population_size
        self.population_logic = user_args.population_logic
        self.mutation_logic = user_args.mutation_logic
        self.mutation_type = user_args.mutation_type
        self.mating_algorithm = user_args.mating_algorithm
        self.mated_couple_logic = user_args.mated_couple_logic
        self.offspring_algorithm = user_args.offspring_algorithm
        self.number_of_iterations = user_args.number_of_iterations
        self.number_of_parallel_threads = user_args.number_of_parallel_threads
        self.save_results_flag = user_args.save_results_flag
        self.verbosity = user_args.verbosity
        # Generated additional Variables ###############################################################################
        (self.core_map_file_existence, self.core_map_list)=_map_file_to_map_list(self.core_map_file,
                                                                                  user_args.verbosity,
                                                                                  static_vars.skip_chars)
        self.core_map_array = _map_list_to_map_array(self.core_map_list)
        self.core_map_viable_number_of_fa_slots = _core_map_array_to_number_of_viable_slots(self.core_map_array)
        (self.vertical_to_horizontal_positioning_vector, self.arrayed_positioning_map) =\
            _chromosome_horizontal_vector_in_vertical_positioning(self.core_map_list)
        (self.right_shift_addresses_vector, self.left_shift_addresses_vector, self.up_shift_addresses_vector,
            self.down_shift_addresses_vector) = _3d_shift_in_vector_addresses(self.arrayed_positioning_map,
                                                                        self.vertical_to_horizontal_positioning_vector)
        self.number_of_fa_types = _concentrations_in_fuel_assembly_to_number_of_variations(self.fuel_assembly_concentrations)
        self.amounts_of_each_fa_type = _amounts_by_each_fuel_assembly(self.fuel_assembly_amounts)
        self.number_of_reactor_core_rows = len(self.arrayed_positioning_map)
        self.number_of_reactor_core_columns = len(self.arrayed_positioning_map[0])

def _3d_shift_in_vector_addresses(tmp_arrayed_positioning_map, tmp_vertical_to_horizontal_positioning_vector):
    map_rows = len(tmp_arrayed_positioning_map)
    map_columns = len(tmp_arrayed_positioning_map[0])
    source_addresses_vector = []
    source_array_addresses_only = []
    right_shift_addresses_vector = []
    right_shift_addresses_array = []
    left_shift_addresses_vector = []
    left_shift_addresses_array = []
    tmp_up_shift_addresses_vector = []
    up_shift_addresses_vector = []
    shift_addresses_array = []
    up_shift_addresses_array = []
    tmp_down_shift_addresses_vector = []
    down_shift_addresses_vector = []
    down_shift_addresses_array = []
    #print(tmp_arrayed_positioning_map)
    for line_number in range(map_rows):
        tmp_vector = []
        for each_char in tmp_arrayed_positioning_map[line_number]:
            if each_char > -1:
                source_addresses_vector.append(int(each_char))
                tmp_vector.append(int(each_char))
        source_array_addresses_only.append(tmp_vector)
        right_shift_addresses_array.append(tmp_vector[-1:] + tmp_vector[:-1])
        left_shift_addresses_array.append(tmp_vector[1:] + tmp_vector[:1])
    for column_number in range(map_columns):
        tmp_vector = []
        for row_number in range(map_rows):
            tmp_char = (int(tmp_arrayed_positioning_map[row_number][column_number]))
            if tmp_char > -1:
                tmp_vector.append(tmp_char)
        down_shift_addresses_array.append(tmp_vector[-1:] + tmp_vector[:-1])
        up_shift_addresses_array.append(tmp_vector[1:] + tmp_vector[:1])
        shift_addresses_array.append(tmp_vector)
    for row_number in range(map_rows):
        for each_char in right_shift_addresses_array[row_number]:
            right_shift_addresses_vector.append(int(each_char))
        for each_char in left_shift_addresses_array[row_number]:
            left_shift_addresses_vector.append(int(each_char))
    for each_vector in up_shift_addresses_array:
        for each_char in each_vector:#down_shift_addresses_array[row_number]:
            tmp_up_shift_addresses_vector.append(int(each_char))
    for each_vector in down_shift_addresses_array:
        for each_char in each_vector:#tmp_up_shift_addresses_vector[row_number]:
            tmp_down_shift_addresses_vector.append(int(each_char))
    tmp_counter = 0
    #print(tmp_vertical_to_horizontal_positioning_vector)
    up_shift_addresses_vector = tmp_vertical_to_horizontal_positioning_vector.copy()
    down_shift_addresses_vector = tmp_vertical_to_horizontal_positioning_vector.copy()
    for tmp_index in tmp_vertical_to_horizontal_positioning_vector:
        #print("...")
        #print(tmp_index)
        #print("...")
        #sys.exit(int(tmp_index))
        up_shift_addresses_vector[tmp_index] = tmp_up_shift_addresses_vector[tmp_counter]
        down_shift_addresses_vector[tmp_index] = tmp_down_shift_addresses_vector[tmp_counter]
        tmp_counter += 1
    #print(tmp_arrayed_positioning_map)
    #p#rint(source_array_addresses_only)
    #print(right_shift_addresses_vector)
    #print(left_shift_addresses_vector)
    #print(down_shift_addresses_vector)
    #print(up_shift_addresses_vector)
    #print(tmp_arrayed_positioning_map)
    return (right_shift_addresses_vector, left_shift_addresses_vector, up_shift_addresses_vector,
            down_shift_addresses_vector)
def _core_map_array_to_number_of_viable_slots(core_map_array):
    number_of_viable_slots = np.count_nonzero(core_map_array == 1)
    #sys.exit("_core_map_array_to_number_of_viable_slots - " + str(number_of_viable_slots))
    return number_of_viable_slots

def _chromosome_horizontal_vector_in_vertical_positioning(core_map_list):
#    horizontal_position_vector = list(range(0, length_of_chromosome))
    arrayed_positioning_map = np.zeros((len(core_map_list), len(core_map_list[1])))    #arrayed_positioning_map = []
    vertical_to_horizontal_positioing_vector = []
    vector_counter = 0
    number_of_lines_in_map = len(core_map_list)
    lenght_of_line_in_map = len(core_map_list[0])
    for line_number in range(number_of_lines_in_map):
        char_position = 0
        for each_char in core_map_list[line_number]:
            if not each_char == '0':
                #print(str(each_char))
                arrayed_positioning_map[line_number,char_position]=int(vector_counter)
                vector_counter += 1
            else:
                arrayed_positioning_map[line_number,char_position]='-1'
            #print(str(int(arrayed_positioning_map[line_number,char_position])) + " ", end=" ")
            char_position += 1
        #print("")
        #print(str(arrayed_positioning_map[line_number]))
    for inline_index in range(lenght_of_line_in_map):
        for line_index in range(number_of_lines_in_map):
            #print("line - " + str(line_index) + " - inline - " + str(inline_index) + " - Map index - " + str(int(arrayed_positioning_map[line_index,inline_index])))
            if not (arrayed_positioning_map[line_index,inline_index] == -1):
                vertical_to_horizontal_positioing_vector.append(int(arrayed_positioning_map[line_index,inline_index]))
    #print(str(horizontal_position_vector))
    #print(str(vertical_to_horizontal_positioing_vector))
    #print(str(arrayed_positioning_map))
    #sys.exit("^ pos vector")
    return vertical_to_horizontal_positioing_vector, arrayed_positioning_map

def _map_list_to_map_array(core_map_list):
    arrayed_map = np.zeros((len(core_map_list), len(core_map_list[1])))
    for line_number in range(len(core_map_list)):
        char_position = 0
        for each_char in core_map_list[line_number]:
            #print(each_char)
            arrayed_map[line_number,char_position]=each_char
            char_position+=1
    #print(str(arrayed_map))
    #sys.exit("^ arraed map")
    return arrayed_map
def _map_file_to_map_list(map_file, verbosity, skip_chars):
    #map=[]
    clean_map=[]
    return_answer = True
    if not fileoperators._check_if_file_exits(map_file, verbosity):
        return_answer = False
        if verbosity == 'y' or verbosity == 'yes':
            helpers._print_norm_red("Failed to locate core map file:", map_file)
    else:
        map=fileoperators._read_from_file(map_file)
        map[:] = [item for item in map if not item.startswith(skip_chars)]
        clean_map = [item.replace('\r', '').replace('\n', '') for item in map]
    #print(str(clean_map))
    #sys.exit("^ clean map")
    return return_answer, clean_map

def _check_offspring_algorithm():
    # need to complete
    return True
def _check_population_size(population_size, minimal_population_size_limit, maximal_population_size_limit):
    # Checking # of population limit upheld
    if population_size < minimal_population_size_limit or population_size > maximal_population_size_limit:
        return False
    else:
        return True
def _check_parallelization_limit(number_of_parallel_threads, number_of_parallel_threads_limit):
        # Checking # of parallel limit upheld
        if number_of_parallel_threads > number_of_parallel_threads_limit:
                return False
        else:
                return True
def _check_iterations_limit(number_of_iterations, number_of_iterations_limit):
        # Checking # of multi-thread limit upheld
        if number_of_iterations > number_of_iterations_limit:
                return False
        else:
                return True

def _check_map_file(map_file, valid_map_chars, verbosity, skip_chars):
    # Test the map file
    # 2. that only 2 types of places viable
        # a. calculate the total number of FA slots
    return_answer = True
    if not fileoperators._check_if_file_exits(map_file, verbosity):
        return_answer = False
        if verbosity == 'y' or verbosity == 'yes':
            helpers._print_norm_red("Failed to locate core map file:", map_file)
    else:
        #map=fileoperators._read_from_file(map_file)
        #map[:] = [item for item in map if not item.startswith(skip_chars)]
        #clean_map = [item.replace('\r', '').replace('\n', '') for item in map]
        (file_answer,map_list) = _map_file_to_map_list(map_file, verbosity, skip_chars)
        if file_answer:
                for line in map_list:
                        if not line.strip().startswith('#') and not line.strip() == "":
                                if not helpers._check_valid_chars_in_line(line, valid_map_chars):
                                        if verbosity == 'y' or verbosity == 'yes':
                                                helpers._print_norm_red("Anomalies detected in line - ",line)
                                        return_answer = False
                if not return_answer:
                        helpers._print_norm_red("Anomalies found in the following map:", map_file)
                        if verbosity == 'y' or verbosity == 'yes':
                                print()
                                helpers._print_norm_red("The following map has anomalies", map_file)
                                for line in map_list:
                                        if not line.strip().startswith('#') and not line.strip() == "":
                                                print(line.rstrip())
                                print()
    return return_answer
def _check_valid_concentration_in_fuel_assembly(fa_concentrations_string,minimal_concentration,maximal_concentration,verbosity):
    return_answer = True
    concentrations=fa_concentrations_string.split('%')
    number_of_concentration=len(concentrations)
    for_counter = 0
    for each_concentration in concentrations:
        for_counter += 1
        if int(number_of_concentration) > int(for_counter):
            try:
                float(each_concentration)
                if float(each_concentration) >= float(maximal_concentration) or float(each_concentration) <= float(minimal_concentration):
                    if (verbosity == 'yes') or (verbosity == 'y'):
                        helpers._print_norm_blue_red("Expecting a number between " + str(minimal_concentration) + " and " + str(maximal_concentration) + " - ", each_concentration,
                                         " - is out of bounds !!!")
                    return_answer = False
            except ValueError:
                if (verbosity == 'yes') or (verbosity == 'y'):
                    helpers._print_norm_blue_red("Expecting numeric concentration - ", each_concentration,
                                                 " - is NOT a number !!!")
                return_answer = False
        else:
            if each_concentration:
                if (verbosity == 'yes') or (verbosity == 'y'):
                    helpers._print_norm_blue_red("Expecting nothing after the last % - ", each_concentration,
                                             " - is NOT empty !!!")
                return_answer = False

    return return_answer
def _concentrations_in_fuel_assembly_to_number_of_variations(fa_concentrations_string):
    concentrations=fa_concentrations_string.split('%')
    length = len(concentrations) - 1
    return length
def _amounts_by_each_fuel_assembly(fa_amounts_string):
    fa_amounts = fa_amounts_string.split('-')
    for i in range(0, len(fa_amounts)):
        fa_amounts[i] = int(fa_amounts[i])
    return fa_amounts
    #length = len(concentrations)
    #return len(concentrations)
def _check_valid_amount_of_fuel_assemblies(fa_amounts_string, fa_concentrations_string, fa_slots_map_file, verbosity):
    return_answer = True
    concentrations=fa_concentrations_string.split('%')
    number_of_concentration=len(concentrations)-1
    amounts=fa_amounts_string.split('-')
    number_of_amounts=len(amounts)
    #print("check amounts" + str(number_of_amounts) + ", " + str(number_of_concentration))
    #print("fa file - " + fa_slots_map_file)
    if not (int(number_of_amounts) == int(number_of_concentration)):
        if (verbosity == 'yes') or (verbosity == 'y'):
            helpers._print_norm_blue_red("Amounts mismatch between concentrations and amounts of fuel assemblies -",
                                            " number of concentration types - " + str(number_of_concentration),
                                            " - number of amount types " + str(number_of_amounts))
            return_answer = False
    else:
        if fileoperators._check_if_file_exits(fa_slots_map_file,verbosity):
            fa_map_text=fileoperators._read_from_file(fa_slots_map_file)
            number_of_fa_slots_in_core=helpers._count_substring_in_text_array(fa_map_text,'1','#')
            #print("number of fa slits in core = " + str(number_of_fa_slots_in_core))
            total_fas_in_agruments = 0
            for fa_type_amount in amounts:
                total_fas_in_agruments += int(fa_type_amount)
            if not number_of_fa_slots_in_core == total_fas_in_agruments:
                return_answer = False
                if (verbosity == 'yes') or (verbosity == 'y'):
                    helpers._print_norm_blue_red("Amounts mismatch between slots in core and amounts of fuel assemblies -",
                                           " number of slots in core - " + str(number_of_fa_slots_in_core),
                                           " - total number of fas " + str(total_fas_in_agruments))
    #sys.exit("_check_valid_amount_of_fuel_assemblies")
    return return_answer

#def _initialzie_weights(length):

