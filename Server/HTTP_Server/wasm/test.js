
var loadedImages = 0;

        // Create a variable from the first image
        var ImageA = new Image(250, 190);
        ImageA.src = "https://www.jpost.com//HttpHandlers/ShowImage.ashx?id=375469&w=822&h=537";

        // Create a variable from the second image
        var ImageB = new Image(250, 190);
        ImageB.src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmkK8A1lJR-e0hHsPGl5jeskzg6zAyAnDzsQ&usqp=CAU";

        /**
         * Callback that should be executed when the images are finally loaded.
         * 
         *  
         **/
        var onImagesLoaded =  function () {
            // Increment the images loaded flag
            loadedImages++;
            console.log("load")

            // Skip execution of the callback if the 2 images have been not loaded
            // Otherwise continue with the diff
            if(loadedImages != 2){
                return;
            }
            console.log(ImageA.height)
            console.log(ImageB.height)
            // Create the image that shows the difference between the images
            var diff = imagediff.diff(ImageA, ImageB);
            // Create a canvas with the imagediff method (with the size of the generated image)
            var canvas = document.getElementsByTagName("canvas")[0];

            var context = canvas.getContext('2d');

            // Draw the generated image with differences on the canvas
            context.putImageData(diff, 0, 0);
            // Add the canvas element to the div element to show
            // document.getElementById("result-container").appendChild(canvas);

            // Display some alert !
            alert("Done!");
        };

        // Set the onLoad callback of the images
        ImageA.onload = onImagesLoaded;
        ImageB.onload = onImagesLoaded;

