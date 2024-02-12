setInterval(function(){
    $.get('/notification/badge/used/deadline/total/',function(data) {
        console.log("value"+data.value);
        document.getElementById("notifbadgedeadline").innerHTML = data.value;
    });
}, 2000);
