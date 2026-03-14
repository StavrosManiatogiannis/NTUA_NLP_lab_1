#!/bin/bash

# Paths
DATA=~/kaldi/egs/usc/data
TRAIN_LM=$DATA/train/lm_train.text
LM_TMP=$DATA/local/lm_tmp
BUILD_LM=~/kaldi/tools/irstlm/bin/build-lm.sh

mkdir -p $LM_TMP

# IRSTLM script must be executable
if [ ! -x "$BUILD_LM" ]; then
    chmod +x "$BUILD_LM"
fi

# Set IRSTLM environment variable
export IRSTLM=~/kaldi/tools/irstlm

# unigram LM
$BUILD_LM -i $TRAIN_LM -n 1 -o $LM_TMP/unigram.ilm.gz
if [ ! -f "$LM_TMP/unigram.ilm.gz" ]; then
    echo "Error: Unigram LM not created"
    exit 1
fi

# bigram LM
$BUILD_LM -i $TRAIN_LM -n 2 -o $LM_TMP/bigram.ilm.gz
if [ ! -f "$LM_TMP/bigram.ilm.gz" ]; then
    echo "Error: Bigram LM not created"
    exit 1
fi
