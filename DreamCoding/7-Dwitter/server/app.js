import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import helmet from 'helmet';
import 'express-async-errors';
import cookieParser from 'cookie-parser';
import yaml from 'yamljs';
import swaggerUI from 'swagger-ui-express';
import * as OpenAPIValidator from 'express-openapi-validator';
import tweetsRouter from './router/tweet.js';
import authRouter from './router/auth.js';
import { config } from './config.js';
import { initSocket } from './connection/socket.js';
import { sequelize } from './db/database.js';
import { csrfCheck } from './middleware/csrf.js';
import rateLimit from './middleware/rate-limiter.js';
import { authHandler } from './middleware/auth.js';
import * as apis from './controller/index.js';

const app = express();
const corsOption = {
  origin: config.cors.allowedOrigin,
  optionsSuccessStatus: 200,
  credentials: true, // allow the Access-Control-Credentials
};
const openAPIDocument = yaml.load('./api/openapi.yaml');

app.use(express.json());
app.use(cookieParser());
app.use(helmet());
app.use(cors(corsOption));
app.use(morgan('tiny'));
app.use(rateLimit);

// app.use(csrfCheck);
app.use('/api-docs', swaggerUI.serve, swaggerUI.setup(openAPIDocument));
app.use('/tweets', tweetsRouter);
app.use('/auth', authRouter);

app.use(
  // routing + validation(set standard in yaml file)
  OpenAPIValidator.middleware({
    apiSpec: './api/openapi.yaml',
    validateResponses: true,
    operationHandlers: {
      resolver: modulePathResolver,
    },
    validateSecurity: {
      handlers: {
        jwt_auth: authHandler,
      },
    },
  })
);

function modulePathResolver(_, route, apiDoc) {
  const pathKey = route.openApiRoute.substring(route.basePath.length);
  const operation = apiDoc.paths[pathKey][route.method.toLowerCase()];
  const methodName = operation.operationId;
  return apis[methodName];
}

app.use((req, res, next) => {
  res.sendStatus(404);
});

app.use((error, req, res, next) => {
  console.error(error);
  res.status(error.status || 500).json({
    message: error.message,
  });
});

sequelize
  .sync()
  //.then((client) => console.log(client));
  .then(() => {
    const server = app.listen(config.port);
    initSocket(server);
    console.log(
      `Server is started...\n\rPORT: ${config.port}\n\rdate: ${new Date()}`
    );
  });
