#Downloads data for training and testing the question classifier
#Runs the scripts for data generation
#Trains and saves the classifier in /models/classifiers/name_accuracy.pkl*

curl "http://cogcomp.cs.illinois.edu/Data/QA/QC/train_5500.label" -o "./questions_train.txt"

curl "http://cogcomp.cs.illinois.edu/Data/QA/QC/TREC_10.label" -o "./questions_test.txt"
