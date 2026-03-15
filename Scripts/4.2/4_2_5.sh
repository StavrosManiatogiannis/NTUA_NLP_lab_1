#!/bin/bash

DATA=~/kaldi/egs/usc/data

for split in train dev test; do
	# sort wav.scp, text and utt2spk by utterance ID (first column)
	sort -k1,1 $DATA/$split/wav.scp -o $DATA/$split/wav.scp
	sort -k1,1 $DATA/$split/text -o $DATA/$split/text
	sort -k1,1 $DATA/$split/utt2spk -o $DATA/$split/utt2spk

done
