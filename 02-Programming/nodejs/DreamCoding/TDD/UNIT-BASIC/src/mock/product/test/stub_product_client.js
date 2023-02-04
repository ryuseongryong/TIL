class StubProductClient {
  async fetchItems() {
    return [
      { item: 'Milk', available: true },
      { item: 'Banana', available: false },
    ];
  }
}
// 실제로 사용하는 함수와 동일한 input을 가지고, 복잡한 로직없이 예상되는 return을 입력해둔 테스트용 stub 클래스
module.exports = StubProductClient;
