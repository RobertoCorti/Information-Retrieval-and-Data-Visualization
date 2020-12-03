
from user import User
from personalizedPagerank import PersonalizedPageRank
from IRsystem import IRsystem

WIKIPEDIA_SEARCH_ASCII = """

'|| '||'  '|'  ||  '||       ||                        '||   ||           .|'''.|                                  '||      
 '|. '|.  .'  ...   ||  ..  ...  ... ...    ....     .. ||  ...   ....    ||..  '    ....   ....   ... ..    ....   || ..   
  ||  ||  |    ||   || .'    ||   ||'  || .|...||  .'  '||   ||  '' .||    ''|||.  .|...|| '' .||   ||' '' .|   ''  ||' ||  
   ||| |||     ||   ||'|.    ||   ||    | ||       |.   ||   ||  .|' ||  .     '|| ||      .|' ||   ||     ||       ||  ||  
    |   |     .||. .||. ||. .||.  ||...'   '|...'  '|..'||. .||. '|..'|' |'....|'   '|...' '|..'|' .||.     '|...' .||. ||. 
                                  ||                                                                                        

"""

WIKIPEDIA_SEARCH_INTRO = """
This demo performs a Personalized PageRank into the simple Wikipedia dump of April 2007 (https://dumps.wikimedia.org/other/static_html_dumps/April_2007/simple) matching some user-defined topic interests. The final result will be a static html page that contains the rank of the Wikipedia pages according to the topics selected by the user.
"""

name = input('\nName: ')
surname = input('Surname: ')

user = User(name=name, surname=surname)

print(WIKIPEDIA_SEARCH_ASCII)

#print('Hello '+name+' '+surname+'!\n')
print('Welcome to the WikipediaSearch!')
print(WIKIPEDIA_SEARCH_INTRO)
print('Please '+name+ ' '+surname+', list your 5 main interests and rate each of them from 1 to 5\n')

for i in range(0, 5):
    topic = input('Topic '+str(i+1)+': ')

    rate = int(input('Rate '+topic+ ' (lower=1, higher=5): '))

    while rate < 0 or rate > 5:
        rate = int(input('Not valid rate!!!\nRate '+topic+' (lower=1, higher=5): '))

    user.getTopicRate(topic, rate)
    print(' ')


p = PersonalizedPageRank(graphFile='data/wikipediaGraph_simple.json',
                         contentFile='data/wikipediaGraph_simple_contents.json')

system = IRsystem(user=user, pagerank=p)

print('\nLoading....\n')

system.compute_final_pagerank(alpha=0.2, epsilon=0.001)

system.write_result()

print('Result written in result/result_'+user.name+user.surname+'.html')