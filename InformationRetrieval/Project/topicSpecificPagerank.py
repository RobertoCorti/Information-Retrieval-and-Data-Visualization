import json
import numpy as np
from scipy.sparse import csr_matrix

class TopicSpecificPageRank:
    
    def __init__(self, graphFile, contentFile):
        '''
        Init method of TopicSpecificPageRank class. It calls generate_graph(), generate_contents() and compute_stochastic_matrix()
        
        Parameters
        ----------   
        graphFile : string
            The json file path on which the web graph is stored.
        contentFile : string
            The json file path on which the content dictionary is stored.
        '''
        self.graph_file = graphFile
        self.content_file = contentFile

        self.generate_graph() 
        self.generate_contents() 
        self.generate_stochastic_matrix() 

        
    def generate_graph(self):
        '''
        Generates from self.graph_file the web graph and stores it into self.graph and the number of nodes into self.num_nodes.
        The web graph will contain for each node (page) a list of strings that contains the list of nodes of the graph by wich the node links in its HTML page.
        '''
        with open(self.graph_file, 'r') as f:
            g = json.load(f)
        self.graph = g
        self.num_nodes = len(g.keys())
        
    def generate_contents(self):
        '''
        Generates from self.content_file the content dictionary and stores it into self.content.
        The content dictionary will contain for each key (page) a list of strings that contains the topics specified from the HTML meta information.
        '''
        with open(self.content_file, 'r') as f: 
            c = json.load(f)
        self.contents = c
        
    def generate_stochastic_matrix(self):
        '''
        Generates from self.graph the stochastic matrix of the graph using scipy.sparse.csr_matrix.
        '''
        key_to_pos = dict(zip(self.graph.keys(), range(0,self.num_nodes)))
        row = []
        col = []
        data = []

        for key in self.graph.keys():
            for edge in self.graph[key]:
                row.append(key_to_pos[key])
                col.append(key_to_pos[edge])
                data.append(1/len(self.graph[key]))
        R = csr_matrix((data, (row, col)), shape=(self.num_nodes, self.num_nodes))
    
        self.R = R
    
    def generate_jump_vector(self, topic):
        '''
        Generates from a given topic the jump vector, a (self.num_nodes,) array that contains for the i-th component 0 if the node doesn't have topic in its contents, 1/|S| otherwise (S subspace of nodes containing topic).
        
        Parameters
        ----------   
        topic : string
            The topic on which we want to generate the jump vector.
        '''
        key_to_pos = dict(zip(self.graph.keys(), range(0,self.num_nodes)))
        seeds = np.zeros(self.num_nodes)

        for key in self.contents.keys():
            lower_key_content = [x.lower() for x in self.contents[key]]
            mask = [topic in x for x in lower_key_content]
            if any(mask):
                seeds[key_to_pos[key]] = 1

        if (np.sum(seeds)!=0):
            self.J = seeds/sum(seeds)
        else: 
            self.J = seeds
        
    def topicSpecificPageRank_iteration(self, x, alpha):
        '''
        Single iteration of Topic-Specific PageRank. It returns an array of shape (self.num_nodes,) which contains un update of the PageRank vector.
        
        Parameters
        ----------   
        x     : array of shape (self.num_nodes,)
            The current PageRank vector.
        alpha : float
            Real-value between [0,1] which represents the teleporting probability.
        '''
        P = (1 - alpha) * self.R
        x_prime = (P.T).dot(x) + alpha * self.J
        return x_prime
    
    def compute_TopicSpecificPageRank(self, topic, alpha, epsilon):
        '''
        Based on one single topic, computes the PageRank of self.graph with teleporting probability alpha and precision epsilon.
        
        Parameters
        ----------   
        topic : string
            The topic on which we want to perform the PageRank.
        alpha : float
            Real-value between [0,1] which represents the teleporting probability.
        epsilon: float
            Precision of the iterative computation of the PageRank vector.
        '''
        self.generate_jump_vector(topic)
        if (np.sum(self.J)==0):
            print('There are no pages related to '+topic)
            x = np.zeros(self.num_nodes)
            return x
        x = np.random.rand(self.num_nodes)
        x = x/x.sum()
        err = np.inf # initially infinity
        while (err > epsilon):
            x_new = self.topicSpecificPageRank_iteration(x, alpha)
            err = (abs(x_new - x)).sum()
            x = x_new
        return x