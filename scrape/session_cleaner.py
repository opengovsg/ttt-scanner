import json
from time import strftime
today = strftime("%Y-%m-%d")


with open('mrtScrape.json', 'r') as file:
    mrt_stations = json.load(file)

def loadFiles(start, end):
    x = []
    for i in xrange(start, end+1):
        with open('data/'+today+'/output%05d.json' % i, 'r') as file:
            x.append(json.load(file))
    return x

def cleanSessionRecords():
    stations = {}
    for i in mrt_stations: 
        station_dict = {}
        if (len(i['stops'])>0):
            station_ssids = loadFiles(i['stops'][0],i['stops'][1])
            ssids = set()
            for station in station_ssids: 
                for ssid in station:
                    if (len(ssid)==17):
                        station_dict[ssid]=i['stationName']
            stations[i['stationName']] = station_dict
    with open('output/'+str(today)+'.json', 'w') as file:
        json.dump(stations, file)

def removeDuplicates():
    with open('output/'+str(today)+'.json', 'r') as file:
        data =  json.load(file)
        seen = set()
        duplicates = set()
        for station in data:
            for ssid in data[station]:
                if ssid in seen:
                    duplicates.add(ssid)
                else:
                    seen.add(ssid)

        for station in data:
            print station
            for duplicate in duplicates:
                data[station].pop(duplicate, None)
            print len(data[station])
    return data


def exportForReader(data):
    for station in data:
        for key in data[station]:
            print "\"" + key.upper() + "\": \"" + data[station][key] + "\"," 


cleanSessionRecords()
exportForReader(removeDuplicates())
