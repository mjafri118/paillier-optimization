import matplotlib.pyplot as plt 
import numpy as np

METHODS = ['package-native', 'multi-processing', 'torch-native', 'abi-tbd']

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
    plt.plot((result[1]), result[2], label="Encryption: " + METHOD)
    plt.plot((result[1]), result[3], label="Decryption: " + METHOD)

# plt.plot((data[1]), data[2], label="Encrypted")
plt.xlabel("Size of tensor")
plt.ylabel("Cycles")
plt.legend()
plt.show()