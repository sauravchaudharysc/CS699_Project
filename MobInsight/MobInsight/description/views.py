from django.shortcuts import get_object_or_404,render
from django.views.generic import ListView
from django.http import JsonResponse
import numpy as np
import matplotlib.pyplot as plt
from .models import Item
from io import BytesIO
import base64
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

def get_plot():
    fb = (120, 90, 110, 100, 95)
    yt = (80, 90, 75, 85, 95)
    ig = (50, 40, 55, 35, 45)
    x = ['Performance', 'Display', 'Camera', 'Battery', 'Storage']
    xpos = np.arange(len(x))
    barWidth = 0.4
    plt.switch_backend('AGG')
    plt.figure(figsize=(7,5))
    plt.bar(xpos, fb, color='royalblue', width= barWidth, label='FB')
    plt.bar(xpos, yt, bottom=fb, color='red', width= barWidth, label='YT')
    plt.bar(xpos, ig, bottom=yt, color='purple', width= barWidth, label='IG')
    plt.xlabel('Specification')
    plt.ylabel('Rating')
    plt.title('Comparison')
    plt.xticks(xpos, x)
    plt.legend()
    graph = get_graph()
    return graph


def item_single(request, item):
    item = get_object_or_404(Item, name=item)
    chart = get_plot()
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
