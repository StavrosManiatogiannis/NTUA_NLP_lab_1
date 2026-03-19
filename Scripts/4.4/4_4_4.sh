#!/bin/bash
cd ~/kaldi/egs/usc


local/score.sh --cmd "utils/run.pl" data/dev exp/mono/graph_ug exp/mono/dev_decoded_ug
local/score.sh --cmd "utils/run.pl" data/test exp/mono/graph_ug exp/mono/test_decoded_ug


local/score.sh --cmd "utils/run.pl" data/dev exp/mono/graph_bg exp/mono/dev_decoded_bg
local/score.sh --cmd "utils/run.pl" data/test exp/mono/graph_bg exp/mono/test_decoded_bg
