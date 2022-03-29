from fastai.learner import load_learner
from flask import Flask,render_template,request
from fastai import *
import numpy as np 
import pandas as pd
#from fastai.vision.widgets import *
import urllib.request
import os
from PIL import Image
#import pathlib
#temp = pathlib.PosixPath
#pathlib.PosixPath = pathlib.WindowsPath
import cv2
import easyocr
from easyocr import Reader
import pickle


#import pathlib
#plt = platform.system()
#pathlib.WindowsPath = pathlib.PosixPath
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


#--------------------------------------------Category----------------------------------------------
All_dictionary = [
    {'Apparel':[{'Topwear':['Tshirt','Shirt','Dress','Jacket','Tops','Undershirt','Pullover']},
            {'Bottomwear':  ['Jeans','Pant','Shorts','Skirt','Trouser']},
            {'Outerwear': ['Coat','Sweater','Hoodie','Cardigan','Blazer']}]},
            
    {'Footwear':[{'Casual':['Sandal','Flipflop','Boots','Heels','Flats']},
            {'Formal': ['Shoes']},
            {'Sports':['Sneaker']}]},
            
    {'Accessories': [{'Bags' : ['Bagpack','Handbag','Dufflebag','Slingbag']},
                {'Wristwear' : ['Watch','Cufflink','Gloves','Wristband']},
                {'Eyewear' : ['Sunglass']},
                {'Jewellery' : ['Necklace','Ring','Bracelet','Pendent','Earring']},
                {'hats' : ['Cap','Hat','Beanie cap']},
                {'Others' : ['Scarf','Socks','Wallet','Belt','Ties']}]},

    {'Furniture': [{'Storage' : ['Wardrobe','Trolley','Drawer','Cabinet']},
                {'Display' : ['Table','Hanger']},
                {'Others' : ['Chair','Stool','Sofa']}]}
                ]

#------------------------------------All product label--------------------------------------------



All_categories = ['Tshirt','Shirt','Dress','Jacket','Tops','Undershirt','Pullover','Jeans','Pant','Shorts','Skirt','Trouser',
                    'Coat','Sweater','Hoodie','Cardigan','Blazer','Sandal','Flipflop','Boots','Heels','Flats','Shoes',
                    'Sneaker','Bagpack','Handbag','Dufflebag','Slingbag','Watch','Cufflink','Gloves','Wristband','Sunglass',
                    'Necklace','Ring','Bracelet','Pendent','Earring','Cap','Hat','Beanie cap','Scarf','Socks','Wallet','Belt',
                    'Ties','Wardrobe','Trolley','Drawer','Cabinet','Table','Hanger','Chair','Stool','Sofa']





app = Flask(__name__, template_folder='template')

def get_category_detail(label):
    if label == 'Innerwear':
        sub_cat = 'Innerwear'
        cat = 'Apparel'
    else:
        for i in All_dictionary:
            for j in i.values():
                for k in j:
                    for l in k.values():
                        if label in l:
                            sub_cat = np.array(list(k.keys()))
                            cat = np.array(list(i.keys()))
                            sub_cat = ''.join(map(str,sub_cat))
                            cat = ''.join(map(str,cat))
                            return (sub_cat,cat)

def extract_label(img):
    lst = []
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img, detail=0)
    lst = ''.join(''.join(i) for i in str(result).title())
    print(lst)
    for i in All_categories:
        if i in lst:
            print(i)
            return (i)

    

def get_model():
    global model
    model = load_learner(fname ='export.pkl')
    print("Model loaded!")
   
def prediction(img_path):
    if img_path is not None:
        pred = model.predict(img_path)
        predt = str(pred[0])
        predt = predt.capitalize()
    return(predt)

get_model()

@app.route("/", methods=['GET', 'POST'])
def home():

    return render_template('home.html')

@app.route("/predict", methods = ['GET','POST'])
def predict():
    lst = []
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file_path = os.path.join('static/', filename)
        file.save(file_path)
        if file_path is not None:
            product = prediction(file_path)
            if product == "T-shirt":
                product = "Tshirt"
            print(product)
            extracted_label = extract_label(file_path)
            print(extracted_label)
            if product == extracted_label:
                sub_cat,cat = get_category_detail(product)
                return render_template('predict.html', product = product,extracted_label=extracted_label, sub_cat = sub_cat,cat = cat,user_image = file_path)
            else:
                sub_cat,cat = get_category_detail(product)
                return render_template('predict2.html', product = product,extracted_label=extracted_label, sub_cat = sub_cat,cat = cat,user_image = file_path)


if __name__ == "__main__":
    app.run()
