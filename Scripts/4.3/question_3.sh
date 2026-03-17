#!/bin/bash

# Necessary for feat-to-len and copy-feats
cd ~/kaldi/egs/usc
. ./path.sh

MFCC=~/kaldi/egs/usc/mfcc

echo "Frames for first 5 training utterances:"
feat-to-len scp:data/train/feats.scp ark,t:- | head -n 5 # feat-to-len reads all ark files
# head -n 5 prints only the fisrt 5 elements

echo "MFCC Feature Dimension:"

# Since all MFCC files have the feature dimension, we can check only one
copy-feats scp:$MFCC/raw_mfcc_train.1.scp ark,t:- | sed -n '2p' | awk '{print "MFCC dimension:", NF}'
# copy-feats scp:$MFCC/raw_mfcc_train.1.scp ark,t:- : calculates the feature vector for each frame
# sed -n '2p': Extracts only the second line, the feature vector
# awk '{print "MFCC dimension:", NF}': Counts the number of fields in the extracted line
