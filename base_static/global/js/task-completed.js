

const formsCompletedTask = document.querySelectorAll(".js-form-completed-task");
const csrftoken = getCookie('csrftoken');
const config = {
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'multipart/form-data', 
    }
}

formsCompletedTask.forEach((form) => {
    form.addEventListener("submit", (event) => {

        event.preventDefault();

        var dataForm = new FormData(form); 
        var id = 'id-task-' + dataForm.get('task_pk');
        var task = document.getElementById(id);
        var idChbx = 'id-chbx-' + dataForm.get('task_pk');
        var chbx = document.getElementById(idChbx);

        var formAction = form.action;

        axios.post(formAction, dataForm, config)
        .then((res)=>{
            task.classList.toggle('task-completed');
            chbx.toggleAttribute("checked");
        })
        .catch((errors)=>{
            console.log(errors)   
        })

    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
    
