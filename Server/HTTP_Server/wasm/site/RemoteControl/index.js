import wasm, {get_image} from "../node_modules/web-client/web_client.js";
let module;

const urlParams = new URLSearchParams(window.location.search);

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");
console.log(urlParams.get("image"))
var body = document.body
var html = document.documentElement;


async function load_module(){
    console.log(wasm)
    module = await wasm();
 

    document.getElementsByTagName('body')[0].style.visibility = "visible";
    document.getElementsByClassName('loader')[0].style.visibility = "hidden";
    document.getElementById('loader-text').style.visibility = "hidden";
    onStart();
}

load_module()

// canvas.addEventListener('mousemove', onMouseMove);
// canvas.addEventListener('click', onMouseClicked);


// this funciton is used to draw an image on the canvas
// the img_src value can be url to image http://..../img.png or local path or data url data://image/jpeg;base64,<data>
function draw(event) {
    
    // console.log(event.detail);
    var img_src = event.detail;
    // try{
    //     img_src = img_src.split("<start>")[1].split("<end>")[0]
    // } catch {
    //     console.log(img_src);
    //     return
    // }
    img_src = "data:image/jpeg;base64," + img_src;
    alert(img_src)
    // console.log(img_src);
    var ctx = document.getElementById('canvas').getContext('2d');
    var img = new Image();
    img.onload = function() {
        console.log(img.naturalWidth);
        console.log(img.naturalHeight);
        console.log(Math.max( body.scrollHeight, body.offsetHeight, 
            html.clientHeight, html.scrollHeight, html.offsetHeight ));
        
        alert("Draw");
        ctx.drawImage(img, 0, 0, canvas.width , canvas.height);
    };
    // console.log(img_src)
    img.src = img_src;
}

// this funciton called every time the user move the mouse anywhere on the canvas
function onMouseMove(event){
    console.log("x: " + event.clientX + " y:" +event.clientY);
}

// this function is called every time the user click anywhere on the canvas
function onMouseClicked(event){
    module.get_image();
    console.log("Mouse cicked at x: " + event.clientX + " y: " + event.clientY);
}

// this function is called on start
// this function fits the canvas size to the screen size
function onStart() {
    ctx.canvas.width  = window.innerWidth ;
    ctx.canvas.height = window.innerHeight - 15 - ((window.innerHeight/100) * 7);
    canvas.style.top = ((window.innerHeight/100) * 7) + "px";
    canvas.style.position = "relative";
    window.addEventListener("newimage", draw)
    setInterval(function() {
        get_image();
        // src = "data:image/jpeg;base64," + src;
        // console.log(src);
        // draw(src);
    }, 100)
}