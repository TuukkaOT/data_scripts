###############################################
# This program accesses the YLE and Guardian  #
# news websites, retrieves text from them and #
# prints the top ten headlines.               #
# ––––––––––––––––––––––––––––––––––––––––––– #
# This was made for an assignment at the NLP  #
# course KIK-LG211 at University of Helsinki  #
# "NLTK and "termcolor" need to be installed  #
# in order for this program to work.          #
###############################################

import nltk, requests, datetime, webbrowser
from bs4 import BeautifulSoup
from termcolor import colored
from urllib import request #to make the Reuters retrieval work

"""Defining functions"""

def guardian_logo():
    print()
    print(colored("   _____                     _ _             ", "cyan"))
    print(colored("  / ____|                   | (_)            ", "cyan"))
    print(colored(" | |  __ _   _  __ _ _ __ __| |_  __ _ _ __  ", "cyan"))
    print(colored(" | | |_ | | | |/ _` | '__/ _` | |/ _` | '_ \ ", "cyan"))
    print(colored(" | |__| | |_| | (_| | | | (_| | | (_| | | | |", "cyan"))
    print(colored("  \_____|\__,_|\__,_|_|  \__,_|_|\__,_|_| |_|", "cyan"))
    print()

def reuters_logo():
    print()
    print(colored("_____________________________  ", "red"))
    print(colored("\______   \______   \_   ___ \ ", "red"))
    print(colored(" |    |  _/|    |  _/    \  \/ ", "red"))
    print(colored(" |    |   \|    |   \     \____", "red"))
    print(colored(" |______  /|______  /\______  /", "red"))
    print(colored("        \/        \/        \/ ", "red"))
    print()



def main():
    open_site = "b"
    while open_site == "b":
        interest = input("Would you like to see news from (1) Guardian or (2) BBC? Type 1 or 2: ")
        if interest == "1":
            lista2 = []
            cleanlist2 = []
            linkit2 = []

            url = "https://www.theguardian.com/world"
            html = requests.get(url)
            page = html.content
            soup = BeautifulSoup(page, 'html.parser')

            for i in soup.find_all(class_="fc-item__title"):
                i = i.get_text()
                i = str(i).strip()
                i = str(i).replace('  ',' ')
                if len(lista2) < 10:
                    lista2.append(i)

            #this for-loop extracts the url links corresponding the headlines
            for link in soup.find_all(class_="fc-item__link"):
                link = link.get("href")
                if len(linkit2) < 10: #appends 10 first headlines to a list
                    linkit2.append(link)

            now = datetime.datetime.now() #creates a variable that contains current time

            print("***********")
            guardian_logo()
            print("Time is", now.strftime("%Y-%m-%d %H:%M:%S"))
            print()
            print("The first ten headlines from Guardian World News website are:\n")
            for i, (x, y) in enumerate(zip(lista2, linkit2)):
                print(x, "\nURL:", y, "\n*")
            #print(*lista2, sep ='\n*\n')
            print("***********")
            print()


        elif interest == "2":

            """Tried another way of retrieving the website"""
            url = "https://www.bbc.com/news/world"
            html = request.urlopen(url).read().decode('utf8')

            #url = "https://www.bbc.com/world"
            #html = requests.get(url)
            #page = html.content

            soup = BeautifulSoup(html, 'html.parser')

            lista4 = []
            cleanlist4 = []
            linkit4 = []

            for i in soup.find_all(class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor"):
                i = i.get_text()
                i = str(i).strip()
                i = str(i).replace('  ',' ')
                if len(lista4) < 10:
                    lista4.append(i)

            #this for-loop extracts the url links corresponding the headlines
            for link in soup.find_all(class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor"):                  #THIS ONE DOESN'T WORK YET, NEED TO FIND THE RIGHT CLASS?
                link = link.get("href")
                if len(linkit4) < 10:                       #appends 10 first headlines to a list
                    if link[0] == "/":                      #checks if the link is missing https://www.bbc.com and adds it to the beginning
                        link = "https://www.bbc.com" + link
                    linkit4.append(link)

            now = datetime.datetime.now() #creates a variable that contains current time

            print("***********")
            reuters_logo()
            print("Time is", now.strftime("%Y-%m-%d %H:%M:%S"))
            print()
            print("The first ten headlines from BBC World News website are:\n")

            for i, (x, y) in enumerate(zip(lista4, linkit4)):
                print(x, "\nURL:", y, "\n*")
            print("***********")
            print()


            """Next, the program asks for input on what the user wants to do, i.e. open a website, refresh the headlines, or quit."""

        open_site = input("If you want to open (1) Guardian, (2) BBC or (3) all websites, enter 1, 2 or 3. \nTo go back to choosing your news, enter \"b\". To quit, press enter: ")
        if open_site == "1":
            webbrowser.open('https://www.theguardian.com/world', new=2)
            print("Thank you. Goodbye!")
        elif open_site == "2":
            webbrowser.open('https://www.bbc.com/news/world', new=2)
            print("Thank you. Goodbye!")
        elif open_site == "3":
            webbrowser.open('https://www.theguardian.com/world', new=2)
            webbrowser.open('https://www.bbc.com/news/world', new=2)
            print("Thank you. Goodbye!")
        if open_site == "":
            print("Thank you. Goodbye!")
main()
