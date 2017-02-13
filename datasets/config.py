from sklearn.ensemble import RandomForestClassifier

config = {
    'models': [RandomForestClassifier()],
    'models_parameters': [{
        'n_estimators': [100],
        'random_state': [1490702865],
        'max_features': [1.0],
        'oob_score': [True]
    }]
}
