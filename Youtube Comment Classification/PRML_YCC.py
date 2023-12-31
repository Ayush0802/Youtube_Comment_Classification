# -*- coding: utf-8 -*-
"""Prml_Minor_Project_B21CS016_B21CS043_B21CS025.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SwQOQeRTL2EVHOual1h4ZrhjiCz6xu-C

# **Team Members :**


*   **Bhut Ayush Dilipbhai (B21CS016)**

*   **Jaysukh Makvana (B21CS043)**
*   **Divyanshu Singhal (B21CS025)**
"""

from google.colab import drive  
drive.mount("/content/drive")

#importing required libraries
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

#to read dataset
data = pd.read_csv("/content/drive/MyDrive/YT_Videos_Comments.csv")
data

data.dtypes

data.isnull().sum()

#Ratio of Null values in dataset
if data.isnull().sum().sum() != 0:
  na_df = (data.isnull().sum() / len(data)) * 100      
  na_df = na_df.drop(na_df[na_df == 0].index).sort_values(ascending=False)
  missing_data = pd.DataFrame({'Missing Ratio %' :na_df})
  missing_data.plot(kind = "barh")
  plt.show()
else:
  print('No Null Values found')

data= data.drop(["Video Title","Video Description","Comment (Displayed)","Comment Author","Comment Time","Comment Author Channel ID"],axis=1)
data

df1=data.copy()
df2=data.copy()
df3=data.copy()
df4=data.copy()
df1 = df1.loc[df1['User'] == 'Cleo Abram']
df2 = df2.loc[df2['User'] == 'Physics Girl']
df3 = df3.loc[df3['User'] == 'neo']
df4 = df4.loc[df4['User'] == 'Jet Lag: The Game']

data = pd.concat([df1,df4,df3,df2])
data

data.describe()

#No. of Comments of a particular Youtuber
fig,ax = plt.subplots()
data['User'].value_counts().plot(ax=ax, kind='bar', xlabel='Youtuber', ylabel='No. of comment on video')
plt.show()

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le.fit(data['User'])
user_data = le.transform(data['User'])
data['User'] = user_data

le.fit(data['Video ID'])
video_ID = le.transform(data['Video ID'])
data['Video ID'] = video_ID

data

data = data.dropna()
data

data.isnull().sum()

import nltk
nltk.download('punkt')

#to find no. of words and sentences in the comments
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

data["num_sentences"] = data['Comment (Actual)'].apply(lambda x: len(sent_tokenize(x)))
data["num_words"] = data['Comment (Actual)'].apply(lambda x: len(word_tokenize(x)))

data

#required libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score

"""# **K Means Clustering**"""

from nltk.corpus import stopwords
nltk.download('stopwords')

from sklearn.cluster import KMeans

df1 = data.copy()

df1['New Comment (Actual)'] = df1['Comment (Actual)'].str.replace('[^a-zA-Z0-9\s]', '') # remove special characters
df1['New Comment (Actual)'] = df1['New Comment (Actual)'].str.lower()

tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_features = tfidf_vectorizer.fit_transform(df1['New Comment (Actual)'])

# Clustering using K-Means
kmeans = KMeans(n_clusters=2)
kmeans.fit(tfidf_features)
tfidf_cluster_labels = kmeans.labels_
df1["label"] = kmeans.labels_

spam_indices = [i for i, label in enumerate(tfidf_cluster_labels) if label == 1]
ham_indices = [i for i, label in enumerate(tfidf_cluster_labels) if label == 0]

df1= df1.drop(["New Comment (Actual)"],axis=1)

temp = {'Spam':len(spam_indices), 'Non Spam':len(ham_indices)}
Type = list(temp.keys())
Count = list(temp.values())
  
fig = plt.figure(figsize = (10, 5))
plt.bar(Type, Count, width = 0.4)
 
plt.xlabel("Type of Comment")
plt.ylabel("No. of Comment")
plt.title("clustering by K-Means Algorithm")
plt.show()

spam_comments = df1.iloc[spam_indices]
spam_comments

ham_comments = df1.iloc[ham_indices]
ham_comments

df1

silhouette_score = silhouette_score(tfidf_features, kmeans.labels_)
print("Silhouette Score:", silhouette_score)

"""# **DBSCAN CLustering**"""

from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer

df2 = data.copy()
df2 = df2.iloc[:20000]

df2['New Comment (Actual)'] = df2['Comment (Actual)'].str.replace('[^a-zA-Z0-9\s]', '') # remove special characters
df2['New Comment (Actual)'] = df2['New Comment (Actual)'].str.lower()

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df2['New Comment (Actual)'])

# Cluster the comments using DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=75)
dbscan.fit(X)
dbscan_cluster_labels = dbscan.labels_
df2['label'] = dbscan.labels_

spam_indices = [i for i, label in enumerate(dbscan_cluster_labels) if label == 0]
ham_indices = [i for i, label in enumerate(dbscan_cluster_labels) if label == -1]

df2= df2.drop(["New Comment (Actual)"],axis=1)

dic = {'Spam':len(spam_indices), 'Non Spam':len(ham_indices)}
Type = list(dic.keys())
Count = list(dic.values())
  
fig = plt.figure(figsize = (10, 5))
plt.bar(Type, Count, width = 0.4)
 
plt.xlabel("Type of Comment")
plt.ylabel("No. of Comment")
plt.title("clustering by DBSCAN Algorithm")
plt.show()

spam_comments = df2.iloc[spam_indices]
spam_comments

ham_comments = df2.iloc[ham_indices]
ham_comments

df2

silhouette_score = silhouette_score(X, dbscan.labels_)
print("Silhouette Score:", silhouette_score)

"""# **Spectral Clustering**"""

from sklearn.cluster import SpectralClustering

df3 = data.copy()
df3 = df3[:20000]

df3['New Comment (Actual)'] = df3['Comment (Actual)'].str.replace('[^a-zA-Z0-9\s]', '') # remove special characters
df3['New Comment (Actual)'] = df3['New Comment (Actual)'].str.lower()

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df3['New Comment (Actual)'])

# Perform spectral clustering
n_clusters = 2
spectral = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors', n_jobs=-1)
spectral.fit(X)
spectral_cluster_labels = spectral.labels_
df3['label'] = spectral.labels_

spam_indices = [i for i, label in enumerate(spectral_cluster_labels) if label == 1]
ham_indices = [i for i, label in enumerate(spectral_cluster_labels) if label == 0]

df3= df3.drop(["New Comment (Actual)"],axis=1)

dic = {'Spam':len(spam_indices), 'Non Spam':len(ham_indices)}
Type = list(dic.keys())
Count = list(dic.values())
  
fig = plt.figure(figsize = (10, 5))
plt.bar(Type, Count, width = 0.4)
 
plt.xlabel("Type of Comment")
plt.ylabel("No. of Comment")
plt.title("clustering by Spectral Algorithm")
plt.show()

spam_comments = df3.iloc[spam_indices]
spam_comments

ham_comments = df3.iloc[ham_indices]
ham_comments

df3

silhouette_score = silhouette_score(X, spectral.labels_)
print("Silhouette Score:", silhouette_score)

"""# **Hierarchical Clustering (Agglomerative)**"""

from sklearn.cluster import AgglomerativeClustering

df4 = data.copy()
df4 = df4.iloc[:5000]

df4['New Comment (Actual)'] = df4['Comment (Actual)'].str.replace('[^a-zA-Z0-9\s]', '') # remove special characters
df4['New Comment (Actual)'] = df4['New Comment (Actual)'].str.lower()

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df4['New Comment (Actual)'])

# Use Agglomerative Clustering to assign cluster labels
n_clusters = 2
agglo = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
agglo.fit(X.toarray())
agglo_cluster_labels = agglo.labels_
df4['label'] = agglo.labels_

spam_indices = [i for i, label in enumerate(agglo_cluster_labels) if label == 1]
ham_indices = [i for i, label in enumerate(agglo_cluster_labels) if label == 0]

df4= df4.drop(["New Comment (Actual)"],axis=1)

dic = {'Spam':len(spam_indices), 'Non Spam':len(ham_indices)}
Type = list(dic.keys())
Count = list(dic.values())
  
fig = plt.figure(figsize = (10, 5))
plt.bar(Type, Count, width = 0.4)
 
plt.xlabel("Type of Comment")
plt.ylabel("No. of Comment")
plt.title("clustering by Hierarchical (Agglomerative) Algorithm")
plt.show()

spam_comments = df4.iloc[spam_indices]
spam_comments

ham_comments = df4.iloc[ham_indices]
ham_comments

df4

silhouette_score = silhouette_score(X, agglo.labels_)
print("Silhouette Score:", silhouette_score)