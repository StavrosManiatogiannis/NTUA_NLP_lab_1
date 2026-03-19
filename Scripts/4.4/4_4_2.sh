#!/bin/bash
cd ~/kaldi/egs/usc
utils/mkgraph.sh data/lang_test_ug exp/mono/ exp/mono/graph_ug
utils/mkgraph.sh data/lang_test_bg exp/mono/ exp/mono/graph_bg  