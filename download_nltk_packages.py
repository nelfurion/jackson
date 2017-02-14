import nltk

print('Starting download of NLTK requirements...')

with open('./nltk_requirements.txt') as nltk_requirements:
    requirements = nltk_requirements.read().splitlines()
    for requirement in requirements:
        nltk.download(requirement)

print('Download finished...')