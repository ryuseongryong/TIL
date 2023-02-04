import rateLimit from 'express-rate-limit';
import { config } from '../config.js';

export default rateLimit({
  windowMs: config.rateLimit.windowMs,
  max: config.rateLimit.maxRequest,
  // 특정 IP 또는 project 명을 기재하면 글로벌하게 카운트할 수 있다.
  keyGenerator: (req, res) => 'dwitter',
});
