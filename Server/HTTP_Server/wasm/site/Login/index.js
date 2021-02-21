import wasm, {login, get_wasm_memory_buffer_pointer} from "../node_modules/web-client/web_client.js";
import {OnStart} from "../Login/on-start.js";
import {Login} from "../Login/login.js";
export {wasm, login, get_wasm_memory_buffer_pointer, showPassword, sign_in, module};

let module;

let onStart = new OnStart();
onStart.loadModule().then(m => { 
    module = m
});

/**
 * This function can show or hide the password from the user
 */
function showPassword() {
    if (document.getElementById('password').getAttribute('type') == 'password') {
        document.getElementById('password').setAttribute('type', 'text');
    } else { 
        document.getElementById('password').setAttribute('type', 'password');
    }
}

/**
 * This function called each time the user press the sign in button
 */
async function sign_in() {
    console.log("damn");
    new Login().start();
}