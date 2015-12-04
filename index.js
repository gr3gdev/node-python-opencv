var child = require('child_process')
	, path = require('path')
	, net = require('net')
	, fs = require('fs');

var options = {
	encoding: 'UTF-8'
};

var idx = 0;
var webcamPort = 4000;
var ports = [4001, 4002, 4003, 4004, 4005];

exports.conf = function (json) {
	// Ports CONF (Communication with Python)
	if (json.ports !== undefined) {
		ports = json.ports;
	}
	// Webcam CONF
	if (json.webcam !== undefined) {
		// Port
		if (json.webcam.port !== undefined) {
			webcamPort = json.webcam.port;
		}
	}
};

var opencvClient = function (pyScript, callback) {
	idx++;
	if (idx > ports.length) {
		idx = 0;
	}
	var script = path.resolve(__dirname, pyScript);
	var command = 'python ' + script + ' ' + ports[idx];
	child.exec(command, options, function (error, stdout, stderr) {
		if (error) {
			console.log(stderr);
		}
	});
	var client = new net.Socket({
		readable: true,
		writable: true
	});
	var timeout = null;
	var tentatives = 5;
	var count = 0;
	client.on('error', function (err) {
		count++;
		// 5 tentatives de connexion
		if (count < tentatives) {
			timeout = setTimeout(function () {
				// Nouvelle tentative de connexion
				client.connect(port, '127.0.0.1');
			}, 100);
		} else {
			callback(client, null, err);
		}
	});
	client.on('connect', function () {
		clearTimeout(timeout);
		client.write('INIT');
	});
	client.on('data', function (data) {
		callback(client, data);
	});
	client.connect(ports[idx], '127.0.0.1');
};

exports.pythonVersion = function () {
	var script = path.resolve(__dirname, 'python/version.py');
	return child.execSync('python ' + script, options);
};

exports.moveDetection = function (json, callback) {
	opencvClient('python/movedetector.py', function (client, data, error) {
		var message = data.toString('UTF-8');
		var buffer1 = json.image1.length + 5;
		var buffer2 = json.image2.length + 5;
		if (error !== undefined) {
			client.write('STOP');
			callback(null, error);
		}
		if (message == 'INITIALIZED') {
			client.write('BUF1:' + buffer1);
		} else if (message == 'BUFFER1 RECEIVED') {
			client.write('IMG1:' + json.image1);
		} else if (message == 'IMAGE1 RECEIVED') {
			client.write('BUF2:' + buffer2);
		} else if (message == 'BUFFER2 RECEIVED') {
			client.write('IMG2:' + json.image2);
		} else if (message == 'IMAGE2 RECEIVED') {
			client.write('EXECUTE');
		} else {
			client.write('STOP');
			callback(JSON.parse(message));
		}
	});
};

exports.faceDetection = function (json, callback) {
	opencvClient('python/facedetector.py', function (client, data, error) {
		var message = data.toString('UTF-8');
		var buffer1 = json.image.length + 5;
		var buffer2 = json.haarcascade.length + 5;
		if (error !== undefined) {
			client.write('STOP');
			callback(null, error);
		}
		if (message == 'INITIALIZED') {
			client.write('BUF1:' + buffer1);
		} else if (message == 'BUFFER1 RECEIVED') {
			client.write('IMG1:' + json.image);
		} else if (message == 'IMAGE1 RECEIVED') {
			client.write('BUF2:' + buffer2);
		} else if (message == 'BUFFER2 RECEIVED') {
			client.write('PTH1:' + json.haarcascade);
		} else if (message == 'PATH1 RECEIVED') {
			client.write('EXECUTE');
		} else {
			client.write('STOP');
			callback(JSON.parse(message));
		}
	});
};

exports.webcam = Webcam;

function Webcam() {
	var script = path.resolve(__dirname, 'python/webcam_frame.py');
	child.exec('python ' + script + ' ' + webcamPort, options, function (error, stdout, stderr) {
		console.log(stdout);
	});
	this.client = new net.Socket({
		readable: true
	});
	this.client.connect(webcamPort, '127.0.0.1');
	this.callback = null;
	var self = this;
	var marqueur = 'WEBCAM';
	var tmp_image = null;
	this.client.on('data', function (data) {
		var str = data.toString('UTF-8');
		var pos = str.indexOf(marqueur);
		if (pos >= 0) {
			if (tmp_image !== null) {
				tmp_image += str.substring(0, pos);
				if (self.callback !== null) {
					self.callback(tmp_image);
				}
			}
			tmp_image = str.substring(pos + marqueur.length);
		} else {
			tmp_image += str;
		}
	});
};
Webcam.prototype.frame = function (callback) {
	this.callback = callback;
};