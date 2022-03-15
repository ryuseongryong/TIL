import axios from "axios";
import faker from "@faker-js/faker";
import { startServer, stopServer } from "../../app.js";
import { sequelize } from "../../db/database";
// 테스트 전 서 시작 및 데이터베이스 초기화 설정
// 테스트 후  데이터베이스 초기화 하기

describe("Auth APIs", () => {
  let server, req;
  beforeAll(async () => {
    server = await startServer();
    req = axios.create({
      baseURL: "http://localhost:8080/",
      validateStatus: null,
    });
  });

  afterAll(async () => {
    await sequelize.drop();
    await stopServer(server);
  });

  describe("POST to /auth/signup", () => {
    it("returns 201 and authorization token when user details are valid", async () => {
      const fakerUser = faker.helpers.userCard();
      const { name, username, email } = fakerUser;
      const user = {
        name,
        username,
        email,
        password: faker.internet.password(10, true),
      };

      const res = await req.post("/auth/signup", user);

      expect(res.status).toBe(201);
      expect(res.data.token.length).toBeGreaterThan(0);
    });
  });
});
