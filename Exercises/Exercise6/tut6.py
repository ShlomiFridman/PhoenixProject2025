# -*- coding: utf-8 -*-
"""tut6.ipynb

Automatically generated by Colab.

"""

pip install requests beautifulsoup4

pip install requests beautifulsoup4 nltk

import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        return None

import re

def index_words(soup):
    index = {}
    words = re.findall(r'\w+', soup.get_text())
    for word in words:
        word = word.lower()
        if word in index:
            index[word] += 1
        else:
            index[word] = 1
    return index

def remove_stop_words(index):
    stop_words = {'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at', 'to'}
    for stop_word in stop_words:
        if stop_word in index:
            del index[stop_word]
    return index

from nltk.stem import PorterStemmer

def apply_stemming(index):
    stemmer = PorterStemmer()
    stemmed_index = {}
    for word, count in index.items():
        stemmed_word = stemmer.stem(word)
        if stemmed_word in stemmed_index:
            stemmed_index[stemmed_word] += count
        else:
            stemmed_index[stemmed_word] = count
    return stemmed_index

def search(query, index):

   stemmer = PorterStemmer()
   query_words = re.findall(r'\w+', query.lower())
   print(query)
   results = {}
   for word in query_words:
        word = stemmer.stem(word)
        if word in index:
            results[word] = index[word]
   return results

def search_engine(url, query):
    soup = fetch_page(url)
    if soup is None:
        return None
    index = index_words(soup)
    index = remove_stop_words(index)
    index = apply_stemming(index)
    results = search(query, index)
    return results

def queryURL(url, query):
  results = search_engine(url, query)
  print(results)
  rank=1
  for word, count in results.items():
    rank = rank*1/count
  rank = 1-rank
  print(f"{rank:.4f}")

url = 'https://w3.braude.ac.il/?lang=en'

for q in ['Industry', 'Braude college', 'Galilee center']:
  queryURL(url, q)

"""the new rank is how much percentage of the total index does the query match"""

def search_engine_ver2(url, query):
    soup = fetch_page(url)
    if soup is None:
        return None
    index = index_words(soup)
    index = remove_stop_words(index)
    index = apply_stemming(index)
    results = search(query, index)
    return results, sum(c for w,c in index.items())

def queryURL_ver2(url, query):
  results, total_cntr = search_engine_ver2(url, query)
  sorted(results, key=lambda x: x[1])
  rank=0
  for word, count in results.items():
    rank += count
  rank /= total_cntr
  rank *= 100
  print(f"{rank:.2f}% match")

for q in ['Industry', 'Braude college', 'Galilee center']:
  queryURL_ver2(url, q)

"""The rank method varies by what he programmer wants, if he wants cover percentage then the new method might be more helpful, if he wants a value in range of [0,1] then the original rank method is better"""