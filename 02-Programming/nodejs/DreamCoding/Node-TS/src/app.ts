import express, { Request, Response, NextFunction } from 'express';
import morgan from 'morgan';
import helmet from 'helmet';
import tweetsRouter from './router/tweets';

const app = express();

app.use(express.json());
app.use(helmet());
app.use(morgan('tiny'));

app.use('/', (req: Request, res: Response) => {
  res.status(200).json({ message: 'hello TypeScript' });
});
app.use('/tweets', tweetsRouter);

app.use((req: Request, res: Response, next: NextFunction) => {
  res.sendStatus(404);
});
app.use((error: any, req: Request, res: Response, next: NextFunction) => {
  console.error(error);
  res.sendStatus(500);
});

app.listen(8080, () => {
  console.log('Started!');
});
