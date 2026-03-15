#!/bin/bash

DATA=~/kaldi/egs/usc/data
S5=~/kaldi/egs/wsj/s5

for split in train dev test; do
    $S5/utils/utt2spk_to_spk2utt.pl $DATA/$split/utt2spk > $DATA/$split/spk2utt
done

