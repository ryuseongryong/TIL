import jwt from "jsonwebtoken";
import bcrypt from "bcrypt";
import {} from "express-async-errors";
import * as userRepository from "../data/auth.js";
import { config } from "../config.js";

export class AuthController {
  constructor(userRepository, config) {
    this.userRepository = userRepository;
    this.config = config;
  }
  createJwtToken(id) {
    return jwt.sign({ id }, config.jwt.secretKey, {
      expiresIn: config.jwt.expiresInSec,
    });
  }

  signup = async (req, res) => {
    const { username, password, name, email, url } = req.body;
    const found = await userRepository.findByUsername(username);
    if (found) {
      return res.status(409).json({ message: `${username} already exists` });
    }
    const hashed = await bcrypt.hash(password, config.bcrypt.saltRounds);
    const userId = await userRepository.createUser({
      username,
      password: hashed,
      name,
      email,
      url,
    });
    const token = this.createJwtToken(userId);
    res.status(201).json({ token, username });
  };

  login = async (req, res) => {
    const { username, password } = req.body;
    const user = await userRepository.findByUsername(username);
    if (!user) {
      return res.status(401).json({ message: "Invalid user or password" });
    }
    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      return res.status(401).json({ message: "Invalid user or password" });
    }
    const token = this.createJwtToken(user.id);
    res.status(200).json({ token, username });
  };

  me = async (req, res, next) => {
    const user = await userRepository.findById(req.userId);
    if (!user) {
      return res.status(404).json({ message: "User not found" });
    }
    res.status(200).json({ token: req.token, username: user.username });
  };
}
