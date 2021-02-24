const pesajeCreate = document.querySelector("#pesaje-create");
const modalContent = document.querySelector(".modal-content");
const myModal = new bootstrap.Modal(document.querySelector('#exampleModal'));

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

pesajeCreate.addEventListener("click", async () => {    
    await axios(pesajeCreate.getAttribute("data-url"))
    .then(res => {
        modalContent.innerHTML =res.data;
        $('#id_proveedor').select2({
            language: 'es',      
            theme: "bootstrap4",   
            width: "100%",
            ajax: {
                url: "/proveedor/proveedor-autocomplete/",
                dataType: 'json',
                delay: 250,
                data: function(params) {
                    return {
                        q: params.term, // search term
                        page: params.page
                    };
                },
                processResults: function(data, params) {
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
            escapeMarkup: function(markup) {
                return markup;
            }, // let our custom formatter work
            minimumInputLength: 3,
            
        });
    });
    myModal.show();
})