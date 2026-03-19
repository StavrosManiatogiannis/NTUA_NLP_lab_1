#!/bin/bash
sudo ln -s $(which python3) /usr/bin/python
cd ~/kaldi/egs/usc


steps/decode.sh --nj 4 --cmd run.pl exp/mono/graph_ug data/dev exp/mono/dev_decoded_ug
steps/decode.sh --nj 4 --cmd run.pl exp/mono/graph_ug data/test exp/mono/test_decoded_ug


steps/decode.sh --nj 4 --cmd run.pl exp/mono/graph_bg data/dev exp/mono/dev_decoded_bg
steps/decode.sh --nj 4 --cmd run.pl exp/mono/graph_bg data/test exp/mono/test_decoded_bg