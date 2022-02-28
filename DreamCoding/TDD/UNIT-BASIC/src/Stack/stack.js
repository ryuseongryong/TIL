class Stack {
  constructor() {
    this.array = [];
  }

  size() {
    return this.array.length;
  }

  push(newElement) {
    this.array.push(newElement);
  }

  pop() {
    if (this.array.length === 0) {
      throw new Error('empty array');
    }
    return this.array.pop();
  }

  peek() {
    if (this.array.length === 0) {
      throw new Error('empty array');
    }
    return this.array.slice(-1)[0];
  }
}

// Stack.prototype.stack = [1, 2, 3, 4];
// console.log(Stack.prototype.pop());
// console.log(Stack.prototype.push(5));

module.exports = Stack;
