import express from 'express';
import postRouter from './router/posts.js';
import userRouter from './router/user.js';

const app = express();

app.use(express.json());

app.use('/posts', postRouter);
app.use('/users', userRouter);

app.listen(8080);
