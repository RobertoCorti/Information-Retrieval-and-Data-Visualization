# Information Retrieval Project: a personalized Wikipedia search engine



This repository contains the content of the project for the Information Retrieval course exam.

**WikipediaSearch** is a user-interactive tool that computes a Personalized PageRank over a Wikipedia corpus.



## How to prepare the input

To run our version of PageRank we need a set of web pages in order to build a web graph. The dataset taken into account for this work is the [simple Wikipedia dump of April 2007](https://dumps.wikimedia.org/other/static_html_dumps/April_2007/simple).

The python script `wikipediaGraph.py` will scrape all the pages collected inside the `simple` folder and at the end it will generate two files:

* `data/wikipediaGraph_simple.json` a file that contains a dictionary where each key represent an HTML page of the database. Each of them will contain a list of html pages that represent the set of pages that the key page specifies in every tag of the following syntax: `<a href="url">link text</a>`
* `data/wikipediaGraph_simple_contents.json` a file that contains a dictionary where each key represent an HTML page of the database. Each of them will contain a list of words specified in the `content ` option inside  `<meta>` tag inside the HTML document 



## Structure of the classes

* `user.py` contains the implementation of the `User` class. An instance of this class is characterized by a name, a surname and a dictionary that for each topic is associated a ranking ranging from 1 to 5.
* `personalizedPageRank.py` contains the implementation of the `PersonalizedPageRank` class. Inside this class we find all the methods used in order to implement a single topic specific PageRank.
* `IRsystem.py` contains the implementation of the `IRSystem` class. This class represent the final model that we would like to compute: given a user and a topic specific PageRank algorithm, the system will take into account all the user preferences specified by its own `rates` and performs a topic specific PageRank for each of these topics and will give as output a linear combination of these results. The weights of each topic PageRank vector is a normalized real value proportional to the rank specified in the user's `rates`.



## Running WikipediaSearch 

Use the interactive demo as follows:

* run ` python3 wikipediaSearch` 
* insert your `name` and `surname`

* specify 5 topics and rank each of them with a score that goes from 1 to 5




![Demo GIF](img/demo.gif)



Once indicated your topic preferences, the WikipediaSearch engine will compute the PersonalizedPageRank and it will generate an HTML file with the following path `results/result_[name][surname].html`



## Resources

* [Wikipedia Downloads](https://dumps.wikimedia.org/other/)
* [Topic-specific PageRank - NLP Standford](https://nlp.stanford.edu/IR-book/html/htmledition/topic-specific-pagerank-1.html)
* [Topic-Sensitive PageRank paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.85.9098&rep=rep1&type=pdf)

