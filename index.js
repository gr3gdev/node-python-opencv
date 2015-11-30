var child = require('child_process')
	, path = require('path')
	, net = require('net');

var options = {
	encoding: 'UTF-8'
};

exports.pythonVersion = function () {
	var script = path.resolve(__dirname, 'python/version.py');
	return child.execSync('python ' + script, options);
};

exports.moveDetection = function (frame1, frame2) {
	var script = path.resolve(__dirname, 'python/movedetector.py');
	var pyRect = child.execSync('python ' + script + ' ' + frame1 + ' ' + frame2, options);
	var rect = {};
	if (pyRect.length > 0) {
		rect = JSON.parse(pyRect);
	}
	return rect;
};

exports.faceDetection = function (frame, haarcascade) {
	var script = path.resolve(__dirname, 'python/facedetector.py');
	var pyJson = child.execSync('python ' + script + ' ' + frame + ' ' + haarcascade, options);
	var json = {};
	if (pyJson.length > 0) {
		json = JSON.parse(pyJson);
	}
	return json;
};

exports.webcam = Webcam;

function Webcam() {
	var script = path.resolve(__dirname, 'python/webcam_frame.py');
	child.exec('python ' + script, options, function (error, stdout, stderr) {
		console.log(stdout);
	});
	this.client = new net.Socket({
		readable: true
	});
	this.client.connect(4004, '127.0.0.1');
	this.image = null;
	var self = this;
	var marqueur = 'WEBCAMimgPY';
	var tmp_image = null;
	this.client.on('data', function (data) {
		var str = data.toString('UTF-8');
		console.log(str);
		var pos = str.indexOf(marqueur);
		if (pos >= 0) {
			if (tmp_image !== null) {
				tmp_image += str.substring(0, pos);
				self.image = tmp_image;
			}
			tmp_image = str.substring(pos + marqueur.length);
		} else {
			tmp_image += str;
		}
	});
};
Webcam.prototype.frame = function (callback) {
	callback(this.image);
};