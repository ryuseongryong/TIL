import exrpess from 'express';

const router = exrpess.Router();

router.get('/', (req, res) => {
  res.status(200).send('GET: /users');
});

export default router;
