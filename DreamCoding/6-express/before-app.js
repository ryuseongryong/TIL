import express from 'express';
const app = express();

// post 처리용 json화
app.use(express.json());
app.post('/', (req, res, next) => {
  console.log(req.body);
});

// all methods에 상관없이 수행된다. 해당 주소값 외에는 처리되지 않는다.
app.all('/api', (req, res, next) => {
  console.log('all');
  next();
});
// 모든 메소드와 sky이하 주소값 모두 처리된다.
app.use('/sky', (req, res, next) => {
  console.log('use');
  next();
});

// res 다음에 next를 호출해서 흐름이 이어지게 해야한다.
app.get(
  '/',
  (req, res, next) => {
    console.log('first');
    if (1) {
      return res.send('Hello');
    }
    res.send('Seongryong');
  },
  (req, res, next) => {
    console.log('first2');
  }
);
app.get('/', (req, res, next) => {
  console.log('second');
});

app.use((req, res, next) => {
  res.status(404).send('Not available! @.@');
});
app.use((error, req, res, next) => {
  console.error(error);
  res.status(500).send('Sorry, try later!');
});
app.listen(8080);
