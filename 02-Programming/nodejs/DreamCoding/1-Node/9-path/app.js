const path = require('path');

console.log(__dirname);
console.log(__filename);

// POSIX(Unix: Mac, Linux): 'Users/temp/myfile.js'
// Windows: 'C:\\temp\myfile.js'

console.log(path.sep); // path separator
console.log(path.delimiter); // environment variable delimiter

// basename
console.log(path.basename(__filename));
console.log(path.basename(__filename, '.js'));

// dirname
console.log(path.dirname(__filename));

// extension
console.log(path.extname(__filename)); // 확장자 명

// parse
const parsed = path.parse(__filename);
console.log(parsed);
parsed.root;
parsed.name;

const str = path.format(parsed);
console.log(str);

// isAbsolute
console.log('isAbsolute?', path.isAbsolute(__dirname)); // absolute path
console.log('isAbsolute?', path.isAbsolute('../')); // relative path

// normalize : abnormal path correction
console.log(path.normalize('./folder//////sub'));

// join
console.log(__dirname + path.sep + 'image');
console.log(path.join(__dirname, 'image'));
