#!/usr/bin/env python3
import sys
import subprocess
import copy
if len(sys.argv) != 2:
    size = input('enter chessboard size:')
else:
    size = sys.argv[1]
    
try:
    n = int(size)
except ValueError:
    print("Invalid size. Please enter an integer.")
    sys.exit(1)


def cardinality(white_counter, counter_length, count):
    card_cnf = []
    bits = []
    n = int(count)
    while n>0:
        bits.append(n % 2)
        n //= 2
    while len(bits) < counter_length:
        bits.append(0)
    for i in range(counter_length):
        if bits[i] == 1:
            card_cnf.append([str(white_counter + i), '0'])
        else:
            card_cnf.append([str(-(white_counter + i)), '0'])
    return card_cnf            


cnf = subprocess.run(['python3', 'sat_create.py', str(n), ''], capture_output=True)
counters = (cnf.stderr.decode())
counters = counters.split(',')
white_counter = int(counters[0])
counter_length = int(counters[1])
cnf = cnf.stdout.decode()
cnf_list = cnf.splitlines()

for i in range(len(cnf_list)):
    cnf_list[i] = cnf_list[i].split()

for i in range(1,n*n):
    card_ = cardinality(white_counter - counter_length + 1, counter_length , i)
    cnf_new = [x for x in cnf_list]
    for x in card_:
        cnf_new.append(x)
    cnf_new[0][3] = str(int(cnf_new[0][3]) + len(card_))
    for j in range(len(cnf_new)):
        cnf_new[j] = ' '.join(cnf_new[j])
        
    cnf_new = '\n'.join(cnf_new).encode('utf-8')

    
    glucose_result = subprocess.run(['./glucose/parallel/glucose-syrup', '-model'], input=cnf_new, capture_output=True)
    satisfiable = int(glucose_result.returncode)
    
    if satisfiable == 20:
        break
    else:
        old_result = copy.deepcopy(glucose_result)

    
formated_sat = subprocess.run(['python3', 'format.py', size], input=old_result.stdout, capture_output=True)
if formated_sat.returncode == 1:
    print("No solution found.")
    sys.exit(0)
print(formated_sat.stdout.decode())