const bodyConf = document.querySelector("#body-conf");
const ulMenu = document.querySelector(".list-group-flush");

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

document.addEventListener('DOMContentLoaded', function() {
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
        selector =e.target;        
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

})

const cargarPerfil = async (url) => {
    await axios(url)
    .then(res => { 
        bodyConf.innerHTML = res.data;
        const photo = document.querySelector("#id_photo");
        const formUpdate = document.querySelector("#edit-user-form")
        photo.addEventListener('change', e => {
            console.log(photo)
            if(e.target.files.length > 0){
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
    await axios(url)    
    .then(res => {
        bodyConf.innerHTML = res.data;        
        const modalContent = document.querySelector(".modal-content");
        const userRegister = document.querySelector("#user-register"); 
        const usuarioList = document.querySelector("#usuario-list");
        const myModal = new bootstrap.Modal(document.querySelector('#exampleModal'));       
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
    await axios(url)
    .then(res => {
        bodyConf.innerHTML = res.data;
        const modalContent = document.querySelector(".modal-content");
        const btnCotizacion = document.querySelector("#cotizacion-register");
        const btnColor = document.querySelector("#color-register");
        const btnDestino =document.querySelector("#destino-register");
        const cotizaciones = document.querySelector("#cotizaciones");
        const myModal = new bootstrap.Modal(document.querySelector('#exampleModal'));               
        const datatable = $('#cotizaciones').DataTable({
            "language" : {
                "thousands":      ".",
                "decimal":        ",",
                "emptyTable":     "No data available in table",
                "info":           "Mostrando del _START_ al _END_ de _TOTAL_ registros",
                "infoEmpty":      "Showing 0 to 0 of 0 entries",
                "infoFiltered":   "(filtered from _MAX_ total entries)",
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
            "ajax": "/user/parametro/cotizacion/json/",
            "columnDefs": [ 
                {
                    "targets": 3,
                    "orderable": false
                } 
            ],      
            "searching": false,            
        });       
        
        cotizaciones.addEventListener("click", async (e) => {
            if (e.target.classList.contains("bi")){
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
                        const fechaFinDP = new Datepicker(fechaFin ,{
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
                    });
                })
            }
        })

        const colores = async () => {
            const colorBody = document.querySelector("#colores");
            await axios(colorBody.getAttribute('data-url'))
            .then(res => {
                colorBody.innerHTML = res.data
                const editores = colorBody.querySelectorAll('i');
                editores.forEach(editor => {
                    editor.addEventListener("click", async () => {
                        await axios(editor.getAttribute("data-url"))
                        .then(res => {                            
                            modalContent.innerHTML = res.data;
                            const formRegister = document.querySelector("#color-form");
                            $(".color-picker").spectrum({
                                preferredFormat: "hex",
                                color: "#fff",
                                chooseText: 'OK',
                                cancelText: 'Cancelar',
                                hideAfterPaletteSelect:true,
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
                                    colores();
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
        colores();

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
                            $(".color-picker").spectrum({
                                preferredFormat: "hex",
                                color: "#fff",
                                chooseText: 'OK',
                                cancelText: 'Cancelar',
                                hideAfterPaletteSelect:true,
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
        
        btnColor.addEventListener("click", async (e) => {
            await axios(e.target.getAttribute("data-url"))
            .then(res => {
                modalContent.innerHTML = res.data;
                const formRegister = document.querySelector("#color-form");
                $(".color-picker").spectrum({
                    preferredFormat: "hex",
                    color: "#fff",
                    chooseText: 'OK',
                    cancelText: 'Cancelar',
                    hideAfterPaletteSelect:true,
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
                        colores();
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

        btnDestino.addEventListener("click", async (e) => {
            await axios(e.target.getAttribute("data-url"))
            .then(res => {
                modalContent.innerHTML = res.data;
                const formRegister = document.querySelector("#destino-form");
                $(".color-picker").spectrum({
                    preferredFormat: "hex",
                    color: "#fff",
                    chooseText: 'OK',
                    cancelText: 'Cancelar',
                    hideAfterPaletteSelect:true,
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

        btnCotizacion.addEventListener("click", async (e) => {
            await axios(e.target.getAttribute("data-url"))
            .then( res => {
                modalContent.innerHTML = res.data;
                const fechaInicio = document.querySelector("#id_fecha_inicio");
                const fechaFin = document.querySelector("#id_fecha_fin");
                const formRegister = document.querySelector("#cotizacion-form");
                const fechaInicioDP = new Datepicker(fechaInicio, {
                    language: 'es',
                    autohide: true,
                    container: '.modal-content',
                });
                const fechaFinDP = new Datepicker(fechaFin ,{
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
                });
            })
        })
    })
}