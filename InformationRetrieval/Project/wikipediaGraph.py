from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import json
import numpy as np
from functools import partial
from operator import is_not
from urllib.parse import unquote, unquote_plus
import warnings
warnings.filterwarnings('ignore')


def filtering(folders):
    '''
    Filtering function that avoids to include in the crawl the 'COPYING.html', 'index.html' files and the 'images', 'raw', 'upload', 'skins' folders.

    Parameters
    ----------   
    folders : list
        List of strings that contains the list of folders of a subset of the Wikipedia dump.
    '''
    no_list = ['COPYING.html', 'index.html', 'images', 'raw', 'upload', 'skins']
    folders_new = []

    for x in folders:
        mask = [x != element for element in no_list]
        if all(mask):
            folders_new.append(x)
        
    return folders_new


def get_dictionaries(folder):
    '''
    Given the Wikipedia dump folder, get a dictionary for the articles graph and contents graph.

    Parameters
    ----------   
    folder : string
        Path of the Wikipedia dump folder.
    '''
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
    '''
    Preprocessing step of graph dictionary where it is removed from the lists of the keys the '..' symbol in the links.

    Parameters
    ----------   
    dictionary : python dictionary
        Dictionary containing the Wikipedia articles graph.
    '''
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
                
def filter_useful_pages(dictionary):
    '''
    Preprocessing step of graph dictionary where it is removed from the keys some not useful articles.

    Parameters
    ----------   
    dictionary : python dictionary
        Dictionary containing the Wikipedia articles graph.
    '''
    not_useful_pages= ['Category~', 'GFDL', 'Help~','Image~',
                        'Special~', 'Talk~', 'Template',
                        'User~', 'User_', 'Wikimedia', 'Wikipedia~', 
                        'Wiktionary']
    
    dictionary_new = {}
    for key in dictionary.keys():
        mask = [x not in key for x in not_useful_pages]
        if all(mask):
             dictionary_new[key] = dictionary[key]
    return dictionary_new
                
def preprocessing_step2(dictionary):
    '''
    Preprocessing step of graph dictionary where it is removed from the lists of the keys all that elements that are not contained in dictionary.keys() (i.e. external pages)

    Parameters
    ----------   
    dictionary : python dictionary
        Dictionary containing the Wikipedia articles graph.
    '''
    for x in dictionary.keys():
        
        dictionary[x] = [y for y in dictionary[x] if y in dictionary.keys()]
        

def split_contents(contents):
    '''
    Preprocessing step of content graph dictionary where happens the following transformation: contents['i/t/a/Italy.html'] = 'Italy, 1861, 1945, ...' ----> ['Italy', '1861', '1945', ...]

    Parameters
    ----------   
    contents : python dictionary
        Dictionary containing the contents of the Wikipedia articles graph.
    '''
    for g in contents.keys():
        contents[g] = contents[g].split(',')
        
        
def write_graph(dictionary, output_file):
    '''
    Write in a json file the dictionary in a outputFile path. 

    Parameters
    ----------   
    dictionary : python dictionary
        Dictionary containing the the Wikipedia articles graph or the Wikipedia contents articles graph.
    output_file : string
        String containing the path of the written graph.
    '''
    with open(output_file, 'w') as fp:
        json.dump(dictionary, fp)



if __name__ == '__main__':
    
    print('\n Scraping into data/simple ....\n')
    sites, contents = get_dictionaries('data/simple')

    preprocessing_step1(sites)

    sites = filter_useful_pages(sites)
    contents = filter_useful_pages(contents)

    preprocessing_step2(sites)

    split_contents(contents)

    write_graph(dictionary=sites, output_file='data/wikipediaGraph_simple.json')
    print('Web graph written in data/wikipediaGraph_simple.json\n')
    
    write_graph(dictionary=contents, output_file='data/wikipediaGraph_simple_contents.json')
    print('Content graph written in data/wikipediaGraph_simple_contents.json\n')

