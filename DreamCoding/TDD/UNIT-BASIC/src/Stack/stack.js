class Stack {
  constructor() {
    this._size = 0;
    this.head = null;
  }

  size() {
    return this._size;
  }

  push(item) {
    const node = { item, next: this.head };
    this.head = node;
    this._size++;
    return node.item;
  }

  pop() {
    if (this.head === null) {
      throw new Error("empty array");
    }
    const node = this.head;
    this.head = node.next;
    this._size--;
    return node.item;
  }

  peek() {
    if (this.head === null) {
      throw new Error("empty array");
    }
    return this.head.item;
  }
}

// Stack.prototype.stack = [1, 2, 3, 4];
// console.log(Stack.prototype.pop());
// console.log(Stack.prototype.push(5));

module.exports = Stack;
