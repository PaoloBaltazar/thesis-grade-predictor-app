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

// Initialize the sliders
updateSliderValue('financialSituation', 'financialSituationValue');
updateSliderValue('learningEnvironment', 'learningEnvironmentValue');

document.getElementById('prediction-form').addEventListener('submit', function (e) {
  e.preventDefault();

  const daysPresent = document.querySelector('input[name="days_present"]').value;
  const schoolDays = document.querySelector('input[name="school_days"]').value;
  const previous_grades = document.querySelector('input[name="previous_grades"]').value;
  const financial_situation = document.querySelector('input[name="financial_situation"]').value;
  const learning_environment = document.querySelector('input[name="learning_environment"]').value;
  const grade_level = document.querySelector('select[name="grade_level"]').value;

  if (schoolDays === '0' || daysPresent === '' || previous_grades === '') {
      alert('Please fill in all fields.');
      return;
  }

  const attendance = (daysPresent / schoolDays) * 100;

  const data = {
      'attendance': attendance,
      'previous_grades': previous_grades,
      'financial_situation': financial_situation,
      'learning_environment': learning_environment,
      'grade_level': grade_level
  };

  // Send the data to the backend via POST request
  fetch('/predict', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(data => {
      if (data.error) {
          throw new Error(data.error);
      }

      // Show the predicted grade
      document.getElementById('prediction-result').textContent = 'Predicted Grade: ' + data.prediction;

      // Dynamically update the input-prediction table
      const inputPredictionTableBody = document.querySelector('#accordionFlushExample tbody');
      const newRowInputs = document.createElement('tr');
      newRowInputs.innerHTML = `
          <td>${attendance.toFixed(2)}</td>
          <td>${previous_grades}</td>
          <td>${financial_situation}</td>
          <td>${learning_environment}</td>
          <td>${grade_level}</td>
          <td>${data.prediction.toFixed(2)}</td>
      `;
      inputPredictionTableBody.appendChild(newRowInputs);  // Add the new row to the table
  })
  .catch(error => {
      console.error('Error:', error);
      alert('Prediction failed: ' + error.message);  // Display the error to the user
  });
});



