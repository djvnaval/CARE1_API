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
            beginAtZero: false,

                callback: function(value, index, ticks) {
                  const date = new Date(Date.parse(data.labels[index]));
                  const previousDate = new Date(Date.parse(data.labels[index-1]));
                  
                  return `${date.toLocaleString('default', { month: 'short' })} ${date.getFullYear()}`; 
                }
            }
        },
        y: {
          ticks: {
            beginAtZero: false,
            callback: function(value, index, ticks){
                return ` ${value}${unit}`;
            }
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