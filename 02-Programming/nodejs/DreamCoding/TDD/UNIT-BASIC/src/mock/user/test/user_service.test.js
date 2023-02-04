const UserService = require('../user_service.js');
const UserClient = require('../user_client.js');
jest.mock('../user_client.js');

describe('UserService', () => {
  const login = jest.fn(async () => 'success');
  UserClient.mockImplementation(() => {
    return {
      login,
    };
  });
  let userService;

  beforeEach(() => {
    userService = new UserService(new UserClient());
    // login.mockClear();
    // UserClient.mockClear();
  });

  it('login once', async () => {
    await userService.login('username', 'password');
    // expect(login.mock.calls.length).toBe(1);
    expect(login).toBeCalledTimes(1);
  });

  it('login twice', async () => {
    await userService.login('username', 'password');
    await userService.login('username', 'password');
    expect(login).toBeCalledTimes(1);
  });
});
