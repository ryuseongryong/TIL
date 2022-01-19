import { Server } from 'socket.io';
import jwt from 'jsonwebtoken';
import { config } from '../config.js';

class Socket {
  constructor(server) {
    this.io = new Server(server, {
      cors: {
        origin: '*',
      },
    });

    this.io.use((socket, next) => {
      // query 전달 시 아래와 같은 방법으로 서버에서 응답에 이용하게 되는데 그렇게 하면 브라우저/콘솔/로그에서 쿼리에 접근할 수 있는 우려가 있다.
      // const token = socket.handshake.query && socket.handshake.query.token;
      const token = socket.handshake.auth.token;
      if (!token) {
        return next(new Error('Authentication error'));
      }
      jwt.verify(token, config.jwt.secretKey, (error, decoded) => {
        if (error) {
          return next(new Error('Authentication error'));
        }
        next();
      });
    });

    this.io.on('connection', (socket) => {
      console.log('Socket client connected');
    });
  }
}

let socket;
export function initSocket(server) {
  if (!socket) {
    socket = new Socket(server);
  }
}

export function getSocketIO() {
  if (!socket) {
    throw new Error('Please call init first');
  }
  return socket.io;
}

// export const sockeIO = new Server(server, {
//   cors: {
//     origin: '*',
//   },
// });
// //event based
// sockeIO.on('connection', (socket) => {
//   console.log('Client is here!');
// });
