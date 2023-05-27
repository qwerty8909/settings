from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd


Link = {'link': ['www.google.ru', 'www.mail.ru', 'www.yandex.ru', 'www.rambler.ru', 'www.avito.ru', 'www.ok.ru'],
        'text': ['Hel', 'Hello', 'Hello world', 'world', 'avito', 'Hemsworth']}
df = pd.DataFrame(Link)


def home(request):
    rows_count = df.shape[0]
    context = {'rows_count': rows_count}
    return render(request, 'home.html', context)


def search(request):
    query = request.GET.get('q')
    links = df[df['text'].str.startswith(query)]
    count = links.shape[0]
    link_texts = list(links['link'])
    data = {'count': count, 'link_texts': link_texts}
    return JsonResponse(data)