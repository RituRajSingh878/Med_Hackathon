var document, store, volatile_store;
const electron = require("electron");
var request = require('request');
const con = require('electron').remote.getGlobal('console');
var dialog = electron.remote.dialog; // Load the dialogs component of the OS

const predict = () => {
    record_id = document.getElementById("record-id").value
    records_id = document.getElementById("records-id").value
    request.post('http://localhost:2000/predict',
        { json: { recordID: record_id, recordsID : records_id} },
        function (error, response, body) {
            
              if(body[0]=='0'){
               $(document).find("#prediction-result").text("Patient has low risk of health problem");
               $(document).find("#prediction-result1").html("")                            
            }
              else{
                     if(body[0]=='1'){
                                        $(document).find("#prediction-result").text("Patient has mild risk of health problem.");
                                        if(body[1] != 'True')
                                          {$(document).find("#prediction-result1").html("<b>"+body[1]+"/b");}
                                
                                     }
                                 else{
                                        $(document).find("#prediction-result").text("Patient has high risk of health problem.");
                                        if(body[1] != 'True')
                                          {$(document).find("#prediction-result1").html("Possible Problems:"+"<b>"+body[1]+"</b>");}                            
                                     }


            }
              
        }
    );
};

const on_init = (_document, _store, _volatile_store)=>{
    document = _document;
    store = _store;
    volatile_store = _volatile_store;
    $(document).find("#make-predictions").on('click', predict);
    volatile_store["selected"] = [];
};

const on_unload = (document)=>{
};

exports.on_init = on_init;
exports.on_unload = on_unload;
