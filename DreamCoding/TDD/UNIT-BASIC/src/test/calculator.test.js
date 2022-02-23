const Calculator = require('../calculator.js');

describe('Calculator', () => {
  // 각각의 Object를 통해 테스트가 독립적으로 수행될 수 있도록 만드는 것이 중요함
  let cal;
  beforeEach(() => {
    cal = new Calculator();
  });

  it(`inits with 0`, () => {
    expect(cal.value).toBe(0);
  });

  it('set', () => {
    cal.set(10);
    expect(cal.value).toBe(10);
  });

  it('clear', () => {
    cal.clear();
    expect(cal.value).toBe(0);
  });

  it('add', () => {
    cal.set(1);
    cal.add(2);

    expect(cal.value).toBe(3);
  });
  it('subtract', () => {
    cal.set(1);
    cal.subtract(2);

    expect(cal.value).toBe(-1);
  });

  it('multiply', () => {
    cal.set(10);
    cal.multiply(2);

    expect(cal.value).toBe(20);
  });

  describe('divides', () => {
    it('0 / 0 === NaN', () => {
      cal.divide(0);

      expect(cal.value).toBe(NaN);
    });

    it('1 / 0 === Infinity', () => {
      cal.set(1);
      cal.divide(0);

      expect(cal.value).toBe(Infinity);
    });

    it('100 / 4 === 25', () => {
      cal.set(100);
      cal.divide(4);

      expect(cal.value).toBe(25);
    });
  });
});
