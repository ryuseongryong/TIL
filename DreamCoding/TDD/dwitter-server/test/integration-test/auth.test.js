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

  // contorller/auth.signup에 대한 것
  describe("POST to /auth/signup", () => {
    it("returns 201 and authorization token when user details are valid", async () => {
      const fakerUser = makeValidUserDetails();

      const res = await req.post("/auth/signup", fakerUser);

      expect(res.status).toBe(201);
      expect(res.data.token.length).toBeGreaterThan(0);
    });

    it("returns 409 when username has already been taken", async () => {
      const fakerUser = makeValidUserDetails();

      const firstSignup = await req.post("/auth/signup", fakerUser);
      expect(firstSignup.status).toBe(201);
      const secondSignup = await req.post("/auth/signup", fakerUser);
      expect(secondSignup.status).toBe(409);
      expect(secondSignup.data.message).toBe(
        `${fakerUser.username} already exists`
      );
    });

    test.each([
      { missingFieldName: "name", expectedMessage: "name is missing" },
      {
        missingFieldName: "username",
        expectedMessage: "username should be at least 5 characters",
      },
      {
        missingFieldName: "email",
        expectedMessage: "invalid email",
      },
      {
        missingFieldName: "password",
        expectedMessage: "password should be at least 5 characters",
      },
    ])(
      `returns 400 when $missingFieldName field is missing`,
      async ({ missingFieldName, expectedMessage }) => {
        const fakerUser = makeValidUserDetails();
        delete fakerUser[missingFieldName];
        const res = await req.post("/auth/signup", fakerUser);

        expect(res.status).toBe(400);
        expect(res.data.message).toBe(expectedMessage);
      }
    );

    it("returns 400 when password is too short", async () => {
      const fakerUser = {
        ...makeValidUserDetails(),
        password: "123",
      };

      const res = await req.post("/auth/signup", fakerUser);

      expect(res.status).toBe(400);
      expect(res.data.message).toBe("password should be at least 5 characters");
    });
  });

  describe("POST to /auth/login", () => {
    it("returns 200 and authorization token when user credentials are valid", async () => {
      const fakerUser = await createNewUserAccount();

      const res = await req.post("/auth/login", {
        username: fakerUser.username,
        password: fakerUser.password,
      });

      expect(res.status).toBe(200);
      expect(res.data.token.length).toBeGreaterThan(0);
    });
    it("returns 401 when password is incorrect", async () => {
      const fakerUser = await createNewUserAccount();

      const res = await req.post("/auth/login", {
        username: fakerUser.username,
        password: faker.internet.password(9),
      });

      expect(res.status).toBe(401);
      expect(res.data).toMatchObject({ message: "Invalid user or password" });
    });
    it("returns 401 when username is not found", async () => {
      const fakerUser = await createNewUserAccount();

      const res = await req.post("/auth/login", {
        username: faker.internet.userName(),
        password: fakerUser.password,
      });

      expect(res.status).toBe(401);
      expect(res.data).toMatchObject({ message: "Invalid user or password" });
    });
  });

  describe("GET to /auth/me", () => {
    it("returns user details when valid token is present in Authorization header", async () => {
      const fakerUser = await createNewUserAccount();

      const res = await req.get("/auth/me", {
        headers: { Authorization: `Bearer ${fakerUser.jwt}` },
      });

      expect(res.status).toBe(200);
      expect(res.data).toMatchObject({
        username: fakerUser.username,
        token: fakerUser.jwt,
      });
    });
  });

  async function createNewUserAccount() {
    const userDetails = makeValidUserDetails();
    const prepareUserRes = await req.post("/auth/signup", userDetails);
    return {
      ...userDetails,
      jwt: prepareUserRes.data.token,
    };
  }
});

function makeValidUserDetails() {
  const fakerUser = faker.helpers.userCard();
  const { name, username, email } = fakerUser;
  const user = {
    name,
    username,
    email,
    password: faker.internet.password(10, true),
  };
  return user;
}
