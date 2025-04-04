import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import tensorflow as tf
import random
import json
import pickle
import tflearn

with open('C:/Users/Abhay/Documents/GitHub/Health_chatbot/intents.json') as f:
    data = json.load(f)

# Initialize variables
words = []
labels = []
docs_x = []
docs_y = []
context = {}

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])  

words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    wrds = [stemmer.stem(w) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)

tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")

# Function to handle context
def update_context(tag, user_input):
    if tag not in context:
        context[tag] = []
    context[tag].append(user_input)

def get_context(tag):
    if tag in context:
        return context[tag]
    return None

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

# Main chat function
def chat():
    print("\033[1;31m Start talking with the bot!, Type quit when you want to quit")
    while True:
        inp = input("\033[1;31m You: ")
        if inp.lower() == "quit":
            break

        # Predict the intent of the input
        results = model.predict([bag_of_words(inp, words)])
        results_index = np.argmax(results)
        tag = labels[results_index]

        # Update context based on input and tag
        update_context(tag, inp)
        user_context = get_context(tag)

        # Retrieve responses from the corresponding intent
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

                # Generate colored responses and print them
                response_list = nltk.sent_tokenize(str(responses[0]))
                colors = [31, 32, 33, 34, 35]

                for i in range(len(response_list)):
                    color_index = i % len(colors)
                    print(f'\033[1;{colors[color_index]}m {response_list[i]:<12s}\n')

                # Print context if available
                if user_context:
                    print(f"\033[1;32mContext for {tag}: {user_context}\n")

chat()

#colab link:  https://colab.research.google.com/drive/1voxCwaTDH1kmf4_eEjTLp7cnjy-ozRQc?usp=sharing

#use college mail ID to access.
