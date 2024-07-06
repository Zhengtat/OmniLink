const totalViewsChart = document.getElementById('total-views-chart');
const revenueChart = document.getElementById("revenue-chart");
const growthRateChart = document.getElementById('growth-rate-chart');

new Chart(totalViewsChart,{
    type:'line',
    data: {
        labels: ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
        datasets: [{
            labels: "# of Votes",
            data: [12345, 19512, 13249, 42492, 328943, 128432],
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
})