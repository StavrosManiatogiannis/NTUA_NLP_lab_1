cd ~/kaldi/egs/usc

source ./path.sh
source ./cmd.sh


steps/align_si.sh --nj 4 --cmd "$train_cmd" data/train data/lang exp/tri exp/tri_ali/tri_ali_train
steps/align_si.sh --nj 4 --cmd "$train_cmd" data/dev data/lang exp/tri exp/tri_ali/tri_ali_dev
steps/align_si.sh --nj 4 --cmd "$train_cmd" data/test data/lang exp/tri exp/tri_ali/tri_ali_test
