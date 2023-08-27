# Network bonding or Network teaming : Feature comparison
- https://documentation.suse.com/smart/network/html/reference-network-bonding-teaming-comparison/index.html

## Bonding or Teaming
- Link aggregation은 논리적 계층을 제공하기 위해 네트워크 연결을 결합하는 일반적인 용어이다. Channel teaming, Ethernet bonding, Port truncating은 동일한 개념을 지칭하는 동의어이다.
- 이 개념의 기존 구현은 networking bonding으로 알려져 있다. 새로운 구현은 network teaming으로 알려져 있다. 두 구현 모두 병렬로 사용할 수 있다. teaming은 bonding을 대체하는 것이 아니라 bonding의 대안이다.
- Bonding과 Teaming의 주요 차이점은 Bonding은 kernal에서만 처리된다는 것이다. Teaming에는 Teaming된 인스턴스에 대한 Interface를 제공하는 작은 커널 모듈 세트가 포함되어 있지만, 그 외의 모든 것은 사용자 공간에서 처리된다.