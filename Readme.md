# Example training of RNN

In the directory `Inputs/` you can find different scripts:

1. `training_chembl_001.py`: Script that trains the model on a large subset of the ChEMBL data set (can be found in the folder `data/`). The output goes in the folder `outputs/transfer_chembl_001`.
2. `predict_chembl_001.py`: This uses the model trained by script `training_chembl_001.py` to generate molecules. It filters any duplicate and invalid smiles and saves the remaining ones in a file in `outputs/predict_chembl_001/predict_chembl_001.smi`.
3.  `transfer_learning_001.py`: This performs transfer learning on the model trained with `training_chembl_001.py`. The transfer learning data set is `data/metap2.smi`. The model obtained is saved in `outputs/transfer_learning_001/tl_model.h5`.
4. `predict_tl_001.py`: This uses the model trained with `transfer_learning_001.py` and uses it to generate SMILES. It filters any duplicate and invalid smiles and saves the remaining ones in a file in `outputs/predict_tl_001/predict_tl_001.smi`. 

In each output folder there is a `*.out` file which shows the standard output for each script that runs. This gives an idea of the runnning time of each script.
