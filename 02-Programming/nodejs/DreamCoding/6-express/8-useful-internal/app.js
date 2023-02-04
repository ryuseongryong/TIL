import express from 'express';
import postRouter from './router/posts.js';
import userRouter from './router/user.js';

const app = express();

app.use(express.json()); // REST API -> Body parsing
app.use(express.urlencoded({ extended: false })); // HTML Form -> Body parsing

const options = {
  dotfiles: 'ignore', //숨겨진 파일 무시
  etag: false,
  index: false,
  maxAge: '1d', //캐시 유효기간
  redirect: false,
  setHeaders: function (res, path, stat) {
    // 헤더 보내기
    res.set('x-timestamp', Date.now());
  },
};
app.use(express.static('public', options));

app.use('/posts', postRouter);
app.use('/users', userRouter);

app.listen(8080);
