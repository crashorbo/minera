const loader = document.querySelector('.loader');
const bodyContent = document.querySelector(".conta-desktop--body-content");
const calculoTotal = document.querySelector(".calculo-total-valor");
const textoRegistros = document.querySelector(".texto-registros");
const imprimirComprobantes = document.querySelector("#imprimir-comprobantes");
const imprimirBoletas = document.querySelector("#imprimir-boletas");
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
                console.log(indices);
                calcularTotales();
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
            console.log("imprimiendo");
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
            console.log("imprimiendo");
            let url = window.URL.createObjectURL(blob);
            printJS(url);
        });
}