income_data = [25, 15, 45, 75, 95, 40, 20, 15, 40, 30, 20, 25, 45, 65, 90]
type_data = ['L', 'L', 'L', 'H', 'H' ,'H', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'H', 'H']
FP = [[1, 2, 3], [13, 14], [4, 6], [7, 8 ,9], [], [5], [11, 12], [15], [10]]

# Sigma Gini Index
PA = []
for p in FP:
	pa = 0
	for i in p:
		my_income = income_data[i-1]	
		for other_income in income_data:
			pa = pa + abs(my_income - other_income)
	PA.append(pa)
print(PA)

# Calculating total income
Total_Income = []
for p in FP:
	total = 0
	for i in p:
		val = income_data[i-1]
		total += val
	Total_Income.append(total)
print(Total_Income)

# Sigma Index of dissimilarity

COUNT_H = 0
COUNT_L = 0
for type in type_data:
	if type == 'L':
		COUNT_L += 1
	elif type == 'H':
		COUNT_H += 1

PDA = []
for p in FP:
	pda = 0.0
	count_h = 0.
	count_l = 0.
	for i in p:
		if (type_data[i-1] == 'L'):
			count_l += 1
		elif (type_data[i-1] == 'H'):
			count_h += 1
	pda = 0.5*abs((count_h / COUNT_H) - (count_l / COUNT_L))
	PDA.append(round(pda,2))
print(PDA)
	
# Sigma IQSR
		
