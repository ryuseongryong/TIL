import express from 'express';

const app = express();

app.get(
  '/',
  (req, res, next) => {
    // 꼭 하나로 끝나야 함
    // next();
    // next('router');
    // next(new Error('error'))
    // res.send..
    res.send('<h1>Index page</h1>');
  },
  (req, res, next) => {
    return next();
    res.send('<h1>Index page</h1>');
  }
);

app.get('/', (req, res, next) => {
  res.send('<h1>Index page</h1>');
});

app.use((err, req, res, next) => {
  console.error('error!');
  res.sendStatus(500);
});

app.listen(8080);
