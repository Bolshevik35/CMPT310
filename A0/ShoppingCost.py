"""
To run this script:
	python shoppingCost.py

In order to pass the autograder your createPricesDict function should
return a dictionary like this:
{'Bananas': 1.56,
 'French fried potatoes': 2.61,
 ...
}
If you run the above script, a correct calculateShoppingCost function should return:

The final cost for our shopping cart is 35.58
"""

import csv

def calculateShoppingCost(productPrices, shoppingCart):
	finalCost = 0
	"*** Add your code in here ***"
	for x in shoppingCart:
		if x in productPrices:
			finalCost = finalCost + float(productPrices.get(x)) * float(shoppingCart.get(x))
	return finalCost


def createPricesDict(filename):
	productPrice = {}
	f = open(filename, "r")
	for x in f:
		check = x.strip("\r\n")
		item , price = check.split(",")
		productPrice[item] = price
	f.close()
	"*** Add your code in here ***"
	return productPrice


if __name__ == '__main__':
	prices = createPricesDict("Grocery.csv")
	print(prices)
	myCart = {"Bacon": 2,
		      "Homogenized milk": 1,
		      "Eggs": 5}
	print("The final cost for our shopping cart is {}".format(calculateShoppingCost(prices, myCart)))
