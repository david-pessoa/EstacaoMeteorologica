import Autocomplete from './autocomplete.js';

const LastUpdate = document.getElementById('last_update') //tag onde fica o texto que informa a ultima atualização
const ctx = document.getElementById('graficoTemperatura');
const AutocompleteDataList = document.getElementById("AutocompleteDataList");
const SwitchThemeButton = document.getElementById('flexSwitchCheckDefault');

  const opts = {
    onSelectItem: console.log,
  };

new Autocomplete(AutocompleteDataList, opts);

AutocompleteDataList.addEventListener('keydown', (event) => {
    const drop_down_menu = document.getElementById('ac-menu-1');
    if(!SwitchThemeButton.checked)
    {
        drop_down_menu.classList.add('dropdown-menu-dark');
    }
    else
    {
        drop_down_menu.classList.remove('dropdown-menu-dark');
    }
    
    if (event.key === 'Enter') {
        event.preventDefault(); // impede que o autocomplete ou o formulário façam outra ação

        const cidade = AutocompleteDataList.value.trim();

        if (cidade) {
            window.location.href = `/?local=${encodeURIComponent(cidade)}`;
        }
    }
});

document.addEventListener('click', function(event) {
    const link = event.target.closest('.dropdown-item');
    if (link) {
        event.preventDefault();  // Impede que o autocomplete só preencha

        const cidade = link.getAttribute('data-value');
        if (cidade) {
            window.location.href = `/?local=${encodeURIComponent(cidade)}`;
        }
    }
});

const data = new Date(ultima_atualizacao); //Obtém data e converte para o fuso horário do Usuário

const horas = data.getHours().toString().padStart(2, '0');
const minutos = data.getMinutes().toString().padStart(2, '0');

const hoje = new Date();
const ehHoje = data.getDate() === hoje.getDate() &&
                data.getMonth() === hoje.getMonth() &&
                data.getFullYear() === hoje.getFullYear();

const texto = ehHoje ? `Última atualização: Hoje às ${horas}:${minutos}` : 
    `${data.getDate()} de ${data.toLocaleString('pt-BR', { month: 'long' })} às ${horas}:${minutos}`;

LastUpdate.textContent = texto

let temperaturas = [];
let temp;
for (let i = 0; i < 24; i++)
{
    temp = Math.round(previsao_hoje.hour[i].temp_c);
    temperaturas.push(temp);
}

const horarios = Array.from({length: 24}, (_, i) => {
    return `${i.toString().padStart(2, '0')}:00`; // Horários das 0:00 até às 23:00
});

const chart = new Chart(ctx, {
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
                min: Math.round(previsao_hoje.day.maxtemp_c) + 3,
                max: Math.round(previsao_hoje.day.mintemp_c) - 3,
                title: {
                    display: true,
                    text: 'Temperatura (°C)'
                }
            }
        }
    }
});

function ChangeChartTheme()
{
    const isDark = !SwitchThemeButton.checked;
    return {
        borderColor: isDark ? '#ff4500': 'rgb(255, 149, 0)',
        backgroundColor: isDark? 'rgba(255, 69, 0, 0.2)': 'rgba(255, 200, 0, 0.37)',
        options: {
            responsive: true,
            scales: {
                x: {
                    ticks: {
                        color: isDark ? 'rgb(86, 86, 86)' : 'rgb(209, 209, 209)',
                        callback: function(val, index) {
                            return index % 2 === 0 ? horarios[index] || '' : '';
                        }
                    },
                    grid: {
                        color: isDark ? '#222' : 'rgb(0, 110, 183)'
                    }
                },
                y: {
                    min: Math.round(previsao_hoje.day.maxtemp_c) + 3,
                    max: Math.round(previsao_hoje.day.mintemp_c) - 3,
                    ticks: {
                        color: isDark ? 'rgb(86, 86, 86)' : 'rgb(209, 209, 209)',
                    },
                    title: {
                        display: true,
                        text: 'Temperatura (°C)',
                        color: isDark ? 'rgb(86, 86, 86)' : 'rgb(209, 209, 209)',
                    },
                    grid: {
                        color: isDark ? '#222' : 'rgb(0, 110, 183)'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: isDark ? 'rgb(86, 86, 86)' : 'rgb(209, 209, 209)',
                    }
                }
            }
        }
    }
}

// Troca entre modo claro e escuro
SwitchThemeButton.addEventListener('click', function(event) { 
    const body = document.getElementById('body');
    const boxes = Array.from(document.getElementsByClassName('bg-dark'));
    const tables = Array.from(document.getElementsByClassName('table-dark'));
    const drops = Array.from(document.getElementsByClassName('fa-droplet'));
    const wind_arrow = document.getElementById('arrow');
    const drop_down_menu = document.getElementById('ac-menu-1');

    const new_chart = ChangeChartTheme();
    chart.data.datasets[0].borderColor = new_chart.borderColor;
    chart.data.datasets[0].backgroundColor = new_chart.backgroundColor;
    chart.options = new_chart.options;
    chart.update();

    // Modo claro
    if (SwitchThemeButton.checked)
    {
        body.style.backgroundColor = 'rgb(24, 138, 213)';
        drop_down_menu.classList.remove('dropdown-menu-dark');

        boxes.forEach(el => {
            el.style.setProperty('background-color', 'rgb(1, 114, 190)', 'important');
        });

        tables.forEach(el => {
            el.style.setProperty('--bs-table-bg', 'rgb(1, 114, 190)');
        });

        drops.forEach(el => {
            el.style.color = '#70b2ff';
        })

        wind_arrow.style.color = 'rgb(249, 126, 0)';
    }
    // Modo escuro
    else
    {
        body.style.backgroundColor = '';
        drop_down_menu.classList.add('dropdown-menu-dark');

        boxes.forEach(el => {
            el.style.setProperty('background-color', 'rgba(33, 37, 41, 1)', 'important');
        });

        tables.forEach(el => {
            el.style.setProperty('--bs-table-bg', '#212529');
        });

        drops.forEach(el => {
            el.style.color = '';
        })

        wind_arrow.style.color = '';
    }
});