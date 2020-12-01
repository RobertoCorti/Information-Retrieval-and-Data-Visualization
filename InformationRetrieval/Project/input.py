
from user import User
from personalizedPagerank import PersonalizedPageRank
from IRsystem import IRsystem


name = input('\nName: ')
surname = input('Surname: ')

user = User(name=name, surname=surname)

print('\n\nHello '+name+' '+surname+'!\n')
print('Welcome to the topic Wikipedia search\n')

print('Before starting the search, please list your 5 main interests and rate from 1 to 5 these\n')

for i in range(0, 5):
    topic = input('Topic '+str(i+1)+': ')

    rate = int(input('Rate '+topic+': '))

    while rate < 1 or rate > 5:
        rate = int(input('Not valid rate!!!\nRate '+topic+': '))

    user.rates[topic] = rate
    print(' ')


p = PersonalizedPageRank(graphFile='wikipediaGraph_simple.json',
                         contentFile='wikipediaGraph_simple_contents.json')

system = IRsystem(user=user, pagerank=p)

print('\nLoading....\n')

system.compute_final_pagerank(alpha=0.2, epsilon=0.0001)

system.write_result()

print('Result written in result.html')