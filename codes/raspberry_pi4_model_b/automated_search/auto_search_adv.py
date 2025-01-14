# this code is designed to:
# 1. fetch search results from DuckDuckGo for the query "feminism is" 
# 2. then parse and analyze the snippets from those results 
# 3. extract and print only the sentences containing the phrase "feminism is"

import logging
from urllib3.exceptions import MaxRetryError, NameResolutionError, TimeoutError, ReadTimeoutError
import requests # requests library used for making HTTP requests in Python (allows the script to fetch web pages)
import traceback
from bs4 import BeautifulSoup # BeautifulSoup class from the bs4 library, for parsing HTML and XML documents
#nltk.download('punkt')  # Ensure the NLTK punkt tokenizer models are downloaded (punkt tokenizer is a pre-trained model used by NLTK for dividing text into a list of sentences)
from nltk.tokenize import sent_tokenize # nltk python library = natural language toolkit, sent_tokenize function is used for splitting text into a list of sentence

logger = logging.getLogger(__name__)

def parse_definitions():
    
    # headers dictionary is used to mimic a browser request, making the server think the request is coming from a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0",
    }
    auto_database = [] # initially defining the database as empty array
    
    try:
        # Fetch the page content from DuckDuckGo search
        page = requests.get('https://duckduckgo.com/html/?q="feminism+is"', headers=headers).text

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(page, 'html.parser').find_all("a", class_="result__snippet")
        
        # Iterate through each search result snippet
        for link in soup:
            # Split the snippet text into sentences using NLTK's sent_tokenize
            sentences = sent_tokenize(link.text)
            
            # Iterate through each sentence in the snippet
            for sentence in sentences:
                # Check if the sentence contains the phrase "feminism is"
                # and does not contain a colon.
                # The .lower() method is used to make the search case insensitive
                if "feminism is" in sentence.lower() and ":" not in sentence:
                    #print(sentence)  # Print the sentence if it contains the phrase
                    auto_database.append(sentence)
                    #print()  # Print a newline for better readability  
                                              
    except ConnectionError as e: # if the ConnectionError occurs, it will return the auto_database as an empty array
        logger.info('Connection error ocurred')
        print('ConnectionError ocurred') 
        #traceback.print_exc() # prints the error details
    except OSError as e: # if the ConnectionError occurs, it will return the auto_database as an empty array
        logger.info('OSError ocurred')
        print('OSError ocurred') 
        #traceback.print_exc() # prints the error details
    except MaxRetryError as e:
        logger.info('MaxRetryError ocurred') 
        print('MaxRetryError ocurred') 
        #traceback.print_exc() # prints the error details
    except NameResolutionError as e:
        logger.info('NameResolutionError ocurred') 
        print('NameResolutionError ocurred') 
        #traceback.print_exc() # prints the error details
    except ReadTimeoutError as e:
        logger.info('ReadTimeoutError ocurred') 
        print('ReadTimeoutError ocurred') 
        #traceback.print_exc() # prints the error details
    except TimeoutError as e:
        logger.info('TimeoutError ocurred') 
        print('TimeoutError ocurred') 
        #traceback.print_exc() # prints the error details
        
    return auto_database

if __name__ == '__main__':
    auto_database = parse_definitions()
    for record in auto_database:
        print(record)