#Run the following command before to install the spacy large model
#!python -m spacy download en_core_web_lg

import re
import itertools

class review_entities(object):

    def __init__(self,nlp):
        self.nlp=nlp

    def __call__(self,reviews):
        reviews=self.preprocess_data(reviews)
        self.entity_list=self.get_entities(reviews)
        name_entities_json=self.convert_to_df_save_as_json()
        return name_entities_json
    
    def preprocess_data(self, reviews):
        for i in range(len(reviews)):
            reviews[i]=re.sub(r"[^a-zA-Z0-9]+", ' ', reviews[i])
            reviews[i]=re.sub(r'^https?:\/\/.*[\r\n]*', '', reviews[i], flags=re.MULTILINE)
        return reviews
    
    def get_entities(self, reviews):
        self.entity_list=[]
        for review in reviews:
            doc=nlp(review)
            for ent in doc.ents:
                if(ent.label_=='PERSON' or ent.label_=='GPE'):
                    self.entity_list.append([ent.text, ent.label_])
        self.entity_list.sort()
        self.entity_list=list(k for k,_ in itertools.groupby(self.entity_list))
        return self.entity_list
    
    def convert_to_df_save_as_json(self):
        entities_df=pd.DataFrame(self.entity_list, columns=['Name', 'Entity'])
        entities_df.to_json('names_entities.json')
        name_entities_json = entities_df.to_json(orient='records')[1:-1].replace('},{', '} {')

        return name_entities_json

if __name__ == "__main__":
    import spacy
    import en_core_web_lg
    import pandas as pd

    
    data=pd.read_csv('imdbreviews.csv')
    reviews=list(data['review'])
    nlp=en_core_web_lg.load()

    entities=review_entities(nlp)
    entities_json=entities(reviews)

    print(entities_json[:2])

