a = document.querySelectorAll('.text-left');
b = document.querySelectorAll('.text-center');
c = document.querySelectorAll('.text-right');
c = document.querySelectorAll('#option-value0 tr');
d = document.querySelectorAll('#option-value0 tr td:nth-child(2)');

c.forEach((tr, i) => {
	if (i >= 1 && i <= 18) {
		sel = tr.querySelector('select');
		sel.value = 452 + i;
	}
});

d.forEach((td, i) => {
	if (i >= 1 && i <= 18) {
		inp = td.querySelector('input[type=text]');
		inp.value = 1000;
	}
});

a.forEach((item, i) => {
	if (i > 0) {
		inps = item.querySelectorAll('input[type=text]');
		inps[0].value = `№${i}`;
		inps[1].value = `№${i}`;
	}
})

vkusy = [
'Banana',
'Bubblegum',
'Candy',
'Grape',
'Grapefruit',
'Lemon',
'Melon',
'Mulberry',
'Orange',
'Peach',
'Raspberry',
'Strawberry',
'Vanila',
'Watermelon',
];

vkusy.forEach((vkus, i) => {
	inp = a[i+1].querySelector('input[type=text]');
	inp.value = vkus;
})

count = 1;
b.forEach((item, i) => {
	if (i > 0) {
		// console.log(item);
		inp = item.querySelector('input[type=text]');
		if (inp) {
			inp.value = count++ * 10;
		};
	}
})

