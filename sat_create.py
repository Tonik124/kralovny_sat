#!/usr/bin/env python3
#size = int(input('enter chessboard size:'))
import math
import sys
n = int(sys.argv[1])
pysat = bool(sys.argv[2])
size = n*n
clauses=[]
'''
variable 1 thru size*size coresponds to a white queen being on squares 1 thru size*size
variable size*size+1 thru 2*size*size+1 coresponds to a black queen being on squares size*size+1 thru 2*size*size+1
-5 means no white queen on square 5 (first row fifth column)

'''
for i in range(n):
    for j in range(n):
        for x in range(n - 1):
            clauses.append([-((i*n)+j+1),-(i*n + (j + 1 + x)% n + 1 + size)]) #no black queen in same row
            clauses.append([-((i*n)+j+1),-(((i + 1 + x)% n )*n + j + 1 + size)]) # no black queen in same column
            if (x < (n-j-1)):
                clauses.append([-((i*n)+j+1),-((i + 1 + x)*n + 1 + (j + 1 + x) + size)]) # no black queen on same diagonal
            if (x < j):
                clauses.append([-((i*n)+j+1),-((i + 1 + x)*n + 1 + (j - 1 - x) + size)])
            clauses.append([-((i*n)+j+1),-((i - 1 - x)*n + 1 + (j + 1 + x) + size)])
            clauses.append([-((i*n)+j+1),-((i - 1 - x)*n + 1 + (j - 1 - x) + size)])
        clauses.append([-((i*n)+j+1),-((i*n)+j+1 + size)])

clauses2 = []
for i in clauses:
    if (abs(i[1]) > size) and (abs(i[1]) < (2*size + 1)):
        clauses2.append(i)

counter_length = math.ceil(math.log2(size))

def binary_counter(i, j):
    old_counter = (2*size + (2*i-2)*counter_length + j)
    new_counter = (2*size + (2*i)*counter_length + j) 
    old_carry = 2*size + (2*i-1) * counter_length + j -1
    new_carry = 2*size + (2*i-1) * counter_length + j
    if j == 1:
        old_carry = i
        if i>size:
            old_carry -=1
        
    clauses2.append([-(old_counter), -old_carry, new_carry ])
    clauses2.append([-(old_counter), -old_carry, -new_counter])
    clauses2.append([ (old_counter), -old_carry,  new_counter])
    clauses2.append([ (old_counter),  old_carry, -new_counter])
    clauses2.append([-(old_counter),  old_carry,  new_counter])
    
    clauses2.append([ (old_counter), -old_carry, -new_carry])
    clauses2.append([ (old_counter),  old_carry, -new_carry])
    clauses2.append([-(old_counter),  old_carry, -new_carry])
    
    return(new_counter)





for i in range(1,size + 1):    #count white
    for j in range(1, counter_length + 1):
        white_counter = binary_counter(i,j)

for i in range(size + 2, 2*size + 2):    #count black
    for j in range(1, counter_length + 1):
        black_counter = binary_counter(i,j)

for i in range(0,counter_length):   #same number of black and white
    clauses2.append([-(white_counter - i), (black_counter - i)])
    clauses2.append([ (white_counter - i),-(black_counter - i)])

for i in range(counter_length):
    clauses2.append([-(2*size + 1 + i)])

for i in range(counter_length):
    clauses2.append([-((white_counter + 1 + counter_length)+i)])
    

#print CNF

print(f'p cnf {black_counter} {len(clauses2)}')
for i in clauses2:
    for j in i:
        print(j,end=' ')
    print('0')


if pysat:
    sys.stderr.write(str(black_counter))
else:
    sys.stderr.write(f'{white_counter},{counter_length}')
