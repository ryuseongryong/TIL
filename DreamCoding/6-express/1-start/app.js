import express from 'express';

const app = express();

app.get('/', (req, res, next) => {
  res.send('<h1>Index page</h1>');
});

app.get('/hello', (req, res, next) => {
  res.setHeader('Content-Type', 'application/json');
  res.status(200).json({ name: 'Ellie', age: 0 });
});

app.use((req, res, next) => {
  res.setHeader('node-course', 'special middleware');
  next();
});

app.use((req, res) => {
  res.send('<h1>Not Found!</h1>');
});

app.listen(8080);
