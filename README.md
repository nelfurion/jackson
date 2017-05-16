# Usage
Jackson requires several third-party packages to run. It's easier to download some of them through Anaconda, so the first step is to download and install Anaconda/Miniconda for your platform.

[Download Anaconda](https://www.continuum.io/downloads)

Create a virtual environment:
```
conda create -n NAME python=3.5.2
```

Activate the environment:
```
Linux:
source activate ENVIRONMENT_NAME

Windows:
activate ENVIRONMENT_NAME
```

Installing the packages:
```
conda install --file conda-requirements.txt
pip install -r pip-requirements.txt
```

The next step is to download the needed NLTK packages.

```
python download_nltk_packages.py
```

Since there is a bug when using the default bllip.py, we need to change it by starting:
```
bash edit_bllip.sh ENVIRONMENT_NAME
```

Talking with Jackson:

1) Through the terminal:

```
python jackson.py
```

2) Start the web interface:
```
python ./web/manage.py runserver
```

# Jackson
Jackson is a chatbot using Machine Learning and Natural Language Processing. It is not a commercial chatbot. It is mostly for educational purposes.

## 1. Input(Question) Classification


For the classificatio a RandomForestClassifier ensemble method is used. It achieves an accuracy of ![Progress](http://progressed.io/bar/79) (78.957).


## 2. Building query

Jackson answers questions by eighter searching in Wikipedia or in a factological database. The database is built on top of neo4j.

To search wikipedia Jackson uses eighter the named entities extracted from the question or all the combinations of adjectives and nouns.

## 3. Information retrieval

If Jackson uses information from Wikipedia it is summarized to three sentences, before being shown to the user. Two types of summarization are implemented:
1) based on the frequiencies of the words in the text_processor;
2) based on the appearances of the adjectives and nouns from the question in the text.

Since the second approach is usually much slower (it is used for summarization of multiple pages), a multiprocessing summarizer is used. It starts several processes which simultaneously score the sentences from different Wikipedia pages. When the scoring finishes the best three sentences are shown to the user.

> User: Who is Donald Trump?

> Jackson: Trump was born and raised in Queens , New York City , and earned an economics degree from the Wharton School of the University of Pennsylvania. In June 2015 , he launched his campaign for the 2016 presidential election , and quickly emerged as the front-runner among 17 candidates in the Republican primaries. He became the oldest and wealthiest person to assume the presidency , the first without prior military or government service , and the fifth elected with less than a plurality of the national popular vote.

## 4. Learning new information

Jackson can learn new information from declarative sentences. Example:

> User: John loves Monika.

> Jackson: John love monika.

> User: Does Monika love John?

> Jackson: I know monika, but i don't know what monika love.

will generate two objects in the database: monica and john, and a connection with label love.

## 5. Architecture

### Static View
![Static View Diagram](http://i.imgur.com/EFzfKAW.png)

Jackson uses a client, a server, Wikipedia and a Neo4J database.

### How Jackson answers questions?

![Question Answering Diagram](http://i.imgur.com/4FFiWxk.png)

Jackson tries to find an answer for the question in it's factological database. If an answer ins't found, it searches for information in Wikipedia and uses the question answer type class to summarize the data.

### Architecture

![Architecture](http://i.imgur.com/qHm2AmH.png)

Jackson uses a stack of Heroku servers to work. First the client sends its request to the main server. Then remote services are used for topic classification and retrieving information. If the found answer is from Wikipedia, the text from the pages is sent to a remote worker, which itself delegates tasks to remote scorers, to score it's sentences and produce a summary. The client receives the endpoint of the worker and polls to see if the job is done. When the job is done, the client takes the summary by it's job id.

## Features that may eventually be implemented

| Features      | Implementation|
| ------------- |:-------------:|
| Summarization | Yes |
| Question answer type classification | Yes |
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
