import math
import os
import sys

import kaldi_io
import numpy as np
import torch
import torch.nn as nn
import torch.utils.data
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from dnn.torch_dataset import TorchSpeechDataset
from dnn.torch_dnn import TorchDNN

if len(sys.argv) < 3:
    print("USAGE: python extract_posteriors.py <MY_TORCHDNN_CHECKPOINT> <OUTPUT_DIR>")

CHECKPOINT_TO_LOAD = sys.argv[1]
OUT_DIR = sys.argv[2]

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)
OUTPUT_ARK_FILE = os.path.join(OUT_DIR, "posteriors.ark")

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

kaldi_root = "~/kaldi/egs/usc"
TRAIN_ALIGNMENT_DIR = f"{kaldi_root}/exp/tri_ali/tri_ali_train"
TEST_ALIGNMENT_DIR = f"{kaldi_root}/exp/tri_ali/tri_ali_test"


def extract_logits(model, test_loader):
    model.eval()
    all_logits = []

    with torch.no_grad():
        for inputs, _ in tqdm(test_loader, desc="Extracting logits"):
            inputs = inputs.to(DEVICE)
            logits = model(inputs)
            all_logits.append(logits)

    return torch.cat(all_logits, dim=0)


trainset = TorchSpeechDataset('./', TRAIN_ALIGNMENT_DIR, 'train')
testset = TorchSpeechDataset('./', TEST_ALIGNMENT_DIR, 'test')

scaler = StandardScaler()
scaler.fit(trainset.feats)
testset.feats = scaler.transform(testset.feats)

test_loader = torch.utils.data.DataLoader(testset, batch_size=128, shuffle=False)

labels = trainset.labels
counts = np.bincount(labels)
priors = counts / counts.sum()
log_priors = np.log(priors + 1e-10)
log_priors = torch.from_numpy(log_priors).float().to(DEVICE)

torch.serialization.add_safe_globals([TorchDNN])
dnn = torch.load(CHECKPOINT_TO_LOAD, map_location="cpu", weights_only=False).to(DEVICE)

logits = extract_logits(dnn, test_loader)
log_post = torch.log_softmax(logits, dim=1)
log_like = log_post - log_priors

post_file = kaldi_io.open_or_fd(OUTPUT_ARK_FILE, 'wb')

start_index = 0
testset.end_indices[-1] += 1

for i, name in enumerate(testset.uttids):
    out = log_like[start_index:testset.end_indices[i]].cpu().numpy()
    start_index = testset.end_indices[i]
    kaldi_io.write_mat(post_file, out, testset.uttids[i])
