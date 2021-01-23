parent = document.querySelector('#edit3_edit_table');
rows = parent.querySelector('tr');

option = function(parent, name) {
	const cells = parent.querySelectorAll('tr > td.adm-detail-content-cell-l');
	let td = null;
	cells.forEach(cell => {
		if (cell.textContent.includes(name)) {
			console.log(cell.textContent);
			td = cell;
		};
	});
	res = td.parentNode.querySelector('select');
	console.log(res);
	return res;
};

fields = [
	{  // Тип детального описания
		name: 'IC_GROUP0_ALIAS',
		value: 'IE_DETAIL_TEXT_TYPE',
	},
	{	// Картинка для анонса
		name: 'IC_GROUP1_ALIAS',
		value: 'IE_PREVIEW_PICTURE',
	}
];

fields.forEach(field => {
	const {name, value} = field;
	option(parent, name).value = value;
});
