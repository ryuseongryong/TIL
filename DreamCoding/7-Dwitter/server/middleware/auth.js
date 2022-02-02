import jwt from 'jsonwebtoken';
import { config } from '../config.js';
import * as userRepository from '../data/auth.js';

const AUTH_ERROR = { message: 'Authentication Error' };

// 모든 요청에 대해 Header에 Authorization이 있는지 확인해서 우리가 가진 코드와 일치하는 지, 실제로 사용자가 있는지 두가지 검증을 처리하는 것
export const isAuth = async (req, res, next) => {
  // 1. Cookie (for Browser)
  // 2. Header (for Non-Browser Client)

  let token;
  // check the header first

  const authHeader = req.get('Authorization');
  // authHeader가 있고 Bearer로 시작된다면
  if (authHeader && authHeader.startsWith('Bearer ')) {
    token = authHeader.split(' ')[1];
  }
  // if no token in the header, check the cookie
  if (!token) {
    token = req.cookies['token'];
  }
  //To Do : 더 보안성있게

  // no token anywhere
  if (!token) {
    return res.status(401).json(AUTH_ERROR);
  }

  jwt.verify(token, config.jwt.secretKey, async (error, decoded) => {
    if (error) {
      return res.status(401).json(AUTH_ERROR);
    }
    const user = await userRepository.findById(decoded.id);
    if (!user) {
      return res.status(401).json(AUTH_ERROR);
    }
    req.userId = user.id; // req.customData를 등록하고 다음 순위로 넘길 수 있음
    req.token = token;
    next();
  });
};

export const authHandler = async (req) => {
  const authHeader = req.get('Authorization');
  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, config.jwt.secretKey);
    const user = await userRepository.findById(decoded.id);
    if (!user) {
      throw { status: 401, ...AUTH_ERROR };
    }
    req.userId = user.id;
    req.token = decoded;
    return true;
  } catch (err) {
    console.log(err);
    throw { status: 401, ...AUTH_ERROR };
  }
};
