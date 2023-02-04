import express from 'express';
import fs from 'fs';
import fsAsync from 'fs/promises';

const app = express();

app.use(express.json());

app.get('/file1', (req, res) => {
  // try {
  //   const data = fs.readFileSync('/file.txt');
  // } catch (error) {
  //   res.status(404).send('File not found');
  // }

  // async function은 last safe area에 도달하지 못함 = async는 try catch로 처리할 수 없다.
  fs.readFile('/file1.txt', (err, data) => {
    if (err) {
      res.status(404).send('File not found');
    }
  });
});

// promise는 then catch로 찾아내기
// promise === async === try catch X / then catch
app.get('/file2', (req, res) => {
  // fsAsync.readFile('/file.txt').catch(next);
  fsAsync //
    .readFile('/file.txt')
    .catch((error) => {
      res.status(404).send('File not found');
    });
});

// code 자체가 동기적이기 때문에 try catch로 에러처리 가능
app.get('/file3', async (req, res) => {
  // code 자체는 동기적, 사용은 비동기적 === middleware가 promise형태로 반환
  try {
    const data = await fsAsync.readFile('/file.txt');
  } catch (error) {
    res.status(404).send('File not found');
  }
});

app.use((error, req, res, next) => {
  console.error(error);
  res.status(500).json({ message: 'Somethig went wrong' });
});

app.listen(8080);
