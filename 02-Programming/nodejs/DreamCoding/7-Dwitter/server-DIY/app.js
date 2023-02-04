import express from 'express';

const app = express();

app.use(express.json());

const tweets = [];

app
  .route('/tweets')
  .get((req, res, next) => {
    if (req.query.username) {
      const tweetByUsername = tweets.filter((tweet) => {
        return tweet.username === req.query.username;
      });
      console.log(tweetByUsername);
      return res.status(200).json(tweetByUsername);
    }
    res.status(200).json(tweets);
  })
  .post((req, res) => {
    const { text, name, username, url } = req.body;
    tweets.push(req.body);
    res.status(201).json(tweets[tweets.length - 1]);
  });

app
  .route('/tweets/:id')
  .get((req, res) => {
    const tweetById = tweets.filter((tweet) => {
      return tweet.id === req.params.id;
    });
    res.status(200).json(tweetById);
  })
  .put((req, res) => {
    let index;
    const tweetById = tweets.filter((tweet, idx) => {
      index = idx;
      return tweet.id === req.params.id;
    });
    tweets.splice(index, 1, req.body);
    res.status(200).json(tweets[index]);
  })
  .delete((req, res) => {
    console.log(req.params);
    let index;
    const tweetById = tweets.filter((tweet, idx) => {
      index = idx;
      return tweet.id === req.params.id;
    });
    tweets.splice(index, 1);
    res.status(204).send();
  });

app.listen(8080);
