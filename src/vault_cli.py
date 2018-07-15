# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 18:28:08 2017

@author: Thorben Jensen
"""

#%% IMPORTS

import os
import sys
import time

#%% DIALOGUE FUNCTIONS


def display_title_bar():
    os.system('clear')
    print('------------------------------')
    print('--------- LIFE VAULT ---------')
    print('------------------------------\n')  


def show_commands():
    print('Please choose from the following commands.\n')
    for command in commands.keys():
        print(command + ':\t' + commands[command])


def user_input(prompt):   
    command = input('\n' + prompt)
    if command not in commands.keys():
        display_title_bar()
        print('Command not found!\n')
        show_commands()
        command = user_input(prompt)
    return command


def execute_command(command):
    if command not in commands.keys():
        raise Exception('Command %s is not implemented.' % command)
    methods[command]()


def dialogue():
    display_title_bar()
    show_commands()
    command = user_input(prompt='')
    execute_command(command)
    # repeat
    dialogue()    


#%% ACTION FUNCTIONS
def command_quit():
    print('\nGoodbye.')
    exit
    quit    
    sys.exit()


def command_google():
    print('To be implemented... returning to main menu.')
    time.sleep(5)
   

#%% GLOBAL INFORMATION

commands = {'google': 'Retrieve data from Google Takeout.',
            'quit': 'Quit Life Vault.',
            }
            
methods = {'google': command_google,
           'quit': command_quit,
           }

#%% MAIN

dialogue()