const apiKey = '3998e2e5095ecacf4ee5d0be174f951c'; // ضع مفتاح API الخاص بك هنا
const city = 'Cairo,eg'; // اسم المدينة، يمكنك تعديله حسب الحاجة
const environmentalInfoDiv = document.getElementById('environmentalInfo');
const ctx = document.getElementById('environmentalChart').getContext('2d');

fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const humidity = data.main.humidity;
        const temperature = data.main.temp - 273.15; // تحويل من كلفن إلى مئوي
        const weather = data.weather[0].description;

        // عرض بيانات البيئة
        environmentalInfoDiv.innerHTML = `
            <p>Humidity: ${humidity}%</p>
            <p>Temperature: ${temperature.toFixed(2)}°C</p>
            <p>Weather: ${weather}</p>
        `;

        // حساب مستوى الخطر وعرضه
        const riskLevel = calculateRiskLevel(humidity, temperature);
        environmentalInfoDiv.innerHTML += `
            <p>Risk Level for Respiratory Disease: ${riskLevel}</p>
        `;

        // عرض الرسم البياني
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Humidity', 'Temperature'],
                datasets: [{
                    label: 'Environmental Data',
                    data: [humidity, temperature],
                    backgroundColor: ['rgba(0, 123, 255, 0.6)', 'rgba(255, 99, 132, 0.6)'],
                    borderColor: ['rgba(0, 123, 255, 1)', 'rgba(255, 99, 132, 1)'],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error('Error fetching environmental data:', error);
        environmentalInfoDiv.innerHTML = '<p>Failed to retrieve environmental data.</p>';
    });

// دالة لحساب مستوى الخطر بناءً على الرطوبة ودرجة الحرارة
function calculateRiskLevel(humidity, temperature) {
    if (humidity > 70 && temperature < 20) {
        return "High";
    } else if (humidity > 50 && temperature < 25) {
        return "Moderate";
    } else {
        return "Low";
    }
}

// رفع ملف الصوت وتحليله
function uploadAudio(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/analyze_sound', {  // تأكد من أن هذا هو عنوان الـ API الخاص بك
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Diagnosis from sound analysis:', data);
        // عرض التشخيص على الموقع
        environmentalInfoDiv.innerHTML += `<p>Sound Analysis Diagnosis: ${data.diagnosis}</p>`;
    })
    .catch(error => {
        console.error('Error analyzing sound:', error);
    });
}

function handleAudioUpload() {
    const audioInput = document.getElementById('audioInput');
    if (audioInput.files.length > 0) {
        uploadAudio(audioInput.files[0]);
    }
}
