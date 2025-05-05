import sys
import random
import drawers
import fileoperators
import wrappers
import numpy as np
import multiprocessing as mp
import helpers
import sysops
import time
import concurrent.futures
########################################################################################################################
# Initialization of population
########################################################################################################################
def _initialization(population_size, genetic_template, genome_length, number_veriaty_of_coding_bases,
                    distribution_of_coding_bases):
    # population_size = (int) = number parents that will be generated for the experiment
    # genetic_template = (array) = 0/1 map of the reactor core slots
    # variability_of_coding_bases = (int) = number of type of rod types - e.g ATGC
    # distribution_of_coding_bases = (array) = amount of each coding base to be used array(A),array(T),...
    population = []
    genome_base_weights_array = []
    tmp_counter = 0 # need to be removed
    for genome_base_weight in distribution_of_coding_bases:
        genome_base_weights_array.append(genome_base_weight)
    for population_member_index in range(0, population_size):
        population_member = _randomize_genome(genome_length, number_veriaty_of_coding_bases, genome_base_weights_array)
        #if tmp_counter == 0:# need to be removed
        #    population.append(population_member)
        population.append(population_member)
        #    tmp_counter = 1# need to be removed
        #else:# need to be removed
        #    ##population_member = copy(population[0])# need to be removed
        #    population.append(population[0].copy())# need to be removed
        #print("Generating population member " + str(population_member_index))
        #print("Population memeber vector length - " + str(len(population_member)))
        #print("Population vector\n" + str(population_member))
        ones = 0
        twos = 0
        threes = 0
        for item in population_member:
            if item == 1:
                ones = ones + 1
            elif item == 2:
                twos = twos+1
            elif item == 3:
                threes = threes + 1
            else:
                sys.exit("unextected pa type")
        #print(ones, twos, threes)
    #print(population[0][0])
    #print(population[1][0])
    #if int(population[0][0]) == 1:# need to be removed
    #    population[0][0] = 2# need to be removed
    #else:# need to be removed
    #    population[0][0] = int(1)# need to be removed
    #population[0][0] == int(1)
    #print("...............................")
    #print(population[0][0])
    #print(population[1][0])
    del genome_base_weights_array
    return population
def _randomize_genome(genome_length, variability_of_coding_bases, genome_weights):
    genome_weights_rg = np.copy(genome_weights)
    coding_base_list = list(range(1, variability_of_coding_bases + 1))
    genome = []
    for index in range(0,genome_length):
        random_choice = random.choices(coding_base_list, weights=genome_weights_rg, k=1)
        genome.append(random_choice[0])
        weight_index_counter = - 1
        for coding_base in coding_base_list:
            weight_index_counter += 1
            if int(coding_base) == int(random_choice[0]):
                genome_weights_rg[weight_index_counter] -= 1
    del genome_weights_rg, coding_base_list
    return genome
########################################################################################################################
# Crossover
########################################################################################################################
def _mating_crossover(population_summary, ordered_population__memebrs_ids, mating_algorithm,
            mated_couple_logic, variability_of_coding_bases, genome_weights, vertical_to_horizontal_positioning_vector,
            arrayed_positioning_map, offspring_algorithm, generation_number, total_number_of_generations):
    population_size = len(ordered_population__memebrs_ids)
    current_generation = generation_number
    if mating_algorithm == "weighted-random" or mating_algorithm == "alpha-fe-male-by-generation":
        coupling_weights = _generate_coupling_weights_by_order__for_ordered_population(population_size)
        alpha_male_coupling_weights = _generate_coupling_weights_by_alpha_male_by_generation__for_ordered_population(
                                                    population_size, current_generation, total_number_of_generations)
        mated_couples_list = _generate_coupling_list__for_ordered_population(ordered_population__memebrs_ids,
                                                                             coupling_weights,
                                                                             alpha_male_coupling_weights,
                                                                             mating_algorithm, mated_couple_logic,
                                                                             generation_number, total_number_of_generations)
    elif mating_algorithm == "random":
        sys.exit(" _mating_crossover() for random selsction is not ready yet !!!!")
    else:
        sys.exit("Requested mating algorithms doesnt exist : " + str(mating_algorithm))
    #print(mated_couples_list)
    next_generation_population = _crossover(population_summary, mated_couples_list, variability_of_coding_bases,
                                            genome_weights, generation_number, total_number_of_generations,
                                            vertical_to_horizontal_positioning_vector,
                                            arrayed_positioning_map, offspring_algorithm)
    return next_generation_population

########################################################################################################################
# Weights for Coupling
########################################################################################################################
def _generate_coupling_weights_by_order__for_ordered_population(population_size):
    coupling_weights_sum = (1+population_size)*population_size/2
    coupling_weights = []
    for index in range(int(population_size), 0, -1):
        weight = index/coupling_weights_sum
        coupling_weights.append(weight)
    return coupling_weights
def _generate_random_coupling_weights__for_ordered_population(population_size):
    coupling_weights = list(range(1,population_size + 1))
    random.shuffle(coupling_weights)
    return coupling_weights
def _generate_coupling_weights_by_alpha_male_by_generation__for_ordered_population(population_size, current_generation, total_number_of_generations):
    alpha_male_coupling_weights = []
    #for index in range(int(population_size), 0, -1):
    alpha_male_weights_sum = 0
    #print(str(current_generation) + " out of " + str(total_number_of_generations) + "")
    #sys.exit()
    generations_ratio = current_generation/total_number_of_generations
    for index in range(int(population_size)):
        weight = np.exp(-(index*generations_ratio))
        alpha_male_coupling_weights.append(weight)
        alpha_male_weights_sum += weight
    for weight_index in range(len(alpha_male_coupling_weights)):
        alpha_male_coupling_weights[weight_index] = alpha_male_coupling_weights[weight_index]/alpha_male_weights_sum
    return alpha_male_coupling_weights
def _generate_Keffective_weights(population_by_memebrs_id, population_scores):
    weights_sum = 0
    population_size = len(population_by_memebrs_id)
    for index in range(int(population_size)):
        weights_sum += population_scores[index]
    weights = []
    for index in range(int(population_size)):
        weight = population_scores[index]/weights_sum
        weights.append(weight)
    del weights_sum
    return weights
########################################################################################################################
# Coupling/Mating lists
########################################################################################################################
def _generate_coupling_list__for_ordered_population(ordered_population__members_ids, coupling_weights,
                                                    alpha_male_coupling_weights, mating_algorithm,
                                                    mated_couple_logic, current_generation_number, total_generations_number):
    couples_list = []
    population_size = int(len(ordered_population__members_ids))
    counter = [0]*population_size
    #number_of_couples = int(population_size/2)*1000
    number_of_couples = int(population_size/2)
    #print(coupling_weights)
    #print(alpha_male_coupling_weights)
    #sys.exit()
    generation_ratio = current_generation_number / total_generations_number
    if (mated_couple_logic == "combination"):
        if (generation_ratio < 0.5) or (current_generation_number < 1000):
            mated_couple_logic = "exclusive"
        else:
            mated_couple_logic = "inclusive"
    for index in range(0, number_of_couples):
        if not mating_algorithm == "alpha-fe-male-by-generation":
            mated_couple = _coupling_by_weights__for_ordered_population(ordered_population__members_ids,
                                                                        coupling_weights, mated_couple_logic)
        else:
            mated_couple = _coupling_by_alpha_male_weights__for_ordered_population(ordered_population__members_ids,
                                                                        coupling_weights, alpha_male_coupling_weights, mated_couple_logic)
        couples_list.append(mated_couple)
        #print(mated_couple)
        for parent in mated_couple:
            #print(parent[0])
            counter[int(ordered_population__members_ids.index(parent))] += 1
    print(ordered_population__members_ids)
    #print(counter)
    #for memebr in ordered_population__memebrs_ids:
    #    print(counter[memebr], end =" ")
    #print(couples_list)
    #print()
    print(counter)
    #sys.exit()
    #return couples_list[:int(population_size/2)]
    return couples_list
def _coupling_by_weights__for_ordered_population(ordered_population__memebrs_ids, coupling_weights, mated_couple_logic):
    mated_couple = random.choices(ordered_population__memebrs_ids, weights=coupling_weights, k=2)
    if mated_couple_logic == 'exclusive':
        while mated_couple[0] == mated_couple[1]:
            mated_couple = random.choices(ordered_population__memebrs_ids, weights=coupling_weights, k=2)
    return mated_couple

def _coupling_by_alpha_male_weights__for_ordered_population(ordered_population__memebrs_ids, coupling_weights, alpha_male_coupling_weights, mated_couple_logic):
    coupling_flag = True
    mated_couple = []
    while coupling_flag:
        coupling_member_1 = random.choices(ordered_population__memebrs_ids, weights=alpha_male_coupling_weights, k=1)
        coupling_member_2 = random.choices(ordered_population__memebrs_ids, weights=coupling_weights, k=1)
        if not (mated_couple_logic == 'exclusive') or not (coupling_member_1 == coupling_member_2):
            coupling_flag = False
    mated_couple.append(coupling_member_1[0])
    mated_couple.append(coupling_member_2[0])
    #print(mated_couple)
    return mated_couple
########################################################################################################################
# Crossover - generating child chromosomes
########################################################################################################################
def _crossover(full_population, mated_couples_list, variability_of_coding_bases, genome_weights , generation_number,
               total_number_of_generations, vertical_to_horizontal_positioning_vector, arrayed_positioning_map,
               offspring_algorithm):
    next_generation_population = []
    single_slice_counter = 0
    double_slice_clounter = 0
    random_counter = 0
    vertical_double_slice_counter = 0
    quadrat_counter = 0
    weighted_quadrat_random_position_counter = 0
    square1x1 = 0
    square321_counter = 0
    square321_counterbyG = 0
    total_number_of_replacments = 0
    #print("............................... offspring_algorithm ............................")
    #print(" starting cross over")
    for mating_couple in mated_couples_list:
        if offspring_algorithm == "3random":
            offspring_algorithm_list = ['random', 'double-slice', 'vertical-double-slice']
            selected_offspring_algorithm = random.choice(offspring_algorithm_list)
        elif offspring_algorithm == "2-double-random":
            offspring_algorithm_list = ['double-slice', 'vertical-double-slice']
            selected_offspring_algorithm = random.choice(offspring_algorithm_list)
        else:
            selected_offspring_algorithm = offspring_algorithm
        #print("algo -" + str(selected_offspring_algorithm) + "-")
        if (selected_offspring_algorithm == "square321"):
            (child1 , child2, number_of_replacments) = _crossover_square321_double_children(full_population, mating_couple,
                                                                     variability_of_coding_bases,
                                                                     arrayed_positioning_map, genome_weights)
            total_number_of_replacments += number_of_replacments
            square321_counter += 1
        elif selected_offspring_algorithm == "single-slice":
            single_slice_counter += 1
            #child = _crossover_couple_single_cut_single_child(full_population, mating_couple,
            #                                                  variability_of_coding_bases, genome_weights)
            (child1, child2) = _crossover_couple_single_cut(full_population, mating_couple,
                                                              variability_of_coding_bases, genome_weights)
        elif selected_offspring_algorithm == "random":
            random_counter += 1
            child = _crossover_couple_random_single_child(full_population, mating_couple, variability_of_coding_bases,
                                                          genome_weights)
        elif selected_offspring_algorithm == "double-slice":
            double_slice_clounter += 1
            child = _crossover_couple_double_slice_single_child(full_population, mating_couple,
                                                               variability_of_coding_bases, genome_weights)
        elif selected_offspring_algorithm == "vertical-double-slice":
            vertical_double_slice_counter += 1
            child = _crossover_couple_vertical_double_slice_single_child(full_population, mating_couple,
                                                                         variability_of_coding_bases,
                                                                         vertical_to_horizontal_positioning_vector,
                                                                         genome_weights)
        elif selected_offspring_algorithm == "quadrat":
            child = _crossover_couple_quadrat_single_child(full_population, mating_couple, variability_of_coding_bases,
                                                          arrayed_positioning_map, genome_weights)
            quadrat_counter += 1
        elif selected_offspring_algorithm == "weighted-quadrat":
            #child = _crossover_weighted_quadrat_single_child(full_population, mating_couple,
            #                                                                   variability_of_coding_bases,
            #                                                                   arrayed_positioning_map, genome_weights)
            #weighted_quadrat_random_position_counter += 1
            (child1, child2) = _crossover_weighted_quadrat_double_child(full_population, mating_couple,
                                                                               variability_of_coding_bases,
                                                                               arrayed_positioning_map, genome_weights)
            weighted_quadrat_random_position_counter += 2
        elif selected_offspring_algorithm == "square1x1":
            (child1 , child2, number_of_replacments) = _crossover_square1x1_double_children(full_population, mating_couple,
                                                                     variability_of_coding_bases,
                                                                     arrayed_positioning_map, genome_weights)
            total_number_of_replacments += number_of_replacments
            square1x1 += 1
        elif selected_offspring_algorithm == "square321byG":
            (child1 , child2, number_of_replacments) = (
                _crossover_square321_by_generation_double_children(full_population, mating_couple, generation_number,
                                                                   total_number_of_generations,
                                                                   variability_of_coding_bases,
                                                                   arrayed_positioning_map, genome_weights))
            total_number_of_replacments += number_of_replacments
            square321_counterbyG += 1
        else:
            sys.exit("Requested offspring algorithm, current is invalid - " + str(offspring_algorithm))
        #print(str(selected_offspring_algorithm) + "; ", end=' ')#end='\r')
        try:
            child
        except:
            next_generation_population.append(child1)
            next_generation_population.append(child2)
            del child1, child2
        else:
            next_generation_population.append(child)
            del child
    print("Square321 - " + str(square321_counter) + "; Single - " + str(single_slice_counter) + "; Double - "
          + str(double_slice_clounter) + ": Vertical_double - " + str(vertical_double_slice_counter)
          + "; Random - " + str(random_counter) + "; Random - " + str(random_counter) + "; Square1x1 - " + str(square1x1))
    print("Quadrat - " + str(quadrat_counter) +"; Weighted_Quadrat - " + str(weighted_quadrat_random_position_counter)
          + "; Weighted_Quadrat by Gen. - " + str(square321_counterbyG))
    if square321_counter > 0:
        print("Avarage number of replacments for square321 - " + str(total_number_of_replacments/square321_counter))
    elif square321_counterbyG > 0:
        print("Avarage number of replacments for square321byG - " + str(total_number_of_replacments/square321_counterbyG))
    return next_generation_population

def _crossover_square321_double_children(full_population, mating_couple, variability_of_coding_bases,
                                         arrayed_positioning_map, genome_weights):
    (parent_chromosome_vector_no1, parent_chromosome_vector_no2) = (
        _mate_couple_index_to_genome_vectors(full_population, mating_couple))
    tmp_child_chromosome_vector_no1 = parent_chromosome_vector_no1[:].copy()
    tmp_child_chromosome_vector_no2 = parent_chromosome_vector_no2[:].copy()
    sqaure321_random_slab_size = random.randint(1, 3)
    number_of_replacments = 0
    initial_coordinate_x = random.randint(0, len(arrayed_positioning_map) - sqaure321_random_slab_size)
    initial_coordinate_y = random.randint(0, len(arrayed_positioning_map[0]) - sqaure321_random_slab_size)
    number_of_columns_to_slice = sqaure321_random_slab_size
    number_of_rows_to_silce = sqaure321_random_slab_size
    #print(arrayed_positioning_map)
    #print(parent_chromosome_vector_no1)
    #sys.exit()
    for index_columns in range(0, number_of_columns_to_slice):
        for index_rows in range(0, number_of_rows_to_silce):
            chromosome_coordinate_x = initial_coordinate_x + index_columns
            chromosome_coordinate_y = initial_coordinate_y + index_rows
            chromosome_coordinate = int(arrayed_positioning_map[chromosome_coordinate_x][chromosome_coordinate_y])
            if not (chromosome_coordinate == -1):
                tmp_child_chromosome_vector_no1[chromosome_coordinate] = (
                    parent_chromosome_vector_no2[chromosome_coordinate])
                tmp_child_chromosome_vector_no2[chromosome_coordinate] = (
                    parent_chromosome_vector_no1[chromosome_coordinate])
            number_of_replacments += 1
    child_chromosome_vector_no1 = _fix_mated_child(tmp_child_chromosome_vector_no1, variability_of_coding_bases,
                                                   genome_weights)
    child_chromosome_vector_no2 = _fix_mated_child(tmp_child_chromosome_vector_no2, variability_of_coding_bases,
                                                   genome_weights)
    # TMP - no fixing test
    ##child_chromosome_vector_no1 = tmp_child_chromosome_vector_no1
    #3child_chromosome_vector_no2 = tmp_child_chromosome_vector_no2
    return child_chromosome_vector_no1, child_chromosome_vector_no2, number_of_replacments
def _crossover_couple_single_cut(full_population, mating_couple, variability_of_coding_bases, genome_weights):
    (parent_vector1, parent_vector2) = _mate_couple_index_to_genome_vectors(full_population, mating_couple)
    vector_length = len(parent_vector1)
    cut_location = random.randint(1, vector_length-1)
    tmp_child_vector1 = parent_vector1[0:cut_location] + parent_vector2[cut_location:vector_length]
    tmp_child_vector2 = parent_vector2[0:cut_location] + parent_vector1[cut_location:vector_length]
    child_vector1 = _fix_mated_child(tmp_child_vector1, variability_of_coding_bases, genome_weights)
    child_vector2 = _fix_mated_child(tmp_child_vector2, variability_of_coding_bases, genome_weights)
    del parent_vector1, parent_vector2, tmp_child_vector1, tmp_child_vector2
    return child_vector1, child_vector2
def _crossover_couple_random_single_child(full_population, mating_couple, variability_of_coding_bases, genome_weights):
    (child_vector1, child_vector2) = _crossover_couple_random(full_population, mating_couple,
                                                              variability_of_coding_bases, genome_weights)
    child_vectors = []
    child_vectors.append(child_vector1)
    child_vectors.append(child_vector2)
    return random.choice(child_vectors)
def _crossover_couple_double_slice_single_child(full_population, mating_couple, variability_of_coding_bases,
                                               genome_weights):
    (parent_vector1, parent_vector2) = _mate_couple_index_to_genome_vectors(full_population, mating_couple)
    children = []
    vector_length = len(parent_vector1)
    cut_location_no1 = random.randint(1, vector_length - 2)
    cut_location_no2 = random.randint(cut_location_no1 + 1, vector_length - 1)
    tmp_child_vector1 = (parent_vector1[0:cut_location_no1] +
                         parent_vector2[cut_location_no1:cut_location_no2] +
                         parent_vector1[cut_location_no2:vector_length])
    tmp_child_vector2 = (parent_vector2[0:cut_location_no1] +
                         parent_vector1[cut_location_no1:cut_location_no2] +
                         parent_vector2[cut_location_no2:vector_length])
    child_vector1 = _fix_mated_child(tmp_child_vector1, variability_of_coding_bases, genome_weights)
    child_vector2 = _fix_mated_child(tmp_child_vector2, variability_of_coding_bases, genome_weights)
    children.append(child_vector1)
    children.append(child_vector2)
    chosen_child = random.choice(children)
    del (parent_vector1, parent_vector2, vector_length, children, tmp_child_vector1, tmp_child_vector2,
        child_vector1, child_vector2)
    return chosen_child
def _crossover_couple_vertical_double_slice_single_child(full_population, mating_couple, variability_of_coding_bases,
                                                         vertical_to_horizontal_positioning_vector, genome_weights):
    (parent_vector1, parent_vector2) = _mate_couple_index_to_genome_vectors(full_population, mating_couple)
    chromosome_vector_length = len(parent_vector1)
    tmp_child_chromosome_vector_no1 = []
    tmp_child_chromosome_vector_no2 = []
    children = []
    cut_location_no1 = random.randint(1, chromosome_vector_length - 2)
    cut_location_no2 = random.randint(cut_location_no1 + 1, chromosome_vector_length - 1)
    total_replacments = 0
    for index in range(0, chromosome_vector_length):
        if (vertical_to_horizontal_positioning_vector[index] < cut_location_no1 or
                vertical_to_horizontal_positioning_vector[index] > cut_location_no2):
            tmp_child_chromosome_vector_no1.append(parent_vector1[index])
            tmp_child_chromosome_vector_no2.append(parent_vector2[index])
        else:
            tmp_child_chromosome_vector_no1.append(parent_vector2[index])
            tmp_child_chromosome_vector_no2.append(parent_vector1[index])
            #print("replacenig adress - " + str(index))
            total_replacments += 1
    child_chromosome_vector_no1 = _fix_mated_child(tmp_child_chromosome_vector_no1, variability_of_coding_bases, genome_weights)
    child_chromosome_vector_no2 = _fix_mated_child(tmp_child_chromosome_vector_no2, variability_of_coding_bases, genome_weights)
    #print("total replacments - " + str(total_replacments))
    #print(parent_vector1)
    #print(parent_vector2)
    #print(vertical_to_horizontal_positioning_vector)
    #print(tmp_child_chromosome_vector_no1)
    #print(tmp_child_chromosome_vector_no2)
    #print(str(cut_location_no1))
    #print(str(cut_location_no2))
    #print(vertical_to_horizontal_positioning_vector)
    #sys.exit("vertical cutting")
    children.append(child_chromosome_vector_no1)
    children.append(child_chromosome_vector_no2)
    chosen_child = random.choice(children)
    return chosen_child
def _crossover_couple_quadrat_single_child(full_population, mating_couple, variability_of_coding_bases,
                                          arrayed_positioning_map, genome_weights):
    (parent_chromosome_vector_no1, parent_chromosome_vector_no2) = (
        _mate_couple_index_to_genome_vectors(full_population, mating_couple))
    #print(parent_chromosome_vector_no1)
    number_of_rows = len(arrayed_positioning_map)
    number_of_columns = len(arrayed_positioning_map[0])
    #tmp_child_chromosome_vector_no1 = []
    #tmp_child_chromosome_vector_no2 = []
    tmp_child_chromosome_vector_no1 = parent_chromosome_vector_no1[:]
    tmp_child_chromosome_vector_no2 = parent_chromosome_vector_no2[:]
    children = []
    coordinate_x1 = random.randint(0, number_of_columns - 1)
    coordinate_y1 = random.randint(0, number_of_rows - 1)
    coordinate_x2 = random.randint(coordinate_x1, number_of_columns - 1)
    coordinate_y2 = random.randint(coordinate_y1, number_of_rows - 1)
    #print("(x1,y1) = " + str(coordinate_x1) + ", " + str(coordinate_y1))
    #print(")x2,y2) = " + str(coordinate_x2) + ", " + str(coordinate_y2))
    #print("11")
    #chromosome_vector_counter = 0
    for coordinate_y_index in range(coordinate_y1, coordinate_y2 + 1):
        #print("11.22")
        for coordinate_x_index in range(coordinate_x1, coordinate_x2 + 1):
            #print(" --- " + str(coordinate_x_index) + ", " + str(coordinate_y_index))
            chromosome_coordinate = int(arrayed_positioning_map[coordinate_y_index][coordinate_x_index])
            #print(str(chromosome_coordinate) + " ", end=' ')
            if not (chromosome_coordinate == -1):
                #print("R_n1-" + str(tmp_child_chromosome_vector_no1[chromosome_coordinate]) + "-with-" +
                #      str(parent_chromosome_vector_no2[chromosome_coordinate]) + " ", end=' ')
                tmp_child_chromosome_vector_no1[chromosome_coordinate] = (
                    parent_chromosome_vector_no2[chromosome_coordinate])
                #tmp_child_chromosome_vector_no1[chromosome_coordinate] = 'X'
                #print("R_n2-" + str(tmp_child_chromosome_vector_no2[chromosome_coordinate]) + "-with-" +
                #      str(parent_chromosome_vector_no1[chromosome_coordinate]) + " ", end=' ')
                tmp_child_chromosome_vector_no2[chromosome_coordinate] = (
                    parent_chromosome_vector_no1[chromosome_coordinate])
                    #parent_chromosome_vector_no1[chromosome_vector_counter])
                #tmp_child_chromosome_vector_no2[chromosome_coordinate] = 'X'

        #print("")
    #print("22")
    #sys.exit("AAAA")
    #print(tmp_child_chromosome_vector_no1)
    #print(tmp_child_chromosome_vector_no2)
    #sys.exit("after children")
    #print("33")
    child_chromosome_vector_no1 = _fix_mated_child(tmp_child_chromosome_vector_no1, variability_of_coding_bases,
                                                   genome_weights)
    child_chromosome_vector_no2 = _fix_mated_child(tmp_child_chromosome_vector_no2, variability_of_coding_bases,
                                                   genome_weights)
    children.append(child_chromosome_vector_no1)
    children.append(child_chromosome_vector_no2)
    chosen_child = random.choice(children)
    #print(child_chromosome_vector_no1)
    #print(child_chromosome_vector_no2)
    #sys.exit("square")
    return chosen_child
def _crossover_weighted_quadrat_double_child(full_population, mating_couple,
                                                               variability_of_coding_bases, arrayed_positioning_map,
                                                               genome_weights):
    #print("_crossover_weighted_quadrat_double_child()")
    (parent_chromosome_vector_no1, parent_chromosome_vector_no2) = (
        _mate_couple_index_to_genome_vectors(full_population, mating_couple))
    tmp_child_chromosome_vector_no1 = parent_chromosome_vector_no1[:].copy()
    tmp_child_chromosome_vector_no2 = parent_chromosome_vector_no2[:].copy()
    children = []
    (number_of_rows, number_of_columns, rows_range_list, columns_range_list, random_rows_weights,
     random_columns_weights) = _random_quadrat_weights_and_size(arrayed_positioning_map)
    number_of_columns_to_slice = int((random.choices(columns_range_list, weights=random_columns_weights, k=1))[0])
    number_of_rows_to_silce = int((random.choices(rows_range_list, weights=random_rows_weights, k=1))[0])
    initial_coordinate_x = random.randint(0, number_of_columns - number_of_columns_to_slice)
    initial_coordinate_y = random.randint(0, number_of_rows - number_of_rows_to_silce)
    for index_columns in range(0, number_of_columns_to_slice):
        for index_rows in range(0, number_of_rows_to_silce):
            chromosome_coordinate_x = initial_coordinate_x + index_columns
            chromosome_coordinate_y = initial_coordinate_y + index_rows

            chromosome_coordinate = int(arrayed_positioning_map[chromosome_coordinate_x][chromosome_coordinate_y])
            #print(str(chromosome_coordinate) + " ", end=' ')
            if not (chromosome_coordinate == -1):
                tmp_child_chromosome_vector_no1[chromosome_coordinate] = (
                    parent_chromosome_vector_no2[chromosome_coordinate])
                tmp_child_chromosome_vector_no2[chromosome_coordinate] = (
                    parent_chromosome_vector_no1[chromosome_coordinate])
    child_chromosome_vector_no1 = _fix_mated_child(tmp_child_chromosome_vector_no1, variability_of_coding_bases,
                                                   genome_weights)
    child_chromosome_vector_no2 = _fix_mated_child(tmp_child_chromosome_vector_no2, variability_of_coding_bases,
                                                   genome_weights)
    #children.append(child_chromosome_vector_no1)
    #children.append(child_chromosome_vector_no2)
    #chosen_child = random.choice(children)
    return child_chromosome_vector_no1, child_chromosome_vector_no2
def _crossover_square1x1_double_children(full_population, mating_couple, variability_of_coding_bases,
                                         arrayed_positioning_map, genome_weights):
    (parent_chromosome_vector_no1, parent_chromosome_vector_no2) = (
        _mate_couple_index_to_genome_vectors(full_population, mating_couple))
    tmp_child_chromosome_vector_no1 = parent_chromosome_vector_no1[:].copy()
    tmp_child_chromosome_vector_no2 = parent_chromosome_vector_no2[:].copy()
    sqaure321_random_slab_size = random.randint(1, 1)
    number_of_replacments = 0
    initial_coordinate_x = random.randint(0, len(arrayed_positioning_map) - sqaure321_random_slab_size)
    initial_coordinate_y = random.randint(0, len(arrayed_positioning_map[0]) - sqaure321_random_slab_size)
    number_of_columns_to_slice = sqaure321_random_slab_size
    number_of_rows_to_silce = sqaure321_random_slab_size
    #print(arrayed_positioning_map)
    #print(parent_chromosome_vector_no1)
    #sys.exit()
    for index_columns in range(0, number_of_columns_to_slice):
        for index_rows in range(0, number_of_rows_to_silce):
            chromosome_coordinate_x = initial_coordinate_x + index_columns
            chromosome_coordinate_y = initial_coordinate_y + index_rows
            chromosome_coordinate = int(arrayed_positioning_map[chromosome_coordinate_x][chromosome_coordinate_y])
            if not (chromosome_coordinate == -1):
                tmp_child_chromosome_vector_no1[chromosome_coordinate] = (
                    parent_chromosome_vector_no2[chromosome_coordinate])
                tmp_child_chromosome_vector_no2[chromosome_coordinate] = (
                    parent_chromosome_vector_no1[chromosome_coordinate])
            number_of_replacments += 1
    child_chromosome_vector_no1 = _fix_mated_child(tmp_child_chromosome_vector_no1, variability_of_coding_bases,
                                                   genome_weights)
    child_chromosome_vector_no2 = _fix_mated_child(tmp_child_chromosome_vector_no2, variability_of_coding_bases,
                                                   genome_weights)
    # TMP - no fixing test
    ##child_chromosome_vector_no1 = tmp_child_chromosome_vector_no1
    #3child_chromosome_vector_no2 = tmp_child_chromosome_vector_no2
    return child_chromosome_vector_no1, child_chromosome_vector_no2, number_of_replacments
def _crossover_square321_by_generation_double_children(full_population, mating_couple, generation_number,
                                                       total_number_of_generations, variability_of_coding_bases,
                                                       arrayed_positioning_map, genome_weights):
    (parent_chromosome_vector_no1, parent_chromosome_vector_no2) = (
        _mate_couple_index_to_genome_vectors(full_population, mating_couple))
    #print(parent_chromosome_vector_no1)
    #print(parent_chromosome_vector_no2)
    tmp_child_chromosome_vector_no1 = parent_chromosome_vector_no1[:].copy()
    tmp_child_chromosome_vector_no2 = parent_chromosome_vector_no2[:].copy()
    square321_list = [1, 2, 3]
    ##number_of_3 = 0
    ##number_of_2 = 0
    ##number_of_1 = 0
    ##square321_weight_2 = 0.333
    ##square321_weight_1 = (1-square321_weight_2)*(generation_number/total_number_of_generations)
    ##square321_weight_3 = (1-square321_weight_1-square321_weight_2)
    square321_weight_1 = 0
    square321_weight_2 = 0
    square321_weight_3 = 0
    generation_ratio = generation_number/total_number_of_generations
    if ((generation_ratio)<0.1) or (generation_number < 500):
        square321_weight_2 = 0.333
        square321_weight_3 = 0.666
    elif ((generation_ratio)<0.2) or (generation_number < 1000):
        square321_weight_2 = 0.666
        square321_weight_3 = 0.333
    elif ((generation_ratio) < 0.3) or (generation_number < 1500):
        square321_weight_2 = 0.333
        square321_weight_3 = 0.333
    elif ((generation_ratio) < 0.4) or (generation_number < 2000):
        square321_weight_2 = 0.5
        square321_weight_3 = 0
    else:
        square321_weight_2 = 0
        square321_weight_3 = 0
    square321_weight_1 = (1 - square321_weight_3 - square321_weight_2)
    sqaure321_random_slab_size = random.choices(square321_list, weights=(square321_weight_1, square321_weight_2,
                                                                             square321_weight_3), k=1)
    number_of_replacments = 0
    initial_coordinate_x = random.randint(0, len(arrayed_positioning_map) - sqaure321_random_slab_size[0])
    initial_coordinate_y = random.randint(0, len(arrayed_positioning_map[0]) - sqaure321_random_slab_size[0])
    number_of_columns_to_slice = sqaure321_random_slab_size[0]
    number_of_rows_to_silce = sqaure321_random_slab_size[0]
    for index_columns in range(0, number_of_columns_to_slice):
        for index_rows in range(0, number_of_rows_to_silce):
            chromosome_coordinate_x = initial_coordinate_x + index_columns
            chromosome_coordinate_y = initial_coordinate_y + index_rows
            chromosome_coordinate = int(arrayed_positioning_map[chromosome_coordinate_x][chromosome_coordinate_y])
            if not (chromosome_coordinate == -1):
                tmp_child_chromosome_vector_no1[chromosome_coordinate] = (
                    parent_chromosome_vector_no2[chromosome_coordinate])
                tmp_child_chromosome_vector_no2[chromosome_coordinate] = (
                    parent_chromosome_vector_no1[chromosome_coordinate])
            number_of_replacments += 1
    child_chromosome_vector_no1 = _fix_mated_child(tmp_child_chromosome_vector_no1, variability_of_coding_bases,
                                                   genome_weights)
    child_chromosome_vector_no2 = _fix_mated_child(tmp_child_chromosome_vector_no2, variability_of_coding_bases,
                                                   genome_weights)
    return child_chromosome_vector_no1, child_chromosome_vector_no2, number_of_replacments
########################################################################################################################
# Correcting Chromosome by template/weights
########################################################################################################################
def _fix_mated_child(child_vector, variability_of_coding_bases, genome_weights):
    current_weights = _calculate_coding_bases_weights(child_vector, variability_of_coding_bases)
    while not current_weights == genome_weights:
        random_position_in_vector = random.randint(0, len(child_vector) - 1)
        #print(genome_weights)
        #print(current_weights)
        #print(child_vector[random_position_in_vector])
        #print(str(child_vector[random_position_in_vector] - 1))
        #print(genome_weights[child_vector[random_position_in_vector] - 1])
        #sys.exit()
        if genome_weights[child_vector[random_position_in_vector] - 1] < current_weights[child_vector[random_position_in_vector] - 1]:
            fix_flag = True
            while fix_flag:
                random_coding_base = random.randint(1, variability_of_coding_bases)
                if not genome_weights[random_coding_base - 1] < current_weights[random_coding_base - 1]:
                    fix_flag = False
                #if not random_coding_base == child_vector[random_position_in_vector]:
                    current_weights[child_vector[random_position_in_vector] - 1] = current_weights[child_vector[random_position_in_vector] - 1] - 1
                    current_weights[random_coding_base - 1] = current_weights[random_coding_base - 1] + 1
                    child_vector[random_position_in_vector] = random_coding_base
    return child_vector
def _calculate_coding_bases_weights(coding_vector, variability_of_coding_bases):
    calculate_coding_weights = []
    for coding_base in range(1, variability_of_coding_bases + 1):
        calculate_coding_weights.append(0)
        for coding_item in coding_vector:
            if coding_base == coding_item:
                calculate_coding_weights[coding_base - 1] = calculate_coding_weights[coding_base - 1] + 1
    return calculate_coding_weights
########################################################################################################################
# Mutations
########################################################################################################################
def _mutation(population_for_mutation, mutation_logic, mutation_type, left_shift_addresses_vector,
              right_shift_addresses_vector, up_shift_addresses_vector, down_shift_addresses_vector,
              core_map_array, total_number_of_generations, current_generation):
    member_counter = -1
    total_number_of_mutations = 0
    # 1st place - counter no mutations
    # 2nd place - counter single switch mutations
    # 3rd place - counter double switch mutations
    # 4th place - counter for triple switch mutations
    # 5th place - counter for 4 or more switch mutations
    # 6th place - counter for number of single shift mutations
    mutations_occourance_counter = [0, 0, 0, 0, 0, 0]
    try:
        if mutated_population:
            del mutated_population
    except NameError:
        pass
    mutated_population = []
    for member in population_for_mutation:
        original_member = member.copy()
        mutated_member = member.copy()
        this_member_mutations_counter = 0
        member_counter += 1
        generations_ratio = current_generation/total_number_of_generations
        ################################################################################################################
        mutation_flag = True
        while mutation_flag:
            probability_of_mutation = _probability_of_mutation(len(member), mutation_logic, total_number_of_generations, current_generation, this_member_mutations_counter)
            if random.random() < probability_of_mutation:
                if (mutation_type == 'switch'):
                    mutated_member = _mutation_switch_base_pair(member)
                elif (mutation_type == 'shift'):
                    mutated_member = _mutation_shift(member, left_shift_addresses_vector, right_shift_addresses_vector, up_shift_addresses_vector, down_shift_addresses_vector)
                    mutations_occourance_counter[5] += 1
                elif (mutation_type == 'switchORshift'):
                    mixlist = [0, 1] ## 0 - base_pair, 1 - shift
                    mix_selection = random.choice(mixlist)
                    if mix_selection == 0:
                        mutated_member = _mutation_switch_base_pair(member)
                    elif mix_selection == 1:
                        mutated_member = _mutation_shift(member, left_shift_addresses_vector, right_shift_addresses_vector, up_shift_addresses_vector, down_shift_addresses_vector)
                        mutations_occourance_counter[5] += 1
                    else:
                        sys.exit("mix select unknow error")
                elif (mutation_type == 'switchANDshift'):
                    mutated_member = _mutation_switch_base_pair(member)
                    mutation_member = mutated_member.copy()
                    mutated_member = _mutation_shift(mutation_member, left_shift_addresses_vector, right_shift_addresses_vector,
                                up_shift_addresses_vector, down_shift_addresses_vector)
                    mutations_occourance_counter[5] += 1
                    total_number_of_mutations += 1
                elif (mutation_type == 'switchORDIMshift'):
                    # start - 50% switch and 50% shifts ->->-> after 50% generations 100% switches and 0% shifts
                    starting_probability = 0.5
                    if (generations_ratio < 0.5):
                        switch_probability = starting_probability + (1-starting_probability)*(2*generations_ratio)
                    else:
                        switch_probability = 1
                    if random.random() < switch_probability:
                        mutated_member = _mutation_switch_base_pair(member)
                    else:
                        #mutation_member = member.copy()
                        mutated_member = _mutation_shift(member, left_shift_addresses_vector, right_shift_addresses_vector,
                                    up_shift_addresses_vector, down_shift_addresses_vector)
                        mutations_occourance_counter[5] += 1
                else:
                    sys.exit("unknown mutation type in _mutation()")
                member = mutated_member.copy()
                total_number_of_mutations += 1
                this_member_mutations_counter += 1
            else:
                mutation_flag = False
        mutated_population.append(mutated_member)
        if this_member_mutations_counter > 3:
            mutations_occourance_counter[4] += 1
        else:
            mutations_occourance_counter[this_member_mutations_counter] += 1
        ################################################################################################################
        #probability_of_mutation = _probability_of_mutation(len(member), mutation_logic, total_number_of_generations, current_generation)
        #mutated_member = member.copy()
        #if probability_of_mutation == 1:
    return mutated_population, total_number_of_mutations, mutations_occourance_counter
        #    if (mutation_type == 'base-pair'):
        #        mutated_member = _mutation_base_pair(member)
        #        this_member_mutations_counter += 1
        #    elif (mutation_type == 'shift'):
        #        mutated_member = _mutation_shift(member, left_shift_addresses_vector, right_shift_addresses_vector,
        #                        up_shift_addresses_vector, down_shift_addresses_vector)
        #        mutations_occourance_counter[5] += 1
        #    elif (mutation_type == 'mix'):
        #        ## 0 - base_pair, 1 - shift
        #        mixlist = [0, 1]
        #        mix_selection = random.choice(mixlist)
        #        if mix_selection == 0:
        #            mutated_member = _mutation_base_pair(member)
        #            this_member_mutations_counter += 1
        #        elif mix_selection == 1:
        #            mutated_member = _mutation_shift(member, left_shift_addresses_vector, right_shift_addresses_vector,
        #                        up_shift_addresses_vector, down_shift_addresses_vector)
        #            mutations_occourance_counter[5] += 1
        #        else:
        #            sys.exit("mix select unknow error")
        ##    elif (mutation_type == '1switch1shift'):
        #        mutated_member = _mutation_base_pair(member)
        #        mutation_member = mutated_member.copy()
        #        mutated_member = _mutation_shift(mutation_member, left_shift_addresses_vector, right_shift_addresses_vector,
        #                        up_shift_addresses_vector, down_shift_addresses_vector)
        #        mutations_occourance_counter[5] += 1
        #        this_member_mutations_counter += 1
        #        total_number_of_mutations += 1
        #    elif (mutation_type == 'switchorshift'):
        #        mutated_member = _mutation_base_pair(member)
        #        mutation_member = mutated_member.copy()
        #        if random.random() > 0.5:
        #            mutated_member = _mutation_shift(mutation_member, left_shift_addresses_vector, right_shift_addresses_vector,
        #                        up_shift_addresses_vector, down_shift_addresses_vector)
        #            mutations_occourance_counter[5] += 1
        #        else:
        #            mutated_member = _mutation_base_pair(member)
        #            this_member_mutations_counter += 1
        #        total_number_of_mutations += 1
        #    else:
        #        sys.exit("unknown mutation type in _mutation()")
        #    total_number_of_mutations += 1
        #else:
        #    while random.random() < probability_of_mutation:
        #        if (mutation_type == 'base-pair'):
        #            mutated_member = _mutation_base_pair(member)
        #            ##mutations_occourance_counter[1] += 1
        #        elif (mutation_type == 'shift'):
        #            mutated_member = _mutation_shift(member, left_shift_addresses_vector, right_shift_addresses_vector,
        #                        up_shift_addresses_vector, down_shift_addresses_vector)
        #            mutations_occourance_counter[5] += 1
        #        elif (mutation_type == 'mix'):
        #            ## 0 - base_pair, 1 - shift
        #            mixlist = [0, 1]
        #            mix_selection = random.choice(mixlist)
        #            if mix_selection == 0:
        #                mutated_member = _mutation_base_pair(member)
        #                ##mutations_occourance_counter[1] += 1
        #            elif mix_selection == 1:
        #                mutated_member = _mutation_shift(member, left_shift_addresses_vector, right_shift_addresses_vector,
        #                        up_shift_addresses_vector, down_shift_addresses_vector)
        #                mutations_occourance_counter[5] += 1
        #            else:
        #                sys.exit("mix select unknow error")
        #        elif (mutation_type == '1switch1shift'):
        #            mutated_member = _mutation_base_pair(member)
        #            mutation_member = mutated_member.copy()
        #            mutated_member = _mutation_shift(mutation_member, left_shift_addresses_vector, right_shift_addresses_vector,
        #                        up_shift_addresses_vector, down_shift_addresses_vector)
        #            ##mutations_occourance_counter[1] += 1
        #            mutations_occourance_counter[5] += 1
        #            total_number_of_mutations += 1
        #        elif (mutation_type == 'switchorshift'):
        #            mutated_member = _mutation_base_pair(member)
        #            mutation_member = mutated_member.copy()
        #            ##if random.random() > 0.5:
        #            if random.random() > (1-((total_number_of_generations - current_generation)^3)/(total_number_of_generations^3)):
        #                mutated_member = _mutation_shift(mutation_member, left_shift_addresses_vector, right_shift_addresses_vector,
        #                            up_shift_addresses_vector, down_shift_addresses_vector)
        #                mutations_occourance_counter[5] += 1
        #            else:
        #                mutated_member = _mutation_base_pair(member)
        #                this_member_mutations_counter += 1
        #            total_number_of_mutations += 1
        #        else:
        #            sys.exit("unknown mutation type in _mutation()")
        #        #mutated_member = _mutation_base_pair(tmp_member)
        #        member = mutated_member.copy()
        #        #index1 = random.randint(0, len(memeber)-1)
        #        #index2 = random.randint(0, len(memeber)-1)
        #        #value1 = memeber[index1]
        #        #value2 = memeber[index2]
        #        #memeber[index1] = value2
        #        #memeber[index2] = value1
        #        total_number_of_mutations += 1
        #        this_member_mutations_counter += 1
        ##population_for_mutation[memeber_counter] = member
        #mutated_population.append(mutated_member)
        #if this_member_mutations_counter > 3:
        #    mutations_occourance_counter[4] += 1
        #else:
        #    mutations_occourance_counter[this_member_mutations_counter] += 1
        ### Verify the number of changes
        ##diff = 0
        ##for index in range(len(member)):
        ##    if not original_member[index] == mutated_member[index]:
        ##        diff += 1
        ##print("Diif - " + str(diff))
        ####sys.exit()
    ###del probability_of_mutation, index1, index2, value1, value2, memeber, memeber_counter
    ###print(mutations_occourance_counter)
    ###print(total_number_of_mutations)
    #return mutated_population, total_number_of_mutations, mutations_occourance_counter
def _mutation_switch_base_pair(original_chromosome_for_mutation):
    value1 = -1
    value2 = -1
    chromosome_for_mutation = original_chromosome_for_mutation.copy()
    while value1 == value2:
        index1 = random.randint(0, len(chromosome_for_mutation)-1)
        index2 = random.randint(0, len(chromosome_for_mutation)-1)
        value1 = chromosome_for_mutation[index1]
        value2 = chromosome_for_mutation[index2]
    chromosome_for_mutation[index1] = value2
    chromosome_for_mutation[index2] = value1
    return chromosome_for_mutation
    #sys.exit("_mutation_base_pair under construction")
def _mutation_shift(mutation_member, left_shift_addresses_vector, right_shift_addresses_vector,
                                up_shift_addresses_vector, down_shift_addresses_vector):
    #mutated_memebr = []
    right = False
    left = False
    up = False
    down = False
    # right-0, left-1, up-2, down-3, up-right-4, up-left-5, down-right-6, down-left-7
    shift_options_list = [0,1,2,3,4,5,6,7]
    shift_random_selection = random.choice(shift_options_list)
    mutated_member = mutation_member.copy()
    if shift_random_selection == 0 or shift_random_selection == 4 or shift_random_selection == 6:
        for index in range(0, len(mutation_member)):
            #print(index)
            mutated_member[index] = mutation_member[right_shift_addresses_vector[index]]
    elif shift_random_selection == 1 or shift_random_selection == 5 or shift_random_selection == 7:
        for index in range(0, len(mutation_member)):
            #print(index)
            mutated_member[index] = mutation_member[left_shift_addresses_vector[index]]
    elif shift_random_selection == 2 or shift_random_selection == 4 or shift_random_selection == 5:
        for index in range(0, len(mutation_member)):
            #print(index)
            mutated_member[index] = mutation_member[up_shift_addresses_vector[index]]
    elif shift_random_selection == 3 or shift_random_selection == 6 or shift_random_selection == 7:
        for index in range(0, len(mutation_member)):
            #print(index)
            mutated_member[index] = mutation_member[down_shift_addresses_vector[index]]
    else:
        sys.exit("unknow shift mutation")
    #sys.exit("NOt ready - unknow shift mutation")
    return mutated_member
def _probability_of_mutation(genome_vector_length, mutation_logic, total_number_of_generations, current_generation_number, this_member_mutations_counter):
    # generation ratio
    generation_ratio = current_generation_number / total_number_of_generations
    # initial mutation probability
    probability_of_mutation = 0
    # 100% for success
    assured_probability = 1
    # around 0.33
    proportional_probability = ((1-1/genome_vector_length)**genome_vector_length)
    # growing through generations from 0.66 to 0.0
    progressing_probability = (proportional_probability*(2*(1-generation_ratio)))
    # constant prbab ~0.5
    constant_probability = 0.5
    # no prob
    zero_probability = 0
    if mutation_logic == 'progressing':
        probability_of_mutation = progressing_probability
    elif mutation_logic == 'min1progressing':
        if this_member_mutations_counter == 0:
            probability_of_mutation = assured_probability
        else:
            probability_of_mutation = progressing_probability
    elif mutation_logic == 'constant':
        probability_of_mutation = constant_probability
    elif mutation_logic == 'assured':
        if this_member_mutations_counter == 0:
            probability_of_mutation = assured_probability
        else:
            probability_of_mutation = zero_probability
    elif mutation_logic == 'proportional':
        probability_of_mutation = proportional_probability
    elif mutation_logic == 'min1proportional':
        if this_member_mutations_counter == 0:
            probability_of_mutation = assured_probability
        else:
            probability_of_mutation = proportional_probability
    elif mutation_logic == 'none':
        return 0
    else:
        sys.exit("Mutation Logic is unknown - " + str(mutation_logic))
    return probability_of_mutation
########################################################################################################################
# Elitism and Survival
########################################################################################################################
def _survival(old_generaion_summary, new_generation):
    probability_counter = 0
    survival_probability = 0
    population_size = len(new_generation)
    total_survival_of_old_generation = 0
    for member in old_generaion_summary:
        probability_counter += 1
        survival_probability = (population_size - probability_counter)/population_size/5
        if random.random() < survival_probability:
            total_survival_of_old_generation += 1
            rundom_index_of_terminated_child = random.randint(0, population_size - 1)
            new_generation[rundom_index_of_terminated_child] = member[2]
    #del (probability_counter, survival_probability, memeber, total_survival_of_old_generation,
    #     rundom_index_of_terminated_child)
    return new_generation
def _elitism_and_survival(best_chromosome, new_generation):
    #best_chromosome = previous_generaion_summary[0][3]
    population_size = len(new_generation)
    random_index_of_terminated_child = random.randint(0, population_size - 1)
    new_generation.remove(new_generation[int(random_index_of_terminated_child)])
    new_generation.append(best_chromosome)
    del population_size
    return new_generation
def _elitism_expanding_population(old_generaion_summary, new_generation):
    #print("Appending elitism - " + str(old_generaion_summary[0]))
    new_generation.append(old_generaion_summary[0][2])
    return new_generation
########################################################################################################################
# Scorring, Calculating Params (e.g Vairances, etc.) and Plotting
########################################################################################################################
def _parallel_results_colector(id, result):
    global results
    results.append(id, result)
def _parallel_population_scoring_ordering_and_logging(optimization_type, population, generations_counter,
                generations_longstring_counter, core_map_array, experiment_results_directory, tmp_generations_directory,
                tmp_base_ffsolver_directory, tmp_ffsolver_scores_directory, ffsolver_exec_command,
                ffsolver_config_file_name, ffsolver_boundary_conditions, ffsolver_config_header_file_name,
                ffsolver_config_ender_file_name, tmp_base_template_directory, base_directory, population_size,
                prev_best_keff_score, prev_best_ppf_score, prev_best_alpha_score, number_of_parallel_threads,
                human_time_string, save_results_flag, number_of_reactor_core_rows, alpha, verbosity):
    number_of_screen_threads = number_of_parallel_threads
    population_keff_scores = []
    population_ppf_scores = []
    population_alpha_scores = []
    ordered_population_by_memebrs_id = []
    ordered_population_keff_scores = []
    ordered_population_ppf_scores = []
    ordered_population_alpha_scores = []
    ordered_population_keff_by_memebrs_id = []
    ordered_population_ppf_by_memebrs_id = []
    population_summary = []
    total_runtime = float(0)
    total_keff_score = float(0)
    total_ppf_score = float(0)
    total_alpha_score = float(0)
    best_ppf_score = float(99999)
    best_keff_score = float(0)
    best_alpha_score = float(0)
    worst_ppf_score = float(0)
    worst_keff_score = float(99999)
    worst_alpha_score = float(99999)
    systems_commands_list = []
    drawing_excution_list = []
    results_log_files_list = []
    print("------------------------------ Calculating Scores ------------------------------")
    print("........... Preparing all directories, commands & config files .................")
    this_generations_directory = tmp_generations_directory + "/generation." + str(generations_longstring_counter) #str(generations_counter)
    tmp_screen_conf_directory = this_generations_directory + "/screenconfs"
    tmp_screen_logs_directory = this_generations_directory + "/screenlogs"
    tmp_generation_base_score_run_directory = (tmp_ffsolver_scores_directory + "/generation."
                                               + str(generations_longstring_counter)) #+ str(generations_counter)
    fileoperators._create_non_exsisting_sub_directory(this_generations_directory, verbosity)
    fileoperators._create_non_exsisting_sub_directory(tmp_screen_conf_directory, verbosity)
    fileoperators._create_non_exsisting_sub_directory(tmp_screen_logs_directory, verbosity)
    fileoperators._create_non_exsisting_sub_directory(tmp_generation_base_score_run_directory, verbosity)
    population_size = len(population)
    for member_number in range(population_size):
        population_member_vector = population[member_number]
        score_run_directory = (tmp_generation_base_score_run_directory + "/member." + str(member_number))
        fileoperators._prepare_singlerun_directory(tmp_base_ffsolver_directory, score_run_directory, verbosity)
        wrappers._ffprepare_config_file(population_member_vector, core_map_array, score_run_directory,
                                        tmp_base_template_directory, ffsolver_config_file_name, ffsolver_boundary_conditions,
                                        ffsolver_config_header_file_name, ffsolver_config_ender_file_name, verbosity)
        (system_command_tmp, results_log_tmp) = wrappers._ffscore_command_and_resultsfile(ffsolver_exec_command,
                                                                                         score_run_directory)
        sys.exit(system_command_tmp + " , " + results_log_tmp)
        systems_commands_list.append(system_command_tmp)
        results_log_files_list.append(score_run_directory + "/kref_lst.dat")
    print(".............................. Spawning scoring jobs ...........................")
    while_counter = -1
    number_of_open_screens = -1
    while True:
        while_counter += 1
        if while_counter > (population_size - 1):
            break
        screen_header = ("GEN_" + str(generations_longstring_counter) + "_MEM_" + str(while_counter))
        screen_config_file = tmp_screen_conf_directory + "/" + screen_header + ".conf"
        screen_log_file = tmp_screen_logs_directory + "/" + screen_header + ".log"
        screen_name = (screen_header + "_time_" + str(human_time_string))[-50:]
        screen_exec_command = sysops._screen_exec_command_prep(screen_name, screen_config_file, screen_log_file,
                                                               systems_commands_list[while_counter])
        sysops._spawn_screen_with_executable_inside_in_detached_mode(screen_exec_command, verbosity)
        number_of_open_screens = sysops._get_number_of_open_screens(human_time_string)
        while int(number_of_open_screens) > int(number_of_screen_threads):
            helpers._print_norm_blue_verb("Number of Open screens is : ",number_of_open_screens, verbosity)
            helpers._print_norm_blue_verb("Expecting lower than : ", number_of_screen_threads, verbosity)
            time.sleep(2)
            number_of_open_screens = sysops._get_number_of_open_screens(human_time_string)
    print(".................... Waiting for all job screens to complete ...................")
    number_of_open_screens = sysops._get_number_of_open_screens(human_time_string)
    while int(number_of_open_screens) > int(0):
            helpers._print_norm_blue_verb("Number of Open screens is : ",number_of_open_screens, verbosity)
            helpers._print_norm_blue_verb("Expecting lower than : ", number_of_screen_threads, verbosity)
            time.sleep(2)
            number_of_open_screens = sysops._get_number_of_open_screens(human_time_string)
    print(".......................... Copy results & extract score ........................")
    for member_number in range(0, population_size):
        population_member = population[member_number]
        log_file_content = fileoperators._read_from_file(results_log_files_list[member_number])
        (keff_score, ppf_score, runtime) = wrappers._ffscore_and_runtime_from_input(log_file_content, number_of_reactor_core_rows)
        alpha_score = float(float(alpha)*float(keff_score) + (float(1-alpha))/float(ppf_score))
        population_keff_scores.append(keff_score)
        population_ppf_scores.append(ppf_score)
        population_alpha_scores.append(alpha_score)
        ############################### Mark Best and worst scores by type #############################################
        if float(best_keff_score) < float(population_keff_scores[member_number]):
            best_keff_score = population_keff_scores[member_number]
        if float(best_ppf_score) > float(population_ppf_scores[member_number]):
            best_ppf_score = population_ppf_scores[member_number]
        if float(best_alpha_score) < float(population_alpha_scores[member_number]):
            best_alpha_score = population_alpha_scores[member_number]
        if float(worst_keff_score) > float(population_keff_scores[member_number]):
            worst_keff_score = population_keff_scores[member_number]
        if float(worst_ppf_score) < float(population_ppf_scores[member_number]):
            worst_ppf_score = population_ppf_scores[member_number]
        if float(worst_alpha_score) > float(population_alpha_scores[member_number]):
            worst_alpha_score = population_alpha_scores[member_number]
        ################################################################################################################
        member_personal_file_name = (this_generations_directory + "/Member." + str(member_number) +
                                     "..Keff.." + str(population_keff_scores[member_number]) +
                                     "..PPF.." + str(population_ppf_scores[member_number]) +
                                     "..Alpha-" + str(alpha) + ".." + str(population_alpha_scores[member_number]) )
        population_summary.append([member_number,
                                   float(population_keff_scores[member_number]),
                                   float(population_ppf_scores[member_number]),
                                   float(population_alpha_scores[member_number]),
                                   population[member_number]])
        fileoperators._write_input_to_file(str(population_member), member_personal_file_name, verbosity)
        total_keff_score = total_keff_score + float(population_keff_scores[member_number])
        total_ppf_score = total_ppf_score + float(population_ppf_scores[member_number])
        total_alpha_score = total_alpha_score + float(population_alpha_scores[member_number])
        total_runtime = total_runtime + float(runtime)
    average_keff_score = total_keff_score/population_size
    average_ppf_score = total_ppf_score/population_size
    average_alpha_score = total_alpha_score/population_size
    average_runtime = total_runtime/population_size
    print("----------------------- Calculating population variance ------------------------")
    variance = _population_variance(population)
    print("------------------------------ Ordering population -----------------------------")
    if (optimization_type == 'keff'):
        population_summary.sort(reverse=True, key=lambda x: x[1])
    elif (optimization_type == 'ppf'):
        population_summary.sort(reverse=False, key=lambda x: x[2])
    elif (optimization_type == 'alpha'):
        population_summary.sort(reverse=True, key=lambda x: x[3])
    else:
        sys.exit("Killed - unknow optimization type - " + str(optimization_type))
    print("------------------------------ Writing member drawing --------------------------")
    for index in range(len(population_summary)):
        ordered_population_by_memebrs_id.append(population_summary[index][0])
        ordered_population_keff_scores.append(population_summary[index][1])
        ordered_population_ppf_scores.append(population_summary[index][2])
        ordered_population_alpha_scores.append(population_summary[index][3])
    best_member_number = population_summary[0][0]
    worst_member_number = population_summary[-1][0]
    best_population_member = population[best_member_number]
    worst_population_member = population[worst_member_number]
    count_of_1 = population_member.count(1)
    count_of_2 = population_member.count(2)
    count_of_3 = population_member.count(3)
    best_member_file_header = ("Gen." + str(generations_longstring_counter)
                               + ".Mem." + str(best_member_number)
                               + "..Keff.." + str(population_keff_scores[best_member_number])
                               + "..PPF.." + str(population_ppf_scores[best_member_number])
                               + "..Alpha-" + str(alpha) + ".." + str(population_alpha_scores[best_member_number]))
    member_personal_file_name = (tmp_generations_directory + "/" + best_member_file_header)
    jpeg_file_name = member_personal_file_name + ".jpeg"
    drawing_title = ("Gen:" + str(generations_longstring_counter)
                     + " , Mem:" + str(best_member_number)
                     + " , Keff:" + str(population_keff_scores[best_member_number])
                     + " , PPF:" + str(population_ppf_scores[best_member_number])
                     + " , Alpha=" + str(alpha) + ":" + str(population_alpha_scores[best_member_number]))
    drawers._save_genome_vector_by_template_to_file(population_member, core_map_array, drawing_title, member_personal_file_name)
    if save_results_flag == 'all':
        ################################################################################################################
        for member_number in range(population_size):
            if not member_number == best_member_number:
                population_member_vector = population[member_number]
                drawing_file_name = ((tmp_generations_directory + "/Gen." + str(generations_longstring_counter)
                                      + ".Mem." + str(member_number)
                                      + "..Keff.." + str(population_keff_scores[best_member_number])
                                      + "..PPF.." + str(population_ppf_scores[best_member_number]))
                                     + " , Alpha=" + str(population_alpha_scores[best_member_number]))
                drawing_title = ("Gen:" + str(generations_longstring_counter) + " , Mem:" + str(member_number)
                                 + " , Keff:" + str(population_keff_scores[best_member_number])
                                 + " , PPF:" + str(population_ppf_scores[best_member_number])
                                 + " , Alpha=" + str(population_alpha_scores[best_member_number]))
                drawers._save_genome_vector_by_template_to_file(population_member_vector, core_map_array, drawing_title, drawing_file_name)
        #print(".............................. Spawning drawing jobs ...........................")
        #with concurrent.futures.ThreadPoolExecutor() as executor:
        #    executor.map(run_command, drawing_excution_list)
        ################################################################################################################
    print("------------------ Saving Best Results in Experiment Direcotry -----------------")
    saving_results_best_chromosome_map = (experiment_results_directory + "/" + best_member_file_header + ".jpeg")
    tmp_time_in_secods = helpers._get_current_time_in_seconds()
    saving_results_best_chromosome_clipmap = (tmp_generations_directory + "/Clipmap." + str(tmp_time_in_secods))
    fileoperators._copy_file_to_file(jpeg_file_name, saving_results_best_chromosome_map, verbosity)
    fileoperators._copy_file_to_file(jpeg_file_name, saving_results_best_chromosome_clipmap, verbosity)
    ################################## Helper Files for clipmap later on ###############################################
    onlychanges_saving_results_best_chromosome_clipmap = (tmp_generations_directory + "/ChangeOnly." + str(tmp_time_in_secods))
    if (optimization_type == 'keff'):
        if (not (best_member_number == (population_size - 1))) or (float(best_keff_score) > float(prev_best_keff_score)):
            fileoperators._copy_file_to_file(jpeg_file_name, onlychanges_saving_results_best_chromosome_clipmap, verbosity)
    elif (optimization_type == 'ppf'):
        if (not (best_member_number == (population_size - 1))) or (float(best_ppf_score) < float(prev_best_ppf_score)):
            fileoperators._copy_file_to_file(jpeg_file_name, onlychanges_saving_results_best_chromosome_clipmap, verbosity)
    elif (optimization_type == 'alpha'):
        if (not (best_member_number == (population_size - 1))) or (float(best_alpha_score) > float(prev_best_alpha_score)):
            fileoperators._copy_file_to_file(jpeg_file_name, onlychanges_saving_results_best_chromosome_clipmap, verbosity)
    else:
        sys.exit("Died in evolution.py - sub _parallel_population_scoring_ordering_and_logging() - unknown optimization type")
    ####################################################################################################################
    ############################################# Cleaning /dev/shm ####################################################
    print("................ Removing tmp ffscore directories and log files ................")
    ##helpers._pause()##
    fileoperators._remove_directory(tmp_generation_base_score_run_directory, verbosity)
    #fileoperators._remove_directory(this_generations_directory, verbosity)
    ####################################################################################################################
    return (population_summary, ordered_population_by_memebrs_id,
            ordered_population_keff_scores, best_keff_score, average_keff_score, worst_keff_score,
            variance, average_runtime, count_of_1, count_of_2, count_of_3,
            ordered_population_ppf_scores, best_ppf_score, average_ppf_score, worst_ppf_score,
            ordered_population_alpha_scores, best_alpha_score, average_alpha_score, worst_alpha_score)
def _score_parallel_runner():
    sys.exit("under construcion parallelizm")
def _population_variance(population):
    total_population_variance_counter = 0
    current_population_variance_counter = 0
    population_size = len(population)
    chromosome_vector_size = len(population[0])
    for index in range(0, population_size - 1):
        for index2 in range(index + 1, population_size):
            for char_index_in_vector in range(0, chromosome_vector_size):
                if population[index][char_index_in_vector] == population[index2][char_index_in_vector]:
                    current_population_variance_counter += 1
                total_population_variance_counter += 1
    if total_population_variance_counter == 0:
        variance = 0
    else:
        variance = 1 - current_population_variance_counter/total_population_variance_counter
    del (total_population_variance_counter, current_population_variance_counter, population_size, chromosome_vector_size)
    return variance
def _population_full_comparison_similarities(population):
    comparison_similarities_counter = []
    total_population_similarities_counter = 0
    population_size = len(population)
    sum_of_similarities = 0
    number_of_similarity_groups = 0
    for index in range(0, population_size - 1):
        for index2 in range(index + 1, population_size):
            if population[index] == population[index2]:
                if len(comparison_similarities_counter) == 0:
                    comparison_similarities_counter.append([1, population[index]])
                else:
                    new_flag = True
                    for index3 in range(len(comparison_similarities_counter)):
                        if comparison_similarities_counter[index3][1] == population[index]:
                            comparison_similarities_counter[index3][0] += 1
                            new_flag = False
                            break
                    if new_flag:
                        comparison_similarities_counter.append([1, population[index]])
    if not comparison_similarities_counter == []:
        for index in range(len(comparison_similarities_counter)):
            sum_of_similarities += comparison_similarities_counter[index][0]
        number_of_similarity_groups = len(comparison_similarities_counter)
    return (sum_of_similarities, number_of_similarity_groups)

########################################################################################################################
# Evolution helper subs
########################################################################################################################
def _mate_couple_index_to_genome_vectors(full_population, mating_couple):
    index_partner1 = -1
    index_partner2 = -1
    for member in full_population:
        if member[0] == mating_couple[0]:
            index_partner1 = member[0]
        if member[0] == mating_couple[1]:
            index_partner2 = member[0]
        if index_partner1 != -1 and index_partner2 != -1:
            break
    genome_vector_partner1 = full_population[index_partner1][4]
    genome_vector_partner2 = full_population[index_partner2][4]
    return genome_vector_partner1, genome_vector_partner2
########################################################################################################################
# Maybe obsolete
########################################################################################################################

