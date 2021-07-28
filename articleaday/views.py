from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
import os
from io import StringIO
from django.core.files.storage import FileSystemStorage
from IPython.display import display
from pygooglenews import GoogleNews
import datetime as dt
import pandas as pd
from .models import *
import os.path
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from io import StringIO
from django.core.files.storage import FileSystemStorage
import json
from IPython.display import display
from pygooglenews import GoogleNews
import datetime as dt
import pandas as pd
import selenium as sel
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import requests
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig, AutoModelForSeq2SeqLM, AutoTokenizer, pipeline, AutoTokenizer, AutoModel
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import *
from django.contrib.auth.decorators import *
import psycopg2
from .forms import ProfessionForm


# Create your views here.

def getProfession(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ProfessionForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            #Get user career
            career_input = request.POST.get['career']

            query(summarization(getArticle(career_input)),
                       'Robotics,Chemistry,Doctor,Computer Science,Business')
    else:
        #Else return an empty form
        form = ProfessionForm() # An unbound form

    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


# Query Functions
def getArticle(user_profession):
    gn = GoogleNews()
    # search for the best matching articles that mention MSFT and
    # do not mention AAPL (over the past 6 month
    search = gn.search(f'{user_profession} news')
    # df = pd.DataFrame(search['entries'])
    # print(df)
    # print(type(search))
    # print(type(search['entries'][0]))
    # # print(search['entries'])

    driver_link = search['entries'][0].link

    PATH = '/Users/harshi/Downloads/chromedriver'  # Path to chromedriver
    driver = webdriver.Chrome(PATH)
    driver.get(driver_link)

    driver_title = driver.title
    content = driver.find_elements_by_tag_name('p')
    total_text = ""
    for item in content:
        total_text += item.text + "--[101]-- "
    return total_text 


def summarization(ARTICLE):
    summarizer = pipeline("summarization")

    model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
    tokenizer = AutoTokenizer.from_pretrained("t5-base")

    # T5 uses a max_length of 512 so we cut the article to 512 tokens.
    inputs = tokenizer.encode(
        "summarize: " + ARTICLE, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=200, min_length=75,
                             length_penalty=2.0, num_beams=4, early_stopping=True)
    output = tokenizer.decode(outputs[0])
    return output[5:(len(output)-4)]


def queryForArticleADAY(title_of_article, otherprofessions):
    model = SentenceTransformer('paraphrase-distilroberta-base-v1')

    otherprofessions = otherprofessions.split(',')
    sentence1 = []
    # Our sentences we like to encode
    for item in otherprofessions:
        sentence1.append(title_of_article)

    sentence2 = otherprofessions

    # Sentences are encoded by calling model.encode()
    embeddings1 = model.encode(sentence1, convert_to_tensor=True)
    embeddings2 = model.encode(sentence2, convert_to_tensor=True)

    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)

    # Print the embeddings
    finalembeddinglist = []
    for i in range(len(sentence1)):
        #print("{} \t\t {} \t\t Score: {:.4f}".format(sentence1[i], sentence2[i], cosine_scores[i][i]))
        finalembeddinglist.append(cosine_scores[i][i])
    finaldict = {}
    for element in finalembeddinglist:

        # finaldict[sentence2[finalembeddinglist.index(element)]].append(element)
        prediction = max(finalembeddinglist)
    return sentence2[finalembeddinglist.index(prediction)]




