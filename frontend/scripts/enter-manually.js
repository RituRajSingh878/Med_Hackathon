var document, store, volatile_store;
const electron = require("electron");
var request = require('request');
const con = require('electron').remote.getGlobal('console');
var dialog = electron.remote.dialog; // Load the dialogs component of the OS

let params = ['Name',
 'Patient_Id',
 'Record_Id',
 'Pain severity - 0-10 verbal numeric rating [Score] - Reported in ({score})',
 'Diastolic Blood Pressure in (mm[Hg])',
 'Systolic Blood Pressure in (mm[Hg])',
 'Heart rate in (/min)',
 'Respiratory rate in (/min)',
 'Body Mass Index in (kg/m2)',
 'Glucose in (mg/dL)',
 'Urea Nitrogen in (mg/dL)',
 'Creatinine in (mg/dL)',
 'Calcium in (mg/dL)',
 'Sodium in (mmol/L)',
 'Potassium in (mmol/L)',
 'Chloride in (mmol/L)',
 'Carbon Dioxide in (mmol/L)',
 'Total Cholesterol in (mg/dL)',
 'Triglycerides in (mg/dL)',
 'Low Density Lipoprotein Cholesterol in (mg/dL)',
 'High Density Lipoprotein Cholesterol in (mg/dL)'];


const proceed = () => {
    // create csv
    const createCsvWriter = require('csv-writer').createObjectCsvWriter;

    var headers = [];
    var records = {};
    for(var i=0; i<params.length; ++i) {
        headers.push({id: params[i], title: params[i]});
        records[params[i]] = document.getElementById(params[i]).value;
    }

    const csvWriter = createCsvWriter({
        path: 'sample.csv',
        header: headers
    });

    csvWriter.writeRecords([records])       // returns a promise
        .then(() => {
            con.log('created csv');
            add_details('sample.csv');
            alert("Details Sucessfully Added!")
            loadState("enter-manually");
        });
};

const add_details = (fname) => {
    request.post('http://127.0.0.1:2000/add_details',
        { json: { filename: fname} }    
    );
};

const on_init = (_document, _store, _volatile_store)=>{
    document = _document;
    store = _store;
    volatile_store = _volatile_store;

    // populate text boxes
    for (var i = 0; i < params.length; i++) {
        var lbl = document.createElement("label");
        lbl.setAttribute("for",params[i]);
        lbl.innerHTML = params[i];
        var txt = document.createElement("input");
        txt.setAttribute("type","text");
        txt.setAttribute("id",params[i]);
        document.getElementById("vitals").appendChild(lbl);
        document.getElementById("vitals").appendChild(txt);
        document.getElementById("vitals").appendChild(document.createElement("br"));
    }

    $(document).find("#proceed").on('click', proceed);
    $(document).find("#home").on('click', home);
    volatile_store["selected"] = [];
};

const on_unload = (document)=>{
};

const home = () => {
    con.log("home pressed");
    loadState("data-selection");
};

exports.on_init = on_init;
exports.on_unload = on_unload;
