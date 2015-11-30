var should = require('should'), opencv = require('../index');

describe('Opencv', function () {
	it('pythonVersion', function () {
		var v = opencv.pythonVersion();
		v.should.startWith('2.7');
	});
	it('moveDetection AUCUN', function () {
		var rect1 = opencv.moveDetection('test/test1.jpg', 'test/test2.jpg');
		should.not.exist(rect1.x);
		should.not.exist(rect1.y);
		should.not.exist(rect1.w);
		should.not.exist(rect1.h);
	});
	it('moveDetection MOUVEMENT', function () {
		var rect2 = opencv.moveDetection('test/test1.jpg', 'test/test3.jpg');
		should.equal(254, rect2.x);
		should.equal(1, rect2.y);
		should.equal(260, rect2.w);
		should.equal(321, rect2.h);
	});
	it('faceDetection', function () {
		var res = opencv.faceDetection('test/test1.jpg', 'test/haarcascade_frontalface_default.xml');
		should.equal(11, res.faces.length);
	});
});
