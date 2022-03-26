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

  describe("Tweets APIs", () => {
    describe("GET /tweets", () => {
      it("returns all tweets when username is not specified in the query", async () => {
        const text = faker.random.words(3);
        const user1 = await createNewUserAccount();
        const user2 = await createNewUserAccount();
        const user1Headers = { Authorization: `Bearer ${user1.jwt}` };
        const user2Headers = { Authorization: `Bearer ${user2.jwt}` };

        await req.post("/tweets", { text }, { headers: user1Headers });
        await req.post("/tweets", { text }, { headers: user2Headers });

        const res = await req.get("/tweets", {
          headers: { Authorization: `Bearer ${user1.jwt}` },
        });

        expect(res.status).toBe(200);
        expect(res.data.length).toBeGreaterThanOrEqual(2);
      });

      it("retuns only tweets of the given user when username is specified in the query", async () => {
        const text = faker.random.words(3);
        const user1 = await createNewUserAccount();
        const user2 = await createNewUserAccount();
        const user1Headers = { Authorization: `Bearer ${user1.jwt}` };
        const user2Headers = { Authorization: `Bearer ${user2.jwt}` };

        await req.post("/tweets", { text }, { headers: user1Headers });
        await req.post("/tweets", { text }, { headers: user2Headers });

        const res = await req.get("/tweets", {
          headers: { Authorization: `Bearer ${user1.jwt}` },
          params: { username: user1.username },
        });

        expect(res.status).toBe(200);
        expect(res.data.length).toEqual(1);
        expect(res.data[0].username).toMatch(user1.username);
      });
    });
    describe("GET /tweets/:id", () => {
      it("returns 404 when tweet id does not exist", async () => {
        const fakerUser = await createNewUserAccount();

        const res = await req.get("/tweet/GhostId", {
          headers: { Authorization: `Bearer ${fakerUser.jwt}` },
        });

        expect(res.status).toBe(404);
      });

      it("return 200 and the tweet when tweet id exist", async () => {
        const fakerUser = await createNewUserAccount();
        const text = faker.random.words(3);
        const createdTweet = await req.post(
          "/tweets",
          { text },
          { headers: { Authorization: `Bearer ${fakerUser.jwt}` } }
        );

        const res = await req.get(`/tweets/${createdTweet.data.id}`, {
          headers: { Authorization: `Bearer ${fakerUser.jwt}` },
        });

        expect(res.status).toBe(200);
        expect(res.data.text).toMatch(text);
      });
    });
    describe("POST /tweets", () => {
      it("returns 201 and the created tweet when a tweet text is 3 characters or more", async () => {
        const text = faker.random.words(3);
        const fakerUser = await createNewUserAccount();

        const res = await req.post(
          "/tweets",
          { text },
          { headers: { Authorization: `Bearer ${fakerUser.jwt}` } }
        );

        expect(res.status).toBe(201);
        expect(res.data).toMatchObject({
          name: fakerUser.name,
          username: fakerUser.username,
          text,
        });
      });

      it("returns 400 when a tweet text is less than 3 characters", async () => {
        const text = faker.random.alpha({ count: 2 });
        const fakerUser = await createNewUserAccount();

        const res = await req.post(
          "/tweets",
          { text },
          { headers: { Authorization: `Bearer ${fakerUser.jwt}` } }
        );

        expect(res.status).toBe(400);
        expect(res.data.message).toMatch(
          "text should be at least 3 characters"
        );
      });
    });
    describe("PUT /tweets/:id", () => {
      it("returns 404 when tweet id does not exist", async () => {
        const text = faker.random.words(3);
        const fakerUser = await createNewUserAccount();

        const res = await req.put(
          "/tweets/GhostId",
          { text },
          { headers: { Authorization: `Bearer ${fakerUser.jwt}` } }
        );

        expect(res.status).toBe(404);
        expect(res.data.message).toMatch("Tweet not found: GhostId");
      });
      it("returns 200 and updated tweet when tweet id exists and the tweet belongs to tweet id", async () => {
        const text = faker.random.words(3);
        const updatedText = faker.random.words(3);
        const fakerUser = await createNewUserAccount();

        const createdTweet = await req.post(
          "/tweets",
          { text },
          { headers: { Authorization: `Bearer ${fakerUser.jwt}` } }
        );
        const res = await req.put(
          `/tweets/${createdTweet.data.id}`,
          { text: updatedText },
          { headers: { Authorization: `Bearer ${fakerUser.jwt}` } }
        );

        expect(res.status).toBe(200);
        expect(res.data.text).toMatch(updatedText);
      });
      it("returns 403 when tweet id exists but the tweet does not belong to the user", async () => {
        const text = faker.random.words(3);
        const updatedText = faker.random.words(3);
        const tweetAuthor = await createNewUserAccount();
        const anotherUser = await createNewUserAccount();

        const createdTweet = await req.post(
          "/tweets",
          { text },
          { headers: { Authorization: `Bearer ${tweetAuthor.jwt}` } }
        );

        const res = await req.put(
          `/tweets/${createdTweet.data.id}`,
          { text: updatedText },
          { headers: { Authorization: `Bearer ${anotherUser.jwt}` } }
        );

        expect(res.status).toBe(403);
      });
    });
    describe("DELETE /tweets/:id", () => {});
  });
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
