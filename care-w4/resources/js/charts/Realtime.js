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