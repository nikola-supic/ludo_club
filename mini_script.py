x, y = 244, 16

with open('tmp.txt', 'w') as file:
	for i in range(3):
		for j in range(15):
			file.write(f'({x}, {y})\n')
			y += 38
		x += 38
		y = 16

