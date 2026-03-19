#!/bin/bash
cd ~/kaldi/egs/usc
steps/train_mono.sh --boost_silence 1.25 --nj 4 --cmd "$train_cmd" data/train data/lang exp/mono