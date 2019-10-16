"""
This example shows how to reload a previously saved model and carrying on fitting. 
"""

from molbot import smiles_generator, data_processing
import os
import numpy as np
import random
import time

# Reading the data
in_d = open("../data/metap2.smi", 'r')

# Parsing the data
molecules = []

for line in in_d:
    if "smiles" in line.lower():
        continue
    line = line.rstrip()
    split_line = line.split("\t")[0]
    molecules.append(split_line)

random.shuffle(molecules)
print("The total number of molecules is: %i \n" % (len(molecules)))

# One-hot encode the molecules
dp = data_processing.Molecules_processing()
dp.load("../outputs/training_chembl_001/post_chembl_dp.pickle")
X = dp.onehot_encode(molecules)
# y is just the same as X just shifted by one
idx_A = dp.char_to_idx['A']
y = np.zeros(X.shape)
idx_A = dp.char_to_idx['A']
y[:, :-1, :] = X[:, 1:, :]
y[:, -1, idx_A] = 1

# Reloading the model
estimator = smiles_generator.Smiles_generator(epochs=10, batch_size=100, tensorboard=False, hidden_neurons_1=256,
                                              hidden_neurons_2=256, dropout_1=0.3, dropout_2=0.5, learning_rate=0.001,
                                              validation=0.005)

estimator.load("../outputs/training_chembl_001/post_chembl_model.h5")

# Transfer learning on smaller dataset
start_time = time.time()
estimator.fit(X, y)
end_time = time.time()

print("Transfer learning took %.2f s" % (end_time-start_time))

# Saving the new model
output_path = "../outputs/transfer_learning_001/"
if not os.path.exists(output_path):
    os.makedirs(output_path)

dp.save(output_path+"tl_dp.pickle")
estimator.save(output_path+"tl_model.h5")

