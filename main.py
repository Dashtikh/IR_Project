import requests
import ssl
import wikipedia
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import math

wikipedia.set_lang('en')
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
# nltk.download()
listOfStemmed = []
numOfDoc = int(input("Insert the Number of docs: "))
tokens = []
indexing = {}
tfidf = {}
listOfTfIdf = []
stopWords = [".", 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
             "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
             'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
             'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were',
             'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
             'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
             'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up',
             'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
             'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
             'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
             'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
             "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
             'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",
             'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn',
             "wouldn't", "(", ")", "[", "]", "{", "}", "&", "$", ",", ".", ":", ";", "%", "''", "'s"]
repository = []
listOfTitles = []
ps = SnowballStemmer("english")
for i in range(0, numOfDoc):
    url = 'https://en.wikipedia.org/wiki/Special:Random'

    reqs = requests.get(url)

    soup = BeautifulSoup(reqs.text, 'html.parser')

    for title in soup.find_all('title'):
        docTitle = title.get_text()

    docTitle = docTitle.replace(" - Wikipedia", "")
    print(docTitle)
    listOfTitles.append(docTitle)
    docContent = wikipedia.summary(docTitle)
    docContent = docContent.lower()
    repository.append(docContent)
    print(repository)

noSW = []

for j in range(0, numOfDoc):
    stringToToken = word_tokenize(repository[j])
    for k in range(0, len(stringToToken)):
        tokenToStem = ps.stem(stringToToken[k])
        if tokenToStem in stopWords:
            pass
        else:
            noSW.append(tokenToStem)
    listOfStemmed.append(noSW)
    noSW = []
    stringToToken = []
print(listOfStemmed)
for m in range(0, numOfDoc):
    for n in range(0, len(listOfStemmed[m])):
        if listOfStemmed[m][n] in tokens:
            pass
        else:
            tokens.append(listOfStemmed[m][n])
tokens.sort()

i = 0
j = 0
# boolean

zeroAndOne = []
for i in range(0, len(tokens)):
    # print(tokens[i] + ": ", end=' ')
    for j in range(0, len(listOfStemmed)):
        if tokens[i] in listOfStemmed[j]:
            # print("1", end=' ')
            zeroAndOne.append(1)
        else:
            # print("0", end=' ')
            zeroAndOne.append(0)
    # print("\n")
    indexing[tokens[i]] = zeroAndOne
    zeroAndOne = []

print(indexing)
# tf-idf
i = 0
j = 0
k = 0
tf = 0
idf = 0
for i in range(0, len(tokens)):
    # print(tokens[i]+":", end=" ")
    for p in range(0, len(listOfStemmed)):
        if tokens[i] in listOfStemmed[p]:
            idf = idf + 1
    for j in range(0, len(listOfStemmed)):
        for k in range(0, len(listOfStemmed[j])):
            if tokens[i] == listOfStemmed[j][k]:
                tf = tf + 1
        # print(F"{tf} - {idf}", end=" ")
        listOfTfIdf.append(math.log10(1 + tf) * math.log10(numOfDoc / idf))
        tf = 0
    tf = 0
    idf = 0
    tfidf[tokens[i]] = listOfTfIdf
    listOfTfIdf = []

print(tfidf)

print("insert your query: ")
query = input()
finalQuery = []
queryToToken = word_tokenize(query)
for k in range(0, len(queryToToken)):
    queryToStem = ps.stem(queryToToken[k])
    if queryToStem in stopWords:
        pass
    else:
        finalQuery.append(queryToStem)
print(finalQuery)
hasIndexingQuery = []
listAvailableTokens = []
hasCounter = 0
multiplyList = []
availableintokens = []
for y in range(0, numOfDoc):
    multiplyList.append(1)
print(multiplyList)
menu = int(input("boolean or TF-IDF? "))
if menu == 1:
    for l in range(0, len(finalQuery)):
        if finalQuery[l] in indexing:
            # print("key exists!")
            hasCounter = hasCounter + 1
            hasIndexingQuery.append(1)
            availableintokens.append(finalQuery[l])
        else:
            # print("does not exist!")
            hasIndexingQuery.append(0)
    j = 0
    print(availableintokens)
    for j in range(0, len(hasIndexingQuery)):
        if hasIndexingQuery[j] == 1:
            print(indexing[finalQuery[j]])
            listAvailableTokens.append(indexing[finalQuery[j]])
        else:
            pass
    print(listAvailableTokens)
    for o in range(0, hasCounter):
        for e in range(0, numOfDoc):
            multiplyList[e] = multiplyList[e] * listAvailableTokens[o][e]

    print(multiplyList)
    booleanFlag = False
    for y in range(0, len(multiplyList)):
        if multiplyList[y] == 1:
            booleanFlag = True
            print(listOfTitles[y])

    if not booleanFlag:
        print("There is no related doc!")
elif menu == 2:
    hasCounter = 0
    hasIndexingQuery = []
    availableintokens = []
    sumList = []
    sortedSumList = []
    for s in range(0, len(finalQuery)):
        if finalQuery[s] in tfidf:
            # print("key exists!")
            hasCounter = hasCounter + 1
            hasIndexingQuery.append(1)
            availableintokens.append(finalQuery[s])
        else:
            # print("does not exist!")
            hasIndexingQuery.append(0)
    j = 0
    for j in range(0, len(hasIndexingQuery)):
        if hasIndexingQuery[j] == 1:
            print(tfidf[finalQuery[j]])
            listAvailableTokens.append(tfidf[finalQuery[j]])
        else:
            pass
    print(listAvailableTokens)
    for b in range(0, numOfDoc):
        sumList.append(0)
    for r in range(0, hasCounter):
        for t in range(0, numOfDoc):
            sumList[t] = sumList[t] + listAvailableTokens[r][t]
    print(sumList)
    for w in range(0, numOfDoc):
        sortedSumList.append(sumList[w])
    sortedSumList.sort(reverse=True)
    print(sortedSumList)
    for u in range(0, numOfDoc):
        if sortedSumList[u] != 0.0:
            for g in range(0, numOfDoc):
                if sortedSumList[u] == sumList[g]:
                    print(listOfTitles[g])
                    sumList[g] = 0.0
                    break
                else:
                    pass
        else:
            pass
