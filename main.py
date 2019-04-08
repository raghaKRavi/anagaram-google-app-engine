import os
import jinja2
import webapp2
import logging
from google.appengine.api import users

# from google.appengine.api import users
from google.appengine.ext import ndb

# from myuser import MyUser
from WordList import WordList

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape = True
)

class MainPage(webapp2.RequestHandler):
    def get(self):

        def createLexicoGraphicalSort(word):
            sortedWord = sorted(word)
            lexicoKey = ""
            for letter in sortedWord:
                lexicoKey += letter
            logging.info(lexicoKey)
            return lexicoKey

        self.response.headers['Content-Type']='text/html'

        userId = users.get_current_user().user_id()

        key = ndb.Key('WordList',userId)
        wordList = key.get()
        if wordList == None:
            wordList = WordList(id=userId)
            wordList.put()

        wordDict = dict()

        for word in wordList.words:
            word = str(word)
            sortedKey = str(createLexicoGraphicalSort(word))
            if sortedKey in wordDict:
                wordDict[sortedKey].append(word)
                continue
            wordDict[sortedKey] = []
            wordDict[sortedKey].append(word)

        lengths = [len(v) for v in wordDict.values()]

        logging.info("lenght : ", lengths)

        logging.info(wordDict)

        # for j in listOfWords:
        #     y = sorted(j)
        #     lexicoList.append(y)
        #
        # # tupleValue = tuple(lexicoList)
        # #
        # tupleValue = [tuple(x) for x in lexicoList]
        #
        # keyExists = False
        # for key in dictionary:
        #     if key == :
        #         keyExists = True
        #         self.redirect('/error')
        #
        # if not keyExists:
        #     dictionary.update(zip(tupleValue, listOfWords))
        # # dictionary = dict(zip(tupleValue, listOfWords))

        template_values = {
        'wordList': wordList,
        'listOfWords': wordDict,
        'uniqueAnagram': len(wordDict),
        'wordsInEngine': len(wordList.words),
        # 'lexicoList': lexicoList,
        # 'tupleValue': tupleValue,
        # # 'length': len(emptyList),
        # 'keyValue': dictionary
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')

        userId = users.get_current_user().user_id()

        if action == 'add':
            newWordToSave = self.request.get('list1')

            key = ndb.Key('WordList', userId)
            wordList = key.get()
            wordList.words.append(newWordToSave.lower())

            wordList.put()

            self.redirect('/')

app = webapp2.WSGIApplication([('/', MainPage)], debug = True)
