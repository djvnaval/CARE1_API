import 'flowbite';

import.meta.glob([
    '../image/**',
    '../js/**'
]);

import Chart from 'chart.js/auto';
import 'chartjs-adapter-date-fns';
import Chart2 from 'chartjs-gauge';
import Alpine from 'alpinejs';
import focus from '@alpinejs/focus';

window.Alpine = Alpine;

Alpine.plugin(focus);

Alpine.start()
 
const ctx = document.getElementById('chart');


const chart = new Chart(ctx, {
    type: data.type,
    data : {
        labels: data.labels,
        datasets: data.datasets,
    },
    options: {
      scales: {
        x: {
            ticks: {
              color: '#ffeadf',
            beginAtZero: false,

                callback: function(value, index, ticks) {
                  const date = new Date(Date.parse(data.labels[index]));
                  const previousDate = new Date(Date.parse(data.labels[index-1]));
                  
                  return `${date.toLocaleString('default', { month: 'short' })} ${date.getFullYear()}`; 
                }
            },
            grid: {
           //   display: false,
            }
        },
        y: {
          ticks: {
            beginAtZero: false,
            color: '#ffeadf',

            callback: function(value, index, ticks){
                return `${value} ${unit}`;
            }
          },
          grid: {
        //    display: false,
          }   
        }
    },
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
                "borderColor" : "#8ce4b1",
                "tension" : 0.1,
                "backgroundColor" : "rgba(140, 228, 177, 0.4)",
                "cornerRadius" : 10,
                "borderWidth" : 3,

            }
        ],
    },
    options: {
        scales: {
            y:{
                beginAtZero: true,
                ticks: {
                  color: '#ffeadf'

                }
            },
            x:{
              ticks: {
                color: '#ffeadf'

              }
            }
        },
        responsive: true,
        maintainAspectRatio: true,  
        plugins: {
           legend: {
              display: false
           }
        }
      }
});

[...document.querySelectorAll('.gauge-chart')].forEach(gaugeChart => {
  const x = new Chart2(gaugeChart, {
    type: "gauge",
    data: {
      labels: threshold,
      legend: { display: false },
      datasets: [
        {
          data: threshold,
          value: gaugeChart.dataset.value,
          borderColor : [
            "black",
            "black",
            "black",
          ],

          backgroundColor: [
            "#BCE29E",
            "#fff37a",
            "rgba(145,39,89)",
          ],
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: false,
      title: {
        display: true,
        text: gaugeChart.dataset.label,
        fontColor: "white",
        fontSize: 14,
      },
      tooltips: { enabled: true },
      //layout: {
      //  padding: {
      //    bottom: 30,
      //  },
      //},
      needle: {
        radiusPercentage: 0, // Needle circle radius as the percentage
        widthPercentage: 4, // Needle width as the percentage
        lengthPercentage: 100, // Needle length as the percentage
        color: 'white', // color of the needle
      },
      cutoutPercentage: 85  ,
      valueLabel: {
        display: true,
        //fontSize: 16,
        color: "black",
        backgroundColor: "white",
        borderRadius: 10,

        formatter: (value) => {
          return Math.round(value * 10) / 10 + ` ${unit}`;
        },
      },
    },
  });

});

const realGaugeCtx = document.getElementById('realtimeGauge');

const realtimeGauge = new Chart2(realGaugeCtx, {
  type: "gauge",
  data: {
    labels: threshold,
    legend: { 
      display: false },
    datasets: [
      {
        data: threshold,
        value: realGaugeCtx.dataset.value,
        borderColor : [
          "black",
            "black",
            "black",
        ],

        backgroundColor: [
          "#BCE29E",
          "#fff37a",
          "rgba(145,39,89)",
        ],
        borderWidth: 2,
      },
    ],
  },
  options: {
    responsive: false,
    title: {
      display: true,
      text: realGaugeCtx.dataset.label,
      fontColor: "white",
      fontSize: 14,
    },
    tooltips: { enabled: true },
    //layout: {
    //  padding: {
    //    bottom: 30,
    //  },
    //},
    needle: {
      radiusPercentage: 0, // Needle circle radius as the percentage
      widthPercentage: 4, // Needle width as the percentage
      lengthPercentage: 100, // Needle length as the percentage
      color: 'white',
      //color: 'black' // color of the needle
    },
    cutoutPercentage: 85  ,
    valueLabel: {
      display: true,
      //fontSize: 16,
      color: "black",
      backgroundColor: "white",
      borderRadius: 10,

      formatter: (value) => {
        return Math.round(value * 10) / 10 + ` ${unit}`;
      },
    },
  },
});


const logJSONData = async (database, folder) => {
    const response = await fetch(`/realtime/${database}/${folder}`);
    const jsonData = await response.json(); 
    const dataset = realtimeChart.data.datasets[0].data;    

    if(jsonData.data <= threshold[2] && jsonData.data > threshold[1] && jsonData.data != dataset[dataset.length - 1]) {
      document.getElementById('toast-danger').classList.remove('hidden','opacity-0');
      document.getElementById('toast-warning').classList.add('hidden','opacity-0');
  }

  if(jsonData.data <= threshold[1] && jsonData.data > threshold[0] && jsonData.data < threshold[2] && jsonData.data != dataset[dataset.length - 1]) {
    document.getElementById('toast-warning').classList.remove('hidden','opacity-0');
    document.getElementById('toast-danger').classList.add('hidden','opacity-0');

  }

    realtimeChart.data.labels.push(jsonData.label); 
    dataset.push(jsonData.data); 

    realtimeChart.update();
    realtimeGauge.data.datasets[0].value = jsonData.data; 
    realtimeGauge.update();
    
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
    }, 11000);
});
/*
$(function() {
  $('input[name="datetimes"]').daterangepicker({
    timePicker: true,
    timePickerSeconds: true,
    startDate: moment().startOf('hour'),
    endDate: moment().startOf('hour').add(32, 'hour'),
    locale: {
      format: 'M/DD/Y H:mm'
    }
  });
});
*/

$(function() {
  $('input[name="datetimes"]').daterangepicker({
    showDropdowns: true,
    timePicker: true,
    timePickerSeconds: true,
    ranges: {
        'Today': [moment(), moment()],
        'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
        'Last 7 Days': [moment().subtract(6, 'days'), moment()],
        'Last 30 Days': [moment().subtract(29, 'days'), moment()],
        'This Month': [moment().startOf('month'), moment().endOf('month')],
        'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
    },
    //startDate: moment().startOf('hour'),
    //endDate: moment().startOf('hour').add(32, 'hour'),
    locale: {
      format: 'M/DD/Y H:mm'
    },
    drops: "auto",
    buttonClasses: "btn btn-md",
    applyButtonClasses: "text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800 mt-2",
    cancelClass: "btn btn-md",

  },
  );
});