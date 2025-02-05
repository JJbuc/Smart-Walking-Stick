import requests

lat = "19.107344"
long = "72.836977"
apiID = "AIzaSyAFyUTH4oaSlpjXcKHXEBqdJu1psvoKjcE"
types = "restaurants"

URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&sensor=true&rankby=distance&key={apiID}&types={types}&opennow=true".format(lat=lat,long=long,apiID=apiID,types=types)

print(URL)
r = requests.get(url = URL).json()
results = r['results']
resp = []
for i in results:
    if 'name' in i.keys() and 'vicinity' in i.keys() and 'rating' in i.keys():
        temp = {}
        temp['name'] = i['name']
        temp['address'] = i['vicinity']
        temp['rating'] = i['rating']
        resp.append(temp)


import pprint
pp = pprint.PrettyPrinter(depth=4)
pp.pprint(resp)



'''
Sample Output

[{'address': 'opp. Prime Mall, Shop No 6, Ahmed Mension, opp. Prime Mall, Irla '
             'Road, Vile Parle West, Mumbai',
  'name': 'Ovenstory Vile Parle',
  'rating': 3},
 {'address': 'opp. Diamond Chemist, Shop no 1,MCGM parking lane, opp. Diamond '
             'Chemist, Irla Road, Vile Parle West, Mumbai',
  'name': 'Priya Fast Food',
  'rating': 4.3},
 {'address': '4R5P+25P, Suvarna Nagar, Juhu, Mumbai',
  'name': 'ISKCON Canteen',
  'rating': 4.1},
 {'address': 'Shop no. 1, New Hazrabai House, near Cooper hospital, 2, Irla '
             'Road, Vile Parle West, Mumbai',
  'name': 'Pappilon Fast Food Corner Irla',
  'rating': 3.9},
 {'address': 'Besides Papillon, Shop no 4/5 Harzabai House, Irla Road, Vile '
             'Parle West, Mumbai',
  'name': 'Udupi 2 Mumbai',
  'rating': 4.1},
 {'address': 'behind ICICI Direct Bank, 13, Shri Dwarkesh Niketan Building, '
             'Plot No 13, 3rd Floor, behind ICICI Direct Bank, North South '
             'Road Number 1, Azadanagar Society, JVPD Scheme, Vile Parle West, '
             'Mumbai',
  'name': 'Juice Lounge Main Office',
  'rating': 4},
 {'address': 'No.3, Gulmohar Road, Beside Cooper Hospital, JVPD Scheme, Vile '
             'Parle West, Mumbai',
  'name': 'Amar Juice Centre',
  'rating': 4.2},
 {'address': 'Shop No-24, Arif Mansion, Irla Lane, Navpada, Irla, Vile Parle '
             'West, Mumbai',
  'name': 'Sai Sagar Fast Food',
  'rating': 4.2},
 {'address': 'Juhu JVPD NS Road no 1, Ram Gadkari Marg, Mumbai',
  'name': 'Bombay Spices - The Flavours of India',
  'rating': 5},
 {'address': '4R5Q+W65, Tata Colony, Vile Parle West, Mumbai',
  'name': 'The happy chef',
  'rating': 4.2},
 {'address': 'De Menthe Eatery, opp. Irla Nursing Home, SV Road, Mumbai',
  'name': 'De Menthe Eatery',
  'rating': 5},
 {'address': 'opposite Prime Mall, Arif Mansion, opposite Prime Mall, Market, '
             'Irla, Vile Parle West, Mumbai',
  'name': 'Asiad',
  'rating': 4},
 {'address': 'Shanti Niketan, Shop Number 1 Opposite Sameer Ceramics, Vile '
             'Parle West, Mumbai',
  'name': 'The Belgian Waffle Co.',
  'rating': 4.3},
 {'address': 'Shop No 4A, Apurva Vaibhav CHS, SV Road, Irla, Vile Parle West, '
             'Mumbai',
  'name': 'Nothing But Chicken , NBC Irla',
  'rating': 4.6},
 {'address': 'near Sony Mony Showroom, SV Road, Indira Nagar, Vile Parle West, '
             'Mumbai',
  'name': 'Anil Sandwich',
  'rating': 4.4}]
'''
