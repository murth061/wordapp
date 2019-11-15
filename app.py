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
    word_length = SelectField("Length of Word (optional)", choices=[(0,"nah"),(3,"3"),(4,"4"),(5,"5"),(6,"6"),(7,"7"),(8,"8"),(9,"9"),(10,"10")
    ])
    #pattern
    pattern_word = StringField("Pattern choice (optional)", validators=[Regexp(r'^[a-z.]+$', message="must contain letters or dots '.' only")
    ])
    # consider importing optional ^

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
        letters = form.avail_letters.data
        length = int(form.word_length.data)
        wordPattern=form.pattern_word.data

    else:
        return render_template("index.html", form=form)

    with open('sowpods.txt') as f:
        #words from sowpods list
        good_words = set(x.strip().lower() for x in f.readlines())

     # if no letters & no pattern
     if letters == '' and wordPattern =='' :
         return render_template("index.html", form=form)
     # if length doesn't equal pattern length
     if length != len(wordPattern):
         return render_template("index.html", form=form)

    word_set = set()
    for l in range(3,len(letters)+1):
        for word in itertools.permutations(letters,l):
            w = "".join(word)
            #match condition
            if w in good_words:
                #length condition
               if length != 0:
                   if len(w) == length:
                        #pattern condition (pending)

                        word_set.add(w)

    return render_template('wordlist.html',
        wordlist=sorted(word_set),
        name="CS4131")




@app.route('/proxy')
def proxy():
    result = requests.get(request.args['url'])
    resp = Response(result.text)
    resp.headers['Content-Type'] = 'application/json'
    return resp
