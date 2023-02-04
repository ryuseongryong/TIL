const bcrypt = require('bcrypt');

const password = 'abcd1234';
// salt = 10~12 추천
const hashed = bcrypt.hashSync(password, 10);
console.log(`password: ${password}, hashed: ${hashed}`);

const result = bcrypt.compareSync('abcd123', hashed);
console.log(result);
