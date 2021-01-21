import wasm, {host, get_wasm_memory_buffer_pointer, lahoh} from "../node_modules/web-client/web_client.js";
let module;

function showPassword(){
    if (document.getElementById('password').getAttribute('type') == 'password') {
        document.getElementById('password').setAttribute('type', 'text');
    } else { 
        document.getElementById('password').setAttribute('type', 'password');
    }
}

async function load_module(){
    console.log(wasm)
    var bar = document.getElementsByClassName("slider")[0];
    bar.top = "50%";
    bar.left = "50%";

    module = await wasm("../node_modules/web-client/web_client_bg.wasm");

    // console.log(module.create_buffer(2));
    console.log(module)
    document.getElementsByClassName('box')[0].style.visibility = "visible";
    document.getElementsByClassName('loading')[0].style.display = "none";
    document.getElementsByClassName('box')[0].style.animation = "boxEnter 2s";

    bar.top = "60%";
    bar.left = "45%";

    document.getElementById('show-password').addEventListener('click', showPassword, false);


}

load_module()


document.getElementsByClassName("sign-in")[0].addEventListener("click", register);



async function register() {
    var register = new Register();
    register.start();
    
}

/**
 * This Class is the Buffer handler.
 * 
 * The Class can write, read in the wasm memory.
 * You can use this Class to send messages between the js and the wasm
 */
class Buffer{
    constructor(module){
        this.module = module;
        this.wasmMemory = new Uint8Array(module.memory.buffer);
        this.bufferPointer = this.getBufferPointer();
        console.log(this.bufferPointer)
    }
    

    // this getter gets the start location of the buffer in the memory
    getBufferPointer(){
        return get_wasm_memory_buffer_pointer();
    }

    // this method read byte at the byte index 
    readAtByte(byteIndex){
        console.log(this.wasmMemory)
        return this.wasmMemory[this.bufferPointer + byteIndex];
    }

    // this method write a byte at the byte index
    writeAtByte(byteIndex, byte){
        this.wasmMemory[this.bufferPointer + byteIndex] = byte;
    }
}

/**
 * This class is used to Login.
 * The class gets the password and the username from the inputs tag sends a md5 hash of them to the server for verification
 * By the result get from the server it determines what to do.
 */
class Register{
    constructor(buffer, module){
        if (password.value == "" || username.value == ""){
            password.style.borderColor = 'red';
            username.style.borderColor = 'red';
            

            return
        } 

        password.style.borderColor = '';
        username.style.borderColor = '';

        this.password = password.value;
        this.username = username.value;
    }

    requestEnd(){
        const event = new Event("onrequestend");

        document.dispatchEvent(event);
    }

    requestEndHandler(){
         document.getElementsByClassName('loading')[0].style.display = "none";
        let wasmMemory = new Uint8Array(module.memory.buffer);
        var bufferPointer = get_wasm_memory_buffer_pointer();

        if (wasmMemory[bufferPointer] == 1) {
            // window.location.href = "http://localhost:5000?username=" + this.username + "&password=" + this.password;
        } else {
            document.getElementById("message").innerHTML = "<p1>The UserName or Password incorrect<p1>";
        }
    }

    start(){
        if (password.value != "" && username.value != "") {
             document.getElementsByClassName('loading')[0].style.display = "inline";
        } else {
            return
        }
        host(username.value, password.value);
        var that = this;

        // window.addEventListener('onrequestend', function () {
        //     that.requestEndHandler();
        // }, false);
    }
    
}