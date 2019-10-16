"""
Using the model that has been through transfer learning, predict molecules at a particular temperature
"""

from models import data_processing, smiles_generator
import sys
import time
from rdkit import Chem
import os

# Number of smiles to generate
n_smiles = 100

# Parameter for the temperature in the Softmax
temperature = 0.75

# Loading the model and the data processing objects
dp = data_processing.Molecules_processing()
estimator = smiles_generator.Smiles_generator(epochs=1, batch_size=100, tensorboard=False, hidden_neurons_1=256,
                                              hidden_neurons_2=256, dropout_1=0.3, dropout_2=0.5,
                                              learning_rate=0.001)

dp.load("../outputs/transfer_learning_001/tl_dp.pickle")
estimator.load("../outputs/transfer_learning_001/tl_model.h5")

# Predicting SMILES 
start_time = time.time()
X_pred_hot = dp.get_empty(n_smiles)
pred_hot = estimator.predict(X_pred_hot, temperature=temperature)
pred = dp.onehot_decode(pred_hot)
end_time = time.time()

print("%i smiles have been generated in %.2f s" % (n_smiles, end_time-start_time))

# Filtering the invalid and duplicated SMILES
pred = set(pred)

valid_smiles = []
for smile in pred:
    mol = Chem.MolFromSmiles(smile)
    if not isinstance(mol, type(None)):
        valid_smiles.append(smile)

print("There are %i valid and unique SMILES" % len(valid_smiles))

# Writing the smiles to file
output_path = "../outputs/predict_tl_001/"
if not os.path.exists(output_path):
    os.makedirs(output_path)
    
filename = "predict_tl_001.smi"
f = open(output_path+filename, 'w')

for i in range(len(valid_smiles)):
    f.write('%s' % (valid_smiles[i]))
    f.write("\n")

f.close()
