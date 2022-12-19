hours = moment().format('HH:mm')
document.getElementById('clock').innerHTML = hours

setInterval(function(){
    hours = moment().format('HH:mm')
    document.getElementById('clock').innerHTML = hours
    
},1000)


