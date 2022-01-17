let users = [
  {
    id: '1',
    username: 'bob',
    password: '$2b$12$G9xf8SFq3oTEgdj7ozHQ/uhD0yeQcUEDU8tn0cvpvApuadr3nE5Vm',
    // password: 'abcd1234',
    name: 'Bob',
    email: 'bob@gmail.com',
    url: 'https://m.media-amazon.com/images/M/MV5BNzg0MWEyZjItOTZlMi00YmRjLWEyYzctODIwMDU0OThiMzNkXkEyXkFqcGdeQXVyNjUxMjc1OTM@._V1_UY317_CR13,0,214,317_AL_.jpg',
  },
  {
    id: '2',
    username: 'seongryong',
    password: '$2b$12$B2i8k/1mnnNGpP3g4PIHkuoZq78vrF6n45pZNAxQuwrqDhJqFGrnG',
    // password: '12345',
    name: 'Seongryong',
    email: 'ryuseongryong@gmail.com',
    url: 'https://avatars.githubusercontent.com/u/58920833?s=400&u=ac2997091b3a84b129630b576fddccaaadabecc4&v=4',
  },
];

export async function findByUsername(username) {
  return users.find((user) => user.username === username);
}

export async function findById(id) {
  return users.find((user) => user.id === id);
}

export async function createUser(user) {
  const created = { ...user, id: Date.now().toString() };
  users.push(created);
  return created.id;
}
