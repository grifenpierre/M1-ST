#
# * This progam uses files under the format:
# * [image]|[question]|[answer]
# * The results of the program are the analysis of the
# * data from 3 perspectives, namely the image, question
# * and answer perspective. One perspective show how many
# * times the item appears in the data and what items are
# * releated to it, including their occurences
#
#Base variables

cyan = ""; reset = ""; IMG = 0; Q = 1; A = 2

#Mode configuration
mode = 1; showImages = True; showAnwsers = True; showQuestions = True; printDataResults = True; demo = 0
#Imported libraries
import nltk, re, gensim, collections
print("\n__________________________________________________\n")
#The class for global variables which hold the resulted data
class subList:
    def __init__(self, dataval=None):
        self.count = []
        self.data = []

class globalList:
    def __init__(self, dataval=None):
        self.byImage = [] #unique data with counter sorted by Image
        self.sizeByImage = []
        self.byQuestion = [] #unique data with counter sorted by Question
        self.sizeByQuestion = []
        self.byAnswer = [] #unique data with counter sorted by Answer
        self.sizeByAnswer = []

#Global variables for the resulted data
gAnswers = globalList(); gQuestions = globalList(); gImages = globalList()

# Function for loading the data
def loadData(fileNames):
    myData = [[' '.join(val.split()) for val in line.strip('(').strip(')').split('|')] for line in open(fileNames[0],'r').readlines()] #strip('\n').strip('\t').
    for i in range(1,len(fileNames),1):
        myData.extend([[' '.join(val.split()) for val in line.split('|')] for line in open(fileNames[i],'r').readlines()])
    return myData

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# * * * * * Functions dealing with soring the data  * * * * * *
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

#Functions dealing with data sorted by Questions
def cleanList(L):
    cleanedList = []
    for i in range(0,len(L),1):
        local = L[i]
        occurences = 1
        if local not in [item[1] for item in cleanedList]:
            for j in range(i+1,len(L),1):
                if L[i] == L[j]:
                    occurences += 1
            cleanedList.append([occurences,local])
    return cleanedList
def sortByImage(data):
    global gImages, gQuestions, gAnswers
    for i in range(0,len(data),1):
        repeats = 1
        LocalImage = data[i][IMG]
        LocalQuestions = [data[i][Q]]
        LocalAnswers = [data[i][A]]
        if LocalImage not in [item[1] for item in gImages.byImage]:
            for j in range(i+1,len(data),1):
                if data[i][IMG] == data[j][IMG]:
                    repeats += 1
                    LocalQuestions.append(data[j][Q])
                    LocalAnswers.append(data[j][A])
            gImages.byImage.append([repeats,LocalImage])
            gQuestions.byImage.append(cleanList(LocalQuestions))
            gAnswers.byImage.append(cleanList(LocalAnswers))
def sortByQuestion(data):
    global gImages, gQuestions, gAnswers
    for i in range(0,len(data),1):
        repeats = 1
        LocalImages = [data[i][IMG]]
        LocalQuestion = data[i][Q]
        LocalAnswers = [data[i][A]]
        if LocalQuestion not in [item[1] for item in gQuestions.byQuestion]:
            for j in range(i+1,len(data),1):
                if data[i][Q] == data[j][Q]:
                    repeats += 1
                    LocalImages.append(data[j][IMG])
                    LocalAnswers.append(data[j][A])
            gImages.byQuestion.append(cleanList(LocalImages))
            gQuestions.byQuestion.append([repeats,LocalQuestion])
            gAnswers.byQuestion.append(cleanList(LocalAnswers))
def sortByAnswer(data):
    global gImages, gQuestions, gAnswers
    for i in range(0,len(data),1):
        repeats = 1
        LocalImages = [data[i][IMG]]
        LocalQuestions = [data[i][Q]]
        LocalAnswer = data[i][A]
        if LocalAnswer not in [item[1] for item in gAnswers.byAnswer]:
            for j in range(i+1,len(data),1):
                if data[i][A] == data[j][A]:
                    repeats += 1
                    LocalImages.append(data[j][IMG])
                    LocalQuestions.append(data[j][Q])
            gImages.byAnswer.append(cleanList(LocalImages))
            gQuestions.byAnswer.append(cleanList(LocalQuestions))
            gAnswers.byAnswer.append([repeats,LocalAnswer])

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# * * * * * * * Post processing to get the sizes * * * * * * *
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def postProcessSizesByImage():
    global gImages, gQuestions, gAnswers
    gImages.sizeByImage = 0
    for i in range(0,len(gImages.byImage),1):
        gImages.sizeByImage += gImages.byImage[i][0]
    for i in range(0,len(gQuestions.byImage),1):
        gQuestions.sizeByImage.extend([0])
        for j in range(0,len(gQuestions.byImage[i]),1):
            gQuestions.sizeByImage[i] += gQuestions.byImage[i][j][0]
    for i in range(0,len(gAnswers.byImage),1):
        gAnswers.sizeByImage.extend([0])
        for j in range(0,len(gAnswers.byImage[i]),1):
            gAnswers.sizeByImage[i] += gAnswers.byImage[i][j][0]
def postProcessSizesByQuestion():
    global gImages, gQuestions, gAnswers
    for i in range(0,len(gImages.byQuestion),1):
        gImages.sizeByQuestion.extend([0])
        for j in range(0,len(gImages.byQuestion[i]),1):
            gImages.sizeByQuestion[i] += gImages.byQuestion[i][j][0]
    gQuestions.sizeByQuestion = 0
    for i in range(0,len(gQuestions.byQuestion),1):
        gQuestions.sizeByQuestion =  gQuestions.sizeByQuestion + gQuestions.byQuestion[i][0]
    for i in range(0,len(gAnswers.byQuestion),1):
        gAnswers.sizeByQuestion.extend([0])
        for j in range(0,len(gAnswers.byQuestion[i]),1):
            gAnswers.sizeByQuestion[i] += gAnswers.byQuestion[i][j][0]
def postProcessSizesByAnswer():
    global gImages, gQuestions, gAnswers
    for i in range(0,len(gImages.byAnswer),1):
        gImages.sizeByAnswer.extend([0])
        for j in range(0,len(gImages.byAnswer[i]),1):
            gImages.sizeByAnswer[i] += gImages.byAnswer[i][j][0]
    for i in range(0,len(gQuestions.byAnswer),1):
        gQuestions.sizeByAnswer.extend([0])
        for j in range(0,len(gQuestions.byAnswer[i]),1):
            gQuestions.sizeByAnswer[i] += gQuestions.byAnswer[i][j][0]
    gAnswers.sizeByAnswer =0
    for i in range(0,len(gAnswers.byAnswer),1):
        gAnswers.sizeByAnswer += gAnswers.byAnswer[i][0]

def postProcessSizes():
    postProcessSizesByImage()
    postProcessSizesByQuestion()
    postProcessSizesByAnswer()

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# * * * * * * * * * * * Printing functions * * * * * * * * * * 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def printByImage():
     print("Different Images:",len(gImages.byImage))
     for i in range(0,len(gImages.byImage),1):
        print(cyan, "Image: ", reset, "Times: ", gImages.byImage[i][0])
        if showImages:
            print(gImages.byImage[i][1])
        print(cyan, "Questions: ", reset, gQuestions.sizeByImage[i])
        if showQuestions:
            for j in range(0,len(gQuestions.byImage[i])):
                print(gQuestions.byImage[i][j])
        print(cyan, "Answers: ", reset, gAnswers.sizeByImage[i])
        if showAnwsers:
            for j in range(0,len(gAnswers.byImage[i]),1):
                print(gAnswers.byImage[i][j])
        print("\n")
def printByQuestion():
    print("Different questions:",len(gQuestions.byQuestion))
    for i in range(0,len(gQuestions.byQuestion),1):
        print(cyan ,"Question:", reset, "Times: ",gQuestions.byQuestion[i][0])
        if showQuestions:
            print("Q: ", gQuestions.byQuestion[i][1])
        print(cyan, "Answers: ", reset, gAnswers.sizeByQuestion[i])
        if showAnwsers:
            for j in range(0,len(gAnswers.byQuestion[i]),1):
                print(gAnswers.byQuestion[i][j])
        print(cyan, "Images: ", reset, gImages.sizeByQuestion[i]) #, gImages.byQuestion[i])
        if showImages:
            for j in range(0,len(gImages.byQuestion[i]),1):
                print(gImages.byQuestion[i][j])
        print("\n")
def printByAnswer():
    print("Different Answers:",len(gAnswers.byAnswer))
    for i in range(0,len(gAnswers.byAnswer),1):
        print(cyan, "Answer: ", reset, "Times: ", gAnswers.byAnswer[i][0])
        if showAnwsers:
            #for j in range(0,len(gAnswers.byAnswer[i]),1):
            print(gAnswers.byAnswer[i][1])
        print(cyan ,"Questions:", reset, gQuestions.sizeByAnswer[i])
        if showQuestions:
            for j in range(0,len(gQuestions.byAnswer[i])):
                print(gQuestions.byAnswer[i][j])
        print(cyan, "Images: ", reset, gImages.sizeByAnswer[i])
        if showImages:
            for j in range(0,len(gImages.byAnswer[i]),1):
                print(gImages.byAnswer[i][j])
        print("\n")

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# * * * * * * * * * * * * NLTK functions * * * * * * * * * * * 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def NLTK_stringNormalizer(text):
    return ' '.join(re.sub(r'[^a-zA-Z0-9\s]+', '', text).split()).lower()

def NLTK_textNormalizer(text):
    for i in range(0,len(text),1):
        text[i] = NLTK_stringNormalizer(text[i])
    return text

def NLTK_sentencesTokenizer(sentences): # Creates tokens from a sentence
    # Can be done either with splitting by word, or by using stop words
    # Make empty list holder for the tokens of each sentence
    sentencesTokenized = ['' for i in range(0,len(sentences))]
    # Tokenize each sentence
    for i in range(0,len(sentences)):
        sentencesTokenized[i] = nltk.tokenize.word_tokenize(sentences[i])
    return sentencesTokenized

def NLTK_removeStopWords(sentencesTokenized,banList):
    #
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(banList)
    sentencesNormalised = []
    for sentence in sentencesTokenized:
        sentencesNormalised.append([word for word in sentence if not word in stopwords])
    return sentencesNormalised


def tokenStemmer(tokenizedSentences): #Uses NLTK to stem words, either with Porter or Lancaster (agressive)
    #Must take a list of lists of strings as an argument
    # Stem the tokens of the list of lists
    for i in range(0,len(tokenizedSentences)):
        for j in range(0,len(tokenizedSentences[i])):
            tokenizedSentences[i][j] =  nltk.stem.PorterStemmer().stem(tokenizedSentences[i][j])
    return tokenizedSentences

def NLTK_tokenLemmatizer(tokenizedSentences): #Uses NLTK to stem words, either with Porter or Lancaster (agressive)
    #Must take a list of lists of strings as an argument
    # Stem the tokens of the list of lists
    for i in range(0,len(tokenizedSentences)):
        for j in range(0,len(tokenizedSentences[i])):
            tokenizedSentences[i][j] =  nltk.stem.WordNetLemmatizer().lemmatize(tokenizedSentences[i][j])
    return tokenizedSentences

def NLTK_makeWordDictionary(sentencesTokenized):
    #Make a dictionary for the words
    definitions = {}

    for sentence in sentencesTokenized:
        sentenceDef = {}
        for word in sentence:
            if word not in definitions:
                try:
                    wordNet = nltk.corpus.wordnet.synsets(word)
                    defs = []
                    for syn in wordNet:
                        defs.append(syn.definition())
                except: defs = [word]
                if len(defs) == 0: defs = [word]
                sentenceDef.update({word:defs})
        definitions.update(sentenceDef)
    return definitions

def NLTK_similarityCalculator(sentencesTokenized,definitions):
    #Calculate the number of similar words between sentences
    sentenceMatches = []
    for sentence1 in sentencesTokenized:
        for sentence2 in sentencesTokenized:
            matches = 0
            for word1 in sentence1:
                match = 0
                for word2 in sentence2:
                    for definition1 in definitions[word1]:
                        for definition2 in definitions[word2]:
                            if definition1 == definition2:
                                match = 1
                matches += match
            sentenceMatches.extend([matches])
    return sentenceMatches

def NLTK_similarityNormalizer(sentencesTokenized,sentenceMatches):
    # Normalize the similarity between sentences
    score = []
    pos = 0
    for sentence1 in sentencesTokenized:
        for sentence2 in sentencesTokenized:
            similarity = 0
            if sentenceMatches[pos] != 0:
                if len(sentence1) <= len(sentence2):
                    similarity = sentenceMatches[pos] / len(sentence2)
                else:
                    similarity = sentenceMatches[pos] / len(sentence1)
            score.extend([similarity])
            pos += 1
    return score

def sentence_SimilarityWindow(tokenizedSentences): # Returns the number of windows matches in a list of lists of sentences
    #Must take as an argument a list of lists of strings
    # Create a simple list to hold each similarity
    windowsMatch = [0 for i in range(0,len(tokenizedSentences)*len(tokenizedSentences))]
    pos = 0
    # Similarity with the window method in a crude and simple way
    for i in range(0,len(tokenizedSentences)):
        for k in range(0,len(tokenizedSentences)):
            match = 0
            for j in range(0, len(tokenizedSentences[i]) -1):
                w1 = tokenizedSentences[i][j] +' '+ tokenizedSentences[i][j +1]
                for m in range(0, len(tokenizedSentences[k]) -1):
                    w2 = tokenizedSentences[k][m] +' '+ tokenizedSentences[k][m +1]
                    if w1 == w2:
                        match += 1
            windowsMatch[pos] = match
            pos += 1
    return windowsMatch

def similarity_WindowNormalizer(tokenizedSentences,windowsMatch):
    # Turns the obtained matches from the method sentence_SimilarityWindow
    # into scores for similarity using a custom method
    # Normalize similarity
    score = []
    pos = 0
    for i in range(0,len(tokenizedSentences)):
        primaryWindowSize = len(tokenizedSentences[i]) - 1
        for j in range(0,len(tokenizedSentences)):
            secondaryWindoSize = len(tokenizedSentences[j]) - 1
            similarity = 0
            if windowsMatch[pos] != 0:
                if primaryWindowSize <= secondaryWindoSize:
                    similarity = windowsMatch[pos] / secondaryWindoSize
                else:
                    similarity = windowsMatch[pos] / primaryWindowSize
            score.extend([similarity])
            pos += 1
    return score
def gsim_getScore(sentencesTokenized):
    score = []
    dictionary = gensim.corpora.Dictionary(sentencesTokenized)
    corpus = [dictionary.doc2bow(sentence) for sentence in sentencesTokenized]
    lsi = gensim.models.LsiModel(corpus, id2word=dictionary, num_topics=2)
    index = gensim.similarities.MatrixSimilarity(lsi[corpus])
    for sentence in sentencesTokenized:
        vec_bow = dictionary.doc2bow(sentence)
        # convert the query to LSI space
        vec_lsi = lsi[vec_bow]
        # perform a similarity query against the corpus
        similarities = index[vec_lsi]
        score.extend(similarities)
    return score
def windowSmilarityMethod(sentences):    
    # Tokenize the sentences and remove extra data from them
    sentencesTokenized = tokenStemmer(NLTK_sentencesTokenizer(sentences))
    
    # Find all the matches from the data
    sentencesMatches = sentence_SimilarityWindow(sentencesTokenized)
    
    # Normalize the score in %
    score = similarity_WindowNormalizer(sentencesTokenized,sentencesMatches)

    # Print results
    pos = 0
    for i in range(0,len(sentencesTokenized)):
        print()
        print(cyan,sentences[i],reset,">>",blue,sentencesTokenized[i],reset)
        for j in range(0,len(sentencesTokenized)):
            if score[pos] > 0.8:
                print("matches:", cyan, sentencesMatches[pos], reset," score:",cyan, "%.2f" % score[pos], reset," >> '",sentences[j],"' >> ", blue, sentencesTokenized[j],reset )
            pos +=1
    
def tokenSimilarityMethod(sentences): 
    # Add extra stop words to remove
    banList = ["im","Im"]
    
    # Tokenize the sentences and remove extra data from them
    sentencesTokenized = NLTK_tokenLemmatizer(NLTK_removeStopWords(NLTK_sentencesTokenizer(sentences),banList))
    
    # Build a dictionary from all the sentences
    definitions = NLTK_makeWordDictionary(sentencesTokenized)
    
    # Add extra synonims for analysis
    extraDefinitions = {"kind":["type"],"scan":["image"],"contrast":["noncontrast"],"t1":["t2","t3","t4","flair"],
        "t2":["t1","t3","t4","flair"],"t3":["t1","t2","t4","flair"],"t4":["t2","t3","t1","flair"],"flair":["t2","t3","t1","t4"],
        "captured":["taken"]
    }
    #definitions.update(extraDefinitions)
    # Find all the matches from the data
    sentencesMatches = NLTK_similarityCalculator(sentencesTokenized,definitions)
    

    # Normalize the score in %
    score = NLTK_similarityNormalizer(sentencesTokenized,sentencesMatches)

    # Print results
    pos = 0
    for i in range(0,len(sentencesTokenized)):
        print()
        print(cyan,sentences[i],reset,">>",blue,sentencesTokenized[i],reset)
        for j in range(0,len(sentencesTokenized)):
            if score[pos] > 0.8:
                print("matches:", cyan, sentencesMatches[pos], reset," score:",cyan, "%.2f" % score[pos], reset," >> '",sentences[j],"' >> ", blue, sentencesTokenized[j],reset )
            pos +=1
    
def gsimSimilarityMethod(sentences): 
    # Add extra stop words to remove
    banList = ["im","Im"]
    
    # Tokenize the sentences and remove extra data from them
    sentencesTokenized = NLTK_tokenLemmatizer(NLTK_removeStopWords(NLTK_sentencesTokenizer(sentences),banList))
    
    # Build a dictionary from all the sentences
    definitions = NLTK_makeWordDictionary(sentencesTokenized)
    
    # Add extra synonims for analysis
    extraDefinitions = {"kind":["type"],"scan":["image"],"contrast":["noncontrast"],"t1":["t2","t3","t4","flair"],
        "t2":["t1","t3","t4","flair"],"t3":["t1","t2","t4","flair"],"t4":["t2","t3","t1","flair"],"flair":["t2","t3","t1","t4"],
        "captured":["taken"]
    }
    #definitions.update(extraDefinitions)
    # Get the score in %
    score = gsim_getScore(sentencesTokenized)
    
    # Print results
    pos = 0
    for i in range(0,len(sentencesTokenized)):
        print()
        print(cyan,sentences[i],reset,">>",blue,sentencesTokenized[i],reset)
        for j in range(0,len(sentencesTokenized)):
            if score[pos] > 0.8:
                print(" score:",cyan, "%.2f" % score[pos], reset," >> '",sentences[j],"' >> ", blue, sentencesTokenized[j],reset )
            pos +=1
    
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
# * * * * * * * * * Main section of the code * * * * * * * * *
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def main(): 
    global showImages, showQuestions, showAnwsers, mode

    path = "Training/QAPairsByCategory/"
    #files = [path + "C1_Modality_train.txt"]
    files = [path + "C1_Modality_train.txt",path + "C2_Plane_train.txt",path + "C3_Organ_train.txt",path + "C4_Abnormality_train.txt"]
    
    #print (fileNames)

    # data = [id][Q][A]
    data = loadData([files[0]])

    print("Number of lines in file: ",len(data))
    #mode = 1
    if mode == 1: #question perspective
        showImages = False ; showQuestions = True ; showAnwsers = True
        sortByQuestion(data)
        postProcessSizesByQuestion()
        if printDataResults: printByQuestion()
    elif mode == 2: #answer perspective
        showImages = False ; showQuestions = True ; showAnwsers = True
        sortByAnswer(data)
        postProcessSizesByAnswer()
        if printDataResults: printByAnswer()
    elif mode == 3: #image perspective
        showImages = False ; showQuestions = False ; showAnwsers = False
        sortByImage(data)
        postProcessSizesByImage()
        if printDataResults: printByImage()
    else: print("Undefined Mode")
    
    #print(gImages.byImage)

    for i in range(0,len(gImages.byImage)):
        if gImages.byImage[i][0] != 4:
            print(gImages.byImage[i][1])
    
    if mode == 1 and demo == 1: # NLTK implemented only with questions
        # NLTK modules

        #debug
        sentences = [
        "The sky is blue",
        "The sky is red",
        "The blue sky is up",
        "The sun in the sky is bright",
        "There is no similarity here",
        "My sky is red"
        ]

        # Put all the unique questions together to find similarities
        sentences = ['' for i in range(0,len(gQuestions.byQuestion))]
        for i in range(0,len(gQuestions.byQuestion)):
            sentences[i] =  gQuestions.byQuestion[i][1]
        
        # Normalize data
        sentences = NLTK_textNormalizer(sentences)

        #windowSmilarityMethod(sentences)
        #tokenSimilarityMethod(sentences)
        gsimSimilarityMethod(sentences)

if __name__ == "__main__":
    main()
