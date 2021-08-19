const loader = document.querySelector('.loader');

window.addEventListener('DOMContentLoaded', (e) => {
    loader.style.visibility = 'hidden';
});

const datatable = $('#produccion').DataTable({
    "language": {
        "thousands": ".",
        "decimal": ",",
        "emptyTable": "Ningún dato disponible en esta tabla",
        "info": "(_START_ - _END_) total: _TOTAL_ registros",
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
    // "processing": true,
    // "serverSide": true,
    // "ajax": "/laboratorio/list/json/",
});