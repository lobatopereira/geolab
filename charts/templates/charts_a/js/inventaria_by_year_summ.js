
var endpoint = '/api/c/g/inventaria/tuir/tinan/summary/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        var ajaxdata = []
        for (let i in data.labels) {
            var totData = []
            for (let j in data.obj) {
                totData.push(data.obj[j][i])
            }
            ajaxdata.push(totData)
        }
        var backgroundColor = ['#4e38c7','#f03','#bebada','#fb8072','#80b1d3','#10f1d3','#89d1a3','#fdb462']
        var plotdata = []
        for (let i in ajaxdata) {
            plotdata.push({
                label: data.labels[i],
                data: ajaxdata[i],
                backgroundColor: backgroundColor[i],
                borderColor: backgroundColor[i],
                borderWidth: 1
            },)
        }
        const dt = {
            labels: data.label,
            datasets: plotdata
        };
        
        const config_chart = {
            type: 'bar',
            data: dt,
            options: groupoption
        };
        const gInventariaByYear_data = new Chart(
            document.getElementById('gInventariaByYear_data'),
            config_chart
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
