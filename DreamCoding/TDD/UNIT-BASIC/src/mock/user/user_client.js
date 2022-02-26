class UserClient {
  login(id, password) {
    return fetch('http://example.com/login/id+password') //
      .then((response) => response.json());
  }
}

module.exports = UserClient;
