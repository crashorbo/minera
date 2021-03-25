const pesajeCreate = document.querySelector("#pesaje-create");
const modalContent = document.querySelector(".modal-content");
const myModal = new bootstrap.Modal(document.querySelector('#exampleModal'));
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
            $('#id_carguio').select2({
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

pesajeCreate.addEventListener("click", async () => {    
    await axios(pesajeCreate.getAttribute("data-url"))
    .then(res => {
        modalContent.innerHTML =res.data;        
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
        $('#id_carguio').select2({
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