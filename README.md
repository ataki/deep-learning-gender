# Reduced Vocab

- download frequency data
- prune data to get top N%
- output (word-vec => word mapping)
- wordvector.txt, vocab.txt, vocab.pdb

# Blog Cleanup

- go through each blog
    - remove unicode
    - extract words without punctuation
    - all lowercase
    - num => DG
    - unknown vocab => UUNNGG
    - have param k that specifies max sent per ex
