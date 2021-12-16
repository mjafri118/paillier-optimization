import matplotlib.pyplot as plt 
import numpy as np

METHODS = ['native-paillier', 'mixed-encryption']

data = np.loadtxt('data.csv', delimiter=",")

for METHOD in METHODS:
    result = []
    for row in data: 
        if row[0] == METHODS.index(METHOD):
            result.append(row)

    # No plotting if method doesn't have any recorded data            
    if len(result) < 1:
        continue
    result = np.array(result).transpose()

    colors = ['b', 'g', 'r']

    plt.plot((result[1]), result[2], colors[METHODS.index(METHOD)] + "-.", label="Encryption: " + METHOD, )
    plt.plot((result[1]), result[3], colors[METHODS.index(METHOD)] + "-", label="Decryption: " + METHOD)

plt.xlabel("Size of tensor")
plt.ylabel("Cycles")
plt.legend()
plt.show()