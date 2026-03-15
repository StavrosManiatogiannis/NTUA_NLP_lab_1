#!/bin/bash

DATA=~/kaldi/egs/usc/data

for split in train dev test; do
    sort $DATA/$split/wav.scp -o $DATA/$split/wav.scp
    sort $DATA/$split/text -o $DATA/$split/text
    sort $DATA/$split/utt2spk -o $DATA/$split/utt2spk
done

