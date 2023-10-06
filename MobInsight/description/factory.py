from .models import Item
import ast
import pandas as pd
def upload_csv():
    df = pd.read_csv("MobInsight/description/phones.csv")
    col_names=list(df.columns)
    for idx,row in df.iterrows():
        name = row['Phone Name']
        image = str(row['Image Link'])
        price = int(row['Price'])
        comment = row['Expert Comment']
        performance = row['Performance']
        display = row['Display']
        camera = row['Camera']
        battery = row['Battery']
        Item.objects.create(
            name = name,
            comment = comment,
            price = price,
            performance = performance,
            display =display,
            camera = camera,
            battery = battery,
            image = "https://"+image
        )
    print("Done Uploading...")
        