const bodyConf = document.querySelector("#body-conf");
const ulMenu = document.querySelector(".list-group-flush");
const modalContent = document.querySelector(".modal-content");
const myModal = new bootstrap.Modal(document.querySelector('#exampleModal'));

let url, selector = '';

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

const subMenuReset = (selector) => {
    const elms = document.querySelectorAll(".list-group-item");
    elms.forEach(elm => {
        elm.classList.remove('active');
    })
    selector.classList.add("active");
}

document.addEventListener('DOMContentLoaded', function () {
    cargarPerfil(bodyConf.getAttribute("data-url"));
    subMenuReset(ulMenu.querySelector("#selector-perfil"));
});


ulMenu.addEventListener("click", (e) => {
    e.preventDefault();

    if (e.target.getAttribute("href")) {
        url = e.target.getAttribute("href");
        selector = e.target.parentNode;
    }
    else {
        url = e.target.firstElementChild.getAttribute("href")
        selector = e.target;
    }

    if (selector.getAttribute("id") == "selector-perfil") {
        subMenuReset(selector);
        cargarPerfil(url);
    }
    if (selector.getAttribute("id") == "selector-usuario") {
        subMenuReset(selector);
        cargarUsuario(url);
    }
    if (selector.getAttribute("id") == "selector-parametro") {
        subMenuReset(selector);
        cargarParametro(url);
    }
    if (selector.getAttribute("id") == "selector-ubicacion") {
        subMenuReset(selector);
        cargarUbicacion(url);
    }
    if (selector.getAttribute("id") == "selector-laboratorio") {
        subMenuReset(selector);
        cargarLaboratorio(url);
    }
})

const cargarPerfil = async (url) => {
    // loader
    const loader = document.querySelector('.loader');
    loader.style.visibility = 'visible';
    //
    await axios(url)
        .then(res => {
            bodyConf.innerHTML = res.data;
            // loader
            const loader = document.querySelector('.loader');
            loader.style.visibility = 'hidden';
            const changePassword = document.querySelector("#cambiar-password");
            //
            const photo = document.querySelector("#id_photo");
            const formUpdate = document.querySelector("#edit-user-form")

            changePassword.addEventListener('click', async (e) => {
                e.preventDefault();
                await axios(e.target.getAttribute('data-url'))
                    .then(res => {
                        bodyConf.innerHTML = res.data;
                        const formPass = document.querySelector("#form-password");
                        formPass.addEventListener("submit", async (e) => {
                            e.preventDefault();
                            axios(formPass.getAttribute("action"), {
                                method: "post",
                                data: new FormData(formPass)
                            })
                                .then(res => {
                                    bodyConf.innerHTML = res.data;
                                })
                        })
                    })
            })

            photo.addEventListener('change', e => {
                console.log(photo)
                if (e.target.files.length > 0) {
                    const src = URL.createObjectURL(e.target.files[0]);
                    const preview = document.querySelector("#preview-img");
                    preview.src = src;
                }
            })
            formUpdate.addEventListener("submit", async (e) => {
                e.preventDefault();
                await axios(e.target.getAttribute("action"), {
                    method: 'post',
                    data: new FormData(e.target)
                })
                    .then(res => {
                        Toast.fire({
                            icon: 'success',
                            title: res.data.message
                        })
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

const cargarUsuario = async (url) => {
    // loader
    const loader = document.querySelector('.loader');
    loader.style.visibility = 'visible';
    //            
    await axios(url)
        .then(res => {
            bodyConf.innerHTML = res.data;
            // loader        
            loader.style.visibility = 'hidden';
            //            
            const userRegister = document.querySelector("#user-register");
            const usuarioList = document.querySelector("#usuario-list");
            userRegister.addEventListener("click", async () => {
                myModal.show();
                await axios(userRegister.getAttribute("data-url"))
                    .then(res => {
                        modalContent.innerHTML = res.data;
                        const formRegister = document.querySelector("#form-register-user");
                        formRegister.addEventListener("submit", async (e) => {
                            e.preventDefault();

                            await axios(e.target.getAttribute("action"), {
                                method: 'post',
                                data: new FormData(e.target)
                            })
                                .then(res => {
                                    Toast.fire({
                                        icon: 'success',
                                        title: res.data.message
                                    });
                                    cargarUsuario(url);
                                    myModal.hide();
                                })
                                .catch(error => {
                                    const parseado = JSON.parse(error.response.data.message)
                                    Toast.fire({
                                        icon: 'error',
                                        title: JSON.stringify(parseado)
                                    })
                                })
                        });
                    })
            })
            usuarioList.addEventListener("click", async (e) => {
                if (e.target.classList.contains('bi')) {
                    await axios(e.target.getAttribute("data-url"))
                        .then(res => {
                            modalContent.innerHTML = res.data;
                            const usuarioForm = document.querySelector("#usuario-form");
                            myModal.show();
                            usuarioForm.addEventListener("submit", async (e) => {
                                e.preventDefault();
                                await axios(usuarioForm.getAttribute('action'), {
                                    method: "post",
                                    data: new FormData(usuarioForm)
                                })
                                    .then(res => {
                                        Toast.fire({
                                            icon: 'success',
                                            title: res.data.message
                                        });
                                        myModal.hide();
                                        cargarUsuario(url);
                                    })
                                    .catch(error => {
                                        const parseado = JSON.parse(error.response.data.message)
                                        Toast.fire({
                                            icon: 'error',
                                            title: JSON.stringify(parseado)
                                        })
                                    })
                            });
                        })
                }
            })
        })
}

const cargarParametro = async (url) => {
    // loader
    const loader = document.querySelector('.loader');
    loader.style.visibility = 'visible';
    //
    await axios(url)
        .then(res => {
            bodyConf.innerHTML = res.data;
            // loader        
            loader.style.visibility = 'hidden';
            //    
            const btnCotizacion = document.querySelector("#cotizacion-register");
            const btnFactor = document.querySelector("#factor-register");
            const cotizaciones = document.querySelector("#cotizaciones");
            const datatable = $('#cotizaciones').DataTable({
                "language": {
                    "thousands": ".",
                    "decimal": ",",
                    "emptyTable": "Ningún dato disponible en esta tabla",
                    "info": "Mostrando del _START_ al _END_ de _TOTAL_ registros",
                    "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                    "infoFiltered": "(filtrado de un total de _MAX_ registros)",
                    "infoPostFix": "",
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
                "ajax": "/user/parametro/cotizacion/json/",
                "columnDefs": [
                    {
                        "targets": 3,
                        "orderable": false
                    }
                ],
                "searching": false,
            });

            const factores = async () => {
                const factorBody = document.querySelector("#factores");
                await axios(factorBody.getAttribute('data-url'))
                    .then(res => {
                        factorBody.innerHTML = res.data
                        const editores = factorBody.querySelectorAll('i');
                        editores.forEach(editor => {
                            editor.addEventListener("click", async () => {
                                await axios(editor.getAttribute("data-url"))
                                    .then(res => {
                                        modalContent.innerHTML = res.data;
                                        const formRegister = document.querySelector("#factor-form");
                                        myModal.show();
                                        formRegister.addEventListener("submit", async (e) => {
                                            e.preventDefault();
                                            await axios(formRegister.getAttribute("action"), {
                                                method: "post",
                                                data: new FormData(formRegister)
                                            })
                                                .then(res => {
                                                    Toast.fire({
                                                        icon: 'success',
                                                        title: res.data.message
                                                    });
                                                    factores();
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
                            })
                        });
                    })
            }
            factores();

            cotizaciones.addEventListener("click", async (e) => {
                if (e.target.classList.contains("bi")) {
                    await axios(e.target.getAttribute("data-url"))
                        .then(res => {
                            modalContent.innerHTML = res.data;
                            const fechaInicio = document.querySelector("#id_fecha_inicio");
                            const fechaFin = document.querySelector("#id_fecha_fin");
                            const formUpdate = document.querySelector("#cotizacion-form");
                            if (fechaInicio) {
                                const fechaInicioDP = new Datepicker(fechaInicio, {
                                    language: 'es',
                                    autohide: true,
                                    container: '.modal-content',
                                });
                            }
                            if (fechaFin) {
                                const fechaFinDP = new Datepicker(fechaFin, {
                                    language: 'es',
                                    autohide: true,
                                    container: '.modal-content',
                                });
                            }
                            myModal.show();
                            formUpdate.addEventListener("submit", async (e) => {
                                e.preventDefault();
                                await axios(formUpdate.getAttribute('action'), {
                                    method: "post",
                                    data: new FormData(formUpdate)
                                })
                                    .then(res => {
                                        Toast.fire({
                                            icon: 'success',
                                            title: res.data.message
                                        });
                                        datatable.ajax.reload(null, false);
                                        myModal.hide();
                                    })
                                    .catch(error => {
                                        const parseado = JSON.parse(error.response.data.message)
                                        Toast.fire({
                                            icon: 'error',
                                            title: JSON.stringify(parseado)
                                        })
                                    })
                            });
                        })
                }
            })

            btnFactor.addEventListener("click", async (e) => {
                await axios(e.target.getAttribute("data-url"))
                    .then(res => {
                        modalContent.innerHTML = res.data;
                        const formRegister = document.querySelector("#factor-form");
                        myModal.show();
                        formRegister.addEventListener("submit", async (e) => {
                            e.preventDefault();
                            await axios(formRegister.getAttribute('action'), {
                                method: "post",
                                data: new FormData(formRegister)
                            })
                                .then(res => {
                                    Toast.fire({
                                        icon: 'success',
                                        title: res.data.message
                                    });
                                    factores()
                                    myModal.hide();
                                })
                                .catch(error => {
                                    const parseado = JSON.parse(error.response.data.message)
                                    Toast.fire({
                                        icon: 'error',
                                        title: JSON.stringify(parseado)
                                    })
                                })
                        });
                    })
            })

            btnCotizacion.addEventListener("click", async (e) => {
                await axios(e.target.getAttribute("data-url"))
                    .then(res => {
                        modalContent.innerHTML = res.data;
                        const fechaInicio = document.querySelector("#id_fecha_inicio");
                        const fechaFin = document.querySelector("#id_fecha_fin");
                        const formRegister = document.querySelector("#cotizacion-form");
                        const fechaInicioDP = new Datepicker(fechaInicio, {
                            language: 'es',
                            autohide: true,
                            container: '.modal-content',
                        });
                        const fechaFinDP = new Datepicker(fechaFin, {
                            language: 'es',
                            autohide: true,
                            container: '.modal-content',
                        });
                        myModal.show();
                        formRegister.addEventListener("submit", async (e) => {
                            e.preventDefault();
                            await axios(formRegister.getAttribute('action'), {
                                method: "post",
                                data: new FormData(formRegister)
                            })
                                .then(res => {
                                    Toast.fire({
                                        icon: 'success',
                                        title: res.data.message
                                    });
                                    datatable.ajax.reload(null, false);
                                    myModal.hide();
                                })
                                .catch(error => {
                                    const parseado = JSON.parse(error.response.data.message)
                                    Toast.fire({
                                        icon: 'error',
                                        title: JSON.stringify(parseado)
                                    })
                                })
                        });
                    })
            })
        })
}
const cargarUbicacion = async (url) => {
    // loader
    const loader = document.querySelector('.loader');
    loader.style.visibility = 'visible';
    //
    await axios(url)
        .then(res => {
            bodyConf.innerHTML = res.data;
            // loader        
            loader.style.visibility = 'hidden';
            //     
            const btnDestino = document.querySelector("#destino-register");
            const btnOrigen = document.querySelector("#origen-register");
            const destinos = async () => {
                const destinoBody = document.querySelector("#destinos");
                await axios(destinoBody.getAttribute('data-url'))
                    .then(res => {
                        destinoBody.innerHTML = res.data
                        const editores = destinoBody.querySelectorAll('i');
                        editores.forEach(editor => {
                            editor.addEventListener("click", async () => {
                                await axios(editor.getAttribute("data-url"))
                                    .then(res => {
                                        modalContent.innerHTML = res.data;
                                        const formRegister = document.querySelector("#destino-form");
                                        myModal.show();
                                        formRegister.addEventListener("submit", async (e) => {
                                            e.preventDefault();
                                            await axios(formRegister.getAttribute("action"), {
                                                method: "post",
                                                data: new FormData(formRegister)
                                            })
                                                .then(res => {
                                                    Toast.fire({
                                                        icon: 'success',
                                                        title: res.data.message
                                                    });
                                                    destinos();
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
                            })
                        });
                    })
            }
            destinos();

            const origenes = async () => {
                const origenBody = document.querySelector("#origenes");
                await axios(origenBody.getAttribute('data-url'))
                    .then(res => {
                        origenBody.innerHTML = res.data
                        const editores = origenBody.querySelectorAll('i');
                        editores.forEach(editor => {
                            editor.addEventListener("click", async () => {
                                await axios(editor.getAttribute("data-url"))
                                    .then(res => {
                                        modalContent.innerHTML = res.data;
                                        const formRegister = document.querySelector("#origen-form");
                                        myModal.show();
                                        formRegister.addEventListener("submit", async (e) => {
                                            e.preventDefault();
                                            await axios(formRegister.getAttribute("action"), {
                                                method: "post",
                                                data: new FormData(formRegister)
                                            })
                                                .then(res => {
                                                    Toast.fire({
                                                        icon: 'success',
                                                        title: res.data.message
                                                    });
                                                    origenes();
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
                            })
                        });
                    })
            }
            origenes();

            btnDestino.addEventListener("click", async (e) => {
                await axios(e.target.getAttribute("data-url"))
                    .then(res => {
                        modalContent.innerHTML = res.data;
                        const formRegister = document.querySelector("#destino-form");
                        myModal.show();
                        formRegister.addEventListener("submit", async (e) => {
                            e.preventDefault();
                            await axios(formRegister.getAttribute("action"), {
                                method: "post",
                                data: new FormData(formRegister)
                            })
                                .then(res => {
                                    Toast.fire({
                                        icon: 'success',
                                        title: res.data.message
                                    });
                                    destinos();
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
            btnOrigen.addEventListener("click", async (e) => {
                await axios(e.target.getAttribute("data-url"))
                    .then(res => {
                        modalContent.innerHTML = res.data;
                        const formRegister = document.querySelector("#origen-form");
                        myModal.show();
                        formRegister.addEventListener("submit", async (e) => {
                            e.preventDefault();
                            await axios(formRegister.getAttribute("action"), {
                                method: "post",
                                data: new FormData(formRegister)
                            })
                                .then(res => {
                                    Toast.fire({
                                        icon: 'success',
                                        title: res.data.message
                                    });
                                    origenes();
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
        });
}

const cargarLaboratorio = async (url) => {
    // loader
    const loader = document.querySelector('.loader');
    loader.style.visibility = 'visible';
    await axios(url)
        .then(res => {
            bodyConf.innerHTML = res.data;
            // loader        
            loader.style.visibility = 'hidden';
            //
            const btnGenerador = document.querySelector("#generador-register");
            const btnLaboratorio = document.querySelector("#laboratorio-register");
            const generadorBody = document.querySelector("#generador");
            const generador = $('#generador').DataTable({
                "language": {
                    "thousands": ".",
                    "decimal": ",",
                    "emptyTable": "Ningún dato disponible en esta tabla",
                    "info": "Mostrando del _START_ al _END_ de _TOTAL_ registros",
                    "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                    "infoFiltered": "(filtrado de un total de _MAX_ registros)",
                    "infoPostFix": "",
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
                "ajax": "/user/parametro/generador/json/",
                "columnDefs": [
                    {
                        "targets": 2,
                        "orderable": false
                    }
                ],
                "searching": false,
            });

            generadorBody.addEventListener("click", async (e) => {
                if (e.target.classList.contains("bi-printer")) {
                    printJS(e.target.dataset.url);
                    // window.open(e.target.dataset.url,"_blank","height=500,width=700,status=no,toolbar=no,menubar=no,location=no,scrollbars=yes");
                }
            })

            const laboratorios = async () => {
                const laboratorioBody = document.querySelector("#laboratorios");
                await axios(laboratorioBody.getAttribute('data-url'))
                    .then(res => {
                        laboratorioBody.innerHTML = res.data
                        const editores = laboratorioBody.querySelectorAll('i');
                        editores.forEach(editor => {
                            editor.addEventListener("click", async () => {
                                await axios(editor.getAttribute("data-url"))
                                    .then(res => {
                                        modalContent.innerHTML = res.data;
                                        const formRegister = document.querySelector("#laboratorio-form");
                                        $(".color-picker").spectrum({
                                            preferredFormat: "hex",
                                            color: "#fff",
                                            chooseText: 'OK',
                                            cancelText: 'Cancelar',
                                            hideAfterPaletteSelect: true,
                                        })
                                        myModal.show();
                                        formRegister.addEventListener("submit", async (e) => {
                                            e.preventDefault();
                                            await axios(formRegister.getAttribute("action"), {
                                                method: "post",
                                                data: new FormData(formRegister)
                                            })
                                                .then(res => {
                                                    Toast.fire({
                                                        icon: 'success',
                                                        title: res.data.message
                                                    });
                                                    laboratorios();
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
                            })
                        });
                    })
            }
            laboratorios();

            btnLaboratorio.addEventListener("click", async (e) => {
                await axios(e.target.getAttribute("data-url"))
                    .then(res => {
                        modalContent.innerHTML = res.data;
                        const formRegister = document.querySelector("#laboratorio-form");
                        myModal.show();
                        formRegister.addEventListener("submit", async (e) => {
                            e.preventDefault();
                            await axios(formRegister.getAttribute("action"), {
                                method: "post",
                                data: new FormData(formRegister)
                            })
                                .then(res => {
                                    Toast.fire({
                                        icon: 'success',
                                        title: res.data.message
                                    });
                                    laboratorios();
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
            })

            btnGenerador.addEventListener("click", async (e) => {
                loader.style.visibility = 'visible';
                await axios(e.target.getAttribute("data-url"))
                    .then(res => {
                        modalContent.innerHTML = res.data;
                        loader.style.visibility = 'hidden';
                        const formRegister = document.querySelector("#generador-form");
                        myModal.show();
                        formRegister.addEventListener("submit", async (e) => {
                            e.preventDefault();
                            loader.style.visibility = 'visible';
                            await axios(formRegister.getAttribute('action'), {
                                method: "post",
                                data: new FormData(formRegister)
                            })
                                .then(res => {
                                    Toast.fire({
                                        icon: 'success',
                                        title: res.data.message
                                    });
                                    generador.ajax.reload(null, false);
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
            })
        });
}
