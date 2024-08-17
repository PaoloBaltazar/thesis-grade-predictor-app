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

document.getElementById('prediction-form').addEventListener('submit', function(e) {
  e.preventDefault();

  const attendance = document.getElementsByName('attendance')[0].value;
  const previousGrades = document.getElementsByName('previous_grades')[0].value;
  const financialSituation = document.getElementsByName('financial_situation')[0].value;
  const learningEnvironment = document.getElementsByName('learning_environment')[0].value;

  const data = {
      features: [attendance, previousGrades, financialSituation, learningEnvironment]
  };

  fetch('/predict', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
      document.getElementById('prediction-result').innerText = 'Predicted Grade: ' + data.prediction;
  })
  .catch(error => console.error('Error:', error));
});

