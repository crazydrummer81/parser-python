links = document.querySelectorAll('a');

res = [];
resStr = '';

links.forEach(link => {
	// console.log(link.innerText.toLowerCase().indexOf('скачать'));
	if (link.innerText.toLowerCase().indexOf('скачать') >= 0) {
		res.push(link.getAttribute('href'));
		resStr += link.getAttribute('href') + '\n';
	}
});

// console.log(res);
console.log(resStr)