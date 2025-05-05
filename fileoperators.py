import sys
import os
#from pathlib import Path
#import platform
import shutil
from termcolor import cprint
import helpers
def _read_from_file(filename_and_path):
	f = open(filename_and_path,"r")
	file_data = f.readlines()
	f.close()
	return file_data
def _die_if_file_not_exist(filename_and_path,verbosity):
	exist_check = _check_if_file_exits(filename_and_path,verbosity)
	if 	not exist_check:
			sys.exit("File \""+filename_and_path+"\" file is missing - EXITING !!!")
def _check_if_file_exits(filename_and_path,verbosity):
	exist_answer = False
	#platformos = platform.platform()
	if os.path.exists(filename_and_path) and os.path.isfile(filename_and_path):
		exist_answer = True
	if verbosity == 'y' and not exist_answer:
		helpers._print_norm_red("The following file does NOT exist !!! = ", filename_and_path)
	return exist_answer
def _check_if_folder_exits(folder_full_path,verbosity):
	exist_answer = False
	if verbosity == 'y':
		print("Checking if the following folder exists = ", end = ''),cprint(folder_full_path,'red',attrs=['bold'])
	if os.path.exists(folder_full_path) and os.path.isdir(folder_full_path):
		exist_answer = True
	if verbosity == 'y' and exist_answer:
		print("The following folder exists !!! = ", end = ''),cprint(folder_full_path,'red',attrs=['bold'])
	elif verbosity == 'y':
		print("The following folder does NOT exist !!! = ", end = ''),cprint(folder_full_path,'red',attrs=['bold'])
	return exist_answer
def _create_non_exsisting_sub_directory(folder_full_path,verbosity):
	exit_status = True
	if verbosity =='y':
		print ("Direcoty ", end = ''),cprint (folder_full_path,'red',attrs=['bold'], end = ''),print (" checking if exist ?!")
	if not os.path.exists(folder_full_path):
		if verbosity =='y':
			print ("Verified directory ", end = ''),cprint (folder_full_path,'red',attrs=['bold'], end = ''),print (" doesn't exist !!!")
			cprint ("Recreating !!!",'red',attrs=['bold'])
		try:
			os.makedirs(folder_full_path)
		except OSError:
				print ("Creation of the directory %s failed" % folder_full_path)
				exit_status = False
		else:
			if verbosity =='y':
				print ("Successfully created the directory %s" % folder_full_path)
	return exit_status
def _copy_directory_to_directory(source_directory, destination_directory, verbosity):
	#print("_copy_directory_to_directory(" + source_directory + "," + destination_directory +"," + verbosity+")")
	exit_status = True
	if verbosity =='y':
		helpers._print_norm_blue("Source " + source_directory, " - checking if exist")
	if not os.path.exists(source_directory):
		exit_status = False
		helpers._print_norm_red("Source " + source_directory, " - doesn't exist !!!")
	if verbosity =='y':
		helpers._print_norm_blue("Destination " + destination_directory, " - checking if exist")
	if os.path.exists(destination_directory):
		exit_status = False
		helpers._print_norm_red("Destination " + destination_directory, " - exist - skipping copy !!!")
	if verbosity =='y' and exit_status:
		helpers._print_norm_blue("Coping - " + source_directory, " - to - " +destination_directory )
	if exit_status:
		try:
			status = shutil.copytree(source_directory, destination_directory, symlinks=True)
		except OSError:
			helpers._print_norm_blue_red("Copy of - " + source_directory, " - to - " + destination_directory,
										 " - Failed !!!")
			exit_status = False
		else:
			if verbosity =='y':
				helpers._print_norm_blue_green("Copy of - " + source_directory, " - to - " + destination_directory,
											  " - Succeeded !")
	return exit_status
def _copy_file_to_file(source_file, destination_file, verbosity):
	#print("_copy_file_to_file(" + source_file + ", " + destination_file + ", " + verbosity + ")")
	exit_status = True
	if verbosity =='y':
		helpers._print_norm_blue("Source " + source_file, " - checking if exist")
	if not os.path.isfile(source_file):
		exit_status = False
		helpers._print_norm_red("Source " + source_file, " - doesn't exist !!!")
	if verbosity =='y':
		helpers._print_norm_blue("Destination " + destination_file, " - checking if exist")
	if os.path.isfile(destination_file):
		exit_status = False
		helpers._print_norm_red("Destination " + destination_file, " - exist - skipping copy !!!")
	if verbosity =='y' and exit_status:
		helpers._print_norm_blue("Coping - " + source_file, " - to - " + destination_file)
	if exit_status:
		try:
			#print("shutil.copy(" + source_file + "," + destination_file + ")")
			shutil.copy(source_file, destination_file)
		except OSError:
			helpers._print_norm_blue_red("Copy of - " + source_file, " - to - " + destination_file,
										 " - Failed !!!")
			exit_status = False
		else:
			if verbosity =='y':
				helpers._print_norm_blue_green("Copy of - " + source_file, " - to - " + destination_file,
											  " - Succeeded !")
	return exit_status
def _append_vector_by_core_map_to_file(chromosome_vector, map_template, config_file, verbosity):
	exit_status = True
	genome_vector_counter = 0
	map_length = len(map_template)
	map_width = len(map_template[0])
	#print(chromosome_vector)
	#print(len(chromosome_vector))
	if verbosity =='y':
		helpers._print_norm_blue("Trying to append data into file - " , config_file)
	try:
		file = open(config_file, 'a')
		for i in range(map_length):
			for j in range(map_width):			#_print(line)
				if map_template[i][j] == 1:
					file.write(str(chromosome_vector[genome_vector_counter]) + " ")
					#file.write("%s ")
					genome_vector_counter += 1
				else:
					#file.write("%s  ")
					file.write("  ")
			#file.write("%s\n")
			file.write("\n")
		file.close()
	except OSError:
		helpers._print_norm_blue_red("Append data into file - ", config_file, " - Failed !!!")
		exit_status = False
	else:
		if verbosity =='y':
			helpers._print_norm_blue_green("Append data into file - ", config_file, " - Succeeded !")
	return exit_status
def _append_file_to_file(source_file, destination_file, verbosity):
	exit_status = True
	if verbosity =='y':
		helpers._print_norm_blue("Trying to append file into file - " + source_file, destination_file)
	try:
		s_file = open(source_file, 'r')
		d_file = open(destination_file, 'a')
		for line in s_file:
			d_file.write(str(line))
			#file.write("\n")
		s_file.close()
		d_file.close()
	except OSError:
		helpers._print_norm_blue_red("Append file into file - " + source_file, destination_file, " - Failed !!!")
		exit_status = False
	else:
		if verbosity =='y':
			helpers._print_norm_blue_green("Append file into file - " + source_file, destination_file, " - Succeeded !")
	return exit_status
def _write_list_to_file(list, file_path_and_name, verbosity):
	exit_status = True
	if verbosity =='y':
		helpers._print_norm_blue("Trying to write data into file - " , file_path_and_name)
	try:
		file = open(file_path_and_name, 'w' )
		for line in list:
			#_print(line)
			file.write("%s\n" % line)
		file.close()
	except OSError:
		helpers._print_norm_blue_red("Write data into file - ", file_path_and_name, " - Failed !!!")
		exit_status = False
	else:
		if verbosity =='y':
			helpers._print_norm_blue_green("Write data into file - ", file_path_and_name, " - Succeeded !")
	return exit_status
def _write_input_to_file(input, file_path_and_name, verbosity):
	exit_status = True
	if verbosity =='y':
		helpers._print_norm_blue("Trying to write input into file - " , file_path_and_name)
	try:
		file = open(file_path_and_name, 'w')
		file.write(input)
		file.close()
	except OSError:
		helpers._print_norm_blue_red("Write input into file - ", file_path_and_name, " - Failed !!!")
		exit_status = False
	else:
		if verbosity =='y':
			helpers._print_norm_blue_green("Write input into file - ", file_path_and_name, " - Succeeded !")
	return exit_status
def _prepare_tmp_working_enviroment(experimets_base_directory, tmp_directory, ffsolver_directory_repo,
									templates_base_directory, verbosity, population_size, population_logic,
									mutation_logic, mutation_type, mating_algorithm, mated_couple_logic,
									offspring_algorithm, number_of_iterations, boundary_conditions, optimization_type, alpha):
	human_time_string = helpers._get_human_time_string()
####	#experiment_results_directory = experimets_base_directory + "/" + human_time_string
	if optimization_type == "alpha":
		optimization_type = "alpha"+str(alpha)
	base_directory_name = ("ps-" + str(population_size) + ".pl-" + str(population_logic) + ".mu-" +
						str(mutation_logic) + ".ma-" + str(mating_algorithm) + ".mcl-" + str(mated_couple_logic) +
						".os-" + str(offspring_algorithm) + ".i-" + str(number_of_iterations) + ".mt-" +
						str(mutation_type) + ".bc-" + str(boundary_conditions) + ".ot-" + str(optimization_type) +
						"." + str(human_time_string))
	experiment_results_directory = str(experimets_base_directory) + "/" + str(base_directory_name)
	tmp_working_directory = str(tmp_directory) + "." + str(base_directory_name)
	#experiment_results_directory = (str(experimets_base_directory) + "/ps-" + str(population_size) + ".pl-" +
	#								str(population_logic) + ".mu-" + str(mutation_logic) + ".ma-" +
	#								str(mating_algorithm) + ".mcl-" + str(mated_couple_logic) + ".os-" +
	#								str(offspring_algorithm) + ".i-" + str(number_of_iterations) + ".mt-" +
	#								str(mutation_type) + ".bc-" + str(boundary_conditions) + ".ot-" +
	#								str(optimization_type) + "." + 	str(human_time_string))
	#tmp_experiment_results_directory = experiment_results_directory + "/tmp"
	#tmp_working_directory = tmp_directory + "." + human_time_string
	#tmp_working_directory = (str(tmp_directory) + ".ps-" + str(population_size) + ".pl-" + str(population_logic) +
	#						 ".ml-" + str(mutation_logic) + ".ma-" + str(mating_algorithm) + ".mcl-" +
	#						 str(mated_couple_logic) + ".os-" + str(offspring_algorithm) + ".i-" +
	#						 str(number_of_iterations) + ".mt-" + str(mutation_type) + ".bc-" +
	#						 str(boundary_conditions) + ".ot-" + str(optimization_type) + "." + str(human_time_string))
	tmp_ffsolver_directory = tmp_working_directory + "/ffsolver"
	tmp_base_ffsolver_directory = tmp_ffsolver_directory + "/base"
	tmp_ffsolver_scores_directory= tmp_ffsolver_directory + "/scores"
	tmp_base_template_directory = tmp_working_directory + "/templates"
	tmp_generations_directory = tmp_working_directory + "/generations"
	#print(experiment_results_directory)
	#sys.exit("exp dir")
	_create_non_exsisting_sub_directory(experiment_results_directory, verbosity)
	#_create_non_exsisting_sub_directory(tmp_experiment_results_directory, verbosity)
	#sys.exit("exp dir")
	_create_non_exsisting_sub_directory(tmp_generations_directory, verbosity)
	_create_non_exsisting_sub_directory(tmp_ffsolver_directory, verbosity)
	_create_non_exsisting_sub_directory(tmp_ffsolver_scores_directory, verbosity)
	_copy_directory_to_directory(ffsolver_directory_repo, tmp_base_ffsolver_directory, verbosity)
	_copy_directory_to_directory(templates_base_directory, tmp_base_template_directory, verbosity)
	if verbosity == "y":
		helpers._print_norm_blue("human_time = ", human_time_string)
		helpers._print_norm_blue("experiment_results_directory = ", experiment_results_directory)
		helpers._print_norm_blue("tmp_working_directory = ", tmp_working_directory)
		helpers._print_norm_blue("tmp_base_template_directory = ", tmp_base_template_directory)
		helpers._print_norm_blue("tmp_ffsolver_directory = ", tmp_ffsolver_directory)
		helpers._print_norm_blue("tmp_ffsolver__scores_directory = ", tmp_ffsolver_scores_directory)
		helpers._print_norm_blue("tmp_base_ffsolver_directory = ", tmp_base_ffsolver_directory)
		helpers._print_norm_blue("tmp_generations_directory = ", tmp_generations_directory)
	return (experiment_results_directory, tmp_working_directory,
			tmp_ffsolver_directory, tmp_ffsolver_scores_directory, tmp_base_ffsolver_directory,
			tmp_base_template_directory, tmp_generations_directory, human_time_string)
def _prepare_singlerun_directory(tmp_base_ffsolver_directory, singlerun_directory, verbosity):
	_copy_directory_to_directory(tmp_base_ffsolver_directory, singlerun_directory, verbosity)
def _remove_file(filename_and_path, verbosity):
	if _check_if_file_exits(filename_and_path,verbosity):
		os.remove(filename_and_path)
def _remove_directory(directory_path, verbosity):
	if _check_if_folder_exits(directory_path,verbosity):
		#os.rmdir(directory_path)
		shutil.rmtree(directory_path)

def _write_to_file(file_name, data_to_append):
	f = open(file_name, "a")
	f.write(data_to_append)
	f.close()

#def _get_keff_and_runtime(ff_log_file, verbosity):
#	for line in _read_from_file(ff_log_file):
