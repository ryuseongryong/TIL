import faker from "@faker-js/faker";
import { AuthController } from "../auth.js";
import httpMocks from "node-mocks-http";
import { config } from "../../config.js";

describe("Auth Controller", () => {
  let authController, userRepository, userId, req, res;

  beforeEach(() => {
    userRepository = {};
    authController = new AuthController(userRepository, config);
    userId = faker.random.alphaNumeric(16);
  });

  it("returns 404 if user does not exist", async () => {
    req = httpMocks.createRequest({
      params: { id: userId },
    });
    res = httpMocks.createResponse();
    userRepository.findById = jest.fn(() => null);

    await authController.me(req, res);

    expect(res.statusCode).toBe(404);
    expect(res._getJSONData()).toMatchObject({
      message: `User not found`,
    });
    expect(userRepository.findById).toHaveBeenCalledTimes(0);
  });
});
