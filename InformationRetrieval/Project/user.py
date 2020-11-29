class User:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

        self.rates = { 'art': 0,
                       'business': 0,
                       'computer': 0,
                       'geography': 0,
                       'history': 0,
                       'society': 0,
                       'sport': 0 }

