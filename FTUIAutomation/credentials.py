import sys
import json

# total arguments
n = len(sys.argv)
creds = {'orgNAme': None, 'username': None,
         'mailid': None, 'clustername': None, 'password': None}
argumentList = sys.argv[1:]

for i, k in enumerate(creds):
    creds[k] = argumentList[i]

file = json.dumps(creds)
my_data_file = open('/var/tmp/credentials.json', 'a+')
with open('/var/tmp/credentials.json', 'a+') as json_file:
    json.dump(file, json_file)

my_data_file.close()
