const jwt = require('jsonwebtoken');

// 필수적인 데이터만 넣는 것이 좋다
const secret = 'fSTwh2471^%Vw9dmUyYR$BXL*VJhq&N&';
const token = jwt.sign(
  {
    id: 'userId',
    isAdmin: true,
  },
  // https://www.lastpass.com/
  secret,
  {
    expiresIn: 2,
  }
);

console.log(token);

jwt.verify(token, secret, (error, decoded) => {
  console.log(error, decoded);
});

setTimeout(() => {
  jwt.verify(token, secret, (error, decoded) => {
    console.log(error, decoded);
  });
}, 3000); // error : jwt expired, decoded = undefined
