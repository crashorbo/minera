const loader = document.querySelector('.loader');
const vehiculos = $('#vehiculos').DataTable({
    "language": {
        "thousands": ".",
        "decimal": ",",
        "emptyTable": "Ningún dato disponible en esta tabla",
        "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
        "infoFiltered": "(filtrado de un total de _MAX_ registros)",
        "infoPostFix": "",
        "thousands": ",",
        "lengthMenu": "Ver _MENU_ entradas",
        "loadingRecords": "Cargando...",
        "processing": "Procesando...",
        "search": "Buscar:",
        "zeroRecords": "No se encontraron resultados",
        "paginate": {
            "first": "Primero",
            "last": "Ultimo",
            "next": "Siguiente",
            "previous": "Anterior"
        },
        "aria": {
            "sortAscending": ": Activar para ordenar la columna de manera ascendente",
            "sortDescending": ": Activar para ordenar la columna de manera descendente"
        }
    },
    "processing": true,
    "serverSide": true,
    "scrollX": true,
    "responsive": true,
    "ajax": "/conductor/list/json/",
    "columnDefs": [
        {
            "targets": 7,
            "orderable": false
        }
    ],
});

const conductores = $('#conductores').DataTable({
    "language": {
        "thousands": ".",
        "decimal": ",",
        "emptyTable": "Ningún dato disponible en esta tabla",
        "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
        "infoFiltered": "(filtrado de un total de _MAX_ registros)",
        "infoPostFix": "",
        "thousands": ",",
        "lengthMenu": "Ver _MENU_ entradas",
        "loadingRecords": "Cargando...",
        "processing": "Procesando...",
        "search": "Buscar:",
        "zeroRecords": "No se encontraron resultados",
        "paginate": {
            "first": "Primero",
            "last": "Ultimo",
            "next": "Siguiente",
            "previous": "Anterior"
        },
        "aria": {
            "sortAscending": ": Activar para ordenar la columna de manera ascendente",
            "sortDescending": ": Activar para ordenar la columna de manera descendente"
        }
    },
    "processing": true,
    "serverSide": true,
    "scrollX": true,
    "responsive": true,
    "ajax": "/conductor/conductor/list/json/",
    "columnDefs": [
        {
            "targets": 3,
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
const conductoresTable = document.querySelector("#conductores");
const conductorCreate = document.querySelector("#conductor-create");
const modalContent = document.querySelector(".modal-content");
const myModal = new bootstrap.Modal(document.querySelector('#exampleModal'));

const getModal = async (url) => {
    loader.style.visibility = 'visible';
    await axios(url)
        .then(res => {
            modalContent.innerHTML = res.data
            loader.style.visibility = 'hidden';
        });
    myModal.show();
}

const postModal = async (datosForm, datatable) => {
    loader.style.visibility = 'visible';
    await axios(datosForm.getAttribute("action"), {
        method: "post",
        data: new FormData(datosForm)
    })
        .then(res => {
            Toast.fire({
                icon: 'success',
                title: res.data.message
            });
            datatable.ajax.reload(null, false);
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
}

vehiculoCreate.addEventListener("click", (e) => {
    e.preventDefault();
    getModal(e.target.dataset.url)
        .then(() => {
            const proveedorForm = document.querySelector("#vehiculo-form");
            proveedorForm.addEventListener("submit", (e) => {
                e.preventDefault();
                postModal(e.target, vehiculos);
            })
        });
});

vehiculosTable.addEventListener("click", (e) => {
    if (e.target.classList.contains("bi-pencil-square")) {
        e.preventDefault()
        console.log(e.target.dataset.url);
        getModal(e.target.dataset.url)
            .then(() => {
                const vehiculoForm = document.querySelector("#vehiculo-form");
                vehiculoForm.addEventListener("submit", (e) => {
                    e.preventDefault();
                    postModal(e.target, vehiculos);
                })
            });
    }
    if (e.target.classList.contains("bi-trash")) {
        e.preventDefault();
        console.log(e.target.dataset.url);
        getModal(e.target.dataset.url)
            .then(() => {
                const vehiculoForm = document.querySelector("#vehiculo-form");
                vehiculoForm.addEventListener("submit", (e) => {
                    e.preventDefault();
                    postModal(e.target, vehiculos);
                })
            });
    }
})

conductorCreate.addEventListener("click", (e) => {
    e.preventDefault();
    getModal(e.target.dataset.url)
        .then(() => {
            const proveedorForm = document.querySelector("#conductor-form");
            proveedorForm.addEventListener("submit", (e) => {
                e.preventDefault();
                postModal(e.target, conductores);
            })
        });
});

conductoresTable.addEventListener("click", (e) => {
    if (e.target.classList.contains("bi-pencil-square")) {
        e.preventDefault()
        getModal(e.target.dataset.url)
            .then(() => {
                const vehiculoForm = document.querySelector("#conductor-form");
                vehiculoForm.addEventListener("submit", (e) => {
                    e.preventDefault();
                    postModal(e.target, conductores);
                })
            });
    }
    if (e.target.classList.contains("bi-trash")) {
        e.preventDefault()
        getModal(e.target.dataset.url)
            .then(() => {
                const vehiculoForm = document.querySelector("#conductor-form");
                vehiculoForm.addEventListener("submit", (e) => {
                    e.preventDefault();
                    postModal(e.target, conductores);
                })
            });
    }
})

window.addEventListener('DOMContentLoaded', (e) => {
    loader.style.visibility = 'hidden';
});