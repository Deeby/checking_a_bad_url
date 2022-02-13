from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
import joblib
import pandas as pd
clf = joblib.load('filename.pkl')
data = pd.read_csv('/home/homi/Downloads/Using-machine-learning-to-detect-malicious-URLs-master/data/data.csv')
vectorizer = CountVectorizer()
X = [ i for i in data.url]
y = [ i for i in data.label]
train_texts, test_texts, _, _ = train_test_split(X, y, random_state = 42, test_size=0.1)
vectorizer.fit_transform(train_texts)
vectorizer.transform(test_texts)

def check(new_data: str):
    return str(clf.predict(vectorizer.transform([new_data]))[0])