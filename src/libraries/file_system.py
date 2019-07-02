'''
This folder is to work with system files
'''

from libraries import *

reader = csv.reader(open('output.csv', 'rb'))
reader1 = csv.reader(open('output1.csv', 'rb'))
writer = csv.writer(open('appended_output.csv', 'wb'))
for row in reader:
    row1 = reader1.next()
    writer.writerow(row + row1)