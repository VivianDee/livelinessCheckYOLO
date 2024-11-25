function onOpenCvReady() {
    cv['onRuntimeInitialized'] = () => {
        main();
    }
}

function main() {
    // Dynamically get the server URL and use the same host and protocol
    var serverUrl = window.location.protocol + '//' + window.location.hostname;

    if (window.location.port) {
        serverUrl += ':' + window.location.port;
    }

    var socket = io(serverUrl);

    socket.on('connect', function () {
        console.log("Connected...!", socket.connected);
    });
    socket.on('connect_error', (err) => {
        console.log('Connection Error: ', err);
    });

    socket.on('connect_timeout', () => {
        console.log('Connection Timeout');
    });

    const video = document.querySelector("#videoElement");
    video.width = 500;
    video.height = 375;

    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
                video.play();
            })
            .catch(function (err0r) {
                console.log(err0r);
                console.log("Something went wrong!");
            });
    }

    var videoId = 'video';
    var scaleFactor = 0.25;
    var snapshots = [];

    function capture(video, scaleFactor) {
        if (scaleFactor == null) {
            scaleFactor = 1;
        }
        var w = video.videoWidth * scaleFactor;
        var h = video.videoHeight * scaleFactor;
        var canvas = document.createElement('canvas');
        canvas.width = w;
        canvas.height = h;
        var ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, w, h);
        return canvas;
    }

    // let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
    // let dst = new cv.Mat(video.height, video.width, cv.CV_8UC1);
    // let cap = new cv.VideoCapture(video);

    const FPS = 22;

    setInterval(() => {
        // cap.read(src);

        var type = "image/png";
        var video_element = document.getElementById("videoElement")
        var frame = capture(video_element, 1)
        var data = frame.toDataURL(type);
        // data = data.replace('data:' + type + ';base64,', ''); //split off junk

        socket.emit('image', data);
    }, 1000 / FPS);

    socket.on('response_back', function (image) {
        // console.log("Received response:", image);
        const image_id = document.getElementById('image');
        image_id.src = image.image;
    });
}