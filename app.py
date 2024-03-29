from flask import Flask, request, Response, render_template
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Regexp
import re

class WordForm(FlaskForm):
    avail_letters = StringField("Letters", validators= [
        Regexp(r'^[a-z]+$', message="must contain letters only"),
    ])
    #word length
    word_length = SelectField("Length (optional)", choices=[(0, 'No thanks'), (3, '3'),(4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], validators=None, coerce=int)
    #pattern
    pattern_word = StringField("Pattern choice (optional)", validators=[Regexp(r'^[a-z.""]+$', message="must contain letters or dots '.' only")
    ])

    submit = SubmitField("Go")



csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)

@app.route('/index')
def index():
    form = WordForm()
    return render_template("index.html", form=form)


@app.route('/words', methods=['POST','GET'])
def letters_2_words():

    form = WordForm()
    # when button is clicked
    if form.validate_on_submit():
        # extract data from form & transform variable
        letters = str(form.avail_letters.data)
        length = int(form.word_length.data)
        wordPattern= str(form.pattern_word.data)
        patternLength = len(wordPattern)
        letterLength = len(letters)

    else:
        return render_template("index.html", form=form)

    with open('sowpods.txt') as f:
        #words from sowpods list
        good_words = set(x.strip().lower() for x in f.readlines())

     # if no letters & no pattern
    #if (letters == '' and wordPattern =='') :
    #    return render_template("index.html", form=form)
     # length doesn't equal pattern length
#    if (length != len(wordPattern)):
#        return render_template("index.html", form=form)

    word_set = set()
    for l in range(3,len(letters)+1):
        for word in itertools.permutations(letters,l):
            w = "".join(word)
        #check here to see if pattern is full but letters is blank



            if w in good_words:
                #length condition (works)
                if(length == 0):
                    if(patternLength ==0):
                        word_set.add(w)
                    elif(patternLength !=0):
                        #match pattern
                        j=0
                        while(j<patternLength):
                            if(w[j] == wordPattern[j] or wordPattern[j] == '.'):
                                j+=1
                                continue
                            elif(w[j] != wordPattern[j] and wordPattern[j] != '.'):
                                word_set.add(w)
                                break
                            if(j == (patternLength-1)):
                                word_set.add(w)

                elif(length != 0):
                    if(patternLength !=0):
                        if(patternLength != length):
                            return render_template("index.html", form=form)
                            #error
                        elif(patternLength == length and len(w) == length):
                            #match pattern
                            j=0
                            while(j<patternLength):
                                if(w[j] == wordPattern[j] or wordPattern[j] == '.'):
                                    j+=1
                                    continue
                                elif(w[j] != wordPattern[j] and wordPattern[j] != '.'):
                                    word_set.add(w)
                                    break
                                if(j == (patternLength-1)):
                                    word_set.add(w)



                    elif(patternLength ==0):
                        if(len(w) == length):
                            word_set.add(w)




    return render_template('wordlist.html',
        wordlist=sorted(word_set),
        name="Suriya Murthy")




@app.route('/proxy')
def proxy():
    result = requests.get(request.args['url'])
    resp = Response(result.text)
    resp.headers['Content-Type'] = 'application/json'
    return resp
