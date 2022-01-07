console.log('logging...');
console.clear();

// log level web browser에서는 구분가능~
console.log('log'); // 개발용
console.info('info'); // 중요 정보용
console.warn('warn'); // 발생하면 안되지만 치명적이진 않음
console.error('error'); // 치명적인 에러, 사용자/시스템 에러

// assert : 첫 번째 인자값이 False일 때만 동작함
console.assert(2 === 3, 'not same!');
console.assert(2 === 2, 'same!');

// print object
const student = { name: 'ellie', age: 20, company: { name: 'AC' } };
console.log(student);
console.table(student);
console.dir(student, { showhidden: true, colors: false, depth: 0 });

// measuring time
console.time('for loop');
for (let i = 0; i < 10; i++) {
  i++;
}
console.timeEnd('for loop');

// counting
function a() {
  console.count('a function');
}
a();
console.countReset('a function');
a();
a();

// trace
function f1() {
  f2();
}
function f2() {
  f3();
}
function f3() {
  console.log('f3');
  console.trace();
}
f1();
