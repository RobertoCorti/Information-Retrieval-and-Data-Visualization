
from user import User
from personalizedPagerank import PersonalizedPageRank
from IRsystem import IRsystem


print('\n')

name = input('Name: ')
surname = input('Surname: ')

user = User(name=name, surname=surname)

print('\n\nHello '+name+' '+surname+'!!\n')
print('Welcome to the topic Wikipedia search!\n')

print('Before starting the search, please rate from 0 to 5 these following arguments\n')


for topic in user.rates.keys():

    rate = int(input(topic+': '))

    while rate < 0 or rate > 5:
        rate = int(input('Not valid rate!!!\n'+topic+': '))

    user.rates[topic] = rate

p = PersonalizedPageRank(graphFile='wikipediaGraph_simple.json',
                         contentFile='wikipediaGraph_simple_contents.json')

system = IRsystem(user=user, pagerank=p)

print('\nLoading....\n')

system.compute_final_pagerank(alpha=0.3, epsilon=0.001)

system.write_result()