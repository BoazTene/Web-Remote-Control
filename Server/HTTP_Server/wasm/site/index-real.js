let js = null

// import("./node_modules/web-client/web_client.js");
load_module();

var password = document.getElementById("password");
var username = document.getElementById("username");


// document.getElementsByClassName("sign-in")[0].addEventListener("click", sign_in);



async function load_module(){
    js = await import("./node_modules/web-client/web_client.js");
    console.log(js.lahoh("d"));
    document.getElementsByClassName('box')[0].style.visibility = "visible";
}

function sign_in(){
    if (password.value == "" || username.value == ""){
        password.style.borderColor = 'red';
        username.style.borderColor = 'red';
        return
    } 

    password.style.borderColor = '';
    username.style.borderColor = '';
    
    console.log(js);

    wasm.login(username.value, password.value);
    
    // js.then(js => {
    //     js.login(username.value, password.value);
    //   });
}
