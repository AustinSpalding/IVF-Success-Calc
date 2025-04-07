from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from ivf_success_chance_calc.core.helpers import calculate_success

def index(request):
    context = {
        "title": "IVF Calculator",
    }
    return render(request, "index.html", context)

@csrf_protect
def calculate(request):
    context = {
        "title": "IVF Calculator",
    }
    if request.method == 'POST':
        context['chance'] = calculate_success(request.POST)
    return render(request, "calculate.html", context)