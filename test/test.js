var should = require('should')
	, opencv = require('../index')
	, fs = require('fs');

var image1 = fs.readFileSync('test/test1.jpg', {encoding: 'base64'});
var image2 = fs.readFileSync('test/test2.jpg', {encoding: 'base64'});
var image3 = fs.readFileSync('test/test3.jpg', {encoding: 'base64'});

describe('Opencv', function () {
	it('pythonVersion', function () {
		console.log('Development with PYTHON 2.7');
		console.log(opencv.pythonVersion());
	});
	describe('#moveDetection', function () {
		it('find=0', function (done) {
			opencv.moveDetection({
				'image1': image1,
				'image2': image2
			}, function (data, error) {
				if (error) {
					done(error);
				}
				should.equal(0, data.x);
				should.equal(0, data.y);
				should.equal(0, data.w);
				should.equal(0, data.h);
				done();
			});
		});
		it('find=1', function (done) {
			opencv.moveDetection({
				'image1': image1,
				'image2': image3
			}, function (data, error) {
				if (error) {
					done(error);
				}
				should.equal(254, data.x);
				should.equal(1, data.y);
				should.equal(260, data.w);
				should.equal(321, data.h);
				done();
			});
		});
	});
	describe('#faceDetection', function () {
		it('find', function (done) {
			opencv.faceDetection({
				'image': image1,
				'haarcascade': 'test/haarcascade_frontalface_default.xml'
			}, function (data, error) {
				if (error) {
					done(error);
				}
				should.equal(11, data.faces.length);
				done();
			});
		});
	});
});
