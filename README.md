# interpolated_ngram
Takes an input corpus, collects n-grams for n=(1,2,3), builts a language model, and calculates the perplexity. 

```ngram_count.sh``` takes training data & produces a file enumerating uni-, bi- and tri-
grams from the file and their respective counts. 

Args: 
* training_data: File formatted as: w1 w2 ... w_n; that is, one sentence per line. Example at examples/training_data_ex.

Returns: 
* ngram_count_file: File formatted as: count word1 ... word_k. Example at examples/ngram_count_ex.

To run: 
```
ngram_count.sh training_data ngram_count_file
```

```build_lm.sh``` builds an LM using ngram counts WITHOUT smoothing. 

Args: 
* ngram_count_file: the output file of ```ngram_count.sh```. Example at examples/ngram_count_ex.

Returns: 
* lm_file: follows the modified ARPA format. Example at examples/lm_ex.

To run: 
```
build_lm.sh ngram_count_file lm_file
```

```ppl.sh``` calculates the perplexity of a test data given an LM and three lambdas that are each non-negative real numbers that sum to 1. 

Args: 
* lm_file: the output file of ```build_lm.sh```. Example at examples/lm_ex.
* l1: lambda_1 in the interpolation formula. 
* l2: lambda_2 in the interpolation formula. 
* l3: lambda_3 in the interpolation formula. 
* test_data: has the same format as the training data. Example at examples/test_data_ex. 

Returns: 
* output_file: n-grams and their respective calculated probability in the format of examples/ppl_ex. 

To run: 
```
ppl.sh lm_file l1 l2 l3 test_data output_file
```

The output folder contains the results of this pipeline when the training_data file is data/wsj_sec0_19.word and the test_data file is data/wsj_sec22.word. Each respective lambda value is listed in the file name. 

HW6 OF LING570 (11/11/2021)