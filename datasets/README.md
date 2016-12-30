# Question classification, dataset, extracted

## Thoughts

Initially I emphasized on Wh-words. I thought that they can give thorough understanding of the question. This does not seem to be the case, as shown in the example:

    What is the distance between Pisa and Rome?

One may assume, only on the Wh-word, that we want a definition, but accurate answer type should be a number.

## Datasets([paper][1])

I use the datasets, assembled from Li and Roth in 2002.

## Feature composition
I will try to follow Olalere Williams from Stanford University. He uses the following types of features to train his informer(table taken from the paper):

| Feature Set | Jaccard overlap | Precision | Recall | F1 |
| ----------- | --------------- | --------- | ------ | -- |
| Current word | 0.380 | 0.840 | 0.410 | 0.551 |
| + Previous label | 0.441 | 0.861 | 0.475 | 0.612 |
| + Previous word | 0.473 | 0.861 | 0.512 | 0.642 |
| + Question word | 0.494 | 0.889 | 0.526 | 0.661 |
| + Brevity(6) | 0.748 | 0.882 | 0.831 | 0.856 |
|`+ Brevity(5)`| 0.767 | 0.910 | 0.831 | 0.868 |
|`+ Brevity(7)`| 0.564 | 0.826 | 0.640 | 0.721 |
| + Next word | 0.806 | 0.904 | 0.882 | 0.893 |

### Informer([paper][2])

A span of words(one or more), sufficient for classifying the question.

These guys use the following features to classify questions:

| Features | Coarse | Fine |
| -------- | ------ | ---- |
| Question trigrams | 91.2 | 77.6 |
| All question qgrams | 87.2 | 71.8 |
| All question unigrams | 88.4 | 78.2 |
| ------------------------ | ------ | ---- |
| Question bigrams | 91.6 | 79.4 |
| `+ informer q-grams` | 94.0 | 82.4 |
| `+ informer hypernyms` | 94.2 | 88.0 |
| ------------------------ | ------ | ---- |
| Question unigrams + all informer | 93.4 | 88.0 |
| Only informer | 92.2 | 85.0 |
| Question bigrams + hypernyms | 91.6 | 79.4 |

## Problems

- Training  DecisionTreeClassifier ...
	C:\Users\nelfurion\Anaconda3\envs\py3\lib\site-packages\sklearn\model_selection\_split.py:581: Warning: The least populated class in y has only 1 members, which is too few. The minimum number of groups for any class cannot be less than n_splits=3.
  	% (min_groups, self.n_splits)), Warning)


- The informer only works for questions that require one answer type - ex:

        How much does a rhino weigh?

    Other types of questions like:

        Where do rhinos live and how much do they weigh?
        What is the name and age of ... ?

    Should be assigned several answer types and actions should be taken accordingly.


[1]:http://ucrel.lancs.ac.uk/acl/C/C02/C02-1150.pdf
[2]:https://www.cse.iitb.ac.in/~soumen/doc/emnlp2005/382.pdf
