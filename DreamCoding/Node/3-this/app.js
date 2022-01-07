function hello() {
  console.log(this);
  console.log(this === global);
  // inner function this is global
}

hello();

class A {
  constructor(num) {
    this.num = num;
  }
  memberFunction() {
    console.log('-----from now on inner class-----');
    console.log(this);
    console.log(this === global);
    // inner class this is class object
  }
}

const a = new A(1);
a.memberFunction();

console.log('---global scope---');
console.log(this);
console.log(this === module.exports);
// global scope this is module.exports

const hi = () => {
  console.log('---arrow function---');
  console.log(this);
};
// arrow function this is same as global scope

hi();
