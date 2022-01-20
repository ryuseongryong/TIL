//     username: 'bob',
//     url: 'https://m.media-amazon.com/images/M/MV5BNzg0MWEyZjItOTZlMi00YmRjLWEyYzctODIwMDU0OThiMzNkXkEyXkFqcGdeQXVyNjUxMjc1OTM@._V1_UY317_CR13,0,214,317_AL_.jpg',
//     username: 'seongryong',
//     url: 'https://avatars.githubusercontent.com/u/58920833?s=400&u=ac2997091b3a84b129630b576fddccaaadabecc4&v=4',

import { db } from '../db/database.js';

export async function findByUsername(username) {
  return db
    .execute('SELECT * FROM users WHERE username=?', [username])
    .then((result) => result[0][0]);
}

export async function findById(id) {
  return db
    .execute('SELECT * FROM users WHERE id=?', [id])
    .then((result) => result[0][0]);
}

export async function createUser(user) {
  const { username, password, name, email, url } = user;
  return db
    .execute(
      'INSERT INTO users (username, password, name, email, url) VALUES (?, ?, ?, ?, ?)',
      [username, password, name, email, url]
    )
    .then((result) => {
      console.log(result[0].insertId);
      return result;
    });
}
