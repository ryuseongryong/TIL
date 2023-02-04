const fs = require('fs');

const data = [];
const beforeMem = process.memoryUsage().rss;
const readStream = fs
  .createReadStream('./file.txt', {
    highWaterMark: 8, // default value: 64kbytes how much data reading at once
    encoding: 'utf-8',
  })
  .once('data', (chunk) => {
    // console.log(chunk);
    data.push(chunk);
    console.count('data');
    readStream.close();
  })
  .on('close', () => {
    console.log('close');
    console.log(data.join(''));
    // calculate
    const afterMem = process.memoryUsage().rss;
    const diff = afterMem - beforeMem;
    const consumed = diff / 1024 / 1024;
    console.log(diff);
    console.log(`Consumed Memory: ${consumed}MB`);
  })
  .on('end', () => {
    console.log('end');
    console.log(data.join(''));
  })
  .on('error', (error) => {
    console.log(error);
  });

// readStream.once('data', (chunk) => {
//   // console.log(chunk);
//   data.push(chunk);
//   console.count('data');
//   readStream.close();
// });

// readStream.on('error', (error) => {
//   console.log(error);
// });
