#Run the following command before to install the spacy large model
#!python -m spacy download en_core_web_lg

from flask import Flask, render_template, request
import json
import os
import spacy
import en_core_web_lg
import pandas as pd

from reviews_entities_json import review_entities


app=Flask(__name__)

file_name='names_entities.json'
#Checking if the names and entities have been extracted from the IMDB dataset
if file_name not in os.listdir():
    data=pd.read_csv('imdbreviews.csv')
    reviews=list(data['review'])
    nlp=en_core_web_lg.load()

    entities=review_entities(nlp)
    #Running the call function from the object of the review_entities class will create the file names_entities.json
    entities_json=entities(reviews)

#Getting our data ready
with open(file_name, 'r') as f:
    names_entities=json.load(f)
names=list(names_entities['Name'].values())
entities=list(names_entities['Entity'].values())

@app.route('/')
def main():
    return render_template('app.html')

@app.route('/send', methods=['POST'])
def send(sum=sum):
    if request.method == 'POST':
        text = request.form['text']

        if text in names:
            index=names.index(text)
            sum=text + ': ' + entities[index]
            if(entities[index]=='GPE'):
                sum=text + ': ' + 'GPE(Geo Political Location) - City/ State'
            return render_template('app.html', sum=sum)

        else:
            return render_template('app.html')


if __name__ == ' __main__':
    app.debug = True
    app.run()