const loader = document.querySelector('.loader');
const bodyContent = document.querySelector(".conta-desktop--body-content");
const calculoTotal = document.querySelector(".calculo-total-valor");
const textoRegistros = document.querySelector(".texto-registros");
const imprimirComprobantes = document.querySelector("#imprimir-comprobantes");
const imprimirBoletas = document.querySelector("#imprimir-boletas");
const redoEspacio = document.querySelector("#redo-espacio");
const modalPagadas = document.querySelector("#cargas-pagadas");
const modalGeneral = document.querySelector("#reporte-general");
const formCargasPagadas = document.querySelector("#form-cargas-pagadas");
let indices = [];

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

window.addEventListener('DOMContentLoaded', (e) => {
    loader.style.visibility = 'hidden';
});

$('#select-boleta').select2({
    language: 'es',
    width: "60%",
    ajax: {
        url: "/pesaje/pesaje-autocomplete/",
        dataType: 'json',
        delay: 250,
        placeholder: "Select a state",
        allowClear: true,
        data: function (params) {
            return {
                q: params.term, // search term
                page: params.page
            };
        },
        processResults: function (data, params) {
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
    escapeMarkup: function (markup) {
        return markup;
    }, // let our custom formatter work
    minimumInputLength: 1,

});

$('#select-boleta').on('select2:select', async (e) => {
    let flag = true;

    indices.forEach((el) => {
        if (el == e.target.value) {
            flag = false;
        }
    });

    if (flag) {
        await axios(`/contabilidad/update/${e.target.value}/`)
            .then(res => {
                $('.conta-desktop--body-content').append(res.data);
                indices.push(e.target.value);
                calcularTotales();
                eliminarEventos();
                generarEventos();
            })
    }
});

bodyContent.addEventListener('click', (e) => {

    if (e.target.classList.contains('fa-minus-circle')) {
        eliminarRow(e.target);
    }
    if (e.target.classList.contains('fa-clipboard-check')) {
        pagarRow(e.target);
    }

    if (e.target.classList.contains('proveedor-item-link')) {
        modalProveedor(e.target);
    }

    if (e.target.classList.contains('carga-item-link')) {
        modalProveedor(e.target);
    }

    if (e.target.classList.contains('laboratorio-link')) {
        modalLaboratorio(e.target);
    }
});

bodyContent.addEventListener('change', (e) => {
    guardarRow(e.target);
})

const calcularTotales = () => {
    let montos = document.querySelectorAll('.carga-pagada');
    let totalMontos = 0;
    let totalRegistros = 0;
    montos.forEach(el => {
        let aux = parseFloat(el.getAttribute('data-value'));
        totalRegistros = totalRegistros + 1;
        totalMontos = totalMontos + aux;
    })
    textoRegistros.textContent = totalRegistros
    calculoTotal.textContent = totalMontos;

}

const eliminarRow = (el) => {
    const row = el.closest('.table-row');
    let aux = [];
    row.parentNode.removeChild(row);

    indices.forEach((el) => {
        if (row.getAttribute("data-id") != el) {
            aux.push(el);
        }
    })
    indices = aux;
    calcularTotales();
    eliminarEventos();
    generarEventos();
}

const guardarRow = async (el) => {
    const row = el.closest('.table-row');
    const url = row.getAttribute("action");
    const form = new FormData(row);
    await axios(url, {
        method: 'post',
        data: form
    }).then(res => {
        document.querySelector(`.total-descuento_${res.data.id}`).textContent = res.data.descuentos;
        document.querySelector(`.liquido-pagable_${res.data.id}`).textContent = res.data.pagable;
        document.querySelector(`.retencion-acuerdo_${res.data.id}`).textContent = res.data.retencion;
        eliminarEventos();
        generarEventos();
    });
}

const pagarRow = async (el) => {
    const row = el.closest('.table-row');
    const formData = new FormData();
    formData.append('id', row.getAttribute("data-id"));
    const request = new Request('/contabilidad/pagar-carga/', { headers: { 'X-CSRFToken': csrftoken } });
    await fetch(request, {
        method: 'post',
        mode: 'same-origin',
        body: formData
    })
        .then(res => res.text())
        .then(text => {
            row.innerHTML = text;
            calcularTotales();
            eliminarEventos();
            generarEventos();
        });
}

imprimirComprobantes.addEventListener('click', (e) => {
    e.preventDefault();
    printComprobantes();
})

imprimirBoletas.addEventListener('click', (e) => {
    e.preventDefault();
    printBoletas();
})

redoEspacio.addEventListener('click', (e) => {
    e.preventDefault();
    const rows = document.querySelectorAll('.table-row');
    rows.forEach(element => {
        element.parentNode.removeChild(element);
    });
    indices = [];
    calcularTotales();
    eliminarEventos();
    generarEventos();
})

const printComprobantes = async () => {
    const formData = new FormData();
    formData.append('indices', indices.toString());
    const request = new Request('/contabilidad/reporte/comprobantes/', { headers: { 'X-CSRFToken': csrftoken } });
    await fetch(request, {
        method: 'post',
        mode: 'same-origin',
        body: formData
    })
        .then(res => res.blob())
        .then(blob => {
            let url = window.URL.createObjectURL(blob);
            printJS(url);
        });
}

const printBoletas = async () => {
    const formData = new FormData();
    formData.append('indices', indices.toString());
    const request = new Request('/contabilidad/reporte/boletas/', { headers: { 'X-CSRFToken': csrftoken } });
    await fetch(request, {
        method: 'post',
        mode: 'same-origin',
        body: formData
    })
        .then(res => res.blob())
        .then(blob => {
            let url = window.URL.createObjectURL(blob);
            printJS(url);
        });
}

const modalProveedor = async (el) => {
    const row = el.closest('.table-row');
    let myModal = new bootstrap.Modal(document.getElementById('modalGen'));
    const modalBody = document.querySelector(".modal-content");
    const cargaId = row.getAttribute("data-id");
    const proveedorId = document.querySelector(`#proveedor-item_${row.getAttribute("data-id")}`).getAttribute("data-id");
    const origenId = document.querySelector(`#origen-item_${row.getAttribute("data-id")}`).getAttribute("data-id");
    const formData = new FormData();
    formData.append('proveedor', proveedorId);
    formData.append('origen', origenId);
    formData.append('carga', cargaId);
    const request = new Request('/contabilidad/proveedor-origen/', { headers: { 'X-CSRFToken': csrftoken } });
    await fetch(request, {
        method: 'post',
        mode: 'same-origin',
        body: formData
    })
        .then(res => res.text())
        .then(text => {
            modalBody.innerHTML = text;
            myModal.show();
        });
}

const modalLaboratorio = async (el) => {
    const row = el.closest('.table-row');
    let myModal = new bootstrap.Modal(document.getElementById('modalGen'));
    const modalBody = document.querySelector(".modal-content");
    const cargaId = row.getAttribute("data-id");
    const formData = new FormData();
    formData.append('carga', cargaId);
    const request = new Request('/contabilidad/laboratorios/', { headers: { 'X-CSRFToken': csrftoken } });
    await fetch(request, {
        method: 'post',
        mode: 'same-origin',
        body: formData
    })
        .then(res => res.text())
        .then(text => {
            modalBody.innerHTML = text;
            myModal.show();
        });
}

modalPagadas.addEventListener("click", () => {
    const hoy = new Date();
    let myModal = new bootstrap.Modal(document.getElementById('modalPagado'));
    const fechaInicio = new Datepicker(document.querySelector("#fecha-inicio"), {
        language: 'es',
        autohide: true,
        format: 'dd/mm/yyyy',
        container: '#modalPagado'
    });
    fechaInicio.setDate(`01/${hoy.getMonth() + 1}/${hoy.getFullYear()}`);
    const fechaFin = new Datepicker(document.querySelector("#fecha-fin"), {
        language: 'es',
        autohide: true,
        format: 'dd/mm/yyyy',
        container: '#modalPagado'
    });
    fechaFin.setDate(new Date());
    myModal.show();
});

modalGeneral.addEventListener("click", () => {
    const hoy = new Date();
    let myModal = new bootstrap.Modal(document.getElementById('modalGeneral'));
    const fechaInicio = new Datepicker(document.querySelector("#fecha-inicio-general"), {
        language: 'es',
        autohide: true,
        format: 'dd/mm/yyyy',
        container: '#modalGeneral'
    });
    fechaInicio.setDate(`01/${hoy.getMonth() + 1}/${hoy.getFullYear()}`);
    const fechaFin = new Datepicker(document.querySelector("#fecha-fin-general"), {
        language: 'es',
        autohide: true,
        format: 'dd/mm/yyyy',
        container: '#modalGeneral'
    });
    fechaFin.setDate(new Date());
    myModal.show();
});

const generarEventos = () => {

    const inputsCarguio = document.querySelectorAll('.tooltip-box-carguio');
    const inputsVolqueta = document.querySelectorAll('.tooltip-box-volqueta');

    inputsCarguio.forEach(element => {
        element.addEventListener("focus", (e) => {
            tooltipOn(e.target.closest('.table-row').getAttribute("data-id"), 'tooltip-box-carguio');
        })
        element.addEventListener("blur", (e) => {
            tooltipOff(e.target.closest('.table-row').getAttribute("data-id"), 'tooltip-box-carguio');
        })
    });

    inputsVolqueta.forEach(element => {
        element.addEventListener("focus", (e) => {
            tooltipOn(e.target.closest('.table-row').getAttribute("data-id"), 'tooltip-box-volqueta');
        })
        element.addEventListener("blur", (e) => {
            tooltipOff(e.target.closest('.table-row').getAttribute("data-id"), 'tooltip-box-volqueta');
        })
    });
}

const eliminarEventos = () => {

    const inputsCarguio = document.querySelectorAll('.tooltip-box-carguio');
    const inputsVolqueta = document.querySelectorAll('.tooltip-box-volqueta');

    inputsCarguio.forEach(element => {
        element.removeEventListener("focus", (e) => {
            tooltipOn(e.target.closest('.table-row').getAttribute("data-id"), 'tooltip-box-carguio');
        })
        element.removeEventListener("blur", (e) => {
            tooltipOff(e.target.closest('.table-row').getAttribute("data-id"), 'tooltip-box-carguio');
        })
    });
    inputsVolqueta.forEach(element => {
        element.removeEventListener("focus", (e) => {
            tooltipOn(e.target.closest('.table-row').getAttribute("data-id"), 'tooltip-box-volqueta');
        })
        element.removeEventListener("blur", (e) => {
            tooltipOff(e.target.closest('.table-row').getAttribute("data-id"), 'tooltip-box-volqueta');
        })
    });
}


const tooltipOn = (e, nombre) => {
    const elTool = document.querySelector(`#${nombre}__${e}`);
    elTool.style.display = "block";
};

const tooltipOff = (e, nombre) => {
    const elTool = document.querySelector(`#${nombre}__${e}`);
    elTool.style.display = "none";
};
// formCargasPagadas.addEventListener("submit", async (e) => {
//     e.preventDefault();
//     const dataForm = new FormData(e.target)
//     await axios('/contabilidad/reporte-cargas-pagadas/', {
//         method: 'post',
//         data: dataForm,
//         responseType: 'blob',
//     }).then(
//         res => {
//             console.log(res.data);
//         }
//     )
// })