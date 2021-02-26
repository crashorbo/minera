const datatable = $('#vehiculos').DataTable({
    "language" : {
        "thousands":      ".",
        "decimal":        ",",
        "emptyTable":     "Ningún dato disponible en esta tabla",
        "info":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
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
    "ajax": "/conductor/list/json/",  
    "columnDefs": [ 
        {
            "targets": 7,
            "orderable": false
        } 
    ],       
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

const vehiculosTable = document.querySelector("#vehiculos");
const vehiculoCreate = document.querySelector("#vehiculo-create");
const modalContent = document.querySelector(".modal-content");
const myModal = new bootstrap.Modal(document.querySelector('#exampleModal'));

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
        datatable.ajax.reload( null, false);                                              
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

vehiculoCreate.addEventListener("click", (e) => {
    e.preventDefault();
    getModal(e.target.dataset.url)
    .then(() => {
        const proveedorForm = document.querySelector("#vehiculo-form");
        proveedorForm.addEventListener("submit", (e) => {
            e.preventDefault();
            postModal(e.target);
        })
    });    
});

vehiculosTable.addEventListener("click", (e) => {    
    if (e.target.classList.contains("bi")) {
        e.preventDefault()
        getModal(e.target.dataset.url)
        .then(() => {
            const vehiculoForm = document.querySelector("#vehiculo-form");
            vehiculoForm.addEventListener("submit", (e) => {
                e.preventDefault();
                postModal(e.target);
            })
        });
    }    
})