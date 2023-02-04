import express from 'express';

const app = express();

app.use(express.json());

app.post('/posts', (req, res) => {
  console.log(req.body);
  res.status(201).send('Thanks, Created');
});

app.put('/posts/:id', (req, res) => {
  console.log(req.body);
  res.status(200).send('Thanks, Updated!');
});

app.listen(8080);
