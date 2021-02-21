import {wasm, showPassword, sign_in} from "../Login/index.js";
export {OnStart};

class OnStart {
    constructor() {
        this.loadingBar = new LoadingBar();
    }

    startLoadingBar() {
        this.loadingBar.setToMiddle();
        this.loadingBar.start();
    }

    stopLoadingBar() {
        this.loadingBar.setToBottom();
        this.loadingBar.stop();
    }

    startEnterAnimation() {
        document.getElementsByClassName('box')[0].style.visibility = "visible";
        document.getElementsByClassName('loading')[0].style.display = "none";
        document.getElementsByClassName('box')[0].style.animation = "boxEnter 2s";
    }

    async loadModule() {
        return new Promise(async resolve => {
            this.startLoadingBar();

            let module = await wasm("../node_modules/web-client/web_client_bg.wasm");

            this.stopLoadingBar();

            this.startEnterAnimation();

            document.getElementById('show-password').addEventListener('click', showPassword, false);
            document.getElementsByClassName("sign-in")[0].addEventListener("click", sign_in);
            document.getElementById("username").focus();

            resolve(module);
        });
    }
}

/**
 * This class is the Loading bar.
 */
class LoadingBar {
    constructor() { 
        /** @private @let bar */
        this.bar = document.getElementsByClassName("slider")[0];
    }

    setToMiddle() {
        this.bar.top = "50%";
        this.bar.left = "50%";
    }

    setToBottom() {
        this.bar.top = "60%";
        this.bar.left = "45%";
    }

    /**
     * This function starts the loading bar.
     */
    start() {
        document.getElementsByClassName('loading')[0].style.display = "inline";
    }

    /**
     * This function stops the loading bar.
     */
    stop() {
        document.getElementsByClassName('loading')[0].style.display = "none";
    }
}