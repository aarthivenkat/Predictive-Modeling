from collections import defaultdict
import numpy as np
import operator
import string
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import f1_score
from sklearn import metrics

category_to_id = {}
id_to_category = {}

myDict = {'goTerm': [], 'goID': [], 'abstract': []}
for line in open("FINAL"):
  go,id,abstract= line.strip().split('\t')
  myDict['goTerm'].append(go)
  myDict['goID'].append(int(id))
  myDict['abstract'].append(abstract.translate(None, ''.join([x for x in string.punctuation if x != '-'])).lower())

  category_to_id[go] = int(id)
  id_to_category[int(id)] = go

df = pd.DataFrame.from_dict(myDict)
train, test = train_test_split(df, test_size=0.33) #66% training

tfidf = TfidfVectorizer(sublinear_tf=True, min_df=1, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(train.abstract)
labels = train.goID

N = 2
for goPhen, goId in sorted(category_to_id.items()):
  features_chi2 = chi2(features, labels == goId)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names())[indices]

  unigrams = [v for v in reversed(feature_names) if len(v.split(' ')) == 1][:N]
  bigrams = [v for v in reversed(feature_names) if len(v.split(' ')) == 2][:N]
  try: print("# '{}':".format(goPhen));
  except: continue
  try: print("  . Top unigrams:\n       . {}".format('\n       . '.join(unigrams)));
  except: continue
  try: print("  . Top bigrams:\n       . {}".format('\n       . '.join(bigrams)));
  except: continue

model = LinearSVC()
model.fit(features, labels)

test_features = tfidf.transform(test.abstract)
y_pred = model.predict(test_features)
y_test = test.goID

print "Testing Metrics:"
print(metrics.classification_report(y_test, y_pred, target_names=df['goTerm'].unique()))
