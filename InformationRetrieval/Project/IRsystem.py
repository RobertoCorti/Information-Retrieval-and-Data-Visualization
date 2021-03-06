import numpy as np
from user import User
from topicSpecificPagerank import TopicSpecificPageRank
from dominate import document
from dominate.tags import ul, li, a, h1, h2

class IRsystem():

    def __init__(self, user, pagerank):
        '''
        Init method of IRsystem class. It sets the user of the system and the current pagerank.
        
        Parameters
        ----------   
        user : class User instance
            User of the current Information Retrieval system.
        pagerank : a TopicSpecificPageRank instance
            A Topic Specific PageRank algorithm.
        '''
        self.user = user
        self.pagerank = pagerank

    def compute_weights(self):
        '''
        Using self.user.rates dictionary, it computes the weights of the linear combination of PageRank vector.
        For each topic specified by self.user.rates the weight will be weights_{topic} = self.user.rate[topic] / sum(weights)
        '''
        self.weights = np.array([self.user.rates[x] for x in self.user.rates.keys()])
        self.weights = self.weights/np.sum(self.weights) 
    
    
    def compute_final_pagerank(self, alpha, epsilon):
        '''
        Compute the final PageRank vector based on the topic specifications of self.user.
        The PageRank vector will be an array of shape (self.pagerank.num_nodes,) and it will be equal to the linear combination: 
                weight_{topic_1}*TopicSpecificPageRank(topic_1)+.....+ weight_{topic_n}*TopicSpecificPageRank(topic_n)
        
        Parameters
        ----------   
        alpha : float
            Real-value between [0,1] which represents the teleporting probability.
        epsilon: float
            Precision of the iterative computation of the PageRank vector.
        '''
        self.compute_weights()
        xs = []
        
        for topic in self.user.rates.keys():
            x = self.pagerank.compute_TopicSpecificPageRank(topic, alpha, epsilon)
            xs.append(x)
        
        xs = np.array(xs)
        self.pagerank_vector = np.dot(self.weights, xs) 
        self.dict = {}
        for i, k in enumerate(self.pagerank.graph.keys()):
            self.dict[k] = self.pagerank_vector[i]

    def write_result(self):
        '''
        Writes self.pagerank_vector into an HTML file with the following path 'result/result_'+self.user.name+self.user.surname+'.html'
        '''
        paths = []
        for w in sorted(self.dict, key=self.dict.get, reverse=True):
            paths.append('../data/simple/'+w)

        with document(title='Result') as doc:
            h1('WikipediaSearch')
            h2('Result for '+self.user.name+' '+self.user.surname)
            for path in paths:
                # remove 'folder1/folder2/folder3/' prefix
                name = path[21:]
                # remove '.html' extension
                name = name.replace('.html','')
                # remove '_ab2c' string at the end of some files
                if len(name)>5:
                    if name[len(name)-5] == '_':
                        name = name[0:len(name)-5]
                # substitute '_' with spaces
                name = name.replace('_',' ')
                # write link tag
                ul(li(a(name, href=path), __pretty=True))


        with open('result/result_'+self.user.name+self.user.surname+'.html', 'w') as f:
            f.write(doc.render())