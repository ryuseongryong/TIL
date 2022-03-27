import faker from "@faker-js/faker";

export async function createNewUserAccount(req) {
  const userDetails = makeValidUserDetails();
  const prepareUserRes = await req.post("/auth/signup", userDetails);
  return {
    ...userDetails,
    jwt: prepareUserRes.data.token,
  };
}

export function makeValidUserDetails() {
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
