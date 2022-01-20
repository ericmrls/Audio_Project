#!/bin/bash

utils/copy_data_dir.sh data/test_dev93 data/test_dev93_hires

steps/make_mfcc.sh --nj 1 --mfcc-config conf/mfcc_hires.conf data/test_dev93_hires
steps/compute_cmvn_stats.sh data/test_dev93_hires
utils/fix_data_dir.sh data/test_dev93_hires

steps/online/nnet2/extract_ivectors_online.sh --cmd "run.pl" --nj 1 data/test_dev93_hires exp/nnet3_cleaned/extractor exp/nnet3_cleaned/ivectors_test_dev93_hires

utils/mkgraph.sh --self-loop-scale 1.0 --remove-oov data/lang_test_tgsmall exp/chain_cleaned/tdnn_1d_sp exp/chain_cleaned/tdnn_1d_sp/graph_tgsmall


steps/nnet3/decode.sh --acwt 1.0 --post-decode-acwt 10.0 --nj 1 --cmd "run.pl" --online-ivector-dir exp/nnet3_cleaned/ivectors_test_dev93_hires exp/chain_cleaned/tdnn_1d_sp/graph_tgsmall data/test_dev93_hires exp/chain_cleaned/tdnn_1d_sp/decode_test_dev93_tgsmall

