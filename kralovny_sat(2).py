#!/usr/bin/env python3
import sys
import subprocess
from pysat import card
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


def kralovny(k,highest_var):
    cardinality = card.CardEnc.equals(range(1,n*n+1), bound=k, top_id=highest_var)
    card_cnf = cardinality.clauses
    for i in range(len(card_cnf)):
        card_cnf[i].append(0)
    for i in range(len(card_cnf)):
        for j in range(len(card_cnf[i])):
            card_cnf[i][j] = str(card_cnf[i][j])
    return card_cnf


cnf = subprocess.run(['python3', 'sat_create.py', str(n), 'True'], capture_output=True)
highest_var = int(cnf.stderr.decode())
cnf = cnf.stdout.decode()
cnf_list = cnf.splitlines()

for i in range(len(cnf_list)):
    cnf_list[i] = cnf_list[i].split()

for i in range(1,n*n):
    card_ = kralovny(i,highest_var + 1)
    new_highest = 0
    
    for x in card_:
        for y in x:
            new_highest = max(new_highest,int(y))
   
    cnf_new = [x for x in cnf_list]
    for x in card_:
        cnf_new.append(x)
    cnf_new[0][2] = str(new_highest)
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