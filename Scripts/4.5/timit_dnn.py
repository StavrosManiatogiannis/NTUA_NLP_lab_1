# Train a torch DNN for Kaldi DNN-HMM model

import math
import sys

import numpy as np
import torch
import torch.utils.data
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from dnn.torch_dataset import TorchSpeechDataset
from dnn.torch_dnn import TorchDNN

import copy



DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# DEVICE = torch.device('cpu')
# CONFIGURATION #

NUM_LAYERS = 3
HIDDEN_DIM = 1024
USE_BATCH_NORM = True
DROPOUT_P = .2
EPOCHS = 50
PATIENCE = 3

if len(sys.argv) < 2:
    print("USAGE: python timit_dnn.py <PATH/TO/CHECKPOINT_TO_SAVE.pt>")

BEST_CHECKPOINT = sys.argv[1]


# FIXME: You may need to change these paths

kaldi_root = "~/kaldi/egs/usc"
TRAIN_ALIGNMENT_DIR = f"{kaldi_root}/exp/tri_ali/tri_ali_train"
DEV_ALIGNMENT_DIR = f"{kaldi_root}/exp/tri_ali/tri_ali_dev"
TEST_ALIGNMENT_DIR = f"{kaldi_root}/exp/tri_ali/tri_ali_test"


def train(model, criterion, optimizer, train_loader, dev_loader, epochs=50, patience=3):
    """Train model using Early Stopping and save the checkpoint for
    the best validation loss
    """

    best_model_params = copy.deepcopy(model.state_dict())
    min_val_loss = float("inf")

    train_loss_hist = []
    val_loss_hist = []
    patience_count = 0


    for epoch in range(epochs):
        model.train()
        running_loss = 0.0

        for inputs, targets in train_loader:
            inputs = inputs.to(DEVICE)
            targets = targets.to(DEVICE)

            optimizer.zero_grad()

            pred = model(inputs)
            loss = criterion(pred, targets)

            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)

        epoch_train_loss = running_loss / len(train_loader.dataset)
        train_loss_hist.append(epoch_train_loss) 

        model.eval()
        running_val_loss = 0.0

        with torch.no_grad():
            for inputs, targets in dev_loader:
                inputs = inputs.to(DEVICE)
                targets = targets.to(DEVICE)

                pred = model(inputs)
                loss = criterion(pred, targets)

                running_val_loss += loss.item() * inputs.size(0)

        epoch_val_loss = running_val_loss / len(dev_loader.dataset)
        val_loss_hist.append(epoch_val_loss)


        if epoch_val_loss < min_val_loss:
            min_val_loss = epoch_val_loss
            best_model_params = copy.deepcopy(model.state_dict())
            patience_count = 0
            torch.save(best_model_params, "best_model.pt")
        else:
            patience_count += 1
        if patience_count >= patience:
            print(epoch)
            break
        
        if epoch % 10 == 0:
            print(f"EPOCH: {epoch} | epoch_val_loss: {epoch_val_loss} | epoch_train_loss: {epoch_train_loss}")


    model.load_state_dict(best_model_params)

    return model, train_loss_hist, val_loss_hist



trainset = TorchSpeechDataset('./', TRAIN_ALIGNMENT_DIR, 'train')
validset = TorchSpeechDataset('./', DEV_ALIGNMENT_DIR, 'dev')
testset = TorchSpeechDataset('./', TEST_ALIGNMENT_DIR, 'test')

scaler = StandardScaler()
scaler.fit(trainset.feats)

trainset.feats = scaler.transform(trainset.feats)
validset.feats = scaler.transform(validset.feats)
testset.feats = scaler.transform(testset.feats)

feature_dim = trainset.feats.shape[1]
n_classes = int(trainset.labels.max() - trainset.labels.min() + 1)


dnn = TorchDNN(
    feature_dim,
    n_classes,
    num_layers=NUM_LAYERS,
    batch_norm=USE_BATCH_NORM,
    hidden_dim=HIDDEN_DIM,
    dropout_p=DROPOUT_P
)
dnn.to(DEVICE)

train_loader = torch.utils.data.DataLoader(trainset, batch_size=128, shuffle=True)
dev_loader = torch.utils.data.DataLoader(validset, batch_size=128, shuffle=True)


optimizer = torch.optim.Adam(params= dnn.parameters(), lr= 0.001)
criterion = torch.nn.CrossEntropyLoss()

model, train_hist, val_hist = train(dnn, criterion, optimizer, train_loader, dev_loader, epochs=EPOCHS, patience=PATIENCE)
for i in range(5):
    print(f"{i}) f{val_hist[-5 + i]}")

torch.save(model, BEST_CHECKPOINT)
