const os = require('os');

console.log(os.EOL);
console.log(os.EOL === '\n'); // mac
console.log(os.EOL === '\r\n'); // win

console.log(os.totalmem()); // total memory
console.log(os.freemem()); // free memory (available)
console.log(os.type()); // operating system type
console.log(os.userInfo());
console.log(os.cpus()); // cpu information
console.log(os.homedir()); // home directory
console.log(os.hostname()); // hostname
