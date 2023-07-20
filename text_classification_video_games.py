# -*- coding: utf-8 -*-
"""Project1_Text_Classification_Video_Games.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XunOmhxaCkv6SZRzucC4R_6bImjBQJ0m

# **Dataset**

Dataset: [Populer Video Games - Kaggle](https://www.kaggle.com/datasets/matheusfonsecachaves/popular-video-games)

I used this data on July 14, 2023

# **Description**

Game rating prediction: Using attributes such as "Rating" as well as other features such as "Title", "Developers", "Summary", "Platforms", and "Genres," using NLP

# **Data Preparation**

## Library Imports
"""

from google.colab import drive
drive.mount('/content/drive')

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

import pandas as pd
import tensorflow as tf
import nltk, os, re, string

import matplotlib.pyplot as plt

"""## Fetching & Exploring Dataset"""

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Belajar Pengembangan Machine Learning/backloggd_games.csv')
df.head()

df.info()

df.shape

df.Rating.value_counts()

df.Genres.value_counts()

"""# **Preprocessing Text**

Remove useless features
"""

cols_to_drop = ['Unnamed: 0', 'Release_Date',
                'Plays', 'Playing',
                'Backlogs', 'Wishlist',
                'Lists', 'Reviews']

df_new = df.drop(cols_to_drop, axis=1)

df_new.head()

df_new.info()

"""From the data.info() output, the Summary column has 55,046 non-null values and the Rating column has 25,405 non-null values, while the other columns (Title, Developers, Platforms, and Genres) all have 60,000 non-null values"""

df_new.sample(3)

df_new.Summary

"""## Download wordnet dan stopwords"""

nltk.download('wordnet')
nltk.download('stopwords')

"""## Lower-case all characters"""

df_new.Title = df_new.Title.apply(lambda x: x.lower())
df_new.Developers = df_new.Developers.apply(lambda x: x.lower())
df_new.Summary = df_new.Summary.fillna('').apply(lambda x: x.lower())
df_new.Platforms = df_new.Platforms.apply(lambda x: x.lower())
df_new.Genres = df_new.Genres.apply(lambda x: x.lower())

"""## Delete functions"""

def cleaner(data):
    return(data.translate(str.maketrans('','', string.punctuation)))
    df_new.Title = df_new.Title.apply(lambda x: cleaner(x))
    df_new.Developers = df_new.Developers.apply(lambda x: lem(x))
    df_new.Summary = df_new.Summary.apply(lambda x: lem(x))
    df_new.Platforms = df_new.Platforms.apply(lambda x: lem(x))
    df_new.Genres = df_new.Genres.apply(lambda x: lem(x))

"""## Lematization"""

lemmatizer = WordNetLemmatizer()
def lem(data):
    pos_dict = {'N': wn.NOUN, 'V': wn.VERB, 'J': wn.ADJ, 'R': wn.ADV}
    return(' '.join([lemmatizer.lemmatize(w,pos_dict.get(t, wn.NOUN)) for w,t in nltk.pos_tag(data.split())]))
    df_new.Title = df_new.Title.apply(lambda x: lem(x))
    df_new.Developers = df_new.Developers.apply(lambda x: lem(x))
    df_new.Summary = df_new.Summary.apply(lambda x: lem(x))
    df_new.Platforms = df_new.Platforms.apply(lambda x: lem(x))
    df_new.Genres = df_new.Genres.apply(lambda x: lem(x))

"""## Delete Numbers"""

def rem_numbers(data):
    return re.sub('[0-9]+','',data)
    df_new['Title'].apply(rem_numbers)
    df_new['Developers'].apply(rem_numbers)
    df_new['Summary'].apply(rem_numbers)
    df_new['Platforms'].apply(rem_numbers)
    df_new['Genres'].apply(rem_numbers)

"""## Delete Stopword"""

st_words = stopwords.words()
def stopword(data):
    return(' '.join([w for w in data.split() if w not in st_words ]))
    df_new.Title = df_new.Title.apply(lambda x: stopword(x))
    df_new.Developers = df_new.Developers.apply(lambda x: lem(x))
    df_new.Summary = df_new.Summary.apply(lambda x: lem(x))
    df_new.Platforms = df_new.Platforms.apply(lambda x: lem(x))
    df_new.Genres = df_new.Genres.apply(lambda x: lem(x))

"""### **Summary column**

Nilai NaN pada kolom atau baris relatif besar, maka untuk mengisi missing values dengan angka atau strategy akan lebih tepat dengan menggunakan 'most_frequent' (nilai yang paling sering muncul)
"""

imputer = SimpleImputer(strategy='most_frequent')
target = df_new['Summary']
features = df_new.drop('Summary', axis=1)

# Melakukan imputasi pada dataset features
features_imputed = pd.DataFrame(imputer.fit_transform(features), columns=features.columns)
df_imputed = pd.concat([features_imputed, target], axis=1)

df_imputed.info()

"""### **Rating column**"""

imputer = SimpleImputer(strategy='most_frequent')
target = df_imputed['Rating']
features = df_imputed.drop('Rating', axis=1)

features_imputed = pd.DataFrame(imputer.fit_transform(features), columns=features.columns)
df_final = pd.concat([features_imputed, target], axis=1)

# df_final = data.dropna(subset=['Summary'])
# df_final = data.dropna(subset=['Rating'])

df_final.info()

df_final.sample(5)

df_final.Rating

"""Create 'positive', 'neutral' and 'negative' columns/labels based on Rating conditions"""

df_final['label_rating'] = df_final['Rating'].apply(
    lambda x: ('positive' if x >= 4 else ('neutral' if x >= 3 else 'negative'))
)

df_final.label_rating

df_final.loc[df_final['label_rating'] == 'positive']

df_final.loc[df_final['label_rating'] == 'neutral']

df_final.loc[df_final['label_rating'] == 'negative']

df_final = df_final.drop('Rating', axis=1)
df_final.head(2)

"""# **Feature Extraction**

Performs a one-hot-encoding process
"""

category = pd.get_dummies(df_final.label_rating)
df_new_final = pd.concat([df_final, category], axis=1)
df_new_final = df_new_final.drop(columns='label_rating')
df_new_final.head(3)

df_new_final.info()

combined_atribut = df_new_final['Title'].values + '' + df_new_final['Developers'].values+ '' + df_new_final['Platforms'].values	+ '' + df_new_final['Genres'].values + '' + df_new_final['Summary'].values
combined_atribut

# Selects all rows and takes columns starting from the 5th index to the end
label = df_new_final.iloc[:, 5:]
label

# Converts the result to a numpy array
label.values

"""# **Building a Classification Model**

Dividing data for training and data for testing
"""

atribut_latih, atribut_test, label_latih, label_test = train_test_split(
      combined_atribut, label, shuffle=True, test_size=0.2
    )

print('Total atribut_latih:', len(atribut_latih))
print('Total atribut_test:', len(atribut_test))

"""*   Turning every word in our dataset into a numeric number with the Tokenizer function
*   Then convert each sample to sequence


"""

tokenizer = Tokenizer(num_words=5000, oov_token='x')
tokenizer.fit_on_texts(atribut_latih)
# tokenizer.fit_on_texts(atribut_test)

sekuens_latih = tokenizer.texts_to_sequences(atribut_latih)
sekuens_test = tokenizer.texts_to_sequences(atribut_test)

padding_latih = pad_sequences(sekuens_latih)
padding_test = pad_sequences(sekuens_test)

maxlen = max(len(sequence) for sequence in sekuens_latih + sekuens_test)
print("Panjang maksimum: ", maxlen)

# padding_latih = pad_sequences(sekuens_latih, padding='post',
#                               maxlen=maxlen, truncating='post')
# padding_test = pad_sequences(sekuens_latih, padding='post',
#                              maxlen=maxlen, truncating='post')

"""# **Model Evaluation**"""

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=5000, output_dim=16),
    # Menggunakan Bidirectional LSTM
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(
    loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy']
)

model.summary()

"""## Callback"""

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.92 and logs.get('val_accuracy')>0.92):
      self.model.stop_training = True
      print('\n\nCallback called --- Done training!')
      print(" Accuracy above 90% ".center(33, '-'), '\n\n')
callbacks = myCallback()

"""## Models Training"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# history = model.fit(
#     padding_latih,
#     label_latih,
#     epochs=50,
#     validation_data=(padding_test, label_test),
#     verbose=2,
#     batch_size=256,
#     shuffle=True,
#     validation_steps=30,
#     callbacks=[callbacks]
# )

"""## Accuracy Graph"""

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Accuracy Graph')
plt.ylabel('Accuracy Value')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""## Loss Graph"""

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss Graph')
plt.ylabel('Loss Value')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()