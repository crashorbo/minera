const loader = document.querySelector('.loader');
const detalle = document.querySelector("#detalle");
const addLaboratorios = document.querySelector("#laboratorios-form");
const modalContent = document.querySelector(".modal-content");
const myModal = new bootstrap.Modal(document.querySelector('#exampleModal'));
const datatable = $('#cargas').DataTable({
    "language" : {
        "thousands":      ".",
        "decimal":        ",",
        "emptyTable":     "Ningún dato disponible en esta tabla",
        "info":           "(_START_ - _END_) total: _TOTAL_ registros",
        "infoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
        "infoFiltered":   "(filtrado de un total de _MAX_ registros)",
        "infoPostFix":    "",
        "thousands":      ",",
        "lengthMenu":     "Ver _MENU_ entradas",
        "loadingRecords": "Cargando...",
        "processing":     "Procesando...",
        "search":         "Buscar:",
        "zeroRecords":    "No se encontraron resultados",
        "paginate": {
            "first":      "Primero",
            "last":       "Ultimo",
            "next":       "Siguiente",
            "previous":   "Anterior"
        },
        "aria": {
            "sortAscending":  ": Activar para ordenar la columna de manera ascendente",
            "sortDescending": ": Activar para ordenar la columna de manera descendente"
        }
    },    
    "processing": true,
    "serverSide": true,
    "ajax": "/laboratorio/list/json/",           
});

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

const tabla = document.querySelector("#cargas");

$('#cargas').on( 'click', 'tbody tr', async (e) =>  {    
    const url = e.target.closest('tr').children[0].children[0].getAttribute("data-url");    
    loader.style.visibility = 'visible';   
    await axios(url)
    .then(res => {
        detalle.innerHTML = res.data;
        const containerList = document.querySelector("#muestras-list");
        loader.style.visibility = 'hidden';   
        $('#id_codigo_generado').select2({
            language: 'es',      
            theme: "bootstrap4",   
            width: "100%",
            ajax: {
                url: "/user/codigo-autocomplete/",
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
        muestrasList(containerList.getAttribute("data-url"), containerList)
    })
} );

detalle.addEventListener("submit", async (e) => {
    e.preventDefault();     
    const containerList = document.querySelector("#muestras-list");   
    loader.style.visibility = 'visible';   
    await axios(e.target.getAttribute("action"), {
        method: "post",
        data: new FormData(e.target)
    })
    .then(res => {              
        Toast.fire({
            icon: 'success',
            title: res.data.message
        });                          
        muestrasList(containerList.getAttribute("data-url"), containerList)
        datatable.ajax.reload( null, false);
        loader.style.visibility = 'hidden';   
        $("#id_codigo_generado").empty().trigger('change')        
    })
    .catch(error => {
        const parseado = JSON.parse(error.response.data.message)                        
        Toast.fire({
            icon: 'error',
            title: JSON.stringify(parseado)
        })
    })
});

const muestrasList = async (url, container) => {
    loader.style.visibility = 'visible';   
    await axios(url)
    .then( res => {
        container.innerHTML = res.data;
        loader.style.visibility = 'hidden';   
        $('#muestras-list').on( 'click', 'tbody tr', async (e) =>  {    
            const url = e.target.closest('tr').getAttribute("data-url");                
            await axios(url)
            .then(res => {
                modalContent.innerHTML = res.data;
                const containerList = document.querySelector("#muestras-list");
                myModal.show();
                const formMuestra = document.querySelector("#form-muestra");
                formMuestra.addEventListener("submit", async (e) => {
                    e.preventDefault();
                    loader.style.visibility = 'visible';   
                    await axios(formMuestra.getAttribute("action"), {
                        method: "post",
                        data: new FormData(formMuestra)
                    })
                    .then(res => {              
                        Toast.fire({
                            icon: 'success',
                            title: res.data.message
                        });   
                        muestrasList(containerList.getAttribute("data-url"), containerList)                                               
                        loader.style.visibility = 'hidden';   
                        myModal.hide();
                    })
                    .catch(error => {
                        const parseado = JSON.parse(error.response.data.message)                        
                        Toast.fire({
                            icon: 'error',
                            title: JSON.stringify(parseado)
                        })
                    })
                })
            })
        });
    })
}

window.addEventListener('DOMContentLoaded', (e) => {
    loader.style.visibility = 'hidden';   
});