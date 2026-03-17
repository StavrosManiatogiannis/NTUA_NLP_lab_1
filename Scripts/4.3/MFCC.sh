#!/bin/bash

# Necessary for make_mfcc.sh and compute_cmvn_stats.sh
cd ~/kaldi/egs/usc
. ./path.sh
. ./cmd.sh

# Number of parallel jobs
nj=5

datasets="train dev test"
for d in $datasets; do
    echo "Extracting MFCCs for $d:"
    steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/$d exp/make_mfcc/$d mfcc
    echo ""
    echo "Computing CMVN stats for $d:"
    steps/compute_cmvn_stats.sh data/$d exp/make_mfcc/$d mfcc
    echo ""
    echo ""
done
