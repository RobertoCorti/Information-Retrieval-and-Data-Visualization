# Information Retrieval Project:  WikipediaSearch


This repository contains the content of the project for the Information Retrieval course exam.

**WikipediaSearch** is a user-interactive tool that computes a Personalized PageRank over a Wikipedia corpus. The user interacts with the system by specifying the 5 topics in which he/she is interested in to look inside Wikipedia. The final result will be an HTML page containing a rank of the Wikipedia articles on which the user may be interested to look.



## How to prepare the input

To run our version of PageRank we need a set of web pages. The dataset taken into account for this work is the [simple Wikipedia dump of April 2007](https://dumps.wikimedia.org/other/static_html_dumps/April_2007/simple).

The python script [`wikipediaGraph.py`](wikipediaGraph.py) will scrape all the pages collected inside the [`simple`](simple) folder and at the output it will generate two files:

* [`data/wikipediaGraph_simple.json`](data/wikipediaGraph_simple.json) a file that contains a dictionary where each key represent an HTML page of the database. Each of them will contain a list of HTML pages of the folder that represent the set of pages that the page specifies in every tag of the following syntax: `<a href="url">link text</a>`
* [`data/wikipediaGraph_simple_contents.json`](data/wikipediaGraph_simple_contents.json) a file that contains a dictionary where each key represent an HTML page of the database. Each of them will contain a list of words specified in the `content` option inside  `<meta>` tag of the HTML document 



## Structure of the classes

* [`user.py`](user.py) contains the implementation of the `User` class. An instance of this class is characterized by a name, a surname and a dictionary that for each topic is associated a ranking ranging from 1 to 5.
* [`topicSpecificPagerank.py.py`](topicSpecificPagerank.py) contains the implementation of the `TopicSpecificPageRank` class. Inside this class we find all the methods used in order to implement a single Topic-Specific PageRank.
* [`IRsystem.py`](IRsystem.py) contains the implementation of the `IRSystem` class. This class represent the final model that we would like to compute: given a user and a Topic-Specific PageRank algorithm, the system will take into account all the user preferences specified by its own `rates` and performs a Personalized PageRank considering  linear combination of Topic-Specific PageRanks on the user's topics. The weights of each Topic-Specific PageRank vector is a normalized real value proportional to the rank specified in the user's `rates`.



## Running WikipediaSearch 

Use the interactive demo as follows:

* run ` python3 wikipediaSearch` 
* insert your `name` and `surname`

* specify 5 topics and rank each of them with a score that goes from 1 to 5

* Once indicated your topic preferences, the WikipediaSearch engine will compute the PersonalizedPageRank and it will generate an HTML file with the following path `results/result_[name][surname].html`. 

Here you find an example:




​											![Demo GIF](img/demo.gif)




## Resources
* [Presentation for the exam](https://robertocorti.github.io/)
* [Wikipedia Downloads](https://dumps.wikimedia.org/other/)
* [Original PageRank paper](http://ilpubs.stanford.edu:8090/422/1/1999-66.pdf)
* [Topic-specific PageRank - NLP Stanford](https://nlp.stanford.edu/IR-book/html/htmledition/topic-specific-pagerank-1.html)
* [Topic-Sensitive PageRank paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.85.9098&rep=rep1&type=pdf)

