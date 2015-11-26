var exec = require('child_process').execSync;

var options = {
	encoding : 'UTF-8'
};

exports.pythonVersion = function () {
	return exec('python python/version.py', options);
};

exports.moveDetection = function (frame1, frame2) {
	var pyRect = exec('python python/movedetector.py ' + frame1 + ' ' + frame2, options);
	var rect = {};
	if (pyRect.length > 0) {
		rect = JSON.parse(pyRect);
	}
	return rect;
};

exports.webcam = Webcam;

function Webcam() {
};
Webcam.prototype.frame = function () {
	return exec('python python/webcam_frame.py', options);
};
