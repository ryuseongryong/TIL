const http = require('http');
// const http2 = require('http2') // https만 적용
const fs = require('fs');

const server = http.createServer((req, res) => {
  console.log('incoming');
  console.log(req.headers);
  console.log(req.httpVersion);
  console.log(req.method);
  console.log(req.url);
  const url = req.url;
  res.setHeader('Content-Type', 'text/html');
  if (url === '/') {
    fs.createReadStream('./html/index.html').pipe(res);
  } else if (url === '/courses') {
    fs.createReadStream('./html/courses.html').pipe(res);
  } else {
    fs.createReadStream('./html/not-found.html').pipe(res);
  }
});

server.listen(8080);
