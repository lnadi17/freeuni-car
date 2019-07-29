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
    ctx.font = '30px Abel';
    ctx.textAlign ='center';
    ctx.textBaseline = 'top';
    ctx.fillStyle = 'white';  // a color name or by using rgb/rgba/hex values
    ctx.fillText('Location: ' + locationString, canvas.width / 2, 10); // text and position
}

function drawBattery(canvas) {
    var ctx = canvas.getContext('2d');
    ctx.font = '30px Abel';
    ctx.textAlign ='right';
    ctx.textBaseline = 'top';
    ctx.fillStyle = 'white';  // a color name or by using rgb/rgba/hex values
    ctx.fillText('Battery: ' + percentage, canvas.width / 2, 10); // text and position
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
    var result = cv.minMaxLoc(hist, mask);
    var max = result.maxVal;

    var brightness = 0;
    for (var i = 0; i < 256; i++) {
        var binVal = hist.data32F[i] * img.rows / max;
        brightness += binVal;
    }

    brightness = brightness / 256;
    if (brightness > 100) {
        brightness = 100;
    }

    // console.log(brightness);

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

var g_l_h = 66
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
    var greenMask = new cv.Mat();

    var lowRed = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [r_l_h, r_l_s, r_l_v, 0]);
    var highRed = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [r_u_h, r_u_s, r_u_v, 255]);

    // lowMagenta previously was 174
    var lowMagenta = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [160, r_l_s, r_l_v, 0]);
    var highMagenta = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [255, r_u_s, r_u_v, 255]);

    var lowGreen = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [g_l_h, g_l_s, g_l_v, 0]);
    var highGreen = new cv.Mat(hsvImg.rows, hsvImg.cols, hsvImg.type(), [g_u_h, g_u_s, g_u_v, 255]);

    cv.inRange(hsvImg, lowRed, highRed, redMask);
    cv.inRange(hsvImg, lowMagenta, highMagenta, magentaMask);
    cv.inRange(hsvImg, lowGreen, highGreen, greenMask);

    // Add red and magenta to get full red mask
    var fullRedMask = new cv.Mat();
    var addMask = new cv.Mat();
    cv.add(redMask, magentaMask, fullRedMask, addMask, -1);

    var rContours = new cv.MatVector();
    var gContours = new cv.MatVector();
    var hierarchy = new cv.Mat();

    cv.findContours(fullRedMask, rContours, hierarchy, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE);
    cv.findContours(greenMask, gContours, hierarchy, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE);

    // Draw approximate contours
    var mask;
    if (rContours.size() > 0 && gContours.size() > 0) {
        var redCoords = drawLine(img, rContours, "r");
        var greenCoords = drawLine(img, gContours, "g");

        if (lineGet) {
            if ((redCoords[0] < 2147483647 && redCoords[1] < 2147483647) && (greenCoords[0] > -241748367 && greenCoords[1] > -241748367)) {
                datachannel.send("line " + redCoords + " " + greenCoords);
            } else {
                datachannel.send("line no");
            }
            console.log("sent line")
            lineGet = false;
        }    
    }

    cv.imshow(canvas, img);

    img.delete();
    imgColor.delete();
    hsvImg.delete();

    redMask.delete();
    magentaMask.delete();
    greenMask.delete();

    lowRed.delete();
    highRed.delete();

    lowMagenta.delete();
    highMagenta.delete();

    lowGreen.delete();
    highGreen.delete();  

    fullRedMask.delete();
    addMask.delete();

    rContours.delete();
    gContours.delete();
    hierarchy.delete();
}

function drawLine(img, contours, color) {
    //var mask = new cv.Mat.zeros(img.rows, img.cols, cv.CV_8UC3);
    var largestAreaIndex = 0;

    for (var i = 0; i < contours.size(); i++) {
        var area = cv.contourArea(contours.get(i), false);
        if (area > 400 && area >= contours.get(largestAreaIndex) < area) {
            largestAreaIndex = i;
        }
    }

    var polygon = new cv.MatVector();
    var tmp = new cv.Mat();
    var arcLength = cv.arcLength(contours.get(largestAreaIndex), true)
    cv.approxPolyDP(contours.get(largestAreaIndex), tmp, arcLength * 0.01, true);
    polygon.push_back(tmp);
    // cv.drawContours(mask, polygon, 0, new cv.Scalar(255, 255, 255), -1);

    // Draw approximate line
    var line = new cv.Mat();
    cv.fitLine(polygon.get(0), line, cv.DIST_L2, 0, 0.01, 0.01)

    var vx = line.data32F[0];
    var vy = line.data32F[1];
    var x = line.data32F[2];
    var y = line.data32F[3];
    var lefty = Math.round((-x * vy / vx) + y);
    var righty = Math.round(((img.cols - x) * vy / vx) + y);
    var point1 = new cv.Point(img.cols - 1, righty);
    var point2 = new cv.Point(0, lefty);

    // lefty and righty should be between C++'s integer limit
    if ((lefty < 2147483647 && righty < 2147483647) && (lefty > -241748367 && righty > -241748367)) {
        cv.line(img, point1, point2, new cv.Scalar(0, 0, 0), 2, cv.LINE_AA, 0);
    }

    tmp.delete();
    polygon.delete();
    //mask.delete();
    line.delete();

    return [lefty, righty];
}