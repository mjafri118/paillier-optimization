from time import sleep, time
import random
import torch
from math import sqrt
import phePN as phePN
import mixcrypt as pheTN

def generateTensors():
    tensors = []
    for i in range(1, 11):
        tensor_data = list([float(random.randint(0, 99999)) for x in range(i * 10)])
        tensor = torch.tensor(tensor_data)
        tensors.append(tensor)
    return tensors

print(time())
torch.save(generateTensors(), 'tensors.pt') # uncomment to generate tensors and save to disk. 
tensors = torch.load('tensors.pt')
print(tensors)

class Counter: 
    def __init__(self):
        self.startCycle = 0
    def begin(self):
        self.startCycle = time()
    def reset(self):
        self.startCycle = 0
    def end(self):
        return time() - self.startCycle


class PaillierEncryption:
    def __init__(self, method):
        self.method = method

        if self.method == "native-paillier":
            public_key, private_key = phePN.generate_paillier_keypair()
            self.encryptPN, self.decryptPN = public_key.encrypt, private_key.decrypt
    
    # Input is a tensor, output is encrypted tensor/data
    def encrypt(self, tensor):
        if self.method == "native-paillier": 
            self.encryptedData = self.encryptPN(tensor)
        if self.method == "mixed-encryption": 
            self.encryptedData = pheTN.encrypt(tensor) 
        return self.encryptedData
    
    # Input is encrypted tensor/data from encrypt() function. Output is 
    # expecting the exact same input tensor
    def decrypt(self, encryptedData):
        if self.method == "native-paillier": 
            self.decryptedData = self.decryptPN(encryptedData)
        if self.method == "mixed-encryption": 
            self.decryptedData = pheTN.decrypt(encryptedData[0], encryptedData[1], encryptedData[2]) 
        return self.decryptedData

## Main execution of code

METHODS = ['native-paillier', 'mixed-encryption']
# METHOD = METHODS[2] # SELECT METHOD HERE if not using for-loop below.

# Clean way of storing the data. First column corresponds to index of the method type
# i.e. 0 -> 'native-paillier'
def logData(methodindex, tensorLength, encryptTime, decryptTime):
    with open('data.csv','a') as fd:
        fd.write(",".join([str(methodindex), str(tensorLength), str(encryptTime), str(decryptTime)]))
        fd.write("\n")  # Next line.
    print(f"Logged to CSV: {[methodindex, tensorLength, encryptTime, decryptTime]}")
    return

for METHOD in METHODS: 
    pheInstance = PaillierEncryption(METHOD)
    counter = Counter()

    encryptResults = []
    decryptResults = []

    for tensor in tensors: 
        counter.reset()
        counter.begin()
        encryptedData = pheInstance.encrypt(tensor)
        encryptTime = counter.end()

        counter.reset()
        counter.begin()
        decryptedData = pheInstance.decrypt(encryptedData)
        decryptTime = counter.end()

        print(tensor == torch.abs(decryptedData)) # Check to see if encryption/decryption is working

        logData(METHODS.index(METHOD), len(tensor), encryptTime, decryptTime)

