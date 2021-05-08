const loader = document.querySelector('.loader');
const containerDetalle = document.querySelector("#detalle");
const modalContent = document.querySelector(".modal-content");
const btnRefresh = document.querySelector("#btn-refresh");
const myModal = new bootstrap.Modal(document.querySelector('#exampleModal'));
const datatable = $('#cargas').DataTable({
    "language" : {
        "thousands":      ".",
        "decimal":        ",",
        "emptyTable":     "Ningún dato disponible en esta tabla",
        "info":           "(_START_ - _END_) Total: _TOTAL_ registros",
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
    "scrollX": true,
    "responsive": true,
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

containerDetalle.addEventListener("click", async (e) => {
    e.preventDefault()
    if (e.target.getAttribute("id") === "carga-pagar"){
        await axios(e.target.getAttribute("data-url"))
        .then(res => {
            modalContent.innerHTML = res.data;
            const pagarForm = document.querySelector("#form-pagar-carga");
            myModal.show();
            pagarForm.addEventListener("submit", async (e) => {
                e.preventDefault();
                const liquidoPagable = document.querySelector('#liquido-pagable');
                let monto = +(liquidoPagable.textContent.replace(',', ''));
                let id_proveedor = document.querySelector(".proveedor-id-hidden").textContent;
                let proveedor_nombre = document.querySelector(".proveedor-nombre").textContent;                
                await axios(pagarForm.getAttribute("action"), {
                    method: "post",
                    data: new FormData(pagarForm)
                })
                .then(res => {              
                    containerDetalle.innerHTML = res.data;
                    sumarPagos(id_proveedor.trim(), proveedor_nombre.trim(), monto);
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
            })
        })
    } 
    if (e.target.getAttribute("id") === "generar-boleta") {
        e.preventDefault();
        printJS(e.target.dataset.url);
        //window.open(e.target.dataset.url,"_blank","height=500,width=700,status=no,toolbar=no,menubar=no,location=no,scrollbars=yes");
    }
})

const sumarPagos = (id, nombre, monto) => {
    let aux_id = localStorage.getItem('idProveedor');
    let aux_proveedor = localStorage.getItem('nombreProveedor');
    let aux_monto = + (localStorage.getItem('monto'));
    let aux_montos = localStorage.getItem('montos');
    const proveedorNombre = document.querySelector('.proovedor-card__nombre');
    const proveedorTotal = document.querySelector('.proveedor-card__total'); 
    const proveedorMontos = document.querySelector('.proveedor-card__montos');    
    if (id === aux_id) {
        aux_monto = aux_monto + monto;
        aux_montos = `${aux_montos} + ${monto} `;
        localStorage.setItem('monto', aux_monto);
        localStorage.setItem('montos', aux_montos);
    } else {
        aux_id = id;
        aux_proveedor = nombre
        aux_monto = monto;        
        aux_montos = `${aux_monto}`;
        localStorage.setItem('idProveedor', aux_id),
        localStorage.setItem('nombreProveedor', aux_proveedor),
        localStorage.setItem('monto', aux_monto);
        localStorage.setItem('montos', aux_montos);
    }        
    proveedorNombre.innerHTML = aux_proveedor;
    proveedorTotal.innerHTML = `${aux_monto} Bs.`;
    proveedorMontos.innerHTML = aux_montos;
}

const visorPagos = () => {
    let aux_id = localStorage.getItem('idProveedor');
    let aux_proveedor = localStorage.getItem('nombreProveedor');
    let aux_monto = + (localStorage.getItem('monto'));
    let aux_montos = localStorage.getItem('montos');
    const proveedorNombre = document.querySelector('.proovedor-card__nombre');
    const proveedorTotal = document.querySelector('.proveedor-card__total');    
    const proveedorMontos = document.querySelector('.proveedor-card__montos');    
    proveedorNombre.innerHTML = aux_proveedor;
    proveedorTotal.innerHTML = `${aux_monto} Bs.`;
    proveedorMontos.innerHTML = aux_montos;
}

btnRefresh.addEventListener('click', (e) => {
    localStorage.setItem('idProveedor', ''),
    localStorage.setItem('nombreProveedor', ''),
    localStorage.setItem('monto', '');
    localStorage.setItem('montos', '');    
    const proveedorNombre = document.querySelector('.proovedor-card__nombre');
    const proveedorTotal = document.querySelector('.proveedor-card__total');    
    const proveedorMontos = document.querySelector('.proveedor-card__montos');    
    proveedorNombre.innerHTML = '';
    proveedorTotal.innerHTML = '0 Bs.';
    proveedorMontos.innerHTML = '';
})

window.addEventListener('DOMContentLoaded', (e) => {
    visorPagos();
    loader.style.visibility = 'hidden';   
});