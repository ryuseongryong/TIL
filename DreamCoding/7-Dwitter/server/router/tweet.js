import express from 'express';
import 'express-async-errors';
import { param, body } from 'express-validator';
import * as tweetController from '../controller/tweet.js';
import { validate } from '../middleware/validator.js';

const router = express.Router();

// validation
// sanitization
// Contract Testing: Client-Server
// Proto-base validation 등
const validateTweet = [
  body('text')
    .trim()
    .isLength({ min: 3 })
    .withMessage('text should be at least 3 characters'),
  validate,
];

// GET /tweets
// GET /tweets?username=:username
router.get('/', tweetController.getTweets);

// GET /tweets/:id
router.get(
  '/:id',
  /*param('id').isInt(), -> id는 없으면 걍 찾을 수 없는 결과를 주기 때문에 불필요함*/ tweetController.getTweet
);

// POST /tweets
// 이름 유효성 검사 생략
router.post('/', validateTweet, tweetController.createTweet);

// PUT /tweets/:id
router.put('/:id', validateTweet, tweetController.updateTweet);

// DELETE /tweets/:id
router.delete('/:id', tweetController.deleteTweet);

export default router;
