# Paillier Optimization
We evaluate different methods of encrypting and decrypting data using partially homomorphic encryption, namely the Paillier method. 

## What this code does
The heavywork in this code is twofold: benchmarking (`test.py`) and visualizing (`visualize.py`) two different implementions of Paillier, both in an attempt to speed up encryption/decryption time given fixed computational resources.

## Approaches
## Native implementation
We extend Python's native pailler `phe` library to support encryption of PyTorch tensors. We achieve this by accepting the Tensor data structure as a valid type, then iterating over any and all dimensions of the tensor, encrypting/decrypting them one by one. 

## Mixed Encryption
See mixcrypt documentation. 

## Benchmarking/Testing, `test.py`
Given fixed resources (CPU, GPU, and availability of both), we first generate a set of sample tensors of increasing dimensions, then iterate over each encryption implmenetation method. Within each method, we time the encryption and decryption separately and pickle that data into an annotated CSV file. 

## Visualizing
We simply visualize the above files using MatPlotLib's PyPlot, noting factors of difference between any given implementation method's encryption and decryption performance. 
