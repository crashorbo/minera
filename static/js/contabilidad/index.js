const containerDetalle = document.querySelector("#detalle");
const datatable = $('#cargas').DataTable({
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
    "ajax": "/contabilidad/list/json/",           
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
    await axios(url)
    .then(res => {
        detalle.innerHTML = res.data;        
    })
} );

containerDetalle.addEventListener("change", async (e) => {        
    e.preventDefault();
    const liquidoPagable = document.querySelector("#liquido-pagable");
    const totalDescuentos = document.querySelector("#total-descuentos");
    const contabilidadForm = document.querySelector("#contabilidad-form");
    console.log(contabilidadForm);
    await axios(contabilidadForm.getAttribute("action"), {
        method: "post",
        data: new FormData(contabilidadForm)
    })
    .then(res => {                                                    
        totalDescuentos.textContent = res.data.descuentos;
        liquidoPagable.textContent = res.data.pagable;
    })
    .catch(error => {
        const parseado = JSON.parse(error.response.data.message)                        
        Toast.fire({
            icon: 'error',
            title: JSON.stringify(parseado)
        })
    })
});