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

    document.getElementsByClassName('box')[0].style.visibility = "visible";
    document.getElementsByClassName('loading')[0].style.display = "none";
    document.getElementsByClassName('box')[0].style.animation = "boxEnter 2s";

    bar.top = "60%";
    bar.left = "45%";

    document.getElementById('show-password').addEventListener('click', showPassword, false);
    document.getElementById("username").focus();
}

load_module()


document.getElementsByClassName("sign-in")[0].addEventListener("click", register);



async function register() {
    var register = new Register();
    register.start();
    
}

/**
 * This class is used to Register as host.
 * This class sends to the http api the username and password.
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
       }
    
}