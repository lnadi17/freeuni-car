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
    ctx.font = '23px Abel';
    ctx.textAlign ='center';
    ctx.textBaseline = 'top';
    ctx.strokeStyle = 'black';  // a color name or by using rgb/rgba/hex values
    ctx.fillStyle = 'white';  // a color name or by using rgb/rgba/hex values
    ctx.fillText('Location: ' + locationString, canvas.width / 2, 10); // text and position
    ctx.strokeText('Location: ' + locationString, canvas.width / 2, 10); // text and position
}

function drawBrightness(canvas) {
    var img = cv.imread(canvas)
    var imgRgb = new cv.Mat();
    var imgGray = new cv.Mat();

    cv.cvtColor(img, imgGray, cv.COLOR_RGBA2GRAY, 0);
    var srcVec = new cv.MatVector();
    srcVec.push_back(imgGray);

    var hist = new cv.Mat();
    var mask = new cv.Mat();
    // You can try more different parameters
    cv.calcHist(srcVec, [0], mask, hist, [256], [0, 255], false);
    let result = cv.minMaxLoc(hist, mask);
    let max = result.maxVal;

    var brightness = 0;
    for (let i = 0; i < 256; i++) {
        let binVal = hist.data32F[i] * img.rows / max;
        brightness += binVal;
    }

    brightness = brightness / 256;
    if (brightness > 100) {
        brightness = 100;
    }

    console.log(brightness);

    img.delete();
    imgGray.delete();
    imgRgb.delete();
    srcVec.delete();
    hist.delete();
    mask.delete();
}

function drawDanger(canvas) {
    var ctx = canvas.getContext('2d');
    ctx.font = '30px Abel';
    ctx.textAlign ='left';
    ctx.textBaseline = 'top';
    ctx.fillStyle = 'red';  // a color name or by using rgb/rgba/hex values
    ctx.fillText('Danger Ahead!', 10, 10); // text and position
    // ctx.strokeStyle = 'black';  // a color name or by using rgb/rgba/hex values
    // ctx.strokeText('Danger Ahead!', 10, 10); // text and position
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

    var lowRed = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [r_l_h, r_l_s, r_l_v, 0]);
    var highRed = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [r_u_h, r_u_s, r_u_v, 255]);

    var lowMagenta = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [174, r_l_s, r_l_v, 0]);
    var highMagenta = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [255, r_u_s, r_u_v, 255]);

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