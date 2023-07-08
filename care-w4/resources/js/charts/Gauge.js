const gaugeCtx = document.getElementById('gaugeChart');

const gaugeChart = new Chart2(gaugeCtx, {
    type: "gauge",
    data: {
      labels: ["good", "poor", "bad"],
      legend: { display: false },
      datasets: [
        {
          data: [15, 40, 60],
          value: 30,
          backgroundColor: [
            "rgb(61,204,91)",
            "rgb(239,214,19)",
            "rgb(255,84,84)",
          ],
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: false,
      title: {
        display: true,
        text: "Gauge",
        fontSize: 16,
      },
      tooltips: { enabled: true },
      //layout: {
      //  padding: {
      //    bottom: 30,
      //  },
      //},
      needle: {
        radiusPercentage: 0, // Needle circle radius as the percentage
        widthPercentage: 5, // Needle width as the percentage
        lengthPercentage: 100, // Needle length as the percentage
        //color: 'black' // color of the needle
      },
      cutoutPercentage: 70,
      valueLabel: {
        display: true,
        //fontSize: 16,
        color: "black",
        backgroundColor: "white",
        borderRadius: 5,

        formatter: (value) => {
          return Math.round(value * 10) / 10 + " µ/m³";
        },
      },
    },
  });

