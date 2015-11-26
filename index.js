var exec = require('child_process').execSync;
var path = require('path');

var options = {
	encoding : 'UTF-8'
};

exports.pythonVersion = function () {
	var script = path.resolve(__dirname, 'python/version.py');
	return exec('python ' + script, options);
};

exports.moveDetection = function (frame1, frame2) {
	var script = path.resolve(__dirname, 'python/movedetector.py');
	var pyRect = exec('python ' + script + ' ' + frame1 + ' ' + frame2, options);
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
	var script = path.resolve(__dirname, 'python/webcam_frame.py');
	return exec('python ' + script, options);
};
