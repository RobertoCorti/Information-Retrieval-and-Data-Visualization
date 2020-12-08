class User:

    def __init__(self, name, surname):
        '''
        Init method of User class. It sets the user's name, surname and initialize the rates of the user with an empty dictionary.
        
        Parameters
        ----------   
        name : string
            Name of the user.
        surname : string
            Surname of the user.
        '''
        self.name = name
        self.surname = surname

        self.rates = {}
        
    def get_topic_rate(self, topic, rate):
        '''
        Set the rate of the given topic.
        
        Parameters
        ----------   
        topic : string
            Topic on which the user is interested.
        rate : int
            Value between [1,5] that specify the degree of interest of the topic.
            Low interest = 1, High interest = 5.
        '''
        self.rates[topic] = rate