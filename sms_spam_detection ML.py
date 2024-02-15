# -*- coding: utf-8 -*-
"""SMS Spam Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ISPB0ej7TBf_wa1M86lrtcNGrt5HLsvR
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
import seaborn as sns

#importing data
df=pd.read_csv("/content/spam.csv", encoding="latin-1")

df.head(6)

"""STEP 1: Data Cleaning using pandas"""

df.shape  #5572 rows and 5 columns

df.columns

#droping the not necessary columns
df.drop(columns=['Unnamed: 2','Unnamed: 3','Unnamed: 4'],inplace=True)

df.sample(5)

"""clearly, v1 column shows whether text is spam or not and v2 shows the text.
v1=output column
v2=text column
"""

# renaming the cols
df.rename(columns={'v1':'output','v2':'text'},inplace=True)
df.sample(7)

df.describe()

df.isnull().sum()

# check for duplicate values
df.duplicated().sum()

# remove duplicates
df = df.drop_duplicates(keep='first')

df.duplicated().sum()

df.shape

"""our data has no nan values to be removed or replaced and the duplicate values have been removed

LabelEncoder is used to encode categorical labels (classes or target variable) into numerical values.

Before Label Encoding:

'ham' represents non-spam messages.
'spam' represents spam messages.
After Label Encoding:

'ham' might be encoded as 0.
'spam' might be encoded as 1.
"""

from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()

df['output'] = encoder.fit_transform(df['output'])

df.tail()

df['output'].value_counts()

#this shows ham=4516 and spam=653

plt.pie(df['output'].value_counts(), labels=['ham','spam'],autopct="%0.2f")
plt.show()

#shows data have more ham i.e imbalanced

nltk.download('punkt')

"""making new columns: no.of characters , no.of words, no.of sentences"""

df['no_characters'] = df['text'].apply(len)

df.head()

df['no_words'] = df['text'].apply(lambda x:len(nltk.word_tokenize(x)))

#creating a new column ('no_words') in the DataFrame that represents the number of words in each text entry, using the NLTK library for tokenization

df.head()

df['no_sentences'] = df['text'].apply(lambda x:len(nltk.sent_tokenize(x)))

#ambda function tokenizes the text into sentences using the nltk.sent_tokenize function and calculates the number of sentences in each text.

df.head()

df[['no_characters','no_words','no_sentences']].describe()

"""analysing, spam and ham seprately"""

df[df['output'] == 1][['no_characters','no_words','no_sentences']].describe()

df[df['output'] == 0][['no_characters','no_words','no_sentences']].describe()

plt.figure(figsize=(10,5))
sns.histplot(df[df['output'] == 0]['no_words'])
sns.histplot(df[df['output'] == 1]['no_words'],color='red')

plt.figure(figsize=(10,5))
sns.histplot(df[df['output'] == 0]['no_characters'])
sns.histplot(df[df['output'] == 1]['no_characters'],color='green')

"""we can clearly see, spam have more no.of words and no.of characters"""

df.corr()

sns.heatmap(df.corr(),annot=True)

"""no_characters vs. no_words: There is a strong positive correlation of approximately 0.966 between 'no_characters' and 'no_words'. This indicates a strong positive linear relationship, which is expected, as more characters in a text generally mean more words.

no_characters vs. no_sentences: There is a moderate positive correlation of approximately 0.624 between 'no_characters' and 'no_sentences'. This suggests a moderate positive linear relationship.

no_words vs. no_sentences: There is a moderate positive correlation of approximately 0.680 between 'no_words' and 'no_sentences'. This indicates a moderate positive linear relationship.

Preprocessing
Lower case
Tokenization
Removing special characters
Removing stop words and punctuation
Stemming
"""

from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer

nltk.download('stopwords')
nltk.download('punkt')

ps=PorterStemmer()

#This line creates an instance of the Porter Stemmer from NLTK, named 'ps'. The Porter Stemmer is used for stemming, which involves reducing words to their root or base form.

ps.stem('enjoying')

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))


    return " ".join(y)

"""Converts text to lowercase.

Tokenizes the text into words.

Removes non-alphanumeric characters.

Removes English stopwords and punctuation.

Applies stemming using the Porter Stemmer.

The function transform_text applied to the input "Did you like mY pResentation on Ml" would return the processed text: "like present ml". It has been converted to lowercase, tokenized, non-alphanumeric characters removed, stopwords removed, and words stemmed.
"""

transform_text("Did you like mY pResentation on Ml")

transform_text("I'm gonna be home soon and i don't want to talk about this stuff anymore tonight, k?")

"""This line creates a new column 'transformed_text' in the DataFrame 'df', containing the preprocessed and transformed text for each message. It applies the transform_text function to the 'text' column using the apply method."""

df['transformed_text'] = df['text'].apply(transform_text)

df.head()

"""
This code imports the WordCloud class from the 'wordcloud' library and creates an instance named 'wc'. The parameters specified are width, height, minimum font size, and background color for generating the word cloud visualization."""

from wordcloud import WordCloud
wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')

spam_wc = wc.generate(df[df['output'] == 1]['transformed_text'].str.cat(sep=" "))
#str.cat(sep=" ") concatenates the transformed text of all spam messages into a single string separated by spaces.

plt.figure(figsize=(10,6))
plt.imshow(spam_wc)

ham_wc = wc.generate(df[df['output'] == 0]['transformed_text'].str.cat(sep=" "))

plt.figure(figsize=(10,6))
plt.imshow(ham_wc)

df.head()

"""This code creates a list named 'spam_corpus' containing individual words from the transformed text of spam messages in the DataFrame 'df'. It iterates through each transformed text, splits it into words, and appends each word to the 'spam_corpus' list."""

spam_corpus = []
for msg in  df[df['output'] == 1]['transformed_text'].tolist():
    for word in msg.split():
        spam_corpus.append(word)

len(spam_corpus)

ham_corpus = []
for msg in df[df['output'] == 0]['transformed_text'].tolist():
    for word in msg.split():
        ham_corpus.append(word)

len(ham_corpus)

df.head()

"""CountVectorizer: Counts word occurrences in each document, creating a matrix of word frequencies.

TfidfVectorizer: Considers not just word frequencies but also the importance of words in the entire dataset using TF-IDF. Often more informative than simple word counts.
"""

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
cv = CountVectorizer()
tfidf = TfidfVectorizer(max_features=3000)

X = tfidf.fit_transform(df['transformed_text']).toarray()
#This line uses the fit_transform method of the TfidfVectorizer instance (tfidf) to transform the 'transformed_text' column in the DataFrame 'df' into a TF-IDF matrix.

X.shape

y = df['output'].values

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=2)

from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score

gnb = GaussianNB()
mnb = MultinomialNB()
bnb = BernoulliNB()

gnb.fit(X_train,y_train)
y_pred1 = gnb.predict(X_test)
print(accuracy_score(y_test,y_pred1))
print(confusion_matrix(y_test,y_pred1))
print(precision_score(y_test,y_pred1))

mnb.fit(X_train,y_train)
y_pred2 = mnb.predict(X_test)
print(accuracy_score(y_test,y_pred2))
print(confusion_matrix(y_test,y_pred2))
print(precision_score(y_test,y_pred2))

bnb.fit(X_train,y_train)
y_pred3 = bnb.predict(X_test)
print(accuracy_score(y_test,y_pred3))
print(confusion_matrix(y_test,y_pred3))
print(precision_score(y_test,y_pred3))

"""Gaussian Naive Bayes (gnb):

Accuracy: 89.17%
Precision: 56.44%

Multinomial Naive Bayes (mnb):

Accuracy: 97.20%
Precision: 100.0%

Bernoulli Naive Bayes (bnb):

Accuracy: 98.36%
Precision: 99.19%

Based on accuracy and precision, the Bernoulli Naive Bayes (bnb) model seems to perform the best in this context. It achieved the highest accuracy and a high precision score. However, it's essential to consider the specific requirements and goals of your application when choosing a model. Sometimes, a balance between precision and recall is crucial, depending on the consequences of false positives and false negatives in your task.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier

svc = SVC(kernel='sigmoid', gamma=1.0)
knc = KNeighborsClassifier()
mnb = MultinomialNB()
dtc = DecisionTreeClassifier(max_depth=5)
lrc = LogisticRegression(solver='liblinear', penalty='l1')
rfc = RandomForestClassifier(n_estimators=50, random_state=2)
abc = AdaBoostClassifier(n_estimators=50, random_state=2)
bc = BaggingClassifier(n_estimators=50, random_state=2)
etc = ExtraTreesClassifier(n_estimators=50, random_state=2)
gbdt = GradientBoostingClassifier(n_estimators=50,random_state=2)
xgb = XGBClassifier(n_estimators=50,random_state=2)

"""
created a dictionary named clfs that maps short names to their respective classifier instances:

'SVC': Support Vector Machine with a sigmoid kernel (svc).

'KN': K-Nearest Neighbors (knc).

'NB': Multinomial Naive Bayes (mnb).

'DT': Decision Tree with a maximum depth of 5 (dtc).

'LR': Logistic Regression (lrc).

'RF': Random Forest with 50 trees (rfc).

'AdaBoost': AdaBoost with 50 weak learners (abc).

'BgC': Bagging with 50 base classifiers (bc).

'ETC': Extra Trees with 50 trees (etc).

'GBDT': Gradient Boosting with 50 trees (gbdt).

'xgb': XGBoost with 50 trees (xgb)."""

clfs = {
    'SVC' : svc,
    'KN' : knc,
    'NB': mnb,
    'DT': dtc,
    'LR': lrc,
    'RF': rfc,
    'AdaBoost': abc,
    'BgC': bc,
    'ETC': etc,
    'GBDT':gbdt,
    'xgb':xgb
}

def train_classifier(clf,X_train,y_train,X_test,y_test):
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test,y_pred)
    precision = precision_score(y_test,y_pred)

    return accuracy,precision

train_classifier(svc,X_train,y_train,X_test,y_test)

""" Support Vector Machine (svc) classifier:

Accuracy: 97.29%

Precision: 97.41%

This indicates that the SVM model performed well on the test data, achieving a high accuracy and precision.
"""

accuracy_scores = []
precision_scores = []

for name,clf in clfs.items():

    current_accuracy,current_precision = train_classifier(clf, X_train,y_train,X_test,y_test)

    print("For ",name)
    print("Accuracy - ",current_accuracy)
    print("Precision - ",current_precision)

    accuracy_scores.append(current_accuracy)
    precision_scores.append(current_precision)

""" Random Forest (RF), Extra Trees (ETC), and XGBoost (xgb) demonstrate high accuracy and precision in this context."""

performance_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy':accuracy_scores,'Precision':precision_scores}).sort_values('Precision',ascending=False)
performance_df

"""reated a DataFrame named performance_df containing algorithm names, accuracy scores, and precision scores. The DataFrame is sorted in descending order based on precision scores. This can be helpful for easily comparing and visualizing the performance of different classifiers.





"""

performance_df1 = pd.melt(performance_df, id_vars = "Algorithm")
performance_df1

sns.catplot(x = 'Algorithm', y='value',
               hue = 'variable',data=performance_df1, kind='bar',height=5)
plt.ylim(0.5,1.0)
plt.xticks(rotation='vertical')
plt.show()

"""CONCLUSION TILL NOW:
Among the classifiers, Extra Trees (ETC) and Random Forest (RF) exhibit the highest precision and accuracy in spam detection.

Naive Bayes (NB) performs well, showing perfect precision but slightly lower accuracy.

Support Vector Machine (SVC) struggles with precision, likely due to class imbalance.

Decision Tree (DT) and K-Nearest Neighbors (KN) show lower performance compared to other models.

# model improve
# 1. Change the max_features parameter of TfIdf
"""

temp_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy_max_ft_3000':accuracy_scores,'Precision_max_ft_3000':precision_scores}).sort_values('Precision_max_ft_3000',ascending=False)

temp_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy_scaling':accuracy_scores,'Precision_scaling':precision_scores}).sort_values('Precision_scaling',ascending=False)

new_df = performance_df.merge(temp_df,on='Algorithm')
new_df_scaled = new_df.merge(temp_df,on='Algorithm')

temp_df = pd.DataFrame({'Algorithm':clfs.keys(),'Accuracy_num_chars':accuracy_scores,'Precision_num_chars':precision_scores}).sort_values('Precision_num_chars',ascending=False)

new_df_scaled.merge(temp_df,on='Algorithm')

"""creating a Voting Classifier combines the strengths of multiple models to enhance overall performance, increase robustness, handle diverse aspects of the data, and provide flexibility in decision-making. It's a strategy to improve predictive accuracy and generalization by leveraging the strengths of different algorithms."""

# Voting Classifier
svc = SVC(kernel='sigmoid', gamma=1.0,probability=True)
mnb = MultinomialNB()
etc = ExtraTreesClassifier(n_estimators=50, random_state=2)

from sklearn.ensemble import VotingClassifier

voting = VotingClassifier(estimators=[('svm', svc), ('nb', mnb), ('et', etc)],voting='soft')

voting.fit(X_train,y_train)

y_pred = voting.predict(X_test)
print("Accuracy",accuracy_score(y_test,y_pred))
print("Precision",precision_score(y_test,y_pred))

"""This indicates that the ensemble of Support Vector Machine, Multinomial Naive Bayes, and Extra Trees models, working together through the Voting Classifier, performed very well on the given task"""

# Applying stacking
estimators=[('svm', svc), ('nb', mnb), ('et', etc)]
final_estimator=RandomForestClassifier()

from sklearn.ensemble import StackingClassifier

"""stacking combines predictions from diverse models (SVM, Naive Bayes, and Extra Trees) using a final meta-model (Random Forest). This approach aims to harness the strengths of each model, improving overall predictive accuracy and robustness."""

clf = StackingClassifier(estimators=estimators, final_estimator=final_estimator)
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
print("Accuracy",accuracy_score(y_test,y_pred))
print("Precision",precision_score(y_test,y_pred))

"""This indicates that the classifier performed well in making accurate predictions, with a high precision rate"""