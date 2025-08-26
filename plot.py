from matplotlib import pyplot as plt

x_values = range(5001)
squares = [x**2 for x in x_values]

plt.style.use('seaborn')
fig, ax = plt.subplots()
ax.plot(x_values, squares, linewidth=3) 

plt.title("Square Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Square of Value", fontsize=14)

plt.tick_params(axis='both', which='major', labelsize=14)

plt.axis([0, 5100, 0, 5100**2])

plt.show()
