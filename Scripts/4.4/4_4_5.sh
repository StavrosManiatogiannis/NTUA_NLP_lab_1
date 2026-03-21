#!/bin/bash
cd ~/kaldi/egs/usc

. ./path.sh
. ./cmd.sh



steps/align_si.sh --nj 4 --cmd "$train_cmd" data/train data/lang exp/mono exp/mono_ali



steps/train_deltas.sh --cmd "$train_cmd" 2000 11000 data/train data/lang  exp/mono_ali exp/tri




utils/mkgraph.sh data/lang_test_ug exp/tri exp/tri/graph_ug

utils/mkgraph.sh data/lang_test_bg exp/tri exp/tri/graph_bg



steps/decode.sh --nj 4 --cmd "$decode_cmd" exp/tri/graph_ug data/dev exp/tri/dev_decoded_ug
steps/decode.sh --nj 4 --cmd "$decode_cmd" exp/tri/graph_ug data/test exp/tri/test_decoded_ug


steps/decode.sh --nj 4 --cmd "$decode_cmd" exp/tri/graph_bg data/dev exp/tri/dev_decoded_bg
steps/decode.sh --nj 4 --cmd "$decode_cmd" exp/tri/graph_bg data/test exp/tri/test_decoded_bg






local/score.sh --cmd "utils/run.pl" data/dev exp/tri/graph_ug exp/tri/dev_decoded_ug
local/score.sh --cmd "utils/run.pl" data/test exp/tri/graph_ug exp/tri/test_decoded_ug




local/score.sh --cmd "utils/run.pl" data/dev exp/tri/graph_bg exp/tri/dev_decoded_bg
local/score.sh --cmd "utils/run.pl" data/test exp/tri/graph_bg exp/tri/test_decoded_bg
