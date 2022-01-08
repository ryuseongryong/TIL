const process = require('process');

console.log(process.execPath); // node path
console.log(process.version); // node version
console.log(process.pid); // process id
console.log(process.ppid); // parent process id
console.log(process.platform); // platform information
console.log(process.env); // environment variable information
console.log(process.uptime()); // uptime count
console.log(process.cwd()); // current working directory
console.log(process.cpuUsage()); // cpu usage

setTimeout(() => {
  console.log('setTimeout');
}, 0);

// Task Queue 젤 앞에 입력해줌
process.nextTick(() => {
  console.log('nextTick');
});

for (let i = 0; i < 1000; i++) {
  console.log('for loop', i);
}
