document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', event => {
        const scoreInput = form.querySelector('input[name="score"]');
        const budgetInput = form.querySelector('input[name="budget"]');
        const collegeSelect = form.querySelector('select[name="college"]');
        const branchSelect = form.querySelector('select[name="branch"]');
        const submitBtn = form.querySelector('button[type="submit"]');

        // quick front-end validation
        if (scoreInput.value === '' || isNaN(scoreInput.value)) {
            event.preventDefault();
            alert('Please enter a valid numeric score.');
            scoreInput.focus();
            return;
        }

        if (budgetInput.value === '' || isNaN(budgetInput.value)) {
            event.preventDefault();
            alert('Please enter a valid budget amount.');
            budgetInput.focus();
            return;
        }

        if (collegeSelect.value === '') {
            event.preventDefault();
            alert('Please select a college.');
            collegeSelect.focus();
            return;
        }

        if (branchSelect.value === '') {
            event.preventDefault();
            alert('Please select a branch.');
            branchSelect.focus();
            return;
        }

        // disable button while request is processed
        submitBtn.disabled = true;
        submitBtn.textContent = 'Checking…';
    });
});