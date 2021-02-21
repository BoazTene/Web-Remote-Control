import {login, get_wasm_memory_buffer_pointer, module} from "../Login/index.js";
export {Login};

/**
 * This class is used to Login.
 * The class gets the password and the username from the inputs tag sends a md5 hash of them to the server for verification
 * By the result get from the server it determines what to do.
 */
class Login {
    constructor() {
        if (password.value == "" || username.value == ""){
            password.style.borderColor = 'red';
            username.style.borderColor = 'red';
            return
        } 

        password.style.borderColor = '';
        username.style.borderColor = '';

        /** @private @const password */
        this.password = password.value;

        /** @private @const username */
        this.username = username.value;
    }

    /**
     * This function runs when the request is done.
     */
    requestEnd() {
        const event = new Event("onrequestend");

        document.dispatchEvent(event);
    }

    /**
     * This function is the called when the requst is done.
     * The function reads the Web Assembly memory buffer:
     * 1 => The Handshake went succefully.
     * 0 => The Handshake failed.
     * 3 => The handshake didn't end yet.
     * 
     * If the handshake failed the function will display a Username or password incorrect message.
     */
    requestEndHandler() {
        document.getElementsByClassName('loading')[0].style.display = "none";
        let wasmMemory = new Uint8Array(module.memory.buffer);
        var bufferPointer = get_wasm_memory_buffer_pointer();

        if (wasmMemory[bufferPointer] == 0) {
            password.style.borderColor = 'red';
            username.style.borderColor = 'red';
            document.getElementById("message").innerHTML = "<p1>The UserName or Password incorrect<p1>";
        } else if(wasmMemory[bufferPointer] == 3) {
            document.getElementById("message").innerHTML = "<p1>Something went wrong...<p1>";
        }
    }

    /**
     * This function Starts the http request to the Http_api server.
     */
    start() {
        document.getElementById("message").innerHTML = "";
        
        if (password.value == "" || username.value == "") return;
        document.getElementsByClassName('loading')[0].style.display = "inline";

        login(username.value, password.value);
        var that = this;

        window.addEventListener('onrequestend', function () {
            that.requestEndHandler();
        }, false);
    }
    
}