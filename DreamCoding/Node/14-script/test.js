console.log(Boolean('IMG_E0710.jpg'.includes('IMG_0710.jpg')));
const arr = [
  'IMG_E0710.jpg',
  'IMG_E0711.jpg',
  'IMG_E0712.jpg',
  'IMG_0710.jpg',
  'IMG_0711.jpg',
  'IMG_0712.jpg',
];

console.log(arr.sort());

process.argv.forEach(function (val, index, array) {
  console.log(index + ': ' + val);
});

const subFolder = process.argv.slice(2);
console.log(subFolder);
