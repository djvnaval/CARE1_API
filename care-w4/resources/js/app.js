import 'flowbite';

import.meta.glob([
    '../image/**',
    '../js/**'
]);

import Chart from 'chart.js/auto';

import Alpine from 'alpinejs';
import focus from '@alpinejs/focus';
window.Alpine = Alpine;

Alpine.plugin(focus);

Alpine.start()
 
const ctx = document.getElementById('chart');

const chart = new Chart(ctx, {
    type : data.type,
    data : {
        labels: data.labels,
        datasets: data.datasets,
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,  
        plugins: {
           legend: {
              display: false
           }
        }
      }
});

const realCtx = document.getElementById('realtimeChart');

const realtimeChart = new Chart(realCtx, {
    type : 'line',
    data : {
        labels: ["0"],
        datasets: [
            {
                'label' : 'Realtime',
                'data' : [0],
                'fill' : true,
                "borderColor" : "#1434A4",
                "tension" : 0.1,
                "backgroundColor" : "rgba(0, 150, 255,0.5)",
                "cornerRadius" : 10
            }
        ],
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,  
        plugins: {
           legend: {
              display: false
           }
        }
      }
});


const logJSONData = async (database, folder) => {
    const response = await fetch(`/realtime/${database}/${folder}`);
    const jsonData = await response.json(); 

    realtimeChart.data.labels.push(jsonData.label); 
    realtimeChart.data.datasets[0].data.push(jsonData.data); 

    realtimeChart.update();

    if(realtimeChart.data.datasets[0].data.length > 24) {
        realtimeChart.data.datasets[0].data.shift();
        realtimeChart.data.labels.shift();
    }
}

setInterval(() => logJSONData(database, folder), 1000);

const request =  async (url, method, id) => {
    const response = await fetch(url, {method: method});
    const jsonData = await response.json(); 
    
    document.getElementById(id).checked = jsonData.data.value == 1 ? true : false;
}

const toggleButtons = document.querySelectorAll('.toggle-buttons');

[...toggleButtons].forEach(toggleButton => {
    toggleButton.addEventListener('click', element => request(toggleButton.dataset.url, toggleButton.dataset.method, toggleButton.id));
        toggleButton.checked = toggleButton.dataset.visible == 1 ? true : false;

        setInterval(() => {
           const jsonData = request(toggleButton.dataset.update_url, toggleButton.dataset.method, toggleButton.id);
        }, 2000);
});

