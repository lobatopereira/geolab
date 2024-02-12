
var endpoint = '/api/c/g/equipments/condition/summary/'
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
                    '#007bff','#242555','#5fa638','#fb8072','#80b1d3','#fdb462'
                ],
                borderWidth: 1
            }]
        };
        
        const config_equipment_condition_summ = {
            type: 'doughnut',
            data: dt,
            options: pieoption
        };
        const equipment_condition_summ_Chart_data = new Chart(
            document.getElementById('equipment_condition_summ_Chart_data'),
            config_equipment_condition_summ
        );
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
