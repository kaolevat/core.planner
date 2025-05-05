###! /home/kaolevat/miniconda3/envs/core.planner.env/bin/python
import sys
import argsandvars
import helpers
import evolution
import fileoperators
import drawers
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    print("############################ Main - static_vars_list ###########################")
    static_vars_list = argsandvars._static_variables_set()
    print("########################### Main - users_vars_list #############################")
    users_args_list = argsandvars._get_arguments()
    print("########################### Main - _check_arguments ############################")
    argsandvars._check_arguments(users_args_list, static_vars_list)
    print("############################# Main - _merge_arguments ##########################")
    merged_variables = argsandvars._merge_variables(static_vars_list, users_args_list)
    #sys.exit("Die after merge")
    print("######################## Main - _generate_run_directories ######################")
    (experiment_results_directory, tmp_working_directory, tmp_ffsolver_directory, tmp_ffsolver_scores_directory,
    tmp_base_ffsolver_directory, tmp_base_template_directory, tmp_generations_directory,
     human_time_string) = fileoperators._prepare_tmp_working_enviroment(
                                                        merged_variables.experimets_base_directory,
                                                        merged_variables.tmp_directory,
                                                        merged_variables.ffsolver_directory_repo,
                                                        merged_variables.templates_base_directory,
                                                        merged_variables.verbosity,
                                                        merged_variables.population_size,
                                                        merged_variables.population_logic,
                                                        merged_variables.mutation_logic,
                                                        merged_variables.mutation_type,
                                                        merged_variables.mating_algorithm,
                                                        merged_variables.mated_couple_logic,
                                                        merged_variables.offspring_algorithm ,
                                                        merged_variables.number_of_iterations,
                                                        merged_variables.boundary_conditions,
                                                        merged_variables.optimization_type,
                                                        merged_variables.alpha)
    ##helpers._pause() ###
    print("################### Main - Initiating all operational Variables ################")
    generations_counter = 0
    generations_longstring_counter = str(0)
    generations = []
    best_keff_scores = []
    best_ppf_scores = []
    best_alpha_scores = []
    average_keff_scores = []
    average_ppf_scores = []
    average_alpha_scores = []
    worst_keff_scores = []
    worst_ppf_scores = []
    worst_alpha_scores = []
    variance_scores = []
    standart_diviation_Keff_scores = []
    similarities_counts_list = []
    number_of_similarity_groups_list = []
    similarities_array = []
    ffsolver_avarage_runtimes = []
    total_runtimes = []
    evolution_flag = True
    total_number_of_mutations = 0
    #print("######################## Main - Generating 1st generation ######################")
    #population = evolution._initialization(merged_variables.population_size, merged_variables.core_map_array,
    #                          merged_variables.core_map_viable_number_of_fa_slots,
    #                          merged_variables.number_of_fa_types,
    #                          merged_variables.amounts_of_each_fa_type)
    while evolution_flag:
        if generations_counter == (merged_variables.number_of_iterations - 1):
            evolution_flag = False
        round_start_time_in_seconds = helpers._get_current_time_in_seconds()
        ## Create a Long 0000XY counter for generations - good for computational comparisons ##
        generations_longstring_counter = str(generations_counter)
        for index in range(len(str(merged_variables.number_of_iterations))):
            if index > (len(str(generations_counter)) - 1):
                generations_longstring_counter = str(0) + str(generations_longstring_counter)
        #######################################################################################
        if generations_counter == 0:
            print("######################## Main - Generating 1st generation ######################")
            population = evolution._initialization(merged_variables.population_size, merged_variables.core_map_array,
                              merged_variables.core_map_viable_number_of_fa_slots,
                              merged_variables.number_of_fa_types,
                              merged_variables.amounts_of_each_fa_type)
        else:
            print("########################## Main - Mating/Crossover #############################")
            next_population = evolution._mating_crossover(population_summary, ordered_population_by_memebrs_id,
                                                #ordered_population_scores,
                                                merged_variables.mating_algorithm, merged_variables.mated_couple_logic,
                                                merged_variables.number_of_fa_types,
                                                merged_variables.amounts_of_each_fa_type,
                                                merged_variables.vertical_to_horizontal_positioning_vector,
                                                merged_variables.arrayed_positioning_map,
                                                merged_variables.offspring_algorithm,
                                                generations_counter, merged_variables.number_of_iterations)
            #print(population_summary)
            #sys.exit()
            print("############################### Main - Mutating ################################")
            (mutated_population, total_number_of_mutations, mutations_occurrence_counter) = (
                evolution._mutation(next_population, merged_variables.mutation_logic, merged_variables.mutation_type,
                                    merged_variables.left_shift_addresses_vector,
                                    merged_variables.right_shift_addresses_vector,
                                    merged_variables.up_shift_addresses_vector,
                                    merged_variables.down_shift_addresses_vector,
                                    merged_variables.core_map_array,
                                    merged_variables.number_of_iterations,
                                    generations_counter))
            #print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
            #print(mutated_population)
            #print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
            if merged_variables.population_logic == 'static':
                print("########################## Main - Elitism & Survival ###########################")
                population = evolution._elitism_and_survival(best_chromosome, mutated_population)
            elif (merged_variables.population_logic == 'growing'):
                if (len(best_keff_scores) < 2):
                    print("########################## Main - Elitism & Growing =###########################")
                    population = evolution._elitism_expanding_population(population_summary, mutated_population)
                elif (float(best_keff_scores[generations_counter-1]) > float(best_keff_scores[generations_counter-2])):
                    print("########################## Main - Elitism & Growing =###########################")
                    population = evolution._elitism_expanding_population(population_summary, mutated_population)
                else:
                    print("########################## Main - Elitism & Survival ###########################")
                    population = evolution._elitism_and_survival(best_chromosome, mutated_population)
            else:
                sys.exit("Unknown population logic - " + str(merged_variables.population_logic))
            del next_population, mutated_population
        #print("----------------------------")
        #print(population)
        #print("----------------------------")
        population_size = len(population)
        ##helpers._pause()###
        print("##################### Main - Scoring & Mapping population ######################")
        if len(best_keff_scores) < 1:
            previous_generation_best_keff_score = float(0)
        else:
            previous_generation_best_keff_score = best_keff_scores[-1]
        if len(best_ppf_scores) < 1:
            previous_generation_best_ppf_score = float(9999)
        else:
            previous_generation_best_ppf_score = best_ppf_scores[-1]
        if (len(best_alpha_scores) <1) and (merged_variables.alpha > -1):
            previous_generation_best_alpha_score = float(0)
        else:
            previous_generation_best_alpha_score = best_alpha_scores[-1]
        (population_summary, ordered_population_by_memebrs_id,
         ordered_population_keff_scores, best_keff_score, average_keff_score, worst_keff_score,
         variance, avarage_runtime, count_of_1, count_of_2, count_of_3,
         ordered_population_ppf_scores, best_ppf_score, average_ppf_score, worst_ppf_score,
         ordered_population_alpha_scores, best_alpha_score, average_alpha_score, worst_alpha_score) =\
            evolution._parallel_population_scoring_ordering_and_logging(
                                                                merged_variables.optimization_type,
                                                                population, generations_counter,
                                                                generations_longstring_counter,
                                                                merged_variables.core_map_array,
                                                                experiment_results_directory, tmp_generations_directory,
                                                                tmp_base_ffsolver_directory,
                                                                tmp_ffsolver_scores_directory,
                                                                merged_variables.ffsolver_exec_command,
                                                                merged_variables.ffsolver_config_file_name,
                                                                merged_variables.boundary_conditions,
                                                                merged_variables.ffsolver_config_header_file_name,
                                                                merged_variables.ffsolver_config_ender_file_name,
                                                                tmp_base_template_directory,
                                                                merged_variables.base_directory,
                                                                population_size, previous_generation_best_keff_score,
                                                                previous_generation_best_ppf_score,
                                                                previous_generation_best_alpha_score,
                                                                merged_variables.number_of_parallel_threads,
                                                                human_time_string, merged_variables.save_results_flag,
                                                                merged_variables.number_of_reactor_core_rows,
                                                                merged_variables.alpha,
                                                                merged_variables.verbosity)
        ##helpers._pause()
        best_chromosome = population_summary[0][4]
        print("============================= Generational Summery =============================")
        round_end_time_in_seconds = helpers._get_current_time_in_seconds()
        generations.append(generations_counter)
        best_keff_scores.append(float(best_keff_score))
        best_ppf_scores.append(float(best_ppf_score))
        best_alpha_scores.append(float(best_alpha_score))
        average_keff_scores.append(float(round(average_keff_score,6)))
        average_ppf_scores.append(float(average_ppf_score))
        average_alpha_scores.append(float(average_alpha_score))
        worst_keff_scores.append(float(worst_keff_score))
        worst_ppf_scores.append(float(worst_ppf_score))
        worst_alpha_scores.append(float(worst_alpha_score))
        variance_scores.append(variance)
        total_runtimes.append(round_end_time_in_seconds - round_start_time_in_seconds)
        standart_diviation_Keff = statistics.stdev(ordered_population_keff_scores)
        standart_diviation_Keff_scores.append(standart_diviation_Keff)
        (similarities_amount, number_of_similarity_groups) = evolution._population_full_comparison_similarities(population)
        similarities_counts_list.append(similarities_amount)
        number_of_similarity_groups_list.append(number_of_similarity_groups)
        print("Generation - " + str(generations_longstring_counter) + "/" + str(merged_variables.number_of_iterations)
                                                                        + ", Population size - " + str(len(population)))
        #print("Generation - " + str(generations_counter) + ", Population size - " + str(len(population)))
        print("Total number of mutations - " + str(total_number_of_mutations) + " - with distribution of:")
        if not generations_counter == 0:
            print("Number of - 0z=" + str(mutations_occurrence_counter[0]) + " - 1z=" + str(mutations_occurrence_counter[1]) +
              " - 2z=" + str(mutations_occurrence_counter[2]) + " - 3z=" + str(mutations_occurrence_counter[3]) +
              " - 4z++=" + str(mutations_occurrence_counter[4]) + " - #shifts=" + str(mutations_occurrence_counter[5]))
        print("Keff Scores - Best - " + str(best_keff_score) + " - Avrg - " + str(round(average_keff_score,6)) + " - Worst - " + str(worst_keff_score))
        print("PPF Scores  - Best - " + str(best_ppf_score) + " - Avrg - " + str(round(average_ppf_score,6)) + " - Worst - " + str(worst_ppf_score))
        print("Alpha Score - Best - " + str(best_alpha_score) + " - Avrg - " + str(round(average_alpha_score,6)) + " - Worst - " + str(worst_alpha_score))
        print("Variance - " + str(round(variance,6)) + " and Keff standard deviation - " + str(round(standart_diviation_Keff,6)))
        print("Counts of - 1z=" + str(count_of_1) + " - 2z=" + str(count_of_2) + " - 3z=" + str(count_of_3))
        print("Total count if identical - " + str(similarities_amount) + " - Distributed between #"
              + str(number_of_similarity_groups) + " groups")
        print("Total time for this round (sec) - " + str(round_end_time_in_seconds - round_start_time_in_seconds))
        print("================================================================================")
        print("============================ Plotting Histograms ===============================")
        ######################### Plotting by Keff #######################
        y1_array = []
        y1_array.append(best_keff_scores)
        y1_array.append(average_keff_scores)
        y1_array.append(worst_keff_scores)
        y1_label_list = ['Best Scores', 'Average Scores', 'Worst Scores']
        y2 = variance_scores
        y2_label = "Population Variance"
        tmp_plot_file_name = drawers._plot_linear_histogram(generations, y1_array, y1_label_list, y2, y2_label,
                                                            tmp_generations_directory, generations_longstring_counter)# generations_counter)
        fileoperators._copy_file_to_file(tmp_plot_file_name, experiment_results_directory + "/PopVar.Keff.Summary.UptoGen." +
                                         str(generations_longstring_counter) + ".jpeg",
                                         merged_variables.verbosity)
        y2 = standart_diviation_Keff_scores
        y2_label = "Keff Standard Deviation"
        tmp_plot_file_name = drawers._plot_linear_histogram(generations, y1_array, y1_label_list, y2, y2_label,
                                                            tmp_generations_directory, generations_longstring_counter)#, generations_counter)
        fileoperators._copy_file_to_file(tmp_plot_file_name, experiment_results_directory + "/KeffSTD.Summary.UptoGen." +
                                         str(generations_longstring_counter) + ".jpeg", merged_variables.verbosity)
        ######################### Plotting by PPF #######################
        y1_array = []
        y1_array.append(best_ppf_scores)
        y1_array.append(average_ppf_scores)
        y1_array.append(worst_ppf_scores)
        y1_label_list = ['Best Scores', 'Average Scores', 'Worst Scores']
        y2 = variance_scores
        y2_label = "Population Variance"
        tmp_plot_file_name = drawers._plot_linear_histogram(generations, y1_array, y1_label_list, y2, y2_label,
                                                            tmp_generations_directory, generations_longstring_counter)# generations_counter)
        fileoperators._copy_file_to_file(tmp_plot_file_name, experiment_results_directory + "/PopVar.PPF.Summary.UptoGen." +
                                         str(generations_longstring_counter) + ".jpeg",
                                         merged_variables.verbosity)
        ######################### Similarities Plot #######################
        similarities_array = []
        similarities_array.append(similarities_counts_list)
        header = "Similarities UptoGen - " + str(generations_longstring_counter)
        similarities_array.append(number_of_similarity_groups_list)
        y_list = [similarities_counts_list[generations_counter] , number_of_similarity_groups_list[generations_counter]]
        #bins_list = ['SimSum','#GRPs']
        y1_label = 'Total Sum of Similarities'
        y2_label = 'Number of Similarity Groups'
        sim_label_list = [y1_label, y2_label]
        tmp_header = 'Similarity'
        tmp_sim_file_name = (tmp_generations_directory + "/Similarity.Summary.Gen."
                               + str(generations_longstring_counter) + ".jpeg")
        sim_file_name = (experiment_results_directory + "/Similarity.Summary.Gen."
                               + str(generations_longstring_counter) + ".jpeg")
        drawers._2parameters_histogram(y_list, y1_label, y2_label, tmp_header, population_size, tmp_sim_file_name)
        fileoperators._copy_file_to_file(tmp_sim_file_name, sim_file_name, merged_variables.verbosity)
        similaties_over_time_file_name = (experiment_results_directory + "/Similarity.Over.Time.UptoGen."
                               + str(generations_longstring_counter) + ".jpeg")
        ##tmp_similaties_over_time_file_name = drawers._plot_linear_histogram(generations,similarities_array,  sim_label_list, False, False,
        ##                                                    tmp_generations_directory, generations_longstring_counter)
        tmp_similaties_over_time_file_name = drawers._singlesidesY_plot_linear_histogram(generations,
                                                                                         similarities_array,
                                                                                         sim_label_list,
                                                                                         header,
                                                                                         tmp_generations_directory,
                                                                                         generations_counter)
        fileoperators._copy_file_to_file(tmp_similaties_over_time_file_name, similaties_over_time_file_name,
                                          merged_variables.verbosity)
        #print("HistogramOfScoresGen")
        ################ Over Time drawings #################################
        _Keff_scaled_histograma_file_name = (tmp_generations_directory + "/HistogramOfScoresGen."
                                             + str(generations_longstring_counter) + ".jpeg")
        drawers._Keff_scaled_histograma_by_population(ordered_population_keff_scores, _Keff_scaled_histograma_file_name,
                                                      generations_counter)
        fileoperators._copy_file_to_file(_Keff_scaled_histograma_file_name,
                                         experiment_results_directory + "/Keff_Histogram.Gen."
                                         + str(generations_longstring_counter)
                                         + ".jpeg", merged_variables.verbosity)
        generations_counter += 1
    print("============================ Creating a Movie Clip =============================")
    movie_core_evolution_per_generation_file = drawers._movie_maker(tmp_generations_directory, "Clipmap", experiment_results_directory)
    movie_core_evolution_per_change_file = drawers._movie_maker(tmp_generations_directory, "ChangeOnly", experiment_results_directory)
    movie_Keff_evolution_per_generation_file = drawers._movie_maker(tmp_generations_directory, "HistogramOfScoresGen", experiment_results_directory)
    movie_similarities_oscilations_file = drawers._movie_maker(tmp_generations_directory, "Similarity.Summary.Gen", experiment_results_directory)
    side_by_side_movie_file = str(experiment_results_directory) + "/side_by_side" + ".mp4"
    drawers._side_by_side_movie_maker(movie_core_evolution_per_generation_file, movie_Keff_evolution_per_generation_file, side_by_side_movie_file)
    print("============================ Saving Final Results ==============================")
    print("Scores:")
    print("Best - " + str(best_keff_scores))
    fileoperators._write_list_to_file(best_keff_scores, tmp_generations_directory + "/best_keff_scores.txt", merged_variables.verbosity)
    fileoperators._write_list_to_file(best_keff_scores, experiment_results_directory + "/best_keff_scores.txt", merged_variables.verbosity)
    print("Avarage - " + str(average_keff_scores))
    fileoperators._write_list_to_file(average_keff_scores, tmp_generations_directory + "/average_keff_scores.txt", merged_variables.verbosity)
    fileoperators._write_list_to_file(average_keff_scores, experiment_results_directory + "/average_keff_scores.txt", merged_variables.verbosity)
    print("Worst - " + str(worst_keff_scores))
    fileoperators._write_list_to_file(worst_keff_scores, tmp_generations_directory + "/worst_keff_scores.txt", merged_variables.verbosity)
    fileoperators._write_list_to_file(worst_keff_scores, experiment_results_directory + "/worst_keff_scores.txt", merged_variables.verbosity)
    print("Variance - " + str(variance_scores))
    fileoperators._write_list_to_file(variance_scores, tmp_generations_directory + "/variance_scores.txt", merged_variables.verbosity)
    fileoperators._write_list_to_file(variance_scores, experiment_results_directory + "/variance_scores.txt", merged_variables.verbosity)
    #sys.exit("################### Main - exit #####################")
    #helpers._print_norm_red("Note - ","This script is under construction and in the initial stage of the project, try utilizing the -h or --help flag for more information")
##################################################################################
############## Run Env ###########################################################
if __name__ == "__main__":
        main()
        sys.exit(0)
############## Run Env ###########################################################
##################################################################################