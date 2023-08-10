# What is Pgpool-II?
- https://Pgpool.net/mediawiki/index.php/Main_Page

- Pgpool-II는 PostgreSQL 서버와 PostgreSQL 데이터베이스 클라이언트 사이에서 작동하는 미들웨어이다.
  BSD 및 MIT와 유사한 라이선스에 따라 배포된다.

## Features
- Connection Pooling
  사용자 이름, 데이터베이스, 프로토콜 버전 등 동일한 속성을 가진 새 연결이 들어올 때마다 PostgreSQL 서버에 연결을 저장하고 이를 재사용한다. 연결 오버헤드가 줄어들고 시스템의 전반적인 처리량이 향상된다.
- Replication
  여러 대의 PostgreSQL 서버를 관리할 수 있다. 복제 기능을 사용하면 2개 이상의 물리적 디스크에 실시간 백업을 생성할 수 있으므로 디스크 장애 발생 시에도 서버를 중단하지 않고 서비스를 계속할 수 있다.
- Load Balancing
  데이터베이스가 복제된 경우 어느 서버에서든 SELECT 쿼리를 실행하면 동일한 결과가 반환된다. Pgpool-II는 복제 기능을 활용하여 SELECT 쿼리를 여러 서버에 분산함으로써 각 PostgreSQL 서버의 부하를 줄이고 시스템의 전체 처리량을 개선한다. PostgreSQL 서버의 수에 비례하여 성능이 향상된다. 부하 분산은 많은 사용자가 동시에 많은 쿼리를 실행하는 상황에서 가장 잘 작동한다.
- Limiting Exceeding Connections
  PostgreSQL에는 최대 동시 연결 수에 제한이 있으며, 이 연결 수를 초과하면 연결이 거부된다. 그러나 최대 연결 수를 설정하면 리소스 소비가 증가하고 시스템 성능에 영향을 미친다. Pgpool-II에도 최대 연결 수에 대한 제한이 있지만 추가 연결은 즉시 오류를 반환하는 대신 큐에 대기한다.
- Watchdog
  워치독은 여러 Pgpool-II를 조정하고, 강력한 클러스터 시스템을 생성하며, 단일 장애 지점 또는 두뇌 분할을 방지할 수 있다. 워치독은 다른 Pgpool-II 노드에 대해 수명 검사를 수행하여 Pgpool-II의 오류를 감지할 수 있다. 활성 Pgpool-II가 다운되면 대기 Pgpool-II가 활성으로 승격되어 가상 IP를 인수할 수 있다.
- In Memory Query Cache
  메모리 내 쿼리 캐시는 한 쌍의 SELECT 문과 그 결과를 저장할 수 있다. 동일한 SELECT가 들어올 경우, Pgpool-II는 캐시에서 값을 반환한다. SQL 구문 분석이나 PostgreSQL에 대한 엑세스가 필요하지 않으므로 메모리 내 캐시를 사용하면 매우 빠르다. 반면 캐시 데이터 저장에 약간의 오버헤드가 추가되므로 경우에 따라 일반 경로보다 느릴 수 있다.
- Pgpool-II는 PostgreSQL의 백엔드 및 프론트엔드 프로토콜을 사용하며, 백엔드와 프론트엔드 간에 메시지를 중계한다. 따라서 데이터베이스 애플리케이션(프론트엔드)은 Pgpool-II를 실제 PostgreSQL 서버로 간주하고, 서버(백엔드)는 Pgpool-II를 클라이언트 중 하나로 간주한다. Pgpool-II는 서버와 클라이언트 모두에 투명하기 때문에 기존 데이터베이스 애플리케이션은 Pgpool-II와 함께 사용할 수 있다.
