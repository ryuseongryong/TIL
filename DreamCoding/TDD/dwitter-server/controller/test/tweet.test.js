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
});
