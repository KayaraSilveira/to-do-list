$("#sortable").sortable({
    update: function(event, ui) {
        var arrayOrder = $("#sortable").sortable("toArray");
        var list_task_pk = [];
        var list_pk = document.getElementById('input-list-pk');

        var getUrl = window.location;
        var baseUrl = getUrl.protocol + "//" + getUrl.host
        var formAction = baseUrl + document.getElementById('input-url-sortable').value;

        arrayOrder.forEach((item) => {
            list_task_pk.push(item.slice(8));
        });
        
        var dataForm = new FormData();
        dataForm.append('list_task_pk', list_task_pk);
        if (list_pk) {
            dataForm.append('list_pk', list_pk.value);
        }
        

        axios.post(formAction, dataForm, config)
        .then((res)=>{
            
        })
        .catch((errors)=>{
            console.log(errors);
        })
    }
});
