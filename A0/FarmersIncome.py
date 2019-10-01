"""
To run this script:
	python FarmersIncome.py

In order to pass the autograder your getMonthlyIncome function should return the income for each farmer. Please use numpy for matrix multiplication.
If you run the above script, a correct getMonthlyIncome function should return:

Monthly income of each farmer is [259000 286000 205000]
"""

import numpy as np

table = np.array([[600, 200, 400, 300], [100, 700, 300, 200], [300, 100, 300, 500]], dtype=np.float64)


def getMonthlyIncome(value):
	result = []  
	for i in range(len(table)) :
		income = 0
		for j in range(len(value)) :
			income = income + table[i][j] * value[j]
		result.append(income)
	return result	
	"*** Add your code in here ***"


if __name__ == '__main__':
	totalValue = np.array([120, 250, 230, 150])
	print("Monthly income of each farmer is {}".format(getMonthlyIncome(totalValue)))
