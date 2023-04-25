###################################################
# This is an app to retrieve critics consensuses  #
# from Rotten Tomatoes 100 best films list.       #
# It will print a preview of the first            #
# few reviews and save all of them on a file.     #
###################################################

import nltk, requests, datetime, webbrowser
from bs4 import BeautifulSoup
from termcolor import colored
from urllib import request
import json
import re, pandas as pd

"""Defining functions"""

def main():
        review_links = [] #links to individual film pages
        preview = [] #links to critics consensuses
        titles = []
        url = "https://www.rottentomatoes.com/top/bestofrt/" #best 100 films url
        parser = "html.parser"
        html = requests.get(url)
        soup = BeautifulSoup(html.text, parser) #parses the 100 best films page
        # Find all links that have the specified attributes
        links = soup.find_all('a', {'data-track': 'scores', 'data-qa': 'discovery-media-list-item-caption', 'slot': 'caption'})

        # Extract the href values using a list comprehension
        href_values = [link.get('href').strip() for link in links if link.get('href')]
        for i in href_values: #iterates through dictionary
            review_links.append("https://www.rottentomatoes.com/"+str(i)) #extracts the url from the dictionary


        for i in review_links: #iterates through links to individual pages
            link = requests.get(i) #retrieves the URLs
            page_content = link.content #extracts URL contents from individual film pages
            soup = BeautifulSoup(page_content, 'html.parser') #parses the film page
            for i in soup.find_all('span', {'data-qa': 'critics-consensus'}): #looks for the tagging for critics consensus
                i = i.get_text() #extracts only the text int he paragraph
                preview.append(i)
            for c in soup.find("title"): #extracts page title
                c = re.sub("- Rotten Tomatoes", "", c) #resubs everything else than film's name
                titles.append(c)

        # Create a dataframe from the data
        df = pd.DataFrame({'Title': titles, 'Review Link': review_links, 'Preview': preview})

        # Print the head of the dataframe
        print(df.head())

        # Save the dataframe to a CSV file
        df.to_csv('rotten_tomatoes.csv', index=False)


main()
