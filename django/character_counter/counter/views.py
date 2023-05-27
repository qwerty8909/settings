from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd


Link = {'link': ['www.google.ru', 'www.mail.ru', 'www.yandex.ru', 'www.rambler.ru', 'www.avito.ru', 'www.ok.ru'],
        'text': ['Hel', 'Hello', 'Hello world', 'world', 'avito', 'Hemsworth']}
df = pd.DataFrame(Link)

def counter(request):
    return render(request, 'counter.html')

def count_characters(request):
    text = request.GET.get('text')
    links = df[df['text'].str.startswith(text)]
    count = links.shape[0]
    data = {'count': count}
    return JsonResponse(data)
