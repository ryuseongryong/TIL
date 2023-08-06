
# Multi Site

- https://docs.ceph.com/en/latest/radosgw/multisite/
- https://docs.oracle.com/cd/E52668_01/E66514/html/ceph-object-gateway-multisite.html


## Single-Zone Configurations and Multi-site configurations
### Single-Zone Configurations
- 단일 영역 구성은 일반적으로 두 가지로 구성된다.
    - 하나의 구역을 포함하는 하나의 zonegroup
    - ceph-radosgw 클라이언트 요청이 로드밸런싱된 하나 이상의 ceph-radosgw 인스턴스
- 일반적인 단일 영역 구성에서는 단일 ceph 스토리지 클러스터를 사용하는 여러 개의 ceph-radosgw 인스턴스가 있다.

### Varieties of Multi-Site Configuration
- 크라켄 릴리스부터 ceph는 ceph 객체 게이트웨이를 위한 여러 멀티 사이트 구성을 지원한다.
- Multi-zone
    - 보다 고급 토폴로지인 multi-zone 구성이 가능하다. 다중 영역 구성은 하나의 영역 그룹과 여러 영역으로 구성되며, 각 영역은 하나 이상의 ceph-radosgw 인스턴스로 구성된다. 각 영역은 자체 ceph 스토리지 클러스터에 의해 지원된다.
    - 특정 영역 그룹에 여러 영역이 있으면 영역 중 하나에 심각한 장애가 발생하는 경우 해당 영역 그룹에 대한 재해 복구가 제공된다. 크라켄 릴리스부터 각 영역은 활성 상태이며 쓰기 작업을 수신할 수 있다. 여러 개의 활성 영역을 포함하는 다중 영역 구성은 재해 복구를 향상시키며 콘텐츠 전송 네트워크의 기반으로도 사용할 수 있다.
- Multi-zonegroups
    - Ceph 객체 게이트워이는 여러 구역 그룹(이전에는 regions라고 함)을 지원한다. 각 영역 그룹에는 하나 이상의 영역이 포함된다. 두 영역이 동일한 영역 그룹에 있고 해당 영역그룹이 두 번째 영역그룹과 동일한 영역에 있는 경우, 두 영역에 저장된 개체는 글로벌 개체 네임스페이스를 공유한다. 이 글로벌 객체 네임스페이스는 영역 그룹과 영역 간에 고유한 객체 ID를 보장한다.
    - 각 버킷은 버킷이 생성된 영역 그룹이 소유하며(버킷 생성 시 LocationConstraint에 의해 재정의된 경우 제외), 해당 버킷의 개체 데이터는 해당 영역 그룹의 다른 영역으로만 복제된다. 다른 영역 그룹으로 전송되는 해당 버킷의 데이터 요청은 버킷이 있는 영역 그룹으로 전달된다.
    - 여러 영역에서 사용자와 버킷의 네임스페이스를 공유하되 개체 데이터를 해당 영역의 하위 집합으로 격리하려는 경우 여러 영역그룹을 만드는 것이 유용할 수 있다. 스토리지를 공유하는 연결된 사이트가 여러 개 있지만 재해 복구 목적으로 단일 백업만 필요할 수 있다. 이러한 경우, 모든 개체를 모든 영역에 복제하지 않도록 각각 두 개의 영역만 있는 여러 개의 영역 그룹을 만드는 것이 합리적일 수 있다.
    - 다른 경우에는 각 영역에 하나의 영역그룹을 사용하여 별도의 영역에서 사물을 격리하는 것이 더 합리적일 수 있다. 영역 그룹은 데이터와 메타데이터의 격리를 개별적으로 제어할 수 있도록 하여 유연성을 제공한다.