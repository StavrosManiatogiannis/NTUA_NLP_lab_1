#!/bin/bash

# Paths
LM_TMP=~/kaldi/egs/usc/data/local/lm_tmp
NIST_LM=~/kaldi/egs/usc/data/local/nist_lm
COMPILE_LM=~/kaldi/tools/irstlm/bin/compile-lm

# Compile unigram
$COMPILE_LM $LM_TMP/unigram.ilm.gz -t=yes /dev/stdout | grep -v unk | gzip -c > $NIST_LM/lm_phone_ug.arpa.gz
# Compile bigram
$COMPILE_LM $LM_TMP/bigram.ilm.gz -t=yes /dev/stdout | grep -v unk | gzip -c > $NIST_LM/lm_phone_bg.arpa.gz
