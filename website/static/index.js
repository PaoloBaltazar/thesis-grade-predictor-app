const toggleBtn = document.getElementById('toggle-btn');
const toggleBtnCollapsed = document.getElementById('toggle-btn-collapsed');
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('main-content');

toggleBtn.addEventListener('click', () => {
sidebar.classList.add('collapsed');
toggleBtn.style.display = 'none';
toggleBtnCollapsed.style.display = 'block';
});

toggleBtnCollapsed.addEventListener('click', () => {
sidebar.classList.remove('collapsed');
toggleBtnCollapsed.style.display = 'none';
toggleBtn.style.display = 'block';
});

function updateSliderValue(sliderId, valueId) {
    const slider = document.getElementById(sliderId);
    const valueDisplay = document.getElementById(valueId);

    slider.addEventListener('input', () => {
        valueDisplay.textContent = slider.value;
    });
}

// Initialize sliders
updateSliderValue('financialSituation', 'financialSituationValue');
updateSliderValue('learningEnvironment', 'learningEnvironmentValue');

document.getElementById('prediction-form').addEventListener('submit', function (e) {
    e.preventDefault();  // Prevent the default form submission

    const daysPresent = document.querySelector('input[name="days_present"]').value;
    const schoolDays = document.querySelector('input[name="school_days"]').value;
    const previousGrades = document.querySelector('input[name="previous_grades"]').value;
    const financialSituation = document.querySelector('input[name="financial_situation"]').value;
    const learningEnvironment = document.querySelector('input[name="learning_environment"]').value;
    const gradeLevel = document.querySelector('select[name="grade_level"]').value;

    if (!daysPresent || !schoolDays || !previousGrades) {
        alert('Please fill in all fields.');
        return;
    }

    const attendance = (daysPresent / schoolDays) * 100;

    const data = {
        attendance: attendance,
        previous_grades: previousGrades,
        financial_situation: financialSituation,
        learning_environment: learningEnvironment,
        grade_level: gradeLevel
    };

    // Send the data to the server
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            throw new Error(result.error);
        }

        // Update the first accordion with the new data (Inputs and Predicted Grades)
        const firstAccordionTable = document.querySelector('#flush-collapseTwo tbody');
        const newRowInputs = document.createElement('tr');
        newRowInputs.innerHTML = `
            <td>${attendance.toFixed(2)}</td>
            <td>${previousGrades}</td>
            <td>${financialSituation}</td>
            <td>${learningEnvironment}</td>
            <td>${gradeLevel}</td>
            <td>${result.prediction.toFixed(2)}</td>
            <td>${result.remarks}</td> <!-- Add remarks -->
        `;
        firstAccordionTable.appendChild(newRowInputs);

        // Update the second accordion with the new data (Student No. and Grade Predicted)
        const secondAccordionTable = document.querySelector('#panelsStayOpen-collapseTwo tbody');
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${result.student_id}</td>
            <td>${result.prediction.toFixed(2)}</td>
            <td>${result.remarks}</td> <!-- Add remarks -->
        `;
        secondAccordionTable.appendChild(newRow);

        // Optionally, show the predicted grade in an alert or a dedicated section
        document.getElementById('prediction-result').textContent = 'Predicted Grade: ' + result.prediction.toFixed(2);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Prediction failed: ' + error.message);
    });
});



