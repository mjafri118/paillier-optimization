import random
import torch

from hwcounter import Timer, count, count_end
from time import sleep
from math import sqrt
import phePN as phePN
import pheMP as pheMP
# import phe as pheTN

def generateTensors():
    tensors = []
    for i in range(1, 11):
        tensor_data = list([float(random.randint(0, 99999)) for x in range(i * 10)])
        tensor = torch.tensor(tensor_data)
        tensors.append(tensor)
    return tensors

# torch.save(generateTensors(), 'tensors.pt') # uncomment to generate tensors and save to disk. 
tensors = torch.load('tensors.pt')

class Counter: 
    def __init__(self):
        self.startCycle = 0
    def begin(self):
        self.startCycle = count()
    def reset(self):
        self.startCycle = 0
    def end(self):
        return count_end() - self.startCycle


class PaillierEncryption:
    def __init__(self, method):
        self.method = method

        public_key, private_key = phePN.generate_paillier_keypair()
        self.encryptPN, self.decryptPN = public_key.encrypt, private_key.decrypt

        public_key, private_key = pheMP.generate_paillier_keypair()
        self.encryptMP, self.decryptMP = public_key.encrypt, private_key.decrypt

        # public_key, private_key = pheTN.generate_paillier_keypair()
        # self.encryptTN, self.decryptTN = public_key.encrypt, private_key.decrypt
    
    # Input is a tensor, output is encrypted tensor/data
    def encrypt(self, tensor):
        if self.method == "package-native": 
            self.encryptedData = self.encryptPN(tensor)
        if self.method == "multi-processing": 
            self.decryptedData = self.encryptMP(tensor)
        if self.method == "torch-native": 
            self.decryptedData = self.encryptTN(tensor)
        
        return self.encryptedData
    
    # Input is encrypted tensor/data from encrypt() function. Output is 
    # expecting the exact same input tensor
    def decrypt(self, encryptedData):
        if self.method == "package-native": 
            self.decryptedData = self.decryptPN(encryptedData)
        if self.method == "multi-processing": 
            self.decryptedData = self.decryptMP(encryptedData)
        if self.method == "torch-native": 
            self.decryptedData = self.decryptTN(encryptedData)
        
        return self.decryptedData

## Main execution of code

METHODS = ['package-native', 'multi-processing', 'torch-native', 'abi-tbd']
METHOD = METHODS[0] # SELECT METHOD HERE. 
pheInstance = PaillierEncryption(METHOD)
counter = Counter()

encryptResults = []
decryptResults = []

# Clean way of storing the data. First column corresponds to index of the method type
# i.e. 0 -> 'package-native'
def logData(methodindex,tensorLength, encryptTime, decryptTime):
    with open('data.csv','a') as fd:
        fd.write(",".join([str(methodindex), str(tensorLength), str(encryptTime), str(decryptTime)]))
        fd.write("\n")  # Next line.
    print(f"Logged to CSV: {[methodindex, tensorLength, encryptTime, decryptTime]}")
    return

for tensor in tensors: 
    counter.reset()
    counter.begin()
    encryptedData = pheInstance.encrypt(tensor)
    encryptTime = counter.end()

    counter.reset()
    counter.begin()
    decryptedData = pheInstance.decrypt(encryptedData)
    decryptTime = counter.end()

    # print(tensor == decryptedData) Check to see if encryption/decryption is working

    logData(METHODS.index(METHOD), len(tensor), encryptTime, decryptTime)

