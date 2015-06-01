# blog-gender-dataset

Maintains dataset generation procedure for our deep-learning project.

Author: Jim Zheng, Aric Bartle

# Reduced Vocab

- [x] download frequency data
- [x] prune data to get top N%
- [x] output (word-vec => word mapping)
- [x] wordvector.txt, vocab.txt, vocab.pdb

# Blog Cleanup

- go through each blog
    - remove unicode
    - extract words without punctuation
    - all lowercase
    - num => DG
    - unknown vocab => UUNNGG
    - have param k that specifies max sent per ex
