const ctx = document.getElementById('graficoTemperatura');

const horarios = Array.from({length: 24}, (_, i) => {
    return `${i.toString().padStart(2, '0')}:00`; // Horários das 0:00 até às 23:00
});

let temperaturas = [];

for (let i = 0; i < 24; i++)
{
    temp = Math.round(previsao_hoje.hour[i].temp_c);
    temperaturas.push(temp);
}

new Chart(ctx, {
    type: 'line',
    data: {
        labels: horarios, // Esconde labels ou usa labels genéricos
        datasets: [{
            label: 'Temperatura (°C)',
            data: temperaturas,
            borderColor: '#ff4500',
            backgroundColor: 'rgba(255, 69, 0, 0.2)',
            tension: 0.3,
            fill: true
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                ticks: {
                    callback: function(val, index) {
                        return index % 2 === 0 ? horarios[index] || '' : '';
                    }
                }
            },
            y: {
                min: 0,
                max: 50,
                title: {
                    display: true,
                    text: 'Temperatura (°C)'
                }
            }
        }
    }
});
