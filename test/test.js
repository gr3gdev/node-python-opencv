var should = require('should')
	, opencv = require('../index')
	, fs = require('fs');

var image1 = fs.readFileSync('test/test1.jpg', {encoding: 'base64'});
var image2 = fs.readFileSync('test/test2.jpg', {encoding: 'base64'});
var image3 = fs.readFileSync('test/test3.jpg', {encoding: 'base64'});

var imageR1 = fs.readFileSync('test/testr1.jpg', {encoding: 'base64'});

var detector = new opencv.detector({
	port: 4004
});

describe('Opencv', function () {
	it('pythonVersion', function () {
		console.log('Development with PYTHON 2.7');
		console.log(opencv.pythonVersion());
	});
	describe('#detector', function () {
		it('findMove=0', function (done) {
			detector.findMove({
				'image1': image1,
				'image2': image2
			}, function (data, err) {
				if (err) {
					done(err);
				}
				should.equal(0, data.x);
				should.equal(0, data.y);
				should.equal(0, data.w);
				should.equal(0, data.h);
				done();
			});
		});
		it('findMove=1', function (done) {
			detector.findMove({
				'image1': image1,
				'image2': image3
			}, function (data, err) {
				if (err) {
					done(err);
				}
				should.equal(254, data.x);
				should.equal(1, data.y);
				should.equal(260, data.w);
				should.equal(321, data.h);
				done();
			});
		});
		it('findFaces=11', function (done) {
			detector.findFaces({
				'image': image1,
				'haarcascade': 'test/haarcascade_frontalface_default.xml'
			}, function (data, err) {
				if (err) {
					done(err);
				}
				should.equal(11, data.faces.length);
				done();
			});
		});
		it('recognizeFaces=girl1', function (done) {
			detector.recognizeFaces({
				'csv': 'test/base.csv',
				'image': imageR1,
				'haarcascade': 'test/haarcascade_frontalface_default.xml'
			}, function (data, err) {
				if (err) {
					done(err);
				}
				should.equal(3, data.faces.length);
				for (var idx in data.faces) {
					should.equal('girl1', data.faces[idx].name);
				}
				done();
			});
		});
		it('close', function (done) {
			detector.close(function (data, err) {
				if (err) {
					done(err);
				}
				should.equal('Socket closed', data);
				done();
			});
		});
	});
});
