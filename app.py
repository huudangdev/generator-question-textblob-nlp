
from flask import Flask, render_template, request
app = Flask(__name__)
from textblob import TextBlob
import nltk
from textblob import Word
import sys


def parse(string):
   """
   Parse a paragraph. Devide it into sentences and try to generate quesstions from each sentences.
   """
   data = []
   try:
      txt = TextBlob(string)
      # Each sentence is taken from the string input and passed to genQuestion() to generate questions.
      for sentence in txt.sentences:
         question = genQuestion(sentence)
         if question != None:
            data.append(question)
      return data
   except Exception as e:
      raise e



def genQuestion(line):

   """
   outputs question from the given text
   """
   answer = line
   if type(line) is str:
      line = TextBlob(line) # Create object of type textblob.blob.TextBlob

   bucket = {}               # Create an empty dictionary
   for i,j in enumerate(line.tags):  # line.tags are the parts-of-speach in English
      if j[1] not in bucket:
         bucket[j[1]] = i  # Add all tags to the dictionary or bucket variable
    
   if verbose:               # In verbose more print the key,values of dictionary
      print('\n','-'*20)
      print(line ,'\n')  
      print("TAGS:",line.tags, '\n')  
      print(bucket)
    
   question = ''            # Create an empty string 

    # These are the english part-of-speach tags used in this demo program.
    #.....................................................................
    # NNS     Noun, plural
    # JJ  Adjective 
    # NNP     Proper noun, singular 
    # VBG     Verb, gerund or present participle 
    # VBN     Verb, past participle 
    # VBZ     Verb, 3rd person singular present 
    # VBD     Verb, past tense 
    # IN      Preposition or subordinating conjunction 
    # PRP     Personal pronoun 
    # NN  Noun, singular or mass 
    #.....................................................................

    # Create a list of tag-combination

   l1 = ['NNP', 'VBG', 'VBZ', 'IN']
   l2 = ['NNP', 'VBG', 'VBZ']
    

   l3 = ['PRP', 'VBG', 'VBZ', 'IN']
   l4 = ['PRP', 'VBG', 'VBZ']
   l5 = ['PRP', 'VBG', 'VBD']
   l6 = ['NNP', 'VBG', 'VBD']
   l7 = ['NN', 'VBG', 'VBZ']

   l8 = ['NNP', 'VBZ', 'JJ']
   l9 = ['NNP', 'VBZ', 'NN']

   l10 = ['NNP', 'VBZ']
   l11 = ['PRP', 'VBZ']
   l12 = ['NNP', 'NN', 'IN']
   l13 = ['NN', 'VBZ']

   l14 = ['DT', 'NNP', 'VBZ', 'JJ', 'IN']


    # With the use of conditional statements the dictionary is compared with the list created above

   if all(key in bucket for key in l14): #'NN', 'VBZ' in sentence.
      question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + ' ' + line.words[bucket['JJ']] + ' ' + line.words[bucket['IN']] + '?'

   elif all(key in  bucket for key in l1): #'NNP', 'VBG', 'VBZ', 'IN' in sentence.
      question = 'What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NNP']]+ ' '+ line.words[bucket['VBG']] + '?'

    
   elif all(key in  bucket for key in l2): #'NNP', 'VBG', 'VBZ' in sentence.
      question = 'What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NNP']] +' '+ line.words[bucket['VBG']] + '?'

    
   elif all(key in  bucket for key in l3): #'PRP', 'VBG', 'VBZ', 'IN' in sentence.
      question = 'What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['PRP']]+ ' '+ line.words[bucket['VBG']] + '?'

    
   elif all(key in  bucket for key in l4): #'PRP', 'VBG', 'VBZ' in sentence.
      question = 'What ' + line.words[bucket['PRP']] +' '+  ' does ' + line.words[bucket['VBG']]+ ' '+  line.words[bucket['VBG']] + '?'

   elif all(key in  bucket for key in l7): #'NN', 'VBG', 'VBZ' in sentence.
      question = 'What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NN']] +' '+ line.words[bucket['VBG']] + '?'

   elif all(key in bucket for key in l8): #'NNP', 'VBZ', 'JJ' in sentence.
      question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + '?'

   elif all(key in bucket for key in l9): #'NNP', 'VBZ', 'NN' in sentence
      question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + '?'

   elif all(key in bucket for key in l11): #'PRP', 'VBZ' in sentence.
      if line.words[bucket['PRP']] in ['she','he']:
          question = 'What' + ' does ' + line.words[bucket['PRP']].lower() + ' ' + line.words[bucket['VBZ']].singularize() + '?'

   elif all(key in bucket for key in l10): #'NNP', 'VBZ' in sentence.
      question = 'What' + ' does ' + line.words[bucket['NNP']] + ' ' + line.words[bucket['VBZ']].singularize() + '?'

   elif all(key in bucket for key in l13): #'NN', 'VBZ' in sentence.
      question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NN']] + '?'
    
 

    # When the tags are generated 's is split to ' and s. To overcome this issue.
   if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
      question = question.replace(" ’ ","'s ")

   # Print the genetated questions as output.
   if question != '':
      print('\n', 'Question: ' + question )

      return {'question':question,'answer':answer}
      # print('\n', 'Question: ' + question )
   

@app.route('/')
def student():
   return render_template('form.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   global verbose 
   verbose = False
   text_input = ''
   if request.method == 'POST':
      result = request.form
      for key, value in result.items():
         text_input += value
      data = (parse(text_input))
     
      return render_template("result.html",result = data)
   else:
      return render_template('form.html')


if __name__ == '__main__':
   app.run(debug = True)