const Stack = require('../stack.js');

describe('Stack', () => {
  let stack;

  beforeEach(() => {
    stack = new Stack();
  });

  it('new stack is empty', () => {
    expect(stack.size()).toBe(0);
  });

  it('push function can input to array new element', () => {
    stack.push('new element');

    expect(stack.size()).toBe(1);
    expect(stack.array).toEqual(['new element']);
    // expect(stack.array).toContainEqual('new element');
  });

  describe('pop', () => {
    it('throw error, when pop empty array', () => {
      expect(() => {
        stack.pop();
      }).toThrow('empty array');
    });
  });
});
