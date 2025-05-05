#import sys
import os
from termcolor import cprint
#import time
import pytz
import datetime
import time
import re

#def _get_numeric_time():
#	return time.time()
def _is_list_of_lists(var):
    return all(isinstance(sublist, list) for sublist in var) if isinstance(var, list) else False
def _debug_stopper():
	while True:
		Answer = input('Is the information above correct?')
		SimplifiedAnswer = Answer[0].lower()
		if Answer == '' or not SimplifiedAnswer in ['y','n']:
			print('Please answer with yes or no!')
		else:break
	print ("Simplified Answer is:"+SimplifiedAnswer)
	if SimplifiedAnswer != 'y':exit()
def _system_executor(exec_command):
	stream = os.popen(exec_command)
	output = stream.read()
	return (output)
def _get_human_time_string():
    return datetime.datetime.now(pytz.utc).strftime('%Y-%m-%d--%H-%M-%S.%f')
def _get_current_time_in_seconds():
    return time.time()
def _diff_time_seconds(time1, time2):
    return time2 - time1

def _check_valid_chars_in_line(line,valid_chars):
    return bool(re.compile('^['+valid_chars+']+$').match(line))
def _count_substring_in_text_array(text,substring,ignore_lines_with):
    text_counter = 0
    for line in text:
        if not line.strip().startswith(ignore_lines_with) and not line.strip() == "":
            text_counter = text_counter + line.count(substring)
    return text_counter
def _variance_orchestrator():
    print("Variance Orchestrator - still not implemented")

def _print_norm_green(norm_text,green_text):
    print (norm_text, end = ''),cprint (green_text,'green',attrs=['bold'])
def _print_norm_red(norm_text,red_text):
    print (norm_text, end = ''),cprint (red_text,'red',attrs=['bold'])
def _print_norm_blue(norm_text,blue_text):
    print (norm_text, end = ''),cprint (blue_text,'blue',attrs=['bold'])

def _print_norm_blue_verb(norm_text, blue_text, verb):
    if verb == 'y':
        print (norm_text, end = ''),cprint (blue_text,'blue',attrs=['bold'])
def _print_norm_blue_green(norm_text,blue_text,green_text):
    print (norm_text, end = ''),cprint (blue_text,'blue',attrs=['bold'], end = ''),cprint (green_text,'green',attrs=['bold'])
def _print_norm_blue_red(norm_text,blue_text,red_text):
    print (norm_text, end = ''),cprint (blue_text,'blue',attrs=['bold'], end = ''),cprint (red_text,'red',attrs=['bold'])
def _print_norm_green_verb(norm_text, green_text, verbosity):
    if verbosity == 'y':
        print(norm_text, end=''), cprint(green_text, 'green', attrs=['bold'])
def _print_norm_red_verb(norm_text, red_text, verbosity):
    if verbosity == 'y':
        print(norm_text, end=''), cprint(red_text, 'red', attrs=['bold'])
def _pause():
    while True:
        answer = input('Is the information above correct?')
        simplified_answer = answer[0].lower()
        if answer == '' or not simplified_answer in ['y','n']:
            print('Please answer with yes or no!')
        else:break
        print ("Simplified Answer is:"+simplified_answer)
        if simplified_answer != 'y':exit()
