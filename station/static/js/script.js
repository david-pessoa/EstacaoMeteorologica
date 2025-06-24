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

SwitchThemeButton.addEventListener('click', function(event) {
    const body = document.getElementsByTagName('body')[0]
    const boxes = Array.from(document.getElementsByClassName('bg-dark'));
    const tables = Array.from(document.getElementsByClassName('table-dark'));
    const titles = Array.from(document.getElementsByTagName('h4', 'h5'));
    const subtitles = Array.from(document.getElementsByTagName('h5'));

    if (SwitchThemeButton.checked)
    {
        body.style.backgroundColor = '#b2f7d8';
        body.style.color = '#000';
        
        titles.forEach(el => {
            el.style.color = '#FFF';
        });

        subtitles.forEach(el => {
            el.style.color = '#FFF';
        });

        boxes.forEach(el => {
            el.style.setProperty('background-color', 'rgba(26, 161, 121, 1)', 'important');
        });

        tables.forEach(el => {
            el.style.setProperty('--bs-table-bg', '#1AA179');
        });
    }
    else
    {
        body.style.backgroundColor = '';
        body.style.color = ''

        boxes.forEach(el => {
            el.style.setProperty('background-color', 'rgba(33, 37, 41, 1)', 'important');
        });

        tables.forEach(el => {
            el.style.setProperty('--bs-table-bg', '#212529');
        });
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
