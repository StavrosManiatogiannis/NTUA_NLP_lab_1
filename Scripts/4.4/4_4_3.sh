#!/bin/bash
sudo ln -s $(which python3) /usr/bin/python
cd ~/kaldi/egs/usc
. ./path.sh
. ./cmd.sh

if [ ! -x ~/kaldi/egs/usc/local/score.sh ]; then
    chmod +x ~/kaldi/egs/usc/local/score.sh
fi

# decode dev and test for unigram mono model
steps/decode.sh --nj 4 --cmd "$decode_cmd" exp/mono/graph_ug data/dev exp/mono/dev_decoded_ug
steps/decode.sh --nj 4 --cmd "$decode_cmd" exp/mono/graph_ug data/test exp/mono/test_decoded_ug

# decode dev and test for bigram mono model
steps/decode.sh --nj 4 --cmd "$decode_cmd" exp/mono/graph_bg data/dev exp/mono/dev_decoded_bg
steps/decode.sh --nj 4 --cmd "$decode_cmd" exp/mono/graph_bg data/test exp/mono/test_decoded_bg
