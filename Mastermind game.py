# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 14:28:24 2017

@author: Alexandros
"""
import csv;
import getpass
from tkinter import *
import pandas as pd
import numpy as np
from random import randint
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sys
import msvcrt
import tkinter
import os
import base64
import subprocess
import ast


incorrectGuess = "Incorrect guess. Try again"
UsersPath = "C:/Users/Alexandros/Dropbox/PythonChallenges/users.csv"
CongratulationslegendaryModeMsg = "Congratulations! You have achieved so far the best score on legendary mode!"
CongratulationsNormalModeMsg = "Congratulations! You have achieved so far the best score on normal mode!"
LegendaryModePath = "C:/Users/Alexandros/Dropbox/PythonChallenges/highestScoreForLegendaryMode.csv"
EasyModePath = "C:/Users/Alexandros/Dropbox/PythonChallenges/highestScoreForEasyMode.csv"
NormalModePath = "C:/Users/Alexandros/Dropbox/PythonChallenges/highestScoreForNormalMode.csv"
highestScoreNormalMode = "The highest score (minimum number of efforts) recorded on normal mode is "
highestScoreLegendaryMode = "The highest score (minimum number of efforts) recorded on legendary mode is "


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def diff(t_a, t_b):
    t_diff = relativedelta(t_a, t_b)
    print("You played this game for",abs(t_diff.hours),"hours,",abs(t_diff.minutes),"minutes and",abs(t_diff.seconds),"seconds.")
    return 0
    


print("----MASTERMIND----")
print("Guess the digits in as few tries as possible")

while True:
    played_game = input("Have you played this game before? (y/n)")
    if played_game == 'y' or played_game == 'n':
        break


while True:
    while True:
        game_session_difficulty = input("Please choose the difficulty rating (easy - guess 4 numbers, normal - guess 5 numbers, legendary - guess 6 numbers) for this session: ")
        if game_session_difficulty=='easy' or game_session_difficulty=='normal' or game_session_difficulty=='legendary':
            break
        print("Wrong selection, try again")
    

    
    # password rules
    rules = [lambda s: any(x.isupper() for x in s), # must have at least one uppercase
            lambda s: any(x.islower() for x in s),  # must have at least one lowercase
            lambda s: any(x.isdigit() for x in s),  # must have at least one digit
            lambda s: len(s) >= 7                   # must be at least 7 characters
            ]

    # read CSV file & load into list
    my_file = open(UsersPath, 'r')
    reader = csv.reader(my_file, delimiter=',')
    my_list = list(reader)
    my_file.close()
    
    if not my_list:
        current_user_name = input("Please enter your unique user name: ")
        while True:
                print("Your password must contain at least 7 characters, at least one uppercase and one lowercase and one digit!")            
                os.system("python C:/Users/Alexandros/Dropbox/PythonChallenges/getPassword.py")  
                f=open("tmpPasswd.txt",'rb')
                b = f.read()
                f.close()
                decrypted_passwd = base64.b64decode(b)
                current_user_passwd = decrypted_passwd.decode('ascii')
                if all(rule(current_user_passwd) for rule in rules): 
                    print("This is your first time playing this game!")
                    my_list.append([current_user_name,b])
                    my_list_df = pd.DataFrame(my_list)
                    my_list_df.to_csv(UsersPath,sep=",",index=False,header=False)
                    break
    else:    
        # collect information 
        if played_game == "n":    
            while True:
                current_user_name = input("Please enter your unique user name: ")     
                flag = 0
                #for i in my_list:
                #    if current_user_name == i[0]:
                #        flag = 1
                if current_user_name in my_list:
                    flag = 1
                if flag == 0:
                    break
                else:
                    print("This user name already exists!")
            while True:
                print("Your password must contain at least 7 characters, at least one uppercase and one lowercase and one digit!")            
                os.system("python C:/Users/Alexandros/Dropbox/PythonChallenges/getPassword.py")  
                f=open("tmpPasswd.txt",'rb')
                b = f.read()
                f.close()
                decrypted_passwd = base64.b64decode(b)
                current_user_passwd = decrypted_passwd.decode('ascii')
                # print(current_user_passwd)
                if all(rule(current_user_passwd) for rule in rules): 
                    print("This is your first time playing this game!")
                    my_list.append([current_user_name,b])
                    my_list_df = pd.DataFrame(my_list)
                    my_list_df.to_csv(UsersPath,sep=",",index=False,header=False)
                    break
        
        if played_game == "y": 
            while True:
                current_user_name = input("Please enter your unique user name: ")
                flag = 0
                counter = 0
                if not my_list:
                    break
                for i in my_list:
                    if current_user_name == i[0]:
                        flag = 1
                        index_to_test_passwd_for_user = counter 
                    counter = counter + 1 
                if flag == 1:
                    break
                else:
                    print("No such user name exists! Try again")
            while True:
                #current_user_passwd = input("Please enter your password: ")
                os.system("python C:/Users/Alexandros/Dropbox/PythonChallenges/getPassword.py")  
                f=open("tmpPasswd.txt",'rb')
                b = f.read()
                f.close()
                #decrypted_passwd = base64.b64decode(b)
                #current_user_passwd = decrypted_passwd.decode('ascii')
                flag = 0
                #decrypted_passwd = base64.b64decode(b)
                #current_user_passwd = decrypted_passwd.decode('ascii')
                my_decoded_str = b.decode()
                print(my_decoded_str)
                tmp_passwd = my_list[index_to_test_passwd_for_user][1]
                print(tmp_passwd)
                if "b'"+my_decoded_str+"'" == tmp_passwd:
                    flag = 1
                    if flag == 1:
                        print("You have played this game before!")
                        break
                    else:
                        print("Wrong password! Try again")
    
    list_of_efforts = [None]*1000
    count_efforts = 0
    print("You can guess a thousand times")                
    d1 = datetime.now()

    
    if game_session_difficulty == "easy":
        random_num_to_guess = random_with_N_digits(4)
        print(random_num_to_guess)
        for i in range(len(list_of_efforts)):
            while True:
                guess = int(input("Enter your 4 digit number guess: "))
                if (len(str(abs(guess))) == 4):
                    break
            count_efforts = count_efforts + 1
            if str(guess) == str(random_num_to_guess):
                print("*"*4)
                print("Correct!")
                if count_efforts == 1:
                    print("You made ",count_efforts," effort!")
                else:
                    print("You made ",count_efforts," efforts!")
                break
            else:
                count_asterisks = 0
                if (str(random_num_to_guess))[0] == str(guess)[0]:
                    count_asterisks = count_asterisks + 1
                if str(random_num_to_guess)[1] == str(guess)[1]:
                    count_asterisks = count_asterisks + 1 
                if str(random_num_to_guess)[2] == str(guess)[2]:
                    count_asterisks = count_asterisks + 1
                if str(random_num_to_guess)[3] == str(guess)[3]:
                    count_asterisks = count_asterisks + 1
                print("*"*count_asterisks)
                print("Incorrect guess. Efforts made:",count_efforts,". Try again")
    elif game_session_difficulty == "normal":
        random_num_to_guess = random_with_N_digits(5)
        print(random_num_to_guess)
        for i in range(len(list_of_efforts)):
            while True:
                guess = int(input("Enter your 5 digit number guess: "))
                if (len(str(abs(guess))) == 5):
                    break
            count_efforts = count_efforts + 1
            if str(guess) == str(random_num_to_guess):
                print("*"*5)
                print("Correct!")
                if count_efforts == 1:
                    print("You made ",count_efforts," effort!")
                else:
                    print("You made ",count_efforts," efforts!")
                break
            else:
                count_asterisks = 0
                if str(random_num_to_guess)[0] == str(guess)[0]:
                    count_asterisks = count_asterisks + 1
                if str(random_num_to_guess)[1] == str(guess)[1]:
                    count_asterisks = count_asterisks + 1 
                if str(random_num_to_guess)[2] == str(guess)[2]:
                    count_asterisks = count_asterisks + 1
                if str(random_num_to_guess)[3] == str(guess)[3]:
                    count_asterisks = count_asterisks + 1
                if str(random_num_to_guess)[4] == str(guess)[4]:
                    count_asterisks = count_asterisks + 1
                print("*"*count_asterisks)
                print(incorrectGuess)
    else: 
        random_num_to_guess = random_with_N_digits(6)
        print(random_num_to_guess)
        for i in range(len(list_of_efforts)):
            while True:
                guess = int(input("Enter your 6 digit number guess: "))
                if (len(str(abs(guess))) == 6):
                    break
            count_efforts = count_efforts + 1
            if str(guess) == str(random_num_to_guess):
                print("*"*6)
                print("Correct!")
                if count_efforts == 1:
                    print("You made ",count_efforts," effort!")
                else:
                    print("You made ",count_efforts," efforts!")
                break
            else:
                count_asterisks = 0
                if str(random_num_to_guess)[0] == str(guess)[0]:
                    count_asterisks = count_asterisks + 1
                if str(random_num_to_guess)[1] == str(guess)[1]:
                    count_asterisks = count_asterisks + 1 
                if str(random_num_to_guess)[2] == str(guess)[2]:
                    count_asterisks = count_asterisks + 1
                if str(random_num_to_guess)[3] == str(guess)[3]:
                    count_asterisks = count_asterisks + 1
                if str(random_num_to_guess)[4] == str(guess)[4]:
                    count_asterisks = count_asterisks + 1
                if str(random_num_to_guess)[5] == str(guess)[5]:
                    count_asterisks = count_asterisks + 1 
                print("*"*count_asterisks)
                print(incorrectGuess)
    
    
    if game_session_difficulty == "easy":
        with open(EasyModePath, "r") as f:
            reader = csv.reader(f, delimiter=',')
            highest_score = list(reader)
        f.close()
        if not highest_score:
            print("Congratulations! You are the first person to play this game on this",game_session_difficulty,"mode!")
    elif game_session_difficulty == "normal":
        with open(NormalModePath, "r") as f:
            reader = csv.reader(f, delimiter=',')
            highest_score = list(reader)
        f.close()
        if not highest_score:
            print("Congratulations! You are the first person to play this game on this",game_session_difficulty,"mode!")
    else: 
        with open(LegendaryModePath, "r") as f:
            reader = csv.reader(f, delimiter=',')
            highest_score = list(reader)
        f.close()
        if not highest_score:
            print("Congratulations! You are the first person to play this game on this",game_session_difficulty,"mode!")
    
    if len(highest_score[0]) == 0:
        highest_score = [[None,None]]
        if game_session_difficulty == "easy":
            highest_score[0][0] = count_efforts
            highest_score[0][1] = current_user_name
            print("Congratulations! You have achieved so far the best score on easy mode!")
            tmp_df = pd.DataFrame(highest_score)
            tmp_df.to_csv(EasyModePath,sep=",",index=False,header=False)
            print("The highest score (minimum number of efforts) recorded on easy mode is ",int(highest_score[0][0])," made by ",highest_score[0][1])
        elif game_session_difficulty == "normal":
            highest_score[0][0] = count_efforts
            highest_score[0][1] = current_user_name
            print(CongratulationsNormalModeMsg)
            tmp_df = pd.DataFrame(highest_score)
            tmp_df.to_csv(NormalModePath,sep=",",index=False,header=False)
            print(highestScoreNormalMode,int(highest_score[0][0])," made by ",highest_score[0][1])
        else:
            highest_score[0][0] = count_efforts
            highest_score[0][1] = current_user_name
            print(CongratulationslegendaryModeMsg)
            tmp_df = pd.DataFrame(highest_score)
            tmp_df.to_csv(LegendaryModePath,sep=",",index=False,header=False)
            print(highestScoreLegendaryMode,int(highest_score[0][0])," made by ",highest_score[0][1])    
    else:
        tmp_var = highest_score[0][0]
        if game_session_difficulty == "easy":
            if count_efforts < int(tmp_var):
                highest_score[0][0] = count_efforts
                highest_score[0][1] = current_user_name
                print("Congratulations! You have achieved so far the best score on easy mode!")
                tmp_df = pd.DataFrame(highest_score)
                tmp_df.to_csv(EasyModePath,sep=",",index=False,header=False)
            else:
                print("The highest score (minimum number of efforts) recorded on easy mode is ",int(highest_score[0][0])," made by ",highest_score[0][1])
        elif game_session_difficulty == "normal":
             if count_efforts < int(tmp_var):
                highest_score[0][0] = count_efforts
                highest_score[0][1] = current_user_name
                print(CongratulationsNormalModeMsg)
                tmp_df = pd.DataFrame(highest_score)
                tmp_df.to_csv(NormalModePath,sep=",",index=False,header=False)
             else:
                print(highestScoreNormalMode,int(highest_score[0][0])," made by ",highest_score[0][1])
        else:
            if count_efforts < int(tmp_var):
                highest_score[0][0] = count_efforts
                highest_score[0][1] = current_user_name
                print(CongratulationslegendaryModeMsg)
                tmp_df = pd.DataFrame(highest_score)
                tmp_df.to_csv(LegendaryModePath,sep=",",index=False,header=False)
            else:
                print(highestScoreLegendaryMode,int(highest_score[0][0])," made by ",highest_score[0][1])

    
    f=open("timesGameHasBeenPlayed.txt",'r')
    counter = f.read()
    f.close()
    
    
    #counterInt = counterInt + int(counter)     
    if not counter:
        counter_int = 1
    else:
        counter_int = int(counter)               
        counter_int = counter_int + 1
    f=open("timesGameHasBeenPlayed.txt",'w')
    f.write(str(counter_int))
    f.close()
    
    # ask if player wants to play again
    while True:
        askToContinuePlaying = input("Would you like to play again? (y/n)")
        if askToContinuePlaying == 'y' or askToContinuePlaying == 'n':
            break
    if (askToContinuePlaying) == 'n':
        # inform how long was the user playing this game for this session
        print("Game Over")
        d2 = datetime.now()
        diff(d1,d2)
        if counter_int == 1:
            print("This Mastermind game has been played ",counter_int," time.")
        else:
            print("This Mastermind game has been played ",counter_int," times.")
        break
    else:
        played_game = 'y'
    
    
    
    
    