const pesajeCreate = document.querySelector("#pesaje-create");
const modalContent = document.querySelector(".modal-content");
var myModalEl = document.querySelector('#exampleModal');
const myModal = new bootstrap.Modal(document.querySelector('#exampleModal'));
myModalEl.addEventListener('hidden.bs.modal', function (event) {
    detenerWebSocket();
})
const items = document.querySelector("#items");

window.addEventListener('DOMContentLoaded', (e) => {
    cargarItems();
});


const fechaInicio = new Datepicker(document.querySelector("#fecha-inicio"), {
    language: 'es',
    format:'DD - MM dd, yyyy',
    autohide: true,
});
fechaInicio.setDate(new Date());

const fechaFin = new Datepicker(document.querySelector("#fecha-fin"), {
    language: 'es',
    format:'DD - MM dd, yyyy',
    autohide: true,
});
fechaFin.setDate(new Date());

const cargarItems = async () => {
    await axios(items.getAttribute("data-url"))
    .then( res => {
        items.innerHTML = res.data;
    })
}

const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});

const getModal = async (url) => {
    await axios(url)
    .then( res => {
        modalContent.innerHTML = res.data        
    });
    myModal.show();
} 

const postModal = async (datosForm) => {
    await axios(datosForm.getAttribute("action"), {
        method: "post",
        data: new FormData(datosForm)
    })
    .then(res => {              
        Toast.fire({
            icon: 'success',
            title: res.data.message
        });                          
        cargarItems();
        myModal.hide();
    })
    .catch(error => {
        const parseado = JSON.parse(error.response.data.message)                        
        Toast.fire({
            icon: 'error',
            title: JSON.stringify(parseado)
        })
    })
}

items.addEventListener("click", async (e) => {
    if (e.target.classList.contains("bi-pencil")) {
        await axios(e.target.dataset.url)
        .then(res => {
            modalContent.innerHTML =res.data;   
            const pesoBruto = document.querySelector("#id_peso_bruto");
            const pesoTara = document.querySelector("#id_peso_tara");                
            const pesoNeto = document.querySelector("#id_peso_neto");
            const pesoNetoTn = document.querySelector("#id_peso_neto_tn");            
            const handleInput = (e) => {
                pesoNeto.value = pesoBruto.value - pesoTara.value;
                pesoNetoTn.value = pesoNeto.value/1000;
            };
            pesoBruto.oninput = handleInput;
            pesoTara.oninput = handleInput;

            $('#id_proveedor').select2({
                language: 'es',      
                theme: "bootstrap4",   
                width: "100%",
                ajax: {
                    url: "/proveedor/proveedor-autocomplete/",
                    dataType: 'json',
                    delay: 250,
                    data: function(params) {
                        return {
                            q: params.term, // search term
                            page: params.page
                        };
                    },
                    processResults: function(data, params) {
                        // parse the results into the format expected by Select2
                        // since we are using custom formatting functions we do not need to
                        // alter the remote JSON data, except to indicate that infinite
                        // scrolling can be used
                        params.page = params.page || 1;
                        return {
                            results: data.results,
                            pagination: {
                                more: (params.page * 30) < data.total_count
                            }
                        };
                    },
                    cache: true
                },
                escapeMarkup: function(markup) {
                    return markup;
                }, // let our custom formatter work
                minimumInputLength: 3,
                
            });
            $('#id_vehiculo').select2({
                language: 'es',      
                theme: "bootstrap4",   
                width: "100%",
                ajax: {
                    url: "/conductor/vehiculo-autocomplete/",
                    dataType: 'json',
                    delay: 250,
                    data: function(params) {
                        return {
                            q: params.term, // search term
                            page: params.page
                        };
                    },
                    processResults: function(data, params) {
                        // parse the results into the format expected by Select2
                        // since we are using custom formatting functions we do not need to
                        // alter the remote JSON data, except to indicate that infinite
                        // scrolling can be used
                        params.page = params.page || 1;
                        return {
                            results: data.results,
                            pagination: {
                                more: (params.page * 30) < data.total_count
                            }
                        };
                    },
                    cache: true
                },
                escapeMarkup: function(markup) {
                    return markup;
                }, // let our custom formatter work
                minimumInputLength: 3,
                
            });
            $('#id_conductor_vehiculo').select2({
                language: 'es',      
                theme: "bootstrap4",   
                width: "100%",
                ajax: {
                    url: "/conductor/conductor-autocomplete/",
                    dataType: 'json',
                    delay: 250,
                    data: function(params) {
                        return {
                            q: params.term, // search term
                            page: params.page
                        };
                    },
                    processResults: function(data, params) {
                        // parse the results into the format expected by Select2
                        // since we are using custom formatting functions we do not need to
                        // alter the remote JSON data, except to indicate that infinite
                        // scrolling can be used
                        params.page = params.page || 1;
                        return {
                            results: data.results,
                            pagination: {
                                more: (params.page * 30) < data.total_count
                            }
                        };
                    },
                    cache: true
                },
                escapeMarkup: function(markup) {
                    return markup;
                }, // let our custom formatter work
                minimumInputLength: 3,
                
            });
            $('#id_equipo_carguio').select2({
                language: 'es',      
                theme: "bootstrap4",   
                width: "100%",
                ajax: {
                    url: "/conductor/carguio-autocomplete/",
                    dataType: 'json',
                    delay: 250,
                    data: function(params) {
                        return {
                            q: params.term, // search term
                            page: params.page
                        };
                    },
                    processResults: function(data, params) {
                        // parse the results into the format expected by Select2
                        // since we are using custom formatting functions we do not need to
                        // alter the remote JSON data, except to indicate that infinite
                        // scrolling can be used
                        params.page = params.page || 1;
                        return {
                            results: data.results,
                            pagination: {
                                more: (params.page * 30) < data.total_count
                            }
                        };
                    },
                    cache: true
                },
                escapeMarkup: function(markup) {
                    return markup;
                }, // let our custom formatter work
                minimumInputLength: 3,
                
            });    
            $('#id_origen').select2({
                language: 'es',      
                theme: "bootstrap4",   
                width: "100%",
                placeholder: "Seleccionar Origen",
            });
            $('#id_destino').select2({
                language: 'es',      
                theme: "bootstrap4",   
                width: "100%",
                placeholder: "Seleccionar Destino",
            });
            myModal.show();            
            const pesajeForm = document.querySelector("#pesaje-form");
            pesajeForm.addEventListener("submit", (e) => {
                e.preventDefault();
                postModal(pesajeForm);
            });
        });            
    }
    if (e.target.classList.contains("bi-printer")) {
        e.preventDefault();
        //printJS(e.target.dataset.url);
        window.open(e.target.dataset.url,"_blank","height=500,width=700,status=no,toolbar=no,menubar=no,location=no,scrollbars=yes");
    }
});

const calculoPesaje = (bruto, tara) => {
    let calculo = [0,0];    
    calculo[0] = bruto - tara;    
    calculo[1] = calculo[0]/1000
    return calculo;
}

pesajeCreate.addEventListener("click", async () => {    
    await axios(pesajeCreate.getAttribute("data-url"))
    .then(res => {
        modalContent.innerHTML =res.data;    
        // variables temporales
        const serialUno = document.querySelector("#serial1");
        const serialDos = document.querySelector("#serial2");
        //*****/
        const elIndicador = document.querySelector("#indicador-pesaje");
        const visorPesaje = document.querySelector("#visor-pesaje");
        elwebsocketIndicador = elIndicador;
        elwebsocketVisor = visorPesaje;
        elwebsocket = serialUno;        
        iniciarWebSocket();
        const pesoBruto = document.querySelector("#id_peso_bruto");
        const pesoTara = document.querySelector("#id_peso_tara");                
        const pesoNeto = document.querySelector("#id_peso_neto");
        const pesoNetoTn = document.querySelector("#id_peso_neto_tn");
        const pesajeBruto = document.querySelector("#id_pesaje_bruto");
        const pesajeTara = document.querySelector("#id_pesaje_tara");
        const handleInput = (e) => {
            pesoNeto.value = pesoBruto.value - pesoTara.value;
            pesoNetoTn.value = pesoNeto.value/1000;
        };

        const handlePesoBruto = (e) => {
            if (e.target.checked) {
                pesajeTara.checked = false;
                pesoTara.classList.remove('input-selected');
                pesoBruto.classList.add('input-selected');
                elwebsocket = serialUno;
                pesoBruto.readOnly = false;
                pesoTara.readOnly = true;                
            }
        }

        const handlePesoTara = (e) => {
            if (e.target.checked) {
                pesajeBruto.checked = false;
                pesoBruto.classList.remove('input-selected');
                pesoTara.classList.add('input-selected');
                elwebsocket = serialDos;
                pesoTara.readOnly = false;
                pesoBruto.readOnly = true;                
            }
        }

        pesoBruto.oninput = handleInput;
        pesoTara.oninput = handleInput;
        pesajeBruto.onchange = handlePesoBruto;
        pesajeTara.onchange = handlePesoTara;

        $('#id_proveedor').select2({

            language: 'es',      
            theme: "bootstrap4",   
            width: "100%",
            ajax: {
                url: "/proveedor/proveedor-autocomplete/",
                dataType: 'json',
                delay: 250,
                data: function(params) {
                    return {
                        q: params.term, // search term
                        page: params.page
                    };
                },
                processResults: function(data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;
                    return {
                        results: data.results,
                        pagination: {
                            more: (params.page * 30) < data.total_count
                        }
                    };
                },
                cache: true
            },
            escapeMarkup: function(markup) {
                return markup;
            }, // let our custom formatter work
            minimumInputLength: 3,
            
        });
        $('#id_vehiculo').select2({
            language: 'es',      
            theme: "bootstrap4",   
            width: "100%",
            ajax: {
                url: "/conductor/vehiculo-autocomplete/",
                dataType: 'json',
                delay: 250,
                data: function(params) {
                    return {
                        q: params.term, // search term
                        page: params.page
                    };
                },
                processResults: function(data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;
                    return {
                        results: data.results,
                        pagination: {
                            more: (params.page * 30) < data.total_count
                        }
                    };
                },
                cache: true
            },
            escapeMarkup: function(markup) {
                return markup;
            }, // let our custom formatter work
            minimumInputLength: 3,
            
        });
        $('#id_conductor_vehiculo').select2({
            language: 'es',      
            theme: "bootstrap4",   
            width: "100%",
            ajax: {
                url: "/conductor/conductor-autocomplete/",
                dataType: 'json',
                delay: 250,
                data: function(params) {
                    return {
                        q: params.term, // search term
                        page: params.page
                    };
                },
                processResults: function(data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;
                    return {
                        results: data.results,
                        pagination: {
                            more: (params.page * 30) < data.total_count
                        }
                    };
                },
                cache: true
            },
            escapeMarkup: function(markup) {
                return markup;
            }, // let our custom formatter work
            minimumInputLength: 3,
            
        });
        $('#id_equipo_carguio').select2({
            language: 'es',      
            theme: "bootstrap4",   
            width: "100%",
            ajax: {
                url: "/conductor/carguio-autocomplete/",
                dataType: 'json',
                delay: 250,
                data: function(params) {
                    return {
                        q: params.term, // search term
                        page: params.page
                    };
                },
                processResults: function(data, params) {
                    // parse the results into the format expected by Select2
                    // since we are using custom formatting functions we do not need to
                    // alter the remote JSON data, except to indicate that infinite
                    // scrolling can be used
                    params.page = params.page || 1;
                    return {
                        results: data.results,
                        pagination: {
                            more: (params.page * 30) < data.total_count
                        }
                    };
                },
                cache: true
            },
            escapeMarkup: function(markup) {
                return markup;
            }, // let our custom formatter work
            minimumInputLength: 3,
            
        });
        $('#id_origen').select2({
            language: 'es',      
            theme: "bootstrap4",   
            width: "100%",
            placeholder: "Seleccionar Origen",
        });    
        $('#id_destino').select2({
            language: 'es',      
            theme: "bootstrap4",   
            width: "100%",
            placeholder: "Seleccionar Destino",
        });
        myModal.show();
        const pesajeForm = document.querySelector("#pesaje-form");
        pesajeForm.addEventListener("submit", (e) => {
            e.preventDefault();
            postModal(pesajeForm);
        });
    });    
})

/**
 * Inicio del servicio 
 */
var webSocket   = null;
var ws_protocol = 'ws';
var ws_hostname = 'localhost';
var ws_port     = '1337';
var ws_endpoint = '';
var elwebsocket = null;
var elwebsocketIndicador = null;
var elwebsocketVisor = null
/**
 * Event handler for clicking on button "Connect"
 */
function iniciarWebSocket() {        
    openWSConnection(ws_protocol, ws_hostname, ws_port, ws_endpoint);
}
/**
 * Event handler for clicking on button "Disconnect"
 */
function detenerWebSocket() {
    webSocket.close();
}
/**
 * Open a new WebSocket connection using the given parameters
 */
function openWSConnection(protocol, hostname, port, endpoint) {
    var webSocketURL = null;
    webSocketURL = protocol + "://" + hostname + ":" + port + endpoint;
    console.log("openWSConnection::Connecting to: " + webSocketURL);
    try {
        webSocket = new WebSocket(webSocketURL);
        webSocket.onopen = function(openEvent) {
            console.log("WebSocket OPEN: " + JSON.stringify(openEvent, null, 4));            
        };
        webSocket.onclose = function (closeEvent) {
            console.log("WebSocket CLOSE: " + JSON.stringify(closeEvent, null, 4));
            // document.getElementById("btnSend").disabled       = true;
            // document.getElementById("btnConnect").disabled    = false;
            // document.getElementById("btnDisconnect").disabled = true;
        };
        webSocket.onerror = function (errorEvent) {
            console.log("WebSocket ERROR: " + JSON.stringify(errorEvent, null, 4));
            elwebsocketIndicador.classList.add("off");
        };
        webSocket.onmessage = function (messageEvent) {
            var wsMsg = messageEvent.data;
            console.log("WebSocket MESSAGE: " + wsMsg);
            if (wsMsg.indexOf("error") > 0) {
                document.getElementById("incomingMsgOutput").value += "error: " + wsMsg.error + "\r\n";
            } else {
                // document.getElementById("incomingMsgOutput").value += "message: " + wsMsg + "\r\n";
                // document.getElementById("serial-message").value = "message: " + wsMsg + "\r\n";
                elwebsocket.value = wsMsg;
                elwebsocketVisor.innerHTML = wsMsg;
                console.log("message: " + wsMsg + "\r\n")
            }
        };
    } catch (exception) {
        console.error(exception);
    }
}
/**
 * Send a message to the WebSocket server
 */
function onSendClick() {
    if (webSocket.readyState != WebSocket.OPEN) {
        console.error("webSocket is not open: " + webSocket.readyState);
        return;
    }
    var msg = document.getElementById("message").value;
    webSocket.send(msg);
}
