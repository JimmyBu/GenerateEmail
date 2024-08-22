import random
import smtplib
from email.mime.text import MIMEText
from urllib.request import urlopen


def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum


def retrieveRandomWord(wordList):
    randIndex = random.randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word


def buildWordDict(text):
    # get rid of \n and "
    text = text.replace("\n", " ")
    text = text.replace("\"", "")

    # ensure all punctuations are not eliminated
    punctuation = [',', '.', ';', ':']
    for symbol in punctuation:
        text = text.replace(symbol, " " + symbol + " ")

    words = text.split(" ")

    # get rid of empty words
    words = [word for word in words if word != ""]
    wordDict = {}
    for i in range(1, len(words)):
        if words[i - 1] not in wordDict:
            # create a new dictionary for the word
            wordDict[words[i - 1]] = {}
        if words[i] not in wordDict[words[i - 1]]:
            wordDict[words[i - 1]][words[i]] = 0
        wordDict[words[i - 1]][words[i]] = wordDict[words[i - 1]][words[i]] + 1
    return wordDict

text = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')
wordDict = buildWordDict(text)

length = 100
chain = ""
currentWord = "I"
for i in range(0, length):
    chain += currentWord+" "
    currentWord = retrieveRandomWord(wordDict[currentWord])


msg = MIMEText(chain)
msg['Subject'] = "A letter from Jimmy"
msg['From'] = "jimmy.python@outlook.com"
msg['To'] = "hem26@mcmaster.ca"
s = smtplib.SMTP('smtp-mail.outlook.com', 587)
s.set_debuglevel(1)
s.ehlo()
s.starttls()
s.login("jimmy.python@outlook.com", "12345qwert")
s.send_message(msg)
s.quit()
