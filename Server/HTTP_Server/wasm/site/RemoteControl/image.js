export {DrawImage};

/**
 * This class is used to draw new image on the canvas.
 */
class DrawImage {
    /**
     * 
     * @param {canvas} canvas
     * @param {ctx} ctx 
     * @param {event - 'newimage'} event 
     * @param {Image} img 
     */
    constructor(canvas, ctx, event, img=new Image()) {
        /** @private @const event */
        this.event__ = event;
        
        /** @private @const canvasContext */
        this.ctx__ = ctx;

        /** @public @const canvas */
        this.canvas = canvas;

        /** @private @let img */
        this.img__ = img;
    }

    get width() {
        return this.canvas.width;
    }

    get height() {
        return this.canvas.height;
    }

    get imageSrc() {
        return "data:image/jpeg;base64," + this.event__.detail;
    }

    set imageSrc(src) {
        this.img__.src = src;
    }

    /**
     * This function sets the src to the giving src, 
     * then it draws the image on the canvas.
     */
    drawImage() {
        this.imageSrc = this.imageSrc;
        return new Promise(resolve => {
            let that = this;


            this.img__.onload = function () {
                that.ctx__.drawImage(that.img__, 0, 0, that.width, that.height);

                resolve();
            }
        });
    }
}