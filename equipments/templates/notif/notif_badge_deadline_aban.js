setInterval(function(){
    $.get('/notification/badge/used/deadline-aban/total/',function(data) {
        console.log("value"+data.value);
        document.getElementById("notifbadgedeadlineaban").innerHTML = data.value;
    });
}, 2000);
