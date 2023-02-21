from django.http import HttpResponse


def my_view(request):
    words = input()
    words = ''.join(words)
    return HttpResponse(words)
