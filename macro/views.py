from django.shortcuts import render

# Create your views here.

def macro(request):
    context = {}

    return render(request, 'macro/macro.html', context)


def calendar(request):
    context = {}

    return render(request, 'macro/calendar.html', context)