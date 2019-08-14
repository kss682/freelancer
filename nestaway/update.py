from collections import defaultdict
import sys
import csv

Shared_Details = []
Private_Details = []

city_name = sys.argv[1]

with open("{}_Shared Room.csv".format(city_name),'r') as file:
        reader = csv.reader(file)
        for row in reader:
            Shared_Details.append(row)
with open("{}_Private Room.csv".format(city_name),'r') as file:
        reader = csv.reader(file)
        for row in reader:
            Private_Details.append(row)

for sh in range(len(Shared_Details)):
    for pr in range(len(Private_Details)):
        if Shared_Details[sh][2] == Private_Details[pr][2]:
            print(Shared_Details[sh])
            index = pr
            del(Private_Details[index])
            break

with open("{}_Shared Room.csv".format(city_name),'w') as file:
        writer = csv.writer(file)
        writer.writerows(Shared_Details)

with open("{}_Private Room.csv".format(city_name),'w') as file:
        writer = csv.writer(file)
        writer.writerows(Private_Details)
