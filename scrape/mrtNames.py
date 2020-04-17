# ns = ['Jurong East', 'Bukit Batok', 'Bukit Gombak', 'Choa Chua Kang', 'Yew Tee', 'Reserved', 'Kranji', 'Marsiling', 'Woodlands', 'Admiralty', 'Sembawang', 'Canberra', 'Yishun', 'Khatib', 'Yio Chu Kang', 'Ang Mo Kio', 'Bishan', 'Braddell', 'Toa Payoh', 'Novena', 'Newton', 'Orchard', 'Somerset', 'Dhoby Ghaut', 'City Hall', 'Raffles Place', 'Marina Bay', 'Marina Bay South Pier']
ns = []

for i in xrange(len(ns)):
  print '''    {
        "stationName": "NS%d - %s",
        "stops": [], 
    },''' % (i+1, ns[i])

# cc = ['Dhoby Ghaut', 'Bras Basah', 'Esplanade', 'Promenade', 'Nicoll Highway', 'Stadium', 'Mountbatten', 'Dakota', 'Paya Lebar', 'MacPherson', 'Tai Seng', 'Bartley', 'Serangoon', 'Lorong Chuan', 'Bishan', 'Marymount', 'Caldecott', 'Bukit Brown', 'Botanic Gardens', 'Farrer Road', 'Holland Village', 'Buona Vista', 'one-north', 'Kent Ridge', 'Haw Par Villa', 'Pasir Panjang', 'Labrador Park', 'Telok Blangah', 'HarbourFront', 'Keppel', 'Cantonment', 'Prince Edward']
# cc = []

for i in xrange(len(cc)):
  print '''    {
        "stationName": "CC%d - %s",
        "stops": [], 
    },''' % (i+1, cc[i])

# ce = ['Bayfront', 'Marina Bay']
ce = []

for i in xrange(len(ce)):
  print '''    {
        "stationName": "CE%d - %s",
        "stops": [], 
    },''' % (i+1, ce[i])

# ne = ['HarbourFront', 'Reserved', 'Outram Park', 'Chinatown', 'Clarke Quay', 'Dhoby Ghaut', 'Little India', 'Farrer Park', 'Boon Keng', 'Potong Pasir', 'Woodleigh', 'Serangoon', 'Kovan', 'Hougang', 'Buangkok', 'Sengkang', 'Punggol', 'Punggol Coast']
ne = []

for i in xrange(len(ne)):
  print '''    {
        "stationName": "NE%d - %s",
        "stops": [], 
    },''' % (i+1, ne[i])

# dt = ['Bukit Panjang', 'Cashew', 'Hillview', 'Reserved', 'Beauty World', 'King Albert Park', 'Sixth Avenue', 'Tan Kah Kee', 'Botanic Gardens', 'Stevens', 'Newton', 'Little India', 'Rochor', 'Bugis', 'Promenade', 'Bayfront', 'Downtown', 'Telok Ayer', 'Chinatown', 'Fort Canning', 'Bencoolen', 'Jalan Besar', 'Bendemeer', 'Geylang Bahru', 'Mattar', 'MacPherson', 'Ubi', 'Kaki Bukit', 'Bedok North', 'Bedok Reservoir', 'Tampines West', 'Tampines', 'Tampines East', 'Upper Changi', 'Expo', 'Xilin', 'Sungei Bedok']
dt = []

for i in xrange(len(dt)):
  print '''    {
        "stationName": "DT%d - %s",
        "stops": [], 
    },''' % (i+1, dt[i])

ew = []

for i in xrange(len(ew)):
  print '''    {
        "stationName": "EW%d - %s",
        "stops": [], 
    },''' % (i+1, ew[i])
