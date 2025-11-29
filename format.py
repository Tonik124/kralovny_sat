#!/usr/bin/env python3
import sys
import time
a = ''
c=[]
size = int(sys.argv[1])
for line in sys.stdin:
    c.append(line.strip())

a = c[-1]

a = a.split()
a.pop(0)
if len(a) == 1 and a[0] == 'UNSATIFIABLE':
    exit(1)


for i in range(0,size):
    for j in range(0,size):
        print(a[size*i + j], end=' ')
    print('\n',end='')

print()

for i in range(0,size):
    for j in range(0,size):
        print(a[size*i + j + size*size], end=' ')
    print('\n',end='')

print()

queens = ['.' for _ in range(size*size)]

for i in a:
    if abs(int(i))<=size*size and int(i)>0:
        queens[abs(int(i))-1] = 'W'
    if abs(int(i))>size*size and abs(int(i))<=2*size*size and int(i)>0:
        queens[abs(int(i)) - size*size-1] = 'B'

for i in range(len(queens)):
    if i%size == size-1:
        print(queens[i])
    else:
        print(queens[i], end=' ')
