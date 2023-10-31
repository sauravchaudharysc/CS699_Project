from django.shortcuts import get_object_or_404,render
from django.views.generic import ListView
from django.http import JsonResponse
import numpy as np
import matplotlib.pyplot as plt
from .models import Item
from io import BytesIO
import base64
import pandas as pd
import re

# Create your views here.
class HomeView(ListView):
    model = Item
    template_name = "description/index.html"
    context_object_name = "items"
    paginate_by = 10
    def get_template_names(self):
        if self.request.htmx:
            return 'description/components/item-list-elements.html'
        return "description/index.html"

class StatView(ListView):
    model = Item
    def get_template_names(self):
        return "description/stats.html"

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(item):
    phone_scores = (120, 90, 110, 100)
    avg_scores = (80, 90, 75, 85)
    phones = Item.objects.all()
    db_lst = []
    for phone in phones:
        temp_lst = []
        temp_lst.append(phone.name)
        temp_lst.append(phone.performance)
        temp_lst.append(phone.display)
        temp_lst.append(phone.battery)
        temp_lst.append(phone.camera)
        db_lst.append(temp_lst)
    
    x = ['Performance', 'Display', 'Camera', 'Battery']
    xpos = np.arange(len(x))
    barWidth = 0.4
    plt.switch_backend('AGG')
    plt.figure(figsize=(9, 5))
    plt.bar(xpos, phone_scores, color='royalblue', width= barWidth, label=item+' Scores')
    plt.bar(xpos, avg_scores, bottom=avg_scores, color='red', width= barWidth, label='Average')
    plt.xlabel('Specification')
    plt.ylabel('Rating')
    plt.title('Comparison')
    plt.xticks(xpos, x)
    plt.legend(loc='best')
    graph = get_graph()
    return graph


def item_single(request, item):
    item = get_object_or_404(Item, name=item)
    chart = get_plot(item.name)
    return render(request, "description/single.html",{"item":item, "chart": chart})

def get_names(request):
    search = request.GET.get('search')
    payload = []
    if search:
        objs = Item.objects.filter(name__icontains=search)
        for obj in objs:
            payload.append({
                'name': obj.name
            })
    return JsonResponse({
        'status': True,
        'payload': payload
    })
