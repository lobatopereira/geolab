
var endpoint = '/api/c/g/equipments/tama/tuir/tinan/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        const dt = {
            labels: data.label,
            datasets: [{
                label: 'Total Ekipamentu',
                data: data.obj,
                backgroundColor: [
                    '#007bff','#242555','#6c757d','#fb8072','#80b1d3','#10f1d3','#89d1a3','#fdb462','#8ed8a7','#ff3','#bebada','#fb8072','#80b1d3','#10f1d3','#89d1a3','#fdb462'
                ],
                borderWidth: 1
            }]
        };
        
        const config_chartgekipamentutamatuirtinan = {
            type: 'bar',
            data: dt,
            options: myoption
        };
        const chartgekipamentutamatuirtinan_data = new Chart(
            document.getElementById('chartgekipamentutamatuirtinan_data'),
            config_chartgekipamentutamatuirtinan
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
