const loader = document.querySelector('.loader');
const detalle = document.querySelector("#detalle");
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
    "ajax": "/paleta/list/json/",           
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
        // if (document.querySelector("#id_fecha_paleta")) {
        //     const fechaPaleta = new Datepicker(document.querySelector("#id_fecha_paleta"), {
        //         language: 'es',    
        //         autohide: true,
        //     });
        //     fechaPaleta.setDate(new Date());
        // }
        loader.style.visibility = 'hidden';
    })
} );

detalle.addEventListener("submit", async (e) => {
    e.preventDefault();    
    await axios(e.target.getAttribute("action"), {
        method: "post",
        data: new FormData(e.target)
    })
    .then(res => {              
        Toast.fire({
            icon: 'success',
            title: res.data.message
        });                          
        datatable.ajax.reload( null, false);                                                              
    })
    .catch(error => {
        const parseado = JSON.parse(error.response.data.message)                        
        Toast.fire({
            icon: 'error',
            title: JSON.stringify(parseado)
        })
    })
});

window.addEventListener('DOMContentLoaded', (e) => {
    loader.style.visibility = 'hidden';   
});