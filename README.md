# node-python-opencv
*Module NodeJS pour python-opencv*

Ce module permet d'utiliser les fonctionnalités de opencv via python pour :

- la détection de mouvement
- la détection et la reconnaissance faciale
- le streaming d'une webcam


## Pré-requis :
- Installer **Python 2.7**
- Installer les modules python suivants : 
	- *python-opencv* (pour Windows compiler opencv-contrib)
	- *numpy*


## Installation :
    npm install node-python-opencv


## Utilisations :
**Streaming webcam :**

	var opencv = require('node-python-opencv');
	
	// Numéro de port facultatif
	var webcam = new opencv.webcam({
		port: 8090
	});
	webcam.frame(function (image) {
		// image est au format base64
	});


**Détection de mouvement entre 2 images :**

    var opencv = require('node-python-opencv');

	var image1 = fs.readFileSync('path/image1.jpg', {encoding: 'base64'});
	var image2 = fs.readFileSync('path/image2.jpg', {encoding: 'base64'});

	var detector = new opencv.detector({
		port: 9009
	});

	// Arguments :
	// image1 : image de base au format base64
	// image2 : image au format base64 où trouver les différences 
	detector.findMove({
		'image1': image1,
		'image2': image2
	}, function (data, err) {
		// Return JSON object {x: N, y: N, w: N, h: N}
		console.log(JSON.stringify(data));
	});


**Détection de visage(s) :**

    var opencv = require('node-python-opencv');

	var image = fs.readFileSync('path/image.jpg', {encoding: 'base64'});

	var detector = new opencv.detector({
		port: 9009
	});

	// Arguments :
	// image : image au format base64 où trouver les visages
	// haarcascade : fichier haarcascade à utiliser
	// scaleFactor (facultatif) : échelle de redimensionnement de l'image pour la détection
	// minNeighbors (facultatif) : Nombre de voisins que chaque rectangle détecté peut conserver 
	detector.findFaces({
		'image': image,
		'haarcascade': 'path/to/haarcascade_frontalface_default.xml',
		'scaleFactor': 1.2,
		'minNeighbors': 8
	}, function (data, err) {
		// Return JSON object {faces: [{x: N, y: N, w: N, h: N}, ...]}
		console.log(JSON.stringify(data));
	});


**Reconnaissance faciale :**

    var opencv = require('node-python-opencv');

	var image = fs.readFileSync('path/image.jpg', {encoding: 'base64'});

	var detector = new opencv.detector({
		port: 9009
	});

	// Arguments :
	// csv : base de données d'images à utiliser pour la reconnaissance
	// image : image au format base64 où trouver les visages
	// haarcascade : fichier haarcascade à utiliser
	// scaleFactor (facultatif) : échelle de redimensionnement de l'image pour la détection
	// minNeighbors (facultatif) : Nombre de voisins que chaque rectangle détecté peut conserver
	detector.recognizeFaces({
		'csv': 'path/to/database.csv'
		'image': image,
		'haarcascade': 'path/to/haarcascade_frontalface_default.xml'
	}, function (data, err) {
		// Return JSON object {faces: [{name: 'xxx', x: N, y: N, w: N, h: N}, ...]}
		console.log(JSON.stringify(data));
	});

Exemple de fichier csv pour la reconnaissance faciale (**Attention de bien respecter ce format !**) :

	Label;Name;PATH
	1;name_person1;/path/to/person1_image1.jpg
	1;name_person1;/path/to/person1_image2.jpg
	1;name_person1;/path/to/person1_image3.jpg
	2;name_person2;/path/to/person2_image1.jpg
	2;name_person2;/path/to/person2_image2.jpg
	3;name_person3;/path/to/person3_image1.jpg