import requests, json
from django.shortcuts import render
from .forms import Vform
from django.contrib import messages  
from django.shortcuts import render, redirect


def connectToVectaraApi(query,corpusId, lang, apiKey):


    url = "https://api.vectara.io/v1/query"

    payload = json.dumps({
    "query": [
        {
        "query": query,
        "queryContext": "",
        "start": 0,
        "numResults": 10,
        "contextConfig": {
            "charsBefore": 0,
            "charsAfter": 0,
            "sentencesBefore": 2,
            "sentencesAfter": 2,
            "startTag": "<br>",
            "endTag": "<br>"
        },
       "rerankingConfig": {
            "rerankerId": 272725718,
            "mmrConfig": {
                "diversityBias": 0
        }
      },
        "corpusKey": [
            {
            "customerId": 2397699700,
            "corpusId": corpusId,
            "semantics": 0,
            "dim": [],
            "metadataFilter": "",
            "lexicalInterpolationConfig": {
                "lambda": 0.0025
            }
            }
        ],
        
        "summary": [
            {
            "debug": False,
            "maxSummarizedResults": 5,
            "responseLang": lang,
            "summarizerPromptName": "vectara-summary-ext-v1.2.0"
        
            }
        ]

        }
    ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'customer-id': "2397699700",
        'x-api-key': apiKey,
    }

    response = requests.request("POST", url, headers=headers, data=payload)


    output = response.json()["responseSet"][0]["summary"][0]["text"]

    for obj in response.json()["responseSet"][0]["response"]:
        output += f"<br>_________________________<br>{obj['text']}<br>################################<br>"

    print(response.json())

    return output


def ask(request):
    if request.method == 'POST':
        form = Vform(request.POST)
        if form.is_valid():  
            query = form['query'].value()

            response = connectToVectaraApi(query, form.instance.doc.corpus_id, form.instance.doc.language, form.instance.doc.api_key)
           
            form.instance.response = response

            messages.success(request, f'{query}: <br><br> {response}')     
            
            # form.save()
            
            return redirect('v:ask')
        
        else:
            messages.error(request,"Veuillez saisir un message")
    else: 
        form = Vform()

    context = {
        'form': form,
        'lang': form.instance.doc,
    }

    return render(request, 'form.html', context)  




