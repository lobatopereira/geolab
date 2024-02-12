setInterval(function(){
    $.get('/notification/badge/used/total/',function(data) {
        console.log("value"+data.value);
        document.getElementById("notifbadge").innerHTML = data.value;
    });
}, 2000);
