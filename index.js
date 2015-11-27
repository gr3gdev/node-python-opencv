var process = require('child_process');
var path = require('path');

var options = {
	encoding : 'UTF-8'
};

exports.pythonVersion = function () {
	var script = path.resolve(__dirname, 'python/version.py');
	return process.execSync('python ' + script, options);
};

exports.moveDetection = function (frame1, frame2) {
	var script = path.resolve(__dirname, 'python/movedetector.py');
	var pyRect = process.execSync('python ' + script + ' ' + frame1 + ' ' + frame2, options);
	var rect = {};
	if (pyRect.length > 0) {
		rect = JSON.parse(pyRect);
	}
	return rect;
};

exports.faceDetection = function (frame, haarcascade) {
	var script = path.resolve(__dirname, 'python/facedetector.py');
	var pyJson = process.execSync('python ' + script + ' ' + frame + ' ' + haarcascade, options);
	var json = {};
	if (pyJson.length > 0) {
		json = JSON.parse(pyJson);
	}
	return json;
};

exports.webcam = Webcam;

function Webcam() {
};
Webcam.prototype.frame = function (callback) {
	var script = path.resolve(__dirname, 'python/webcam_frame.py');
	process.exec('python ' + script, options, function (error, stdout, stderr) {
		callback(stdout);
	});
};
