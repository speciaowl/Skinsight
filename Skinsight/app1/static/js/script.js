document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector("form");

    form.addEventListener('submit', (e) => {
        if (!form.checkValidity()) {
            e.preventDefault();
        }

        form.classList.add('was-validated');
    });

    const submitButton = document.querySelector("button[type='submit']");

    form.addEventListener('input', () => {
        // Check if all form fields are filled and valid
        const allFieldsValid = Array.from(form.elements).every(field => field.checkValidity());

        // Enable or disable the submit button based on the form's input status
        submitButton.disabled = !allFieldsValid;
    });
});
