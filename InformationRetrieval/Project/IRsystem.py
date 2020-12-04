import numpy as np
from user import User
from personalizedPagerank import PersonalizedPageRank
from dominate import document
from dominate.tags import ul, li, a, h1, h2

class IRsystem():

    def __init__(self, user, pagerank):
        self.user = user
        self.pagerank = pagerank

    def compute_weights(self):
        
        self.weights = np.array([self.user.rates[x] for x in self.user.rates.keys()])
        self.weights = self.weights/np.sum(self.weights) 
    
    
    def compute_final_pagerank(self, alpha, epsilon):
        
        self.compute_weights()
        xs = []
        
        for topic in self.user.rates.keys():
            x = self.pagerank.compute_PersonalizedPageRank(topic, alpha, epsilon)
            xs.append(x)
        
        xs = np.array(xs)
        self.pagerank_vector = np.dot(self.weights, xs) 
        self.dict = {}
        for i, k in enumerate(self.pagerank.graph.keys()):
            self.dict[k] = self.pagerank_vector[i]

    def write_result(self):
        paths = []
        for w in sorted(self.dict, key=self.dict.get, reverse=True):
            not_useful_pages= ['User', 'Category', 'Wiki','Help','Image','Special','License', 'GFDL', 'language']
            mask = [x not in w for x in not_useful_pages]
            if all(mask):
                paths.append('../data/simple/'+w)
                #print(w, self.dict[w])

        with document(title='Result') as doc:
            h1('Wikipedia PersonalizedPageRank')
            h2('Result for '+self.user.name+' '+self.user.surname)
            for path in paths:
                name = path[21:]
                name = name.replace('.html','')
                ul(li(a(name, href=path), __pretty=False))


        with open('result/result_'+self.user.name+self.user.surname+'.html', 'w') as f:
            f.write(doc.render())