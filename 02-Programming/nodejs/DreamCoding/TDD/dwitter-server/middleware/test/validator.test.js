import httpMocks from "node-mocks-http";
import * as validator from "express-validator";
import faker from "@faker-js/faker";
import { validate } from "../validator.js";

jest.mock("express-validator");

describe("Validator Middleware", () => {
  it("calls next if there are no validation errors", async () => {
    const request = httpMocks.createRequest();
    const response = httpMocks.createResponse();
    const next = jest.fn();

    validator.validationResult = jest.fn(() => ({ isEmpty: () => true }));

    await validate(request, response, next);

    expect(next).toBeCalled();
  });

  it("returns 400 if there are validation errors", async () => {
    const request = httpMocks.createRequest();
    const response = httpMocks.createResponse();
    const next = jest.fn();
    const errorMsg = faker.random.words(3);

    validator.validationResult = jest.fn(() => ({
      isEmpty: () => false,
      array: () => [{ msg: errorMsg }],
    }));

    await validate(request, response, next);

    expect(next).not.toBeCalled();
    expect(response.statusCode).toBe(400);
    expect(response._getJSONData().message).toBe(errorMsg);
  });
});
