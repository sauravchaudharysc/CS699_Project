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
def get_Scores(df,phoneName) :
    data =pd.DataFrame(df, columns=['Phone Name','Performance','Display','Battery','Camera'])
    performance_df=data.copy()
    columns_to_drop = list(performance_df.columns)
    performance_df[['Core', 'Processor', 'RAM']] = performance_df['Performance'].str.split('\n', expand=True).iloc[:,:-1]
    performance_df = performance_df.drop(columns_to_drop, axis=1)
    def calculate_phone_score(core, processor, ram):
        # Define a dictionary to assign points based on processors
        processor_scores = {
            'Snapdragon 8 Gen 2':1, 
            'Apple A16 Bionic':8,
           'MediaTek Dimensity 9200':2, 
            'Google Tensor G2':3,
           'MediaTek Dimensity 9000 Plus':2,
            'Apple A15 Bionic':8,
           'Snapdragon 8 Plus Gen 1':5, 
            'Snapdragon 8 Gen 1':4,
           'MediaTek Dimensity 9000':3,
            'MediaTek Dimensity 7050':3,
           'Snapdragon 888':3.5,
            'Snapdragon 888 Plus':4,
            'MediaTek Dimensity 8100':3,
           'MediaTek Dimensity 8100 Max':3.5,
            'Snapdragon 870':3.5,
           'MediaTek Dimensity 920':2,
            'MediaTek Dimensity 1200':2.5,
            # Add more processors and their scores as needed
        }

        # Assign base scores based on core count and RAM size
        core_score = 0
        if 'Octa core' in core:
            core_score = 4
        elif 'Hexa core' in core:
            core_score = 3
        elif 'Quad core' in core:
            core_score = 2
        elif 'Dual core' in core:
            core_score = 1

        ram_score = 0
        if '12 GB' in ram:
            ram_score = 4
        elif '8 GB' in ram:
            ram_score = 3
        elif '6 GB' in ram:
            ram_score = 2
        elif '4 GB' in ram:
            ram_score = 1

        # Get additional processor score from the dictionary
        processor_score = processor_scores.get(processor, 0)

        # Calculate the total score
        total_score = core_score + ram_score + processor_score
        return total_score

    # Apply the function to the DataFrame to calculate the scores
    data['Performance_Score'] = performance_df.apply(lambda row: calculate_phone_score(row['Core'], row['Processor'], row['RAM']), axis=1)
    display_df=data.copy()
    columns_to_drop = list(display_df.columns)
    display_df[['Size', 'Screen_Type', 'Refresh_Rate']]=display_df['Display'].str.split('\n', expand=True).iloc[:,:-1]
    display_df = display_df.drop(columns_to_drop, axis=1)
    def calculate_display_score(size, screen_type, refresh_rate):
        # Score based on screen size (larger screen size gets higher score)
        size_score = float(size.split()[0])

        # Score based on screen type (higher PPI gets higher score, AMOLED screen gets additional points)
        try:
            ppi = float(screen_type.split()[0])
            screen_type_score = ppi / 100  # Scale down PPI to be in a reasonable range
            if 'AMOLED' in screen_type.upper():
                screen_type_score += 5  # Additional points for AMOLED screen
            elif 'OLED' in screen_type.upper():
                screen_type_score += 3     
        except (ValueError, IndexError):
            screen_type_score = 0

        # Score based on refresh rate (higher refresh rate gets higher score)
        refresh_rate_score = 0
        if '90 Hz' in refresh_rate:
            refresh_rate_score = 1
        elif '120 Hz' in refresh_rate:
            refresh_rate_score = 2
        elif '144 Hz' in refresh_rate:
            refresh_rate_score = 3    


        # Calculate the total score
        total_score = size_score + screen_type_score + refresh_rate_score
        return total_score

    # Apply the function to the DataFrame to calculate the scores
    data['Display_Score'] = display_df.apply(lambda row: calculate_display_score(row['Size'], row['Screen_Type'], row['Refresh_Rate']), axis=1)
    battery_df=data.copy()
    columns_to_drop = list(battery_df.columns)
    battery_df[['CapacityMah', 'Charge_Type']]=battery_df['Battery'].str.split('\n', expand=True).iloc[:,:-2]
    battery_df = battery_df.drop(columns_to_drop, axis=1)
    columns_to_drop = list(battery_df.columns)
    battery_df[['Capacity','Unit']]=battery_df['CapacityMah'].str.split(' ',expand=True)
    battery_df = battery_df.drop(columns_to_drop, axis=1)
    battery_df = battery_df.drop(['Unit'], axis=1)
    replace_values = lambda x: 1 if 3000 < x <= 3500 else (2 if 3500 < x <= 4000 else (3 if 4000< x <= 4500 else (4 if 4500 < x <= 5000 else 5)))

    battery_df['Capacity']=battery_df['Capacity'].astype('int')
    data['Battery_Score'] = battery_df['Capacity'].apply(replace_values)
    camera_df=data.copy()
    columns_to_drop = list(camera_df.columns)
    camera_df[['Back','Flash','Front']] =camera_df['Camera'].str.split('\n', expand=True).iloc[:,:-1]
    camera_df = camera_df.drop(columns_to_drop, axis=1)
    camera_df = camera_df.drop(['Flash'], axis=1)
    def sum_of_digits(s):
        # Extract digits using regular expression and sum them up
        digits = [int(digit) for digit in re.findall(r'\d+', s)]
        return sum(digits)

    data['Camera_score'] = camera_df.apply(lambda row: sum_of_digits(row['Back'] + row['Front']), axis=1)
    
    #####################----------------NORMALIZATION#############################
    data['Performance_Score']=round((5*data['Performance_Score']/max(data['Performance_Score'])),2)
    data['Display_Score']=round((5*data['Display_Score']/max(data['Display_Score'])),2)
    data['Battery_Score']=round((5*data['Battery_Score']/max(data['Battery_Score'])),2)
    data['Camera_score']=round((5*data['Camera_score']/max(data['Camera_score'])),2)

    data = data.drop(['Performance','Display','Battery','Camera'], axis=1)
    
    Averages=[data['Performance_Score'].mean(),data['Display_Score'].mean(),data['Battery_Score'].mean(),data['Camera_score'].mean()]

    Averages = list(map(lambda x: round(x, 2),Averages))
    def get_phone_info(phone_name):
        row = data[data['Phone Name'] == phone_name].iloc[0]
        phone_info = row.values.tolist()
        return phone_info

    phone_info = get_phone_info(phoneName)
    phone_info=phone_info[1:]
    phoneScore=[]
    phoneScore.append(phone_info)
    phoneScore.append(Averages)
    return phoneScore

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
    phone_score_avg = get_Scores(db_lst,item)
    phone_scores = phone_score_avg[0]
    avg_scores = phone_score_avg[1]
    print(phone_scores)
    print(avg_scores)
    x = ['Performance', 'Display', 'Camera', 'Battery']
    xpos = np.arange(len(x))
    barWidth = 0.3
    plt.switch_backend('AGG')
    plt.figure(figsize=(9, 5))
    plt.bar(xpos, avg_scores, color='white',edgecolor="green", hatch='/',width= barWidth, label='Average',)
    plt.bar(xpos+0.3, phone_scores, color='white', width= barWidth, edgecolor="red" ,hatch='.',label=item+' Scores')
    plt.xlabel('Specification')
    plt.ylabel('Rating')
    plt.title('Comparison')
    plt.xticks(xpos+0.15, x)
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
