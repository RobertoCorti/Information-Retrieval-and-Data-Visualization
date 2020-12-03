class User:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

        self.rates = {}
        
    def getTopicRate(self, topic, rate):
        
        self.rates[topic] = rate