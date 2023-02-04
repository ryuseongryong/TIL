import express from "express";
import "express-async-errors";
import cors from "cors";
import morgan from "morgan";
import helmet from "helmet";
import tweetsRouter from "./router/tweets.js";
import authRouter from "./router/auth.js";
import { config } from "./config.js";
import { initSocket, getSocketIO } from "./connection/socket.js";
import { sequelize } from "./db/database.js";
import { TweetController } from "./controller/tweet.js";
import { AuthController } from "./controller/auth.js";
import * as tweetRepository from "./data/tweet.js";
import * as userRepository from "./data/auth.js";

const corsOption = {
  origin: config.cors.allowedOrigin,
  optionsSuccessStatus: 200,
};

export async function startServer(port) {
  const app = express();

  app.use(express.json());
  app.use(helmet());
  app.use(cors(corsOption));
  app.use(morgan("tiny"));

  app.use(
    "/tweets",
    tweetsRouter(new TweetController(tweetRepository, getSocketIO))
  );
  app.use("/auth", authRouter(new AuthController(userRepository, config)));

  app.use((req, res, next) => {
    res.sendStatus(404);
  });

  app.use((error, req, res, next) => {
    console.error(error);
    res.sendStatus(500);
  });

  await sequelize.sync();

  const server = app.listen(port);
  initSocket(server);
  console.log(`Server is started.... port: ${server.address().port}`);
  return server;
}
export async function stopServer(server) {
  return new Promise((resolve, reject) => {
    server.close(async () => {
      try {
        await sequelize.close();
        resolve();
      } catch (error) {
        reject(error);
      }
    });
  });
}
