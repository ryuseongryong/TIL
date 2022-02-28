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

    it('return last element and remove', () => {
      stack.push('first');
      stack.push('second');

      const removeElement = stack.pop();
      expect(removeElement).toBe('second');
      expect(stack.size()).toBe(1);
      expect(stack.array).toEqual(['first']);
    });
  });

  describe('peek', () => {
    it('throw error, when pop empty array', () => {
      expect(() => {
        stack.pop();
      }).toThrow('empty array');
    });

    it('return last element but maintain', () => {
      stack.push('first');
      stack.push('second');

      const maintainElement = stack.peek();
      expect(maintainElement).toBe('second');
      expect(stack.size()).toBe(2);
      expect(stack.array).toEqual(['first', 'second']);
    });
  });
});
