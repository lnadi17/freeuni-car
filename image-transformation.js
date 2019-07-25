function decolorize(canvas) {
    var img = cv.imread(canvas);
    var imgGray = new cv.Mat();

    cv.cvtColor(img, imgGray, cv.COLOR_RGBA2GRAY, 0);
    cv.imshow(canvas, imgGray);

    img.delete();
    imgGray.delete();
}

function drawLocation(canvas, locationString) {
    var ctx = canvas.getContext('2d');
    ctx.font = '23px Times New Roman';
    ctx.textAlign ='center';
    ctx.textBaseline = 'top';
    ctx.strokeStyle = 'black';  // a color name or by using rgb/rgba/hex values
    ctx.fillStyle = 'white';  // a color name or by using rgb/rgba/hex values
    ctx.fillText('Location: ' + locationString, canvas.width / 2, 10); // text and position
    ctx.strokeText('Location: ' + locationString, canvas.width / 2, 10); // text and position
}

function computeBrightness(canvas) {
    var ctx = canvas.getContext('2d');
    var imdata = ctx.getImageData(0, 0, canvas.width, canvas.height);
    var mat = cv.matFromArray(imdata, 24); // 24 for rgba

    var data = mat.data(); // output is a Uint8Array that aliases directly into the Emscripten heap
    var channels = mat.channels();

    var brightness = 0;

    for (var i = 0, j = 0; i < data.length; i += channels, j += 3) {
        let r = imdata.data[j];
        let g = imdata.data[j + 1];
        let b = imdata.data[j + 2];
        brightness += (r + g + b) / 3;
    }

    console.log(brightness / data.length);
}

function drawDanger(canvas) {
    var ctx = canvas.getContext('2d');
    ctx.font = '30px Times New Roman';
    ctx.textAlign ='left';
    ctx.textBaseline = 'top';
    ctx.strokeStyle = 'black';  // a color name or by using rgb/rgba/hex values
    ctx.fillStyle = 'red';  // a color name or by using rgb/rgba/hex values
    ctx.fillText('Danger Ahead!', 10, 10); // text and position
    ctx.strokeText('Danger Ahead!', 10, 10); // text and position
}

var r_l_h = 0
var r_l_s = 0
var r_l_v = 97
var r_u_h = 24
var r_u_s = 255
var r_u_v = 180

var g_l_h = 55
var g_l_s = 121
var g_l_v = 49
var g_u_h = 97
var g_u_s = 255
var g_u_v = 204

function detectLines(canvas) {
    var img = cv.imread(canvas);
    var imgColor = new cv.Mat();
    var hsvImg = new cv.Mat();
    cv.cvtColor(img, imgColor, cv.COLOR_RGBA2RGB, 0);
    cv.cvtColor(imgColor, hsvImg, cv.COLOR_RGB2HSV, 0);

    var redMask = new cv.Mat();
    var magentaMask = new cv.Mat();

    let lowRed = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [r_l_h, r_l_s, r_l_v, 0]);
    let highRed = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [r_u_h, r_u_s, r_u_v, 255]);

    let lowMagenta = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [174, r_l_s, r_l_v, 0]);
    let highMagenta = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [255, r_u_s, r_u_v, 255]);

    cv.inRange(hsvImg, lowRed, highRed, redMask);
    cv.inRange(hsvImg, lowMagenta, highMagenta, magentaMask);

    // Add red and magenta to get full red mask
    var fullRedMask = new cv.Mat();
    var addMask = new cv.Mat();
    cv.add(redMask, magentaMask, fullRedMask, addMask, -1);

    cv.imshow(canvas, fullRedMask);

    img.delete();
    imgColor.delete();
    hsvImg.delete();

    redMask.delete();
    magentaMask.delete();

    lowRed.delete();
    highRed.delete();

    lowMagenta.delete();
    highMagenta.delete();

    fullRedMask.delete();
    addMask.delete();
}