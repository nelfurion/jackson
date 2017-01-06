# Usage
Jackson requires several packages to run:

```
scikit-learn>=0.17.1
numpy>=1.11.1
scipy>=0.17.1
nltk>=3.2.1,
clint=0.5.1
bllipparser
```

You can install them from 'requirements.txt' with your
preferred package manager.

Example:

```
PIP: pip install -r './requirements.txt'
CONDA: conda install --file './requirements.txt'
```

Because bllipparser is not readily available for Windows, installation is easier on Linux machines.

You also have to install several nltk packages, found in nltk_requirements.txt:
```
punkt
averaged_perceptron
maxent_ne_chunker
words
stopwords
```

You should also download the Wall Street Journal parsing model.

```
sudo python -m nltk.downloader bllip_wsj_no_aux
```

They can be installed from the command line like so:
```
python
>>> import nltk
>>> nltk.download('package_name')
```

To start the chatbot run:

```
cd ./jackson
python jackson.py
```

To download the train and test data, run:

```
cd ./datasets
sh generate_data.sh
```

To train the questions classifier run:

```
cd ./datasets
python train_question_classifier.py
```

The script will train the model, and save it in './models/classifiers/' as 'classifier_accuracy.py'.

# Jackson
Chatbot using Natural Language Processing

Jackson is a chatbot using natural language processing. Jackson is not a commercial chatbot.
It is mostly for educational purposes.

Jackson is separated into 3 parts.

1) Classify user input

2) Building a query

3) Searching and extracting information based on the query

## 1. Input(Question) Classification
![Progress](http://progressed.io/bar/33)

I am currently using a basic classification - Naive Bayes with no feature engineering.
The classifier works with 33.2% accuracy. It is going to be improved in the future.

## 2. Building query

Currently Jackson can extract Named Entities from the text and search information for them from Wikipedia.

## 3. Information retrieval

After the contents of a page(the information for a Named Entity) is received, it is summarized and shown to the user.

## Features that will eventually be implemented

| Features      | Implementation|
| ------------- |:-------------:|
| Summarization | Basic |
| Sentiment analysis | No |
| Character | No |
| Character analysis | No |
| Adaptation to human learning patterns | No |
| Generating a purpose | No |
| Gender assumption | No |
| Age classification | No |
| Introspection stimulation | No |
| Story generation | No |
| Some different statistical analysis | No |
| Context | No |
