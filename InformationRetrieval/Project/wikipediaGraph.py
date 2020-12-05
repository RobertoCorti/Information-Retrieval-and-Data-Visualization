from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import json
import numpy as np
from functools import partial
from operator import is_not
from urllib.parse import unquote, unquote_plus


def filtering(arr):
    
    no_list = ['COPYING.html', 'index.html', 'images', 'raw', 'upload', 'skins']
    arr_new = []

    for x in arr:
        mask = [x != element for element in no_list]
        if all(mask):
            arr_new.append(x)
        
    return arr_new


def get_dictionaries(folder):

    sites = {}
    contents = {}
    arr = os.listdir(folder)
    arr = filtering(arr)
    for x in arr:
        arr2 = os.listdir(folder+'/'+x)
        arr2 =filtering(arr2)
        for y in arr2:
            arr3 = os.listdir(folder+'/'+x+'/'+y)
            arr3 = filtering(arr3)
            for z in arr3:
                arr4 = os.listdir(folder+'/'+x+'/'+y+'/'+z)
                for k in arr4:
                    urls = []
                    with open(folder+'/'+x+'/'+y+'/'+z+'/'+k, 'r') as f:
                        html_string = f.read()

                    soup = BeautifulSoup(html_string)
                    for link in soup.findAll('a'):
                        lnk = link.get('href')
                        if lnk is not None:
                            lnk = unquote(lnk)
                            urls.append(lnk)
                    
                    sites[x+'/'+y+'/'+z+'/'+k] = urls
                    
                    metatags = soup.find_all('meta')
                    if len(metatags) > 1:
                        contents[x+'/'+y+'/'+z+'/'+k] = metatags[1].get('content')
                    else:
                        contents[x+'/'+y+'/'+z+'/'+k] = metatags[0].get('content')        
                                                     
    return sites, contents



def preprocessing_step1(dictionary):
    
    for x in dictionary.keys():
        
        for i, z in enumerate(dictionary[x]):
            if '../../../..' in z:
                sites[x][i] = z.replace('../../../../','')
            elif '../../..' in z:
                sites[x][i] = z.replace('../../../','')
            elif '../../' in z:
                sites[x][i] = z.replace('../../','')
            elif '../' in z:
                sites[x][i] = z.replace('../','')
                
                
def preprocessing_step2(dictionary):
    
    for x in dictionary.keys():
        
        dictionary[x] = [y for y in dictionary[x] if y in dictionary.keys()]
        

def split_contents(contents):
    
    for g in contents.keys():
        contents[g] = contents[g].split(',')
        
        
def write_graph(dictionary, outputFile):

    with open(outputFile, 'w') as fp:
        json.dump(dictionary, fp)



if __name__ == '__main__':
    print('\n Scraping into data/simple ....\n')
    sites, contents = get_dictionaries('data/simple')

    preprocessing_step1(sites)
    preprocessing_step2(sites)

    split_contents(contents)

    write_graph(dictionary=sites, outputFile='data/wikipediaGraph_simple.json')
    print('Web graph written in data/wikipediaGraph_simple.json\n')
    
    write_graph(dictionary=contents, outputFile='data/wikipediaGraph_simple_contents.json')
    print('Content graph written in data/wikipediaGraph_simple_contents.json\n')

