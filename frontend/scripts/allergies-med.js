var document, store, volatile_store;
const electron = require("electron");
var request = require('request');
const con = require('electron').remote.getGlobal('console');
var dialog = electron.remote.dialog; // Load the dialogs component of the OS

const view = () => {
    record_id = document.getElementById("record-allergy").value
    lat_id = document.getElementById("lat-id").value
    lon_id = document.getElementById("lon-id").value
    request.post('http://localhost:2000/view_details_aller',
        { json: { recordID: record_id, latID : lat_id, lonID : lon_id} },
        function (error, response, body) {
            $(document).find("#patient-aller").html("Basic Med for the allergy- <br>" + body[0]);
            $(document).find("#location").html(" <br> Nearest location of organizations given to your location for med- <br>" + body[1]);
        }
    );
};

const on_init = (_document, _store, _volatile_store)=>{
    document = _document;
    store = _store;
    volatile_store = _volatile_store;
    $(document).find("#view-details").on('click', view);
    volatile_store["selected"] = [];
};

const on_unload = (document)=>{
};

exports.on_init = on_init;
exports.on_unload = on_unload;
