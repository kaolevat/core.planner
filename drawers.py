####! /usr/bin/python3.10
import sys
import cv2
import os
from moviepy.editor import VideoFileClip, clips_array
##from moviepy import VideoFileClip, clips_array
import matplotlib
#matplotlib.use('TkAgg')
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt1
from matplotlib import colors
import numpy as np
import helpers
#import matplotlib
#matplotlib.use('Agg')
#matplotlib.use('TkAgg')
#import matplotlib.pyplot as plt

#import matplotlib as mpl
#import seaborn as sns
#import pandas as pd

def main():
    #print(sys.argv)
    chromosome_vector = sys.argv[1]
    template_map = sys.argv[2]
    title = sys.argv[3]
    file_name = sys.argv[4]
    _save_genome_vector_by_template_to_file(chromosome_vector, template_map, title, file_name)
def _plot_heatmap_2d(heatmap_array, title):
    #plt.imshow(heatmap_array, cmap='hot', interpolation='nearest')
    #plt.imshow(heatmap_array, cmap='OrRd', interpolation='nearest')
    plt.imshow(heatmap_array, cmap='rainbow', interpolation='nearest')
    plt.title(title)
    plt.colorbar()
    plt.show()

def _plot_heatmap_2d_to_file(heatmap_array, title, file):
    #print(heatmap_array)
    #print(title)
    #print(file)

    ###cmap = colors.ListedColormap(['black','red','yellow','green'])
    ###cmap = colors.ListedColormap(['black','red','gold','lawngreen'])
    ###cmap = colors.ListedColormap(['black', 'red', 'yellow', 'lawngreen'])
    cmap = colors.ListedColormap(['white', 'red', 'yellow', 'lawngreen'])
    bounds=[-0.5, 0.5, 1.5, 2.5, 3.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    #heatmap = plt.pcolor(np.array(data), cmap=cmap, norm=norm)
    #heatmap = plt.pcolor(heatmap_array, cmap=cmap, norm=norm)
    #plt.colorbar(heatmap, ticks=[0, 1, 2, 3])
    plt.imshow(heatmap_array, cmap=cmap, norm=norm)

    #cmap = mpl.colormaps["prism"].with_extremes(bad='black', under='red', over='green')
    #g = sns.heatmap(A, vmin=10, vmax=90, cmap=cmap, mask=mask)
    #####plt.imshow(heatmap_array, cmap='rainbow', interpolation='nearest')
    #plt.imshow(heatmap_array, cmap=cmap, interpolation='nearest')
    plt.title(title)
    #plt.colorbar()
    #plt.show()
    #sys.exit("_plot_heatmap_2d_to_file befire write")
    plt.savefig(file + ".jpeg")

def _draw_genome_vector_by_template(genome_vector, map_template, title):
    genome_map = _ceonvert_genome_vector_to_map(genome_vector, map_template)
    _plot_heatmap_2d(genome_map, title)

def _save_genome_vector_by_template_to_file(genome_vector, map_template, title, file):
    #print(genome_vector)
    #print(map_template)
    genome_map = _ceonvert_genome_vector_to_map(genome_vector, map_template)
    #_plot_heatmap_2d(genome_map, title)
    _plot_heatmap_2d_to_file(genome_map, title, file)
def _ceonvert_genome_vector_to_map(genome_vector, map_template):
    #print(genome_vector, map_template)
    genome_vector_counter = 0
    map_length = len(map_template)
    map_width = len(map_template[0])
    genome_map = np.zeros((map_length, map_width))
    for i in range(map_length):
        for j in range(map_width):
            #print("i = " + str(i) + ", j = " + str(j) + ", vcounter = " + str(genome_vector_counter))
            #print(map_template[i][j])
            if map_template[i][j] == 1:
                #print(str(genome_vector[genome_vector_counter]))
                genome_map[i][j] = genome_vector[genome_vector_counter]
                genome_vector_counter += 1
#            else:
#                genome_map[i].append(0)
#    print(genome_map)
#    sys.exit("GMAP")
    return genome_map

def _movie_maker(slides_directory, slide_header, movie_directory):
    video_file = movie_directory + "/" + slide_header + "_Summary_Video.avi"
    slides = [slide for slide in os.listdir(slides_directory) if slide.startswith(slide_header)]
    slides.sort(reverse = False)
    frame = cv2.imread(os.path.join(slides_directory, slides[0]))
    height, width, layers = frame.shape
    #framerate = 5
    framerate = 30
    video = cv2.VideoWriter(video_file, 0, framerate, (width, height))

    for slide in slides:
        video.write(cv2.imread(os.path.join(slides_directory, slide)))
    cv2.destroyAllWindows()
    video.release()
    #sys.exit("drawer._movie_maker not implemented")
    return video_file

def _side_by_side_movie_maker(clip1, clip2, end_file):
    # Load video clips
    clip1 = VideoFileClip(clip1)
    clip2 = VideoFileClip(clip2)
    # Resize video clips to have the same height for side-by-side placement
    clip1 = clip1.resize(height=720)  # Adjust height as needed
    clip2 = clip2.resize(height=720)  # Adjust height as needed
    # Create a side-by-side video by concatenating the clips horizontally
    final_clip = clips_array([[clip1, clip2]])
    # Write the final output to a file
    final_clip.write_videofile(end_file, codec="libx264")
    # Close the clips
    clip1.close()
    clip2.close()
def _Keff_scaled_histograma_by_population(population_scores, histograma_file_name, generation):
    plt.clf()
    plt.cla()
    plt.gca()
    population_size = len(population_scores)
    Keff_scale = [1.13, 1.14, 1.15, 1.16, 1.17, 1.18, 1.19, 1.20, 1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27, 1.28, 1.29, 1.30, 1.31, 1.32, 1.33, 1.34, 1.35, 1.36, 1.37, 1.38, 1.39, 1.40, 1.41, 1.42]
    K_counter =  [  0,    0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0]
    normalized_K_counter = []
    for each_score in population_scores:
        rounded_down_score = round(each_score, 2)
        position_of_rounded_score = Keff_scale.index(rounded_down_score)
        K_counter[position_of_rounded_score] += 1
    for each_K_count in K_counter:
        normalized_K_counter.append(each_K_count/population_size)
    plt.ylim(0, 1)
    plt.hist(Keff_scale, bins=Keff_scale, width=0.01, weights=normalized_K_counter, edgecolor='black')
    # Adding labels and title
    plt.xlabel('Keff - rounded down - Values')
    plt.ylabel('Frequency')
    plt.title('Gen -' + str(generation) + '- Histogram')
    #Save plot
    plt.savefig(histograma_file_name)
    plt.clf()
    plt.cla()
    plt.gca()
    #sys.exit()

def _2parameters_histogram(score_list, score_label1, score_label2, header, populations_size, histogram_file_name):
    #sys.exit(generation)
    #print("```````````````````````````````````")
    #print(score_list)
    #print(score_label1)
    #print(categories)
    #print(score_label2)
    ##print(bins)
    #print(histogram_file_name)
    #print("```````````````````````````````````")
    plt.clf()
    plt.cla()
    plt.gca()
    #################################################################################
    # Data
    values = score_list
    labels = [score_label1, score_label2]
    #colors = ['blue', 'orange']  # Specify colors for each bar
    colors = ['lightblue','purple']
    # Plot
    plt.ylim(0, populations_size*2)
    plt.bar(labels, values, color=colors)
    #plt.xlabel('Categories', fontweight ='bold', fontsize = 15)
    #plt.ylabel('Frequency', fontweight ='bold', fontsize = 15)
    plt.title('Histogram of Two Lists')
    #plt.xlabel('Categories')
    plt.ylabel('Frequency')
    plt.title(header)
    #plt.title('Bar Chart with Dedicated Labels and Different Colors')
    #plt.show()

    #################################################################################
    # set width of bar
    #--#barWidth = 0.25
    #--#fig = plt.subplots(figsize =(12, 8))

    # set height of bar
    #IT = [12, 30, 1, 8, 22]
    #ECE = [28, 6, 16, 5, 10]
    #CSE = [29, 3, 24, 25, 17]
    ##score_list

    # Set position of bar on X axis
    #br1 = np.arange(1)
    #br2 = [br1 + barWidth ]
    #br3 = [x + barWidth for x in br2]

    # Make the plot
    #plt.bar([0.5 ,1], score_list , color=['lightblue','purple'], width = barWidth, edgecolor='grey', label=categories)
    #--#plt.bar([0 ,1], score_list , color=['lightblue','purple'] , width = barWidth, edgecolor='grey', align='center')# , height=1)
    #print(score_list[0])
    #plt.bar(br1, score_list[0] , color='r', width = barWidth, edgecolor='grey', label=categories[0])
    #plt.bar(br2, score_list[1], color='g', width = barWidth, edgecolor='grey', label=categories[1])
    #plt.bar(br3, CSE, color ='b', width = barWidth,
    #    edgecolor ='grey', label ='CSE')

    # Adding Xticks
    #--#plt.xlabel('Categories', fontweight ='bold', fontsize = 15)
    #--#plt.ylabel('Frequency', fontweight ='bold', fontsize = 15)
    #--#plt.title('Histogram of Two Lists')

    #plt.xticks([r + barWidth for r in range(len(score_list))], [score_label1, score_label2])
    #plt.xticks([p + barWidth/2 for p in range(len(score_list))])
    #--#plt.figure(figsize=(3,6))
    #--#plt.xticks([p + barWidth/2 for p in range(len(score_list))], categories)
    #--#plt.ylim(0, 20)

    #--#plt.legend()
    #################################################################################
    #--#x = range(len(categories))
    #--#width = 0.4  # Width of the bars
    #colors = ['green', 'blue']
    #colors = (0.2, 0.6)
    #--#color = ['lightblue', 'purple']
    #plt.bar(x, score_list[0], width=width, label=score_label1, align='center')
    #plt.bar([p + width for p in x], score_list[1], width=width, label=score_label2, align='center')
    #plt.bar(categories, score_list, colors=colours, width=width, labels=[score_label1, score_label2])
    #--#plt.bar(categories, score_list, colors=color)#, width=width)#, labels=[score_label1, score_label2])#colors=colors)#, width=width)#, labels=[score_label1, score_label2])
    # Add labels and title
    #--#plt.xlabel('Categories')
    #--#plt.ylabel('Frequency')
    #--#plt.title('Bar Chart of Two Parameters')

    #--#plt.ylim(0, 20)
    # Set x-axis ticks to the category names
    #--#plt.xticks([p + width/2 for p in x], categories)

    # Add a legend
    #plt.legend()


    #################################################################################
    #plt.hist(score_list, alpha=0.7, label=[score_label1, score_label2])
    #plt.legend()
    #plt.xlabel('Generation #')
    #plt.ylabel('Frequency')
    #plt.title('Histogram of Two Lists')
    #plt.show()
    #sys.exit()
    plt.savefig(histogram_file_name)
    plt.clf()
    plt.cla()
    plt.gca()

def _plot_linear_histogram(generations, y1_array, y1_label_list, y2, y2_label, tmp_generations_directory, generations_counter):
    plt.clf()
    fig, ax1 = plt.subplots()
    color_list = ['tab:green', 'tab:orange', 'tab:red']
    color_blue = 'tab:blue'
    ax1.set_xlabel('Generation (#)')
    ax1.set_ylabel('Scores')
    plt.title("Histograma")
    if helpers._is_list_of_lists(y1_array):
        for index in range(len(y1_array)):
            #print("------------------------------------------------------")
            #print("------------------------- y1 array -------------------")
            #print(y1_array[index])
            #print("------------------------------------------------------")
            #sys.exit()
            ax1.plot(generations, y1_array[index], color=color_list[index], label=y1_label_list[index])
    else:
        ax1.plot(generations, y1_array, color=color_list[0], label=y1_label_list)
    ax1.legend(y1_label_list)
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    ax2.set_ylabel(y2_label, color=color_blue)
    ax2.plot(generations, y2, color=color_blue)
    ax2.tick_params(axis='y', labelcolor=color_blue)
    fig.tight_layout()
    # plt.legend()
    savefig_file_name = (tmp_generations_directory + "/" + str(y2_label) + ".Summary.UptoGen."
                         + str(generations_counter) + ".jpeg")
    plt.savefig(savefig_file_name)
    plt.clf()
    plt.cla()
    plt.gca()
    fig.clear()
    del ax1, ax2
    return savefig_file_name

def _singlesidesY_plot_linear_histogram(generations, y1_array, y1_label_list, header, tmp_generations_directory, generations_counter):
    plt.clf()
    fig, ax1 = plt.subplots()
    color_list = ['tab:green', 'tab:orange', 'tab:red']
    ax1.set_xlabel('Generation (#)')
    ax1.set_ylabel('Scores')
    plt.title("Histograma")
    if helpers._is_list_of_lists(y1_array):
        for index in range(len(y1_array)):
            #print("------------------------------------------------------")
            #print("------------------------- y1 array -------------------")
            #print(y1_array[index])
            #print("------------------------------------------------------")
            #sys.exit()
            ax1.plot(generations, y1_array[index], color=color_list[index], label=y1_label_list[index])
    else:
        ax1.plot(generations, y1_array, color=color_list[0], label=y1_label_list)
    ax1.legend(y1_label_list)
    ax1.tick_params(axis='y')
    fig.tight_layout()
    savefig_file_name = (tmp_generations_directory + "/" + str(header) + ".Summary.UptoGen."
                         + str(generations_counter) + ".jpeg")
    plt.savefig(savefig_file_name)
    plt.clf()
    plt.cla()
    plt.gca()
    fig.clear()
    del ax1
    return savefig_file_name

##################################################################################
############## Run Env ###########################################################
if __name__ == "__main__":
        main()
        sys.exit(0)
############## Run Env ###########################################################
##################################################################################
