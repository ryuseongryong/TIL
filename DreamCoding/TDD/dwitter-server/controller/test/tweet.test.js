import faker from "@faker-js/faker";
import { TweetController } from "../tweet.js";
import httpMocks from "node-mocks-http";

describe("Tweet Controller", () => {
  let tweetController, tweetRepository, mockedSocket;

  beforeEach(() => {
    tweetRepository = {};
    mockedSocket = { emit: jest.fn() };
    tweetController = new TweetController(tweetRepository, () => mockedSocket);
  });

  describe("getTweets", () => {
    it("returns all tweets when username is not provided", async () => {
      const req = httpMocks.createRequest();
      const res = httpMocks.createResponse();
      const allTweets = [
        { text: faker.random.words(3) },
        { text: faker.random.words(3) },
      ];
      tweetRepository.getAll = () => allTweets;

      await tweetController.getTweets(req, res);

      expect(res.statusCode).toBe(200);
      expect(res._getJSONData()).toEqual(allTweets);
    });

    it("returns tweets for the given user when username is provide", async () => {
      const username = faker.internet.userName();
      const req = httpMocks.createRequest({
        query: { username },
      });
      const res = httpMocks.createResponse();
      const userTweet = [{ text: faker.random.words(3) }];
      tweetRepository.getAllByUsername = () => userTweet;
      tweetRepository.getAllByUsername = jest.fn(() => userTweet);

      await tweetController.getTweets(req, res);

      expect(res.statusCode).toBe(200);
      expect(res._getJSONData()).toEqual(userTweet);
      expect(tweetRepository.getAllByUsername).toHaveBeenCalledTimes(1);
      expect(tweetRepository.getAllByUsername).toHaveBeenCalledWith(username);
    });
  });

  describe("getTweet", () => {
    let tweetId, req, res;

    beforeEach(() => {
      tweetId = faker.random.alphaNumeric(16);
      req = httpMocks.createRequest({
        params: { id: tweetId },
      });
      res = httpMocks.createResponse();
    });

    it("returns the tweet if tweet exists", async () => {
      const aTweet = { text: faker.random.words(3) };
      tweetRepository.getById = jest.fn(() => aTweet);

      await tweetController.getTweet(req, res);

      expect(res.statusCode).toBe(200);
      expect(res._getJSONData()).toEqual(aTweet);
      expect(tweetRepository.getById).toHaveBeenCalledWith(tweetId);
    });

    it("returns 404 if tweet does not exist", async () => {
      tweetRepository.getById = jest.fn(() => undefined);

      await tweetController.getTweet(req, res);

      expect(res.statusCode).toBe(404);
      expect(res._getJSONData()).toMatchObject({
        message: `Tweet id(${tweetId}) not found`,
      });
      expect(tweetRepository.getById).toHaveBeenCalledWith(tweetId);
    });
  });

  describe("createTweet", () => {
    let newTweet, authorId, req, res;
    beforeEach(() => {
      newTweet = faker.random.words(3);
      authorId = faker.random.alphaNumeric(16);
      req = httpMocks.createRequest({
        body: { text: newTweet },
        userId: authorId,
      });
      res = httpMocks.createResponse();
    });

    it("returns 201 with created tweet object including userId", async () => {
      tweetRepository.create = jest.fn((text, userId) => ({
        text,
        userId,
      }));

      await tweetController.createTweet(req, res);

      expect(res.statusCode).toBe(201);
      expect(res._getJSONData()).toMatchObject({
        text: newTweet,
        userId: authorId,
      });
      expect(tweetRepository.create).toHaveBeenCalledWith(newTweet, authorId);
    });

    it("should send an event to a websocket channel", async () => {
      tweetRepository.create = jest.fn((text, userId) => {
        return { text, userId };
      });

      await tweetController.createTweet(req, res);

      expect(mockedSocket.emit).toHaveBeenCalledWith("tweets", {
        text: newTweet,
        userId: authorId,
      });
    });
  });

  describe("updateTweet", () => {
    let tweetId, updatedText, req, res, authorId;
    beforeEach(() => {
      tweetId = faker.random.alphaNumeric(16);
      updatedText = faker.random.words(3);
      authorId = faker.random.alphaNumeric(16);
      req = httpMocks.createRequest({
        params: { id: tweetId },
        body: { text: updatedText },
        userId: authorId,
      });
      res = httpMocks.createResponse();
    });

    it("updates the repository and return 200", async () => {
      tweetRepository.getById = () => {
        return {
          text: faker.random.words(3),
          userId: authorId,
        };
      };
      tweetRepository.update = (tweetId, newTweet) => {
        return { text: newTweet };
      };

      await tweetController.updateTweet(req, res);

      expect(res.statusCode).toBe(200);
      expect(res._getJSONData()).toMatchObject({
        text: updatedText,
      });
    });

    it("returns 403 and should not update the repository if the tweet does not belong", async () => {
      tweetRepository.getById = () => {
        return {
          text: faker.random.words(3),
          userId: faker.random.alphaNumeric(16),
        };
      };
      tweetRepository.update = jest.fn();

      await tweetController.updateTweet(req, res);

      expect(res.statusCode).toBe(403);
    });

    it("returns 404 and should not update the repository if the tweet does not exist", async () => {
      tweetRepository.getById = () => undefined;
      tweetRepository.update = jest.fn();

      await tweetController.updateTweet(req, res);

      expect(res.statusCode).toBe(404);
      expect(res._getJSONData()).toMatchObject({
        message: `Tweet not found: ${tweetId}`,
      });
    });
  });

  describe("deleteTweet", () => {
    let tweetId, req, res, authorId;

    beforeEach(() => {
      tweetId = faker.random.alphaNumeric(16);
      authorId = faker.random.alphaNumeric(16);
      req = httpMocks.createRequest({
        params: { id: tweetId },
        userId: authorId,
      });
      res = httpMocks.createResponse();
    });

    it("returns 204 and remove the tweet from the repository if the tweet exists", async () => {
      tweetRepository.getById = () => {
        return {
          userId: authorId,
        };
      };
      tweetRepository.remove = jest.fn();

      await tweetController.deleteTweet(req, res);

      expect(res.statusCode).toBe(204);
      expect(tweetRepository.remove).toHaveBeenCalledWith(tweetId);
    });

    it("returns 403 and should not update the repository if the tweet does not belong to the user", async () => {
      tweetRepository.getById = () => {
        return {
          userId: faker.random.alphaNumeric(16),
        };
      };

      tweetRepository.remove = jest.fn();

      await tweetController.deleteTweet(req, res);

      expect(res.statusCode).toBe(403);
      expect(tweetRepository.remove).not.toHaveBeenCalled();
    });

    it("returns 404 and should not update the repository if the tweet does not exist", async () => {
      tweetRepository.getById = () => undefined;
      tweetRepository.remove = jest.fn();

      await tweetController.deleteTweet(req, res);

      expect(res.statusCode).toBe(404);
      expect(res._getJSONData()).toMatchObject({
        message: `Tweet not found: ${tweetId}`,
      });
      expect(tweetRepository.remove).not.toHaveBeenCalled();
    });
  });
});
