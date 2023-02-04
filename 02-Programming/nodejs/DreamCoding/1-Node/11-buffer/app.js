// Fixed-size chuck of memory
// array of integers, byte of data

const buf = Buffer.from('Hi'); // Unicode
console.log(buf);
console.log(buf.length);
console.log(buf[0]); // AscII
console.log(buf[1]);
console.log(buf.toString());

// create
const buf2 = Buffer.alloc(2); // find available memory -> initialization
const buf3 = Buffer.allocUnsafe(2); // find available memory -> not initialization, fast, but may be side effects
buf2[0] = 72;
buf2[1] = 105;
buf2.copy(buf3);
console.log(buf2.toString());
console.log(buf3.toString());

// concat
const newBuf = Buffer.concat([buf, buf2, buf3]);
console.log(newBuf.toString());
