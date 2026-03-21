#!/usr/bin/env bash

USC_ROOT=~/kaldi/egs/usc

cd $USC_ROOT
source ./path.sh
source ./cmd.sh

DATA_PATH=$USC_ROOT/data/test

# FIXME: CHANGE THESE PATHS TO MATCH YOUR CONFIG
GRAPH_PATH=$USC_ROOT/exp/tri
TEST_ALI_PATH=$USC_ROOT/exp/tri/tri_ali_test
OUT_DECODE_PATH=$USC_ROOT/exp/tri/decode_test_dnn


CHECKPOINT_FILE=$OUT_DECODE_PATH/best_usc_dnn.pt
DNN_OUT_FOLDER=$USC_ROOT/exp/dnn

# ------------------- Data preparation for DNN -------------------- #
# Compute cmvn stats for every set and save them in specific .ark files
# These will be used by the python dataset class that you were given
for set in train dev test; do
  compute-cmvn-stats --spk2utt=ark:data/${set}/spk2utt scp:data/${set}/feats.scp ark:data/${set}/${set}"_cmvn_speaker.ark"
  compute-cmvn-stats scp:data/${set}/feats.scp ark:data/${set}/${set}"_cmvn_snt.ark"
done

# ------------------ TRAIN DNN ------------------------------------ #
python ~/lab2/timit_dnn.py $CHECKPOINT_FILE


# ----------------- EXTRACT DNN POSTERIORS ------------------------ #
python ~/lab2/extract_posteriors $CHECKPOINT_FILE $DNN_OUT_FOLDER


# ----------------- RUN DNN DECODING ------------------------------ #
~/lab2/decode_dnn.sh $GRAPH_PATH $DATA_PATH $TEST_ALI_PATH $OUT_DECODE_PATH "cat $DNN_OUT_FOLDER/posteriors.ark"
