from subprocess import check_output
from datetime import datetime
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time import sleep
from time import strftime
from os import listdir, path, makedirs

today = strftime("%Y-%m-%d")

cred = credentials.Certificate("traintraintrain-bb07a.json")
firebase_admin.initialize_app(cred, {
  'databaseURL': 'https://traintraintrain-bb07a.firebaseio.com/'
})

filenames = []

# mkdir data/
if not path.exists('data/'):
  print "Making data dir"
  makedirs('data/')

# mkdir data/[date-today]
directory = 'data/' + str(today)
if not path.exists(directory):
  print "Making data/" + str(today) + " dir"
  makedirs(directory)

for f in listdir(directory):
  filenames.append(int(f[6:11]))

count =  max(filenames)+1 if (len(filenames) > 0) else 1

sessionId = ''
while sessionId == '':
  sessionId = raw_input("Enter the sessionId\n")

print "Using sessionId =", sessionId

ref = db.reference('raw-data/' + sessionId)

while True:
  try:
    print "Started scanning...",
    airportOutput = check_output(['airport', '-s'])
    print "complete!"

    result = dict()
    result2 = []
    time = datetime.now()
    result['time'] = str(time)
    result2.append(str(time))
    print ('Timestamp: ' + str(time))

    for line in airportOutput.split('\n'):
      if line != '':
        line = line.split()
        address = line[1]
        result[address] = line
        result2.append(address)

    with open('data/' + str(today) + '/output%05d.json' % count, 'w') as file:
      print ("Saving to data/" + str(today) + "/output%05d.json" % count)
      json.dump(result2, file)
      count += 1

    # print "Pushing to firebase...",
    # ref.push({
    #   'local_time': str(time),
    #   'server_time': {'.sv': 'timestamp'},
    #   'data': result
    # })
    print "complete!"
  except Exception as error:
    print "Something crashed"
    print error
  finally:
    sleep(5)
