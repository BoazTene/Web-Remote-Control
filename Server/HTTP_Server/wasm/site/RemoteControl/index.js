import wasm, {get_image, send_key, keys, send_mouse_pos, store_value_in_wasm_memory_buffer_index_zero, get_wasm_memory_buffer_pointer, close, Keyboard, web_socket} from "../node_modules/web-client/web_client.js";
import {OnStart} from "../RemoteControl/on_start.js";


export {onWindowResize, keys, get_image, send_key};

let keyboard;

setInterval(function () {
    // let key_queue_temp = key_queue.map((x) => x);
    // for (let i = key_queue_temp.length; i > 0; i--) {
    //     console.log(key_queue_temp)

    //     Keyboard.press_key(key_queue_temp[i-1]);
    //     key_queue.pop(key_queue.indexOf(key_queue[i-1]));
    // }
    timerId = undefined;
    // key_queue = []
    // console.log(key_queue)
    // let wasmMemory = new Uint8Array(module.memory.buffer);
    // var bufferPointer = get_wasm_memory_buffer_pointer();
    // if (wasmMemory[bufferPointer] == 0) {
    //     timerId = undefined;
    // }
}, 5)
let module;
let timerId;
let key_queue = [];


var canvas = document.getElementById('canvas');
var ctx = canvas.getContext("2d");

new OnStart(canvas, ctx, wasm).start().then(m => {
        module = m;
        eventListeners();
        let socket = new web_socket("ws://localhost:9898");
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
    document.onkeydown = onKeyPress;
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
    send_mouse_pos(event.clientX, event.clientY);
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
            timerId = throttleFunction(Keyboard.key_combination, 5, key, timerId);
        } else {
            timerId = throttleFunction(Keyboard.press_key, 5, event.key, timerId);
        }
        
        event.preventDefault();

    }

    

var  throttleFunction  =  function (func, delay, key, timerId) {
    // If setTimeout is already scheduled, no need to do anything
    console.log(timerId)
	if (timerId) {
        key_queue.push(key)
		return
	}

	// Schedule a setTimeout after delay seconds
	timerId  =  setTimeout(function () {
        // for (let i = 0; i < key_queue.length; i++) if (key_queue.includes(key)) key_queue.pop(key_queue.indexOf(key));
        console.log("Sending...")
		func(key)
		
		// Once setTimeout function execution is finished, timerId = undefined so that in <br>
		// the next scroll event function execution can be scheduled by the setTimeout
		timerId  =  undefined;
    }, delay)
    
    return timerId
}

/**
 * This function called each time the 'mouseclick' event is triggered.
 * 
 * The function sends to the Http_api the mouse x, y + the mouse state 
 * 
 * @param {event} event 
 */
function onMouseClicked(event){
    module.get_image();
    console.log("Mouse cicked at x: " + event.clientX + " y: " + event.clientY);
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