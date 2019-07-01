import os

domino = True
if domino:
    data_path = os.path.join('..', '..', 'data', 'plans')
    #code_path = os.path.join('/Users/kylieleblancKylie/domino/dofis/code_one', 'data_from_plans')

if not domino:
    data_path = os.path.join('/Users/kylieleblancKylie/domino/dofis/data', 'plans')
    code_path = os.path.join('/Users/kylieleblancKylie/domino/dofis/code_one', 'data_from_plans')