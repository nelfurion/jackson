import numpy as np

#from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB

config = {
    'models': [MultinomialNB()],
    'models_parameters': [{
        'alpha': np.arange(0, 0.1, 0.2),
    }]
}
