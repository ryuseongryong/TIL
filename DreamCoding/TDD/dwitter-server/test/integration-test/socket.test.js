import axios from "axios";
import { startServer, stopServer } from "../../app.js";
import faker from "@faker-js/faker";
import { io as SocketClient } from "socket.io-client";
import { createNewUserAccount } from "./auth_utils.js";

describe("Sockets", () => {
  let server, req, clientSocket;

  beforeAll(async () => {
    server = await startServer();
    const baseURL = `http://localhost:${server.address().port}`;
    req = axios.create({ baseURL, validateStatus: null });
  });
  afterAll(async () => {
    await stopServer(server);
  });

  beforeEach(() => {
    clientSocket = new SocketClient(
      `http://localhost:${server.address().port}`
    );
  });
  afterEach(() => {
    clientSocket.disconnect();
  });

  it("does not accept a connection without authorization token", (done) => {
    clientSocket.on("connect_error", () => {
      done();
    });

    clientSocket.on("connect", () => {
      done(new Error("Accepted a connection while expected not to"));
    });

    clientSocket.connect();
  });

  it("accepts a connection with authorization token", async () => {
    const fakerUser = await createNewUserAccount(req);
    clientSocket.auth = (callback) => callback({ token: fakerUser.jwt });

    const socketPromise = new Promise((resolve, reject) => {
      clientSocket.on("connect", () => {
        resolve("success");
      });

      clientSocket.on("connect_error", () => {
        reject(
          new Error("Server was expected to accept the connection but did not")
        );
      });
    });

    clientSocket.connect();
    await expect(socketPromise).resolves.toEqual("success");
  });

  it("emit 'tweets' event when new tweet is posted", async () => {
    const fakerUser = await createNewUserAccount(req);
    clientSocket.auth = (callback) => callback({ token: fakerUser.jwt });
    const text = faker.random.words(10);

    clientSocket.on("connect", async () => {
      await req.post(
        "/tweets",
        { text },
        {
          headers: {
            Authorization: `Bearer ${fakerUser.jwt}`,
          },
        }
      );
    });

    const socketPromise = new Promise((resolve) => {
      clientSocket.on("tweets", (tweet) => resolve(tweet));
    });

    clientSocket.connect();

    await expect(socketPromise).resolves.toMatchObject({
      name: fakerUser.name,
      username: fakerUser.username,
      text,
    });
  });
});
