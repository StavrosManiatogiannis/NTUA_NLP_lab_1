#!/bin/bash

# Paths
EGS=~/kaldi/egs
DATA=$EGS/usc/data
DICT=$DATA/local/dict
LANG=$DATA/lang
LOCAL_LANG=$DATA/local/lang_tmp
PREPARE_LANG=utils/prepare_lang.sh

mkdir -p $LOCAL_LANG # create the directory LOCAL_LANG

cd ~/kaldi/egs/wsj/s5 # necessary for utils/parse_options.sh and utils/validate_dict_dir.pl 

# prepare_lang script must be executable
if [ ! -x "$PREPARE_LANG" ]; then
    chmod +x "$PREPARE_LANG"
fi

# prepare_lang.sh
# Arguments:
# 1: dict directory
# 2: out of vocabulary symbol (<oov>)
# 3: temporary lang directory
# 4: output lang directory

$PREPARE_LANG $DICT "<oov>" $LOCAL_LANG $LANG

