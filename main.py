from matplotlib import pyplot as pyp
import matplotlib
import numpy
import csv

file = 'McDonaldsDataCapture.csv'

with open(file,'r') as csv_file:
    reader = csv.reader(csv_file)
    head=True
    data = []
    for row in reader:
        if head:
            headers = tuple(row)
            head = False
        packet = {}
        for i in range(len(headers)):
            packet[headers[i]] = row[i]
        data.append(packet)
    data = tuple(data)

tcp_rec = []
for packet in data:
    tcp_rec.append(packet['Protocol'])
tcp_rec = tuple(tcp_rec)

pyp.hist(tcp_rec)
pyp.show()