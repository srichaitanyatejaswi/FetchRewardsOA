import re
import math
from flask import Flask, request, render_template

split_words = re.compile(r"\w+")

def vectors(sentence):
    '''Vectors Function takes a raw text as input from user and
    gives tokens/words with their count of occurences.'''
    sentence = sentence.lower()
    x = 0
    new_sentence = ""
    while x < len(sentence):
        if sentence[x].isalpha():
            new_sentence += sentence[x]
        elif sentence[x] == " ":
            new_sentence += sentence[x]
        x += 1
    tokens = split_words.findall(new_sentence) #Breaks a line into words.
    dictionary = {}
    for i in tokens:
        if i not in dictionary:
            dictionary[i] = 1
        else:
            dictionary[i] += 1
    return dictionary

def cosine_similarity(sent1, sent2):
    ''' cosine similarity function takes two inputs (two tokenized
    sentences with their vectors) and calculates the cosine similarity
    between those vectors'''
    common_words = set(sent1.keys())&set(sent2.keys())
    numer_sum_a_b = sum([sent1[i] * sent2[i] for i in common_words])
    denom_sum_a = sum([sent1[i] ** 2 for i in list(sent1.keys())])
    denom_sum_b = sum([sent2[i] ** 2 for i in list(sent2.keys())])
    denom_a_b = math.sqrt(denom_sum_a) * math.sqrt(denom_sum_b)
    similarity = float(numer_sum_a_b/denom_a_b)
    return similarity

''' TFIDF with Cosine Similarity'''

def vectorstfidf(sentence):
    '''Vectors Function takes a raw text as input from user and
    gives tokens/words with their count of occurences.'''
    sentence = sentence.lower()
    x = 0
    new_sentence = ""
    while x < len(sentence):
        if sentence[x].isalpha():
            new_sentence += sentence[x]
        elif sentence[x] == " ":
            new_sentence += sentence[x]
        x += 1
    tokens = split_words.findall(new_sentence)  # Breaks a line into words.
    dictionary = {}
    for i in tokens:
        if i not in dictionary:
            dictionary[i] = 1
        else:
            dictionary[i] += 1
    return dictionary

def TFDict(sentence):
    """ Returns a tf dictionary for each sentence whose keys are all
    the unique words in the sentence and whose values are their
    corresponding tf.
    """
    # Counts the number of times the word appears in sentence
    TFDict = {}
    for word in vectorstfidf(sentence):
        if word in TFDict:
            TFDict[word] += 1
        else:
            TFDict[word] = 1
    # Computes tf for each word
    for word in TFDict:
        TFDict[word] = TFDict[word] / len(sentence)
    return TFDict

def CountDict(text):
    """ Returns a dictionary whose keys are all the unique words in
    the dataset
    """
    countDict = {}
    # Run through each sentence's tf dictionary and increment countDict's (word, sentence) pair
    for sentence in text:
        sentence = sentence.lower()
        x = 0
        new_sentence = ""
        while x < len(sentence):
            if sentence[x].isalpha():
                new_sentence += sentence[x]
            elif sentence[x] == " ":
                new_sentence += sentence[x]
            x += 1
        for word in split_words.findall(new_sentence.lower()): # Breaks a line into words.
            if word in countDict:
                countDict[word] += 1
            else:
                countDict[word] = 1
    return countDict

def IDFDict(countDict,text):
    """ Returns a dictionary whose keys are all the unique words in the
    dataset and whose values are their corresponding idf.
    """
    idfDict = {}
    for word in countDict:
        idfDict[word] = math.log(len(text) / countDict[word])
    return idfDict

def TFIDFDict(TFDict, idfDict):
    """ Returns a dictionary whose keys are all the unique words in the
    sentencee and whose values are their corresponding tfidf.
    """
    TFIDFDict = {}
    # For each word in the sentence, we multiply its tf and its idf.
    for word in TFDict:
        TFIDFDict[word] = TFDict[word] * idfDict[word]
    return TFIDFDict

def TFIDFVector(sentence, wordDict):
    tfidfVector = [0.0] * len(wordDict)
    '''For each unique word, if it is in the sentence, store its TF-IDF value.'''
    for i, word in enumerate(wordDict):
        if word in sentence:
            tfidfVector[i] = sentence[word]
    return tfidfVector

def cosine_similaritytfidf(vec_1, vec_2):
    "compute cosine similarity of vec_1 to vec_2: (vec_1 dot vec_2)/{||vec_1||*||vec_2||)"
    denom_vec1, numerator, denom_vec2 = 0, 0, 0
    for i in range(len(vec_1)):
        x = vec_1[i]
        y = vec_2[i]
        denom_vec1 += x * x
        denom_vec2 += y * y
        numerator += x * y
        denom = denom_vec1*denom_vec2
    if denom ==0 or numerator == 0:
        return "TF-IDF Cosine Similarity Fails in this case as either TF or IDF are zero "
    return "TF-IDF Cosine similarity is {:.3f}".format(numerator / math.sqrt(denom))


app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods=["GET", "POST"])
def textsimilarity():
    if request.method == "POST":
        # getting 1st sentence input with name = sentence1 in HTML form
        sentence1 = request.form.get("sentence1")
        # getting 2nd sentence with name = sentence2 in HTML form
        sentence2 = request.form.get("sentence2")
        text1 = str(sentence1)
        text2 = str(sentence2)
        sent_to_vectors1 = vectors(text1)
        sent_to_vectors2 = vectors(text2)
        cos_sim = cosine_similarity(sent_to_vectors1, sent_to_vectors2)

        ##Appending two texts into a list
        text = []
        text.append(text1)
        text.append(text2)

        # Stores the words count dictionary
        countDict = CountDict(text)

        #Stores the idf dictionary
        idfDict = IDFDict(countDict, text)

        # Stores the TF-IDF dictionaries
        tfidfDict = [TFIDFDict(vectorstfidf(sentence), idfDict) for sentence in text]

        wordDict = sorted(countDict.keys())

        tfidfVector = [TFIDFVector(sentence, wordDict) for sentence in tfidfDict]

        vec_1, vec_2 = tfidfVector[0], tfidfVector[1]

        cos_simtfidf = cosine_similaritytfidf(vec_1, vec_2)

        return "Cosine Similarity between Two texts is: {:.3f}  {}".format(cos_sim,cos_simtfidf)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)