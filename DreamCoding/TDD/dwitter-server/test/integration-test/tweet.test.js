import axios from "axios";
import faker from "@faker-js/faker";
import { startServer, stopServer } from "../../app.js";
import { sequelize } from "../../db/database";
import { createNewUserAccount } from "./auth_utils.js";

describe("Tweets APIs", () => {
  let server, req;
  beforeAll(async () => {
    server = await startServer();
    req = axios.create({
      baseURL: `http://localhost:${server.address().port}`,
      validateStatus: null,
    });
  });

  afterAll(async () => {
    await stopServer(server);
  });
  describe("GET /tweets", () => {
    it("returns all tweets when username is not specified in the query", async () => {
      const text = faker.random.words(3);
      const user1 = await createNewUserAccount(req);
      const user2 = await createNewUserAccount(req);
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
      const user1 = await createNewUserAccount(req);
      const user2 = await createNewUserAccount(req);
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
      const fakerUser = await createNewUserAccount(req);

      const res = await req.get("/tweet/GhostId", {
        headers: { Authorization: `Bearer ${fakerUser.jwt}` },
      });

      expect(res.status).toBe(404);
    });

    it("return 200 and the tweet when tweet id exist", async () => {
      const fakerUser = await createNewUserAccount(req);
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
      const fakerUser = await createNewUserAccount(req);

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
      const fakerUser = await createNewUserAccount(req);

      const res = await req.post(
        "/tweets",
        { text },
        { headers: { Authorization: `Bearer ${fakerUser.jwt}` } }
      );

      expect(res.status).toBe(400);
      expect(res.data.message).toMatch("text should be at least 3 characters");
    });
  });
  describe("PUT /tweets/:id", () => {
    it("returns 404 when tweet id does not exist", async () => {
      const text = faker.random.words(3);
      const fakerUser = await createNewUserAccount(req);

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
      const fakerUser = await createNewUserAccount(req);

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
      const tweetAuthor = await createNewUserAccount(req);
      const anotherUser = await createNewUserAccount(req);

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
  describe("DELETE /tweets/:id", () => {
    it("returns 404 when tweet id does not exist", async () => {
      const fakerUser = await createNewUserAccount(req);

      const res = await req.delete("/tweets/GhostId", {
        headers: { Authorization: `Bearer ${fakerUser.jwt}` },
      });

      expect(res.status).toBe(404);
      expect(res.data.message).toMatch("Tweet not found: GhostId");
    });
    it("returns 403 and the tweet should still be there when tweet id exists but the tweet does not belong to user", async () => {
      const text = faker.random.words(3);
      const tweetAuthor = await createNewUserAccount(req);
      const anotherUser = await createNewUserAccount(req);

      const createdTweet = await req.post(
        "/tweets",
        { text },
        { headers: { Authorization: `Bearer ${tweetAuthor.jwt}` } }
      );

      const deleteResult = await req.delete(`/tweets/${createdTweet.data.id}`, {
        headers: { Authorization: `Bearer ${anotherUser.jwt}` },
      });

      const checkTweetResult = await req.get(
        `/tweets/${createdTweet.data.id}`,
        { headers: { Authorization: `Bearer ${anotherUser.jwt}` } }
      );
      expect(deleteResult.status).toBe(403);
      expect(checkTweetResult.status).toBe(200);
      expect(checkTweetResult.data).toMatchObject({ text });
    });

    it("returns 204 and the tweet should be deleted when tweet id exists and the tweet belong to user", async () => {
      const text = faker.random.words(3);
      const tweetAuthor = await createNewUserAccount(req);

      const createdTweet = await req.post(
        "/tweets",
        { text },
        { headers: { Authorization: `Bearer ${tweetAuthor.jwt}` } }
      );

      const deleteResult = await req.delete(`/tweets/${createdTweet.data.id}`, {
        headers: { Authorization: `Bearer ${tweetAuthor.jwt}` },
      });

      const checkTweetResult = await req.get(
        `/tweets/${createdTweet.data.id}`,
        { headers: { Authorization: `Bearer ${tweetAuthor.jwt}` } }
      );

      expect(deleteResult.status).toBe(204);
      expect(checkTweetResult.status).toBe(404);
    });
  });
});
