#!/bin/bash

cd ~/kaldi/egs/usc
. ./path.sh || exit 1; # needed for arpa2fst and fstisstochastic

# Paths
DATA=~/kaldi/egs/usc/data
lmdir=$DATA/local/nist_lm

# local/timit_format_data.sh main procedure to create G.fst
for lm_suffix in ug bg; do
  test=$DATA/lang_test_${lm_suffix}
  mkdir -p $test
  cp -r $DATA/lang/* $test

  gunzip -c $lmdir/lm_phone_${lm_suffix}.arpa.gz | \
    arpa2fst --disambig-symbol=#0 \
             --read-symbol-table=$test/words.txt - $test/G.fst
  fstisstochastic $test/G.fst
done
