import {onWindowResize, keys, get_image} from "../RemoteControl/index.js";
import {DrawImage} from "../RemoteControl/image.js";
export {OnStart};

/* This Class runs at first **/
class OnStart {
    constructor(canvas, ctx, wasm) {
        /** @private @let wasm */
        this.wasm__ = wasm;

        /**@private @const canvas */
        this.canvas__ = canvas;

        /**@private @const ctx */
        this.ctx__ = ctx;
    }
    
    /**
     * This method load and return the module from this.wasm__ 
     */
    async loadModule() {
        return new Promise(async resolve => {
            let module = await this.wasm__();

            resolve(module);
        });

    }

    /**
     * This method loads the module,
     * sets the page to the fit the window,
     * sets some event listeners,
     * sets interval for the image drawing.
     */
    async start() {
        return new Promise(async resolve => {
            let module = await this.loadModule();
            
            onWindowResize();

            window.addEventListener("resize", onWindowResize);
            
            let that = this;

            window.addEventListener("newimage", function (event) {

                let drawImage = new DrawImage(that.canvas__, that.ctx__, event);
                drawImage.drawImage();
            });
            
            setInterval(function() {
                if (!document.hidden) {
                    get_image();
                }
            }, 300)

            keys();

            document.getElementsByTagName('body')[0].style.visibility = "visible";
            document.getElementsByClassName('loader')[0].style.visibility = "hidden";
            document.getElementById('loader-text').style.visibility = "hidden";

            resolve(module);
        });
    }
}

