import express from 'express';
import * as tweetControler from '../controller/tweets';

const router = express.Router();

router.get('/', tweetControler.getTweets);

export default router;
