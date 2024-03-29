# Multisite Sync Policy
- https://docs.ceph.com/en/latest/radosgw/multisite-sync-policy/

- 멀티사이트 버킷 단위 동기화 정책은 서로 다른 영역에 있는 버킷 간의 데이터 이동을 세밀하게 제어할 수 있다.
  이것은 영역 동기화 메커니즘을 확장한다.
  이전에는 버킷이 대칭적으로 처리되었다. 즉 각 (데이터) 영역은 다른 모든 영역과 동일해야 하는 해당 버킷의 미러를 보유하고 있었다. 반면, 버킷 단위 동기화 정책을 활용하면 버킷이 분산될 수 있으며, 한 버킷이 다른 영역에 있는 다른 버킷(이름이나 ID를 공유하지 않는 버킷)에서 데이터를 가져올 수 있었다. 따라서 동기화 프로세스는 버킷 동기화 소스와 버킷 동기화 대상이 항상 동일한 버킷을 참조한다고 가정했지만, 이제는 더 이상 그렇지 않다.
- 동기화 정책은 이전 영역 그룹의 조잡한 구성(sync_from*)을 대체한다. 동기화 정책은 영역 그룹 수준에서 구성할 수 있고(구성한 경우 이전 스타일 구성을 대체함), 버킷 수준에서도 구성할 수 있다.
- 동기화 정책에서는 데이터 흐름 구성 목록과 파이프 구성 목록을 포함할 수 있는 여러 그룹을 정의할 수 있다. 
  데이터 흐름은 서로 다른 영역 간의 데이터 흐름을 정의한다. 여러 영역이 서로 데이터를 동기화하는 대칭 데이터 흐름을 정의할 수 있으며, 한 영역에서 다른 영역으로 데이터가 한 방향으로 이동하는 방향성 데이터 흐름을 정의할 수도 있다.
- 파이프는 이러한 데이터 흐름을 사용할 수 있는 실제 버킷과 이와 연결된 속성(e.g. source object prefix)을 정의한다.

- 동기화 정책 그룹은 3가지 상태로 존재할 수 있다.
    enabled : sync is allowed and enabled
    allowed : sync is allowed
    forbidden : sync (as defined by this group) is not allowed and can override other groups

- 정책은 버킷 수준에서 정의할 수 있다. 버킷 수준 동기화 정책은 영역 그룹 정책의 데이터 흐름을 상속하며 영역 그룹이 허용하는 것의 하위 집합만 정의할 수 있다.

- 와일드카드 영역 및 정책의 와일드카드 버킷 매개변수는 모든 관련 영역 또는 모든 과련 버킷을 정의한다. 버킷 정책의 맥락에서 이는 현재 버킷 인스턴스를 의미한다. 전체 영역이 미러링되는 재해 복구 구성에서는 버킷에 아무것도 구성할 필요가 없다. 그러나 세분화된 버킷 동기화를 위해서는 와일드카드 사용 등 영역 그룹 수준에서는 파이프를 허용(상태=허용)하여 동기화하도록 구성하되, 버킷 수준에서는 특정 동기화만 활성화(상태=활성화)하는 것이 더 좋다. 필요한 경우 버킷 수준에서 정책을 통해 데이터 이동을 특정 관련 영역으로 제한할 수 있다.

- 영역 그룹 정책에 대한 변경 사항은 영역 그룹 마스터 영역에 적용해야 하며, 주기 업데이트 및 커밋이 필요하다. 버킷 정책에 대한 변경 사항은 영역 그룹 마스터 영역에 적용해야 한다. 변경 사항은 rgw에 의해 동적으로 처리된다.

## S3 Replication API
- S3 버킷 복제 API도 구현되어 사용자가 서로 다른 버킷 간에 복제 규칙을 만들 수 있다. 단, AWS 복제 기능은 동일한 영역 내에서 버킷 복제를 허용하지만, rgw는 현재로서는 이를 허용하지 않느다는 점에 유의해야 한다. 그러나 rgw API는 사용자가 특정 버킷을 동기화할 영역을 선택할 수 있는 새로운 영역 배열도 추가했다.