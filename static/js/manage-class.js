
function toggleCreateForm() {
    var form = document.getElementById('create-class-form');
    if (form.classList.contains('hidden')) {
        form.classList.remove('hidden');
    } else {
        form.classList.add('hidden');
    }
}
