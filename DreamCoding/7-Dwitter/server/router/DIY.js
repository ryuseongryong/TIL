import express from 'express';
import 'express-async-errors';
import controller from '../controller/DIY.js';

const router = express.Router();

// GET /tweets
// GET /tweets?username=:username
router.get('/', controller.getAll);
// GET /tweets/:id
router.get('/:id', controller.getById);
// POST /tweets
router.post('/', controller.postTweet);
// PUT /tweets/:id
router.put('/:id', controller.updateTweet);
// DELETE /tweets/:id
router.delete('/:id', controller.deleteTweet);

export default router;
