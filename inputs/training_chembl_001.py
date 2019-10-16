
"""
This example shows how to train an RNN on a set of smiles and how to predict new smiles with the trained model.
"""

from molbot import smiles_generator, data_processing
import os
import random
import numpy as np
import time

# Reading the data
current_dir = os.path.dirname(os.path.realpath(__file__))
in_d = open(current_dir + "/../data/chembl.smi", 'r')

# Parsing the data
molecules = []

for line in in_d:
    if "REOSHits" in line:
        continue
    line = line.rstrip().split("\t")[0]
    molecules.append(line)
    if len(molecules) >= 500000:
        break

print("The total number of molecules is: %i \n" % (len(molecules)))

# One-hot encode the molecules
start = time.time()
dp = data_processing.Molecules_processing()
X = dp.onehot_encode(molecules)
# y is just the same as X just shifted by one with the A character at the end
idx_A = dp.char_to_idx['A']
y = np.zeros(X.shape)
y[:, :-1, :] = X[:, 1:, :]
y[:, -1, idx_A] = 1
end = time.time()
print("Data processing took %2.f s" % (end-start))

# Creating the model
start = time.time()
estimator = smiles_generator.Smiles_generator(epochs=20, batch_size=100, tensorboard=False, hidden_neurons_1=256,
                                              hidden_neurons_2=256, dropout_1=0.3, dropout_2=0.5, learning_rate=0.001,
                                              validation=0.005)

# Training the model on the one-hot encoded molecules
estimator.fit(X, y)
end = time.time()
print("Training took %2.f s" % (end-start))

# Predicting 10 new molecules from the fitted model at a temperature of 0.75
X_pred_hot = dp.get_empty(10)
pred_hot = estimator.predict(X_pred_hot, temperature=0.75)
pred = dp.onehot_decode(pred_hot)

print(pred)

# Saving the estimator for later re-use
if not os.path.exists("../outputs/training_chembl_001/"):
    os.makedirs("../outputs/training_chembl_001/")

estimator.save("../outputs/training_chembl_001/post_chembl_model.h5")
dp.save("../outputs/training_chembl_001/post_chembl_dp.pickle")

