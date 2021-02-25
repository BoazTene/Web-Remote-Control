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
            // offscreen = new OffscreenCanvas(this.canvas__.width, this.canvas__.height);
            // gl = offscreen.getContext('2d');

            window.addEventListener("resize", onWindowResize);
            
            let that = this;

            window.addEventListener("newimage", function (event) {
                // alert("data:image/jpeg;base64," + event.detail);
                
                let drawImage = new DrawImage(that.canvas__, that.ctx__, event);
                drawImage.drawImage();
                // alert(1)
            });
            
            // setInterval(function() {
            //     if (!document.hidden) {
            //         // get_image();
            //     }
            // }, 300)

            function image() {
                if (!document.hidden) {
                    get_image();
                    setTimeout(function() {
                        requestAnimationFrame(image);
                    }, 200);
                }
                
            };

            requestAnimationFrame(image)

            keys();

            document.getElementsByTagName('body')[0].style.visibility = "visible";
            document.getElementsByClassName('loader')[0].style.visibility = "hidden";
            document.getElementById('loader-text').style.visibility = "hidden";

            resolve(module);
        });
    }
}

