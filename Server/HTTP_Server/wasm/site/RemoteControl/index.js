import wasm, {get_image, send_key, keys, send_mouse_pos, store_value_in_wasm_memory_buffer_index_zero, get_wasm_memory_buffer_pointer, close, send_mouse, Keyboard, web_socket} from "../node_modules/web-client/web_client.js";
import {OnStart} from "../RemoteControl/on_start.js";


export {onWindowResize, keys, get_image, send_key};

let keyboard;
var offscreen;
var gl;
var last_x;
var last_y;

// setInterval(function () {
//     // let key_queue_temp = key_queue.map((x) => x);
//     // for (let i = key_queue_temp.length; i > 0; i--) {
//     //     console.log(key_queue_temp)

//     //     Keyboard.press_key(key_queue_temp[i-1]);
//     //     key_queue.pop(key_queue.indexOf(key_queue[i-1]));
//     // }
//     timerId = undefined;
//     // key_queue = []
//     // console.log(key_queue)
//     // let wasmMemory = new Uint8Array(module.memory.buffer);
//     // var bufferPointer = get_wasm_memory_buffer_pointer();
//     // if (wasmMemory[bufferPointer] == 0) {
//     //     timerId = undefined;
//     // }
// }, 1000)
let module;
let timerId;
let key_queue = [];


var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");

new OnStart(canvas, ctx, wasm).start().then(m => {
        module = m;
        eventListeners();
        // let socket = new web_socket("ws://localhost:9898");
        keyboard = new Keyboard();
        // let socket = new web_socket("ws://127.0.0.1:1234");
        // setTimeout(function() {
        //     socket.send("hey Whats going on?");
        //     socket.on_message();
        //     eventListeners();
        // }, 1000)
        
});


/* Event listeners */

function eventListeners() {
    // canvas.addEventListener('mousemove', onMouseMove);
    // canvas.addEventListener('click', onMouseClicked);
    // event_test();
    // document.addEventListener('keydown', onkeypress, { passive: false, once: false });
    // document.onkeydown = onKeyPress;
    $("body").keydown(function(e){
        onKeyPress(e);
    });

    $("canvas").click(function(event) {
      onMouseClicked(event);
    });

    console.log($("canvas"))
    console.log(document.getElementsByTagName('canvas')[0]);

    $("canvas").mousemove(function(event) {
        onMouseMove(event);
    });

    document.addEventListener('wheel', event => {
        onWheelScrolled(event);
    })

    $('canvas').on('contextmenu', event => event.preventDefault());

    store_value_in_wasm_memory_buffer_index_zero(0);
    // send_key('d');
}

/* Events */

/**
 * This function called each time the 'mousemove' event is triggered.
 * 
 * The function sends to the Http_api server the mouse x, y.
 * 
 * @param {event} event
 */
function onMouseMove(event){
    event.preventDefault();

    throttleFunction(send_mouse, 300, ((event.clientX+10)/canvas.width).toString(),((event.clientY-65)/canvas.height).toString(), 'n', "1");
}

/**
 * This function called each time the 'mouseclick' event is triggered.
 * 
 * The function sends to the Http_api the mouse x, y + the mouse state 
 * 
 * @param {event} event 
 */
function onMouseClicked(event) {
    event.preventDefault();
    let button;


    if (event.which == 1) button = 'l';
    if (event.which == 2) button = 'm';
    if (event.which == 3) button = 'r';

    send_mouse(((event.clientX+10)/canvas.width).toString(), ((event.clientY-65)/canvas.height).toString() , button, "1");
}

/**
 * This function called each time the 'keypress' event is triggered.
 * 
 * The function cancle all of the default shurtcut,
 * The funciton sends to the Http_api the pressed key.
 * 
 * @param {event} event 
 */
function onKeyPress(event) {    
        console.log(event.key)
        console.log(Keyboard.press_key)
        if (event.altKey == true || event.ctrlKey == true || event.shiftKey){
            console.log("Paste")
            let key = "";
            if (event.altKey == true) key += "Alt**";
            if (event.ctrlKey == true) key += "Control**";
            if (event.shiftKey == true) key += "Shift**";
            key += event.key;
            throttleFunction(Keyboard.key_combination, 5, key);
        } else {
             throttleFunction(Keyboard.press_key, 5, event.key);
             console.log(timerId)

        }
        
        event.preventDefault();
}

function onWheelScrolled(event) {
    send_mouse(((event.clientX+10)/canvas.width).toString(), ((event.clientY-65)/canvas.height).toString() , 's', (-event.deltaY).toString());
}

/**
 * This function called each time the 'resize' event is triggered.
 * 
 * The function resizing the canvas to fit the new window size.
 */
function onWindowResize() {
    canvas.style.position = "relative";
    ctx.canvas.width  = window.innerWidth;
    ctx.canvas.height = window.innerHeight - 25 - ((window.innerHeight/100) * 7);
    canvas.style.top = ((window.innerHeight/100) * 6) + "px";
}

/**
 * This function performs the throttling technique.
 * 
 * @param {function} func a function to call...
 * @param {number} delay the delay between each call.
 * @param  {...any} args additional args to pass to the function
 */
var  throttleFunction  =  function (func, delay, ...args) {
    // If setTimeout is already scheduled, no need to do anything
	if (timerId != undefined) {
        // key_queue.push(key)
		return 
	}

	// Schedule a setTimeout after delay seconds
	timerId = setTimeout(function () {
        console.log("Sending...")
		func(...args)
		
		// Once setTimeout function execution is finished, timerId = undefined so that in <br>
		// the next scroll event function execution can be scheduled by the setTimeout
		timerId  =  undefined;
    }, delay)
    
    return 
}