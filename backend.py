from flask import Flask, request, jsonify
import time
import json
import regex
import pandas as pd
import numpy as np
from math import cos, asin, sqrt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing

import pickle as p
app = Flask(__name__)
regexps = dict()

@app.route("/")
def echo():
    return json.dumps({"started":"True"})

def scale(X_train, X_test, X_val = np.empty([0,])):
    std=p.load(open("./model/scaler.p","rb"))
    X_tr = std.transform(X_train.values)
    X_te = std.transform(X_test.values)
    
    #When I want to test the set and the data
    if X_val.size != 0 :
        X_va = std.transform(X_val.values)
        return X_tr, X_te, X_va
    return X_tr, X_te


@app.route("/predict", methods=['POST'])
def predict():
    PatientID = request.json['recordID']
    RecordID = request.json['recordsID']

    master = pd.read_csv("master.csv")
    data = master[master['Patient_Id']==int(PatientID)]
    data = data[master['Record_Id']==int(RecordID)]
    print((data['Diastolic Blood Pressure in (mm[Hg])']))
    prob = ""
    try:
        if float(data['Diastolic Blood Pressure in (mm[Hg])'])>80:
            prob = prob+"High Diastolic Blood Pressure, "
        elif float(data['Diastolic Blood Pressure in (mm[Hg])'])<60:
            prob = prob+"Low Diastolic Blood Pressure, "
    except( TypeError):
        pass
    try:
        if float(data['Systolic Blood Pressure in (mm[Hg])'])>120:
            prob = prob+"High Systolic Blood Pressure, "
        elif float(data['Systolic Blood Pressure in (mm[Hg])'])<90:
            prob = prob+"Low Systolic Blood Pressure, "
    except( TypeError):
        pass

    try:
        if float(data['Respiratory rate in (/min)'])<12:
            prob = prob+"Low Respiratory rate, "
        elif float(data['Respiratory rate in (/min)'])>16:
            prob = prob+"High Respiratory rate, "
    except TypeError:
        pass

    try:
        if float(data['Heart rate in (/min)'])<60:
            prob = prob+"Low Heart Rate, "
        elif float(data['Heart rate in (/min)'])>100:
            prob = prob+"High Heart Rate, "
    except TypeError:
        pass

    try:
        if float(data['Total Cholesterol in (mg/dL)'])<125:
            prob = prob+"Low Cholesterol, "
        elif float(data['Total Cholesterol in (mg/dL)'])>200:
            prob = prob+"High Cholesterol, "
    except TypeError:
        pass


    if len(prob)==0:
        prob = 'True'

    data = data.drop(columns=['Name', 'Patient_Id', 'Record_Id'])
    imp = p.load(open("./model/imputer.pkl","rb"))
    data_n = imp.transform(data)
    model = p.load(open("./model/kmodel.pkl","rb"))
    pred = model.predict(data_n)[0]
    print(pred)
    return jsonify(str(pred), prob)

@app.route("/add_details", methods=['POST'])
def add_details():
    fname = request.json['filename']
    data = pd.read_csv(fname)
    master = pd.read_csv("master.csv")
    master = master.append(data, ignore_index=True)
    master.to_csv("master.csv", index=None)

@app.route("/view_details", methods=['POST'])
def view_details():
    recordID = request.json['recordID']
    master = pd.read_csv("master.csv")
    data = master[master['Patient_Id']==int(recordID)]
    return jsonify(data.transpose().to_html(classes='table table-striped" id= "a_nice_table', border=0, header=None, bold_rows=True))

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def closest(data, v):
    return min(data, key=lambda p: distance(v['lat'],v['lon'],p['LAT'],p['LON']))

@app.route("/view_details_aller", methods=['POST'])
def view_details_aller():
    recordID = request.json['recordID']
    latID = request.json['latID']
    lonID = request.json['lonID']
    allermed = p.load(open("./model/allermed.pickle","rb"))
    med = allermed[recordID][0][0] + ", " + allermed[recordID][1][0] + ", "+allermed[recordID][2][0]
    address = "Not Available"
    if len(latID) == 0 or len(lonID) == 0:
        return jsonify(med, address)    
    allerorg = p.load(open("./model/allerorg.pickle","rb"))
    nearorg = closest(allerorg[recordID], {'lat':float(latID), 'lon':float(lonID)})
    address = nearorg.iloc[0]['NAME'] + ", " + nearorg.iloc[0]['ADDRESS'] + ", CITY-"+ nearorg.iloc[0]['CITY'] + ", Zip -"+ nearorg.iloc[0]['ZIP'] + ", Phone NO.-"+nearorg.iloc[0]['PHONE']
    #print(str(address))

    return jsonify(med, address)

@app.route("/view_height_details", methods=['POST'])
def view_height_details():
    recordID = request.json['recordID']
    if len(recordID) == 0:
        return jsonify("Height can't be None")
    sexID = request.json['sexID']
    if sexID != 'M' and sexID != 'F':
        return jsonify("Sex should be 'M' or 'F'")

    height = 30.48*float(recordID)
    if height <= 49.3:
        return jsonify("around 3.3 kg")
    elif height <=54.8:
        return jsonify("around 4.4 kg")
    elif height <=58.4:
        return jsonify("around 5.6 kg")
    elif height <=61.4:
        return jsonify("around 6.4 kg")
    elif height <=64:
        return jsonify("around 7 kg")
    elif height <=66:
        return jsonify("around 7.5 kg")
    elif height <=67.5:
        return jsonify("around 7.9 kg")
    elif height <=69:
        return jsonify("around 8.3 kg")
    elif height <=70.6:
        return jsonify("around 8.6 kg")
    elif height <=71.8:
        return jsonify("around 8.9 kg")
    elif height <=73.1:
        return jsonify("around 9.1 kg")
    elif height <=74.4:
        return jsonify("around 9.4 kg")
    elif height <=75.7:
        return jsonify("around 9.6 kg")
    elif height <=76.9:
        return jsonify("around 10.1 kg")
    elif height <=80.2:
        return jsonify("around 10.5 kg")
    elif height <=85:
        return jsonify("around 11.5 kg")
    elif height <=86.8:
        return jsonify("around 11.9 kg")
    elif height <=95.2:
        return jsonify("around 14 kg")
    elif height <=110:
        return jsonify("around 18.4 kg")
    elif height <=115.5:
        return jsonify("around 20.6 kg")
    elif height <=121:
        return jsonify("around 22.9 kg")
    elif height <=133:
        return jsonify("around 28.5 kg")
    else:
        if sexID == 'M':
            if(height <=137):
                return jsonify("28.5-34.9 kg")
            elif(height <= 140):
                return jsonify("30.8-38.1 kg")
            elif(height <= 142):
                return jsonify("33.5-40.8 kg")
            elif(height <= 145):
                return jsonify("35.8-43.9 kg")
            elif(height <= 147):
                return jsonify("38.5-46.7 kg")
            elif(height <= 150):
                return jsonify("40.8-49.9 kg")
            elif(height <= 152):
                return jsonify("43.1-53 kg")
            elif(height <= 155):
                return jsonify("45.8-55.8 kg")
            elif(height <= 157):
                return jsonify("48.1-58.9 kg")
            elif(height <= 160):
                return jsonify("50.8-61.6 kg")
            elif(height <= 163):
                return jsonify("53-64.8 kg")
            elif(height <= 165):
                return jsonify("55.3-68 kg")
            elif(height <= 168):
                return jsonify("58-70.7 kg")
            elif(height <= 170):
                return jsonify("60.3-73.9 kg")
            elif(height <= 173):
                return jsonify("63-76.6 kg")
            elif(height <= 175):
                return jsonify("65.3-79.8 kg")
            elif(height <= 178):
                return jsonify("67.6-83 kg")
            elif(height <= 180):
                return jsonify("70.3-85.7 kg")
            elif(height <= 183):
                return jsonify("72.6-88.9 kg")
            elif(height <= 185):
                return jsonify("75.3-91.6 kg")
            elif(height <= 188):
                return jsonify("77.5-94.8 kg")
            elif(height <= 191):
                return jsonify("79.9-98 kg")
            elif(height <= 193):
                return jsonify("82.5-100.6 kg")
            elif(height <= 195):
                return jsonify("84.8-103.8 kg")
            elif(height <= 198):
                return jsonify("87.5-106.5 kg")
            elif(height <= 201):
                return jsonify("89.8-109.7 kg")
            elif(height <= 203):
                return jsonify("93-112.9 kg")
            elif(height <= 205):
                return jsonify("94.8-115.6 kg")
            elif(height <= 208):
                return jsonify("97-118.8 kg")
            elif(height <= 210):
                return jsonify("99.8-121.5 kg")
            elif(height <= 213):
                return jsonify("102-124.7 kg")
            else:
                return jsonify("No data available")
        else:
            if(height <=137):
                return jsonify("28.5-34.9 kg")
            elif(height <= 140):
                return jsonify("30.8-37.6 kg")
            elif(height <= 142):
                return jsonify("32.6-39.9 kg")
            elif(height <= 145):
                return jsonify("34.9-42.6 kg")
            elif(height <= 147):
                return jsonify("36.4-44.9 kg")
            elif(height <= 150):
                return jsonify("39-47.6 kg")
            elif(height <= 152):
                return jsonify("40.8-49.9 kg")
            elif(height <= 155):
                return jsonify("43.1-52.6 kg")
            elif(height <= 157):
                return jsonify("44.9-54.9 kg")
            elif(height <= 160):
                return jsonify("47.2-57.6 kg")
            elif(height <= 163):
                return jsonify("49-59.9 kg")
            elif(height <= 165):
                return jsonify("51.2-62.6 kg")
            elif(height <= 168):
                return jsonify("53-64.8 kg")
            elif(height <= 170):
                return jsonify("55.3-67.6 kg")
            elif(height <= 173):
                return jsonify("57.1-69.8 kg")
            elif(height <= 175):
                return jsonify("59.4-72.6 kg")
            elif(height <= 178):
                return jsonify("61.2-74.8 kg")
            elif(height <= 180):
                return jsonify("63.5-77.5 kg")
            elif(height <= 183):
                return jsonify("65.3-79.8 kg")
            elif(height <= 185):
                return jsonify("67.6-82.5 kg")
            elif(height <= 188):
                return jsonify("69.4-84.8 kg")
            elif(height <= 191):
                return jsonify("71.6-87.5 kg")
            elif(height <= 193):
                return jsonify("73.5-89.8 kg")
            elif(height <= 195):
                return jsonify("75.7-92.5 kg")
            elif(height <= 198):
                return jsonify("77.5-94.8 kg")
            elif(height <= 201):
                return jsonify("79.8-97.5 kg")
            elif(height <= 203):
                return jsonify("81.6-99.8 kg")
            elif(height <= 205):
                return jsonify("83.9-102.5 kg")
            elif(height <= 208):
                return jsonify("85.7-104.8 kg")
            elif(height <= 210):
                return jsonify("88-107.5 kg")
            elif(height <= 213):
                return jsonify("89.8-109.7 kg")
            else:
                return jsonify("No data available")
        
    if sexID == 'M':
        return jsonify("sahi male")
    elif sexID == 'F':
        return jsonify("sahi female")
    else:
        return jsonify("Sex should be 'M' or 'F'")

if __name__ == "__main__":
    app.run(host='localhost', port=2000)
