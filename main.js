var locationString = "Not yet known";

(function () {
    var signalObj = null;

    window.addEventListener('DOMContentLoaded', function () {
        var isStreaming = false;
        var start = document.getElementById('start');
        var stop = document.getElementById('stop');
        var video = document.getElementById('v');
        var canvas = document.getElementById('c');
        var ctx = canvas.getContext('2d');
        var capture = document.getElementById('capture');

        // Effects
        var faceEffect = document.getElementById('faceEffect');
        var isFaceEffectActive = false;

        var bwEffect = document.getElementById('bwEffect');
        var isBwEffectActive = false;

        var locationEffect = document.getElementById('locationEffect');
        var isLocEffectActive = false;

        var headlightsEffect = document.getElementById('headlightsEffect');
        var isHlEffectActive = false;

        start.addEventListener('click', function (e) {
            var address = document.getElementById('address').value;
            var protocol = location.protocol === "https:" ? "wss:" : "ws:";
            var wsurl = protocol + '//' + address;

            if (!isStreaming) {
                signalObj = new signal(wsurl,
                        function (stream) {
                            console.log('Got a stream.');
                            video.srcObject = stream;
                            video.play();
                        },
                        function (error) {
                            alert(error);
                        },
                        function () {
                            console.log('Websocket closed.');
                            video.srcObject = null;
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                            isStreaming = false;
                        },
                        function (message) {
                            alert(message);
                        }
                );
            }
        }, false);

        stop.addEventListener('click', function (e) {
            if (signalObj) {
                signalObj.hangup();
                signalObj = null;
            }
        }, false);

        // Wait until the video stream can play
        video.addEventListener('canplay', function (e) {
            if (!isStreaming) {
                canvas.setAttribute('width', video.videoWidth);
                canvas.setAttribute('height', video.videoHeight);
                isStreaming = true;
            }
        }, false);

        // Wait for the video to start to play
        video.addEventListener('play', function () {
            // Every 33 milliseconds copy the video image to the canvas
            setInterval(function () {
                if (video.paused || video.ended) {
                    return;
                }
                var w = canvas.getAttribute('width');
                var h = canvas.getAttribute('height');
                ctx.fillRect(0, 0, w, h);
                ctx.drawImage(video, 0, 0, w, h);

                if (isFaceEffectActive) {
                    detectFace(canvas);
                }

                if (isBwEffectActive) {
                    decolorize(canvas);
                }

                if (isLocEffectActive) {
                    drawLocation(canvas, locationString);
                }
            }, 33);
        }, false);

        // faceEffect.addEventListener('click', function () {
        //     console.log("Toggled face detection.");
        //     isFaceEffectActive = !isFaceEffectActive;
        //     console.log(isFaceEffectActive);
        // }, false);

        bwEffect.addEventListener('click', function () {
            console.log("Toggled black and white.");
            isBwEffectActive = !isBwEffectActive;
            console.log(isBwEffectActive);
        }, false);

        capture.addEventListener('click', function () {
            console.log("Clicked capture image.");
            var link = document.getElementById('link');
            link.setAttribute('download', 'freeuni-car-capture.png');
            link.setAttribute('href', canvas.toDataURL("image/png").replace("image/png", "image/octet-stream"));
            link.click();
        }, false);

        locationEffect.addEventListener('click', function () {
            isLocEffectActive = !isLocEffectActive;
            console.log("Toggled location.");
        }, false);

        headlightsEffect.addEventListener('click', function () {
            isHlEffectActive = !isHlEffectActive;
            var dt = "headlights " + isHlEffectActive;
            datachannel.send("headlights " + isHlEffectActive);
            console.log(dt);
        }, false);
    });
})();