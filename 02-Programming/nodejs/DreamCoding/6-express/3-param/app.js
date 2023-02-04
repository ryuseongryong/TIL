import express from 'express';

const app = express();

app.get('/posts', (req, res) => {
  console.log('handling for /post');
  console.log('path: ', req.path);
  console.log('params: ', req.params);
  console.log('query: ', req.query);
  if (req.query) {
    console.log('searching for: ', req.query.search, req.query.max);
  }
  res.sendStatus(200);
});

app.get('/posts/:id', (req, res) => {
  console.log('handling for /post/:id');
  console.log('path: ', req.path);
  console.log('params: ', req.params);
  console.log('query: ', req.query);
  if (req.params) {
    console.log('id is ', req.params.id);
  }
  res.sendStatus(200);
});

app.delete('/posts/:id', (req, res) => {
  res.status(200).send(`${req.params.id} will be deleted`);
});

app.get('/posts/:id/sub', (req, res) => {
  console.log('handling for /post/:id/sub');
  console.log('id is ', req.params.id);
  res.sendStatus(200);
});

// regex
//expressjs.com/en/guide/routing.html
app.get(['/sky', '/blue'], (req, res) => {
  res.send('Blue Sky!');
});

app.listen(8080);
