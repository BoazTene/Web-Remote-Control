
function client() {
    document.getElementById("header").style.animation = "on_end 1s";
    document.getElementById("client").style.animation = "on_end_button 1s";
    document.getElementById("host").style.animation = "on_end_button 1s";
    document.getElementById("download").style.animation = "on_end_button 1s";

    

    setTimeout(function(){
        document.getElementById("header").style.display = "none";
        document.getElementById("client").style.display = "none";
        document.getElementById("host").style.display = "none";
        document.getElementById("download").style.display = "none";
        window.location.href = "Login";
    }, 1000)
}

function host() {
    document.getElementById("header").style.animation = "on_end 1s";
    document.getElementById("client").style.animation = "on_end_button 1s";
    document.getElementById("host").style.animation = "on_end_button 1s";
    document.getElementById("download").style.animation = "on_end_button 1s";

    

    setTimeout(function(){
        document.getElementById("header").style.display = "none";
        document.getElementById("client").style.display = "none";
        document.getElementById("host").style.display = "none";
        document.getElementById("download").style.display = "none";
        window.location.href = "Host";
    }, 1000)
}

function download() {
    window.location.href += "#download";
}