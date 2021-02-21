
/**
 * This function start the exist animation,
 * it redirect the user after 1000 ms.
 */
function client() {
    existAnimation();

    setTimeout(function(){
        document.getElementById("header").style.display = "none";
        document.getElementById("client").style.display = "none";
        document.getElementById("host").style.display = "none";
        document.getElementById("download").style.display = "none";
        window.location.href = "Login";
    }, 1000)
}

/**
 * This function start the exist animation, 
 * it redirecting the user to the host site.
 */
function host() {
    existAnimation();

    setTimeout(function(){
        document.getElementById("header").style.display = "none";
        document.getElementById("client").style.display = "none";
        document.getElementById("host").style.display = "none";
        document.getElementById("download").style.display = "none";
        window.location.href = "Host";
    }, 1000)
}

/**
 * This function start the exist animation, 
 * it redirecting the user to the download site.
 */
function download() {
    window.location.href += "#download";
}

/**
 * This function starts the exist animation.
 */
function existAnimation() {
    document.getElementById("header").style.animation = "on_end 1s";
    document.getElementById("client").style.animation = "on_end_button 1s";
    document.getElementById("host").style.animation = "on_end_button 1s";
    document.getElementById("download").style.animation = "on_end_button 1s";
}
