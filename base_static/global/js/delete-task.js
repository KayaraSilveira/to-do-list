const formsDeleteTask = document.querySelectorAll(".js-form-delete-task");
const modalDeleteTask = document.getElementById('modal-delete-task');
const btnCancelDeleteTask = document.getElementById('btn-cancel-del-task');
const btnConfirmDeleteTask = document.getElementById('btn-confirm-del-task');

formsDeleteTask.forEach((form) => {
    form.addEventListener("submit", (event) => {

        event.preventDefault();
        openModalDelTask();

        btnCancelDeleteTask.addEventListener("click", closeModalDelTask);
        modalDeleteTask.children[0].addEventListener("click", closeModalDelTask);
        btnConfirmDeleteTask.addEventListener("click", () => {

            var dataForm = new FormData(form);
            var id = 'id-task-' + dataForm.get('task_pk');
            var task = document.getElementById(id);
            var formAction = form.action; 

            axios.post(formAction, dataForm, config)
            .then((res)=>{
                task.classList.add('hidden');
                closeModalDelTask();
            })
            .catch((errors)=>{
                console.log(errors);
                closeModalDelTask();
            })
        })

    });
});

function openModalDelTask() {
    modalDeleteTask.children[0].classList.remove('hide');
    modalDeleteTask.children[1].classList.remove('hide');
}

function closeModalDelTask() {
    modalDeleteTask.children[0].classList.add('hide');
    modalDeleteTask.children[1].classList.add('hide');
}
