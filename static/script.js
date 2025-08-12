document.addEventListener('DOMContentLoaded', () => {
    const diabetesForm = document.getElementById('diabetes-form');
    const predictionResultDiv = document.getElementById('prediction-result');
    const resultText = document.getElementById('result-text');
    const resultProbability = document.getElementById('result-probability');
    const errorMessageDiv = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');

    const totalPredictionsSpan = document.getElementById('total-predictions');
    const modelAccuracySpan = document.getElementById('model-accuracy');
    const statsTotalSpan = document.getElementById('stats-total');
    const statsPositiveSpan = document.getElementById('stats-positive');
    const statsNegativeSpan = document.getElementById('stats-negative');
    const featureImportanceList = document.getElementById('feature-importance-list');

    async function fetchStats() {
        try {
            const response = await fetch('/api/diabetes/stats');
            const stats = await response.json();
            totalPredictionsSpan.textContent = stats.total_predictions;
            statsTotalSpan.textContent = stats.total_predictions;
            statsPositiveSpan.textContent = stats.positive_predictions;
            statsNegativeSpan.textContent = stats.negative_predictions;
        } catch (error) {
            console.error('Erreur lors de la récupération des statistiques:', error);
        }
    }

    async function fetchModelAccuracy() {
        try {
            const response = await fetch('/api/diabetes/accuracy');
            const data = await response.json();
            modelAccuracySpan.textContent = `${(data.accuracy * 100).toFixed(1)}%`;
        } catch (error) {
            console.error('Erreur lors de la récupération de la précision du modèle:', error);
            modelAccuracySpan.textContent = 'N/A';
        }
    }

    async function fetchFeatureImportance() {
        try {
            const response = await fetch('/api/diabetes/feature-importance');
            const importance = await response.json();
            featureImportanceList.innerHTML = '';
            const sortedImportance = Object.entries(importance).sort(([, a], [, b]) => b - a);
            sortedImportance.forEach(([feature, value]) => {
                const listItem = document.createElement('li');
                const percentage = (value * 100).toFixed(1);
                listItem.innerHTML = `
                    <span>${feature.replace(/_/g, ' ')}</span>
                    <div class="bar-container">
                        <div class="bar" style="width: ${percentage}%;"></div>
                    </div>
                    <span>${percentage}%</span>
                `;
                featureImportanceList.appendChild(listItem);
            });
        } catch (error) {
            console.error('Erreur lors de la récupération de l\'importance des facteurs:', error);
        }
    }

    fetchStats();
    fetchModelAccuracy();
    fetchFeatureImportance();

    diabetesForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(diabetesForm);
        const data = {};
        formData.forEach((value, key) => {
            if (['age', 'bmi', 'HbA1c_level', 'blood_glucose_level'].includes(key)) {
                data[key] = parseFloat(value);
            } else if (['hypertension', 'heart_disease'].includes(key)) {
                data[key] = parseInt(value);
            } else {
                data[key] = value;
            }
        });

        predictionResultDiv.style.display = 'none';
        errorMessageDiv.style.display = 'none';
        resultText.textContent = 'Analyse en cours...';
        predictionResultDiv.style.display = 'block';
        predictionResultDiv.style.backgroundColor = '#FFF3CD';
        predictionResultDiv.style.color = '#664D03';
        resultProbability.textContent = '';

        try {
            const response = await fetch('/api/diabetes/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                predictionResultDiv.style.backgroundColor = '#D4EDDA';
                predictionResultDiv.style.color = '#155724';
                if (result.prediction === 1) {
                    resultText.textContent = 'Risque de diabète détecté.';
                } else {
                    resultText.textContent = 'Faible risque de diabète.';
                }
                resultProbability.textContent = `Probabilité: ${(result.probability * 100).toFixed(2)}%`;
                fetchStats();
            } else {
                predictionResultDiv.style.display = 'none';
                errorMessageDiv.style.display = 'block';
                errorText.textContent = result.error || 'Une erreur inconnue est survenue.';
            }
        } catch (error) {
            predictionResultDiv.style.display = 'none';
            errorMessageDiv.style.display = 'block';
            errorText.textContent = 'Impossible de se connecter au serveur. Veuillez vérifier la console pour plus de détails.';
            console.error('Erreur lors de la soumission du formulaire:', error);
        }
    });
});