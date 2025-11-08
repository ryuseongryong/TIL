## NVMeOT

- NVMeOT의 기본 동작 원리
- 쿠버네티스 CSI 드라이버
    - CSI RWO, RWX
        - RWO, RWX는 pod level이 아니라 node level
        - RWOncePod?가 새로 생겼음(pod하나에서만 쓰기 가능)
    - 하나의 노드에 같은 target을 두 번 이상 mount가 되지 않음
    하나의 노드에 읽기쓰기/읽기전용 동시에 마운트 불가
        - 하나는 Read only로 사용하고, 하나는 RW로 사용할 예정이었으나 안 됨
        - 커널 단에서 막음(슈퍼블록을 공유)
        - 블록디바이스를 마운트한다는 것은 ext4의 슈퍼블록을 마운트하는 것이기 때문에 섞어서 마운트가 되지 않음
        - 오픈스택을 사용하는 회사에서는 바로 연결할 수 있음
        - 로컬패스프로비저너 스타일로 적용할까 했었는데 CSI가 있어서 사용함
    - 그럼 해결책은 RW로 마운트하고 binding을 Readonly로 하여 subfilesystem으로 진행
    - controller의 unique한 target ID, server에서 device하나를 열때 nvme0이라는 이름이 생성됨 + host mqn이라는 접속정보

## DeltaStore

- 다양한 데이터 저장소를 사용하는 이유
    - 확장성 vs 사용성
        - 확장성 → 스케일아웃(Hadoop)
        - 사용성 → Transaction, SQL 지원(RDBMS)
    - OLTP(OnlineTransactionProcessing) vs OLAP(OnlineAnalyticalProcessing)
        - OLTP → Row Oriented(RDBMS/NoSQL)
        - OLAP → Column Oriented(AWS RedShift/DeltaLake)
    - Elasticsearch, TimescaleDB
    - DeltaLake
        - 확장성 + 사용성(ACID) + OLAP
            - Atomicity + Consistency + Isolation + Durability
        - 스냅샷 관리(RocksDB)
        - 접근 제어
        - 로그를 기반으로 Parquet file을 정리함
            - 한번 쓸 때마다 logfile이 생성
            - checkpoint로 log file 정리
        - Query
            - partitioning filtering(Day=asdf/Hour=asdf/min=asdf…)가 있음
            - partition의 개수가 10만개이면, query가 들어오면 10만개를 비요해야하는 문제가 있음
            - RockDB의 key를 partition filter로 적용(RocksDB에서 Key를 기준으로 정렬 가능)
- parquet file은 column 기반, 확장성이 좋음, ACID도 지원
- 개발 목적
    - DeltaLake 확장성 + 사용성
    - 효율적인 데이터 공유(Sharing) + 관리(Governance) → DeltaSore
        - 데이터 클린룸(CleanRoom)
            - 많은 IT 회사들이 개발/홍보
            - 빅데이터 수집 → 빅데이터 활용
        - 오픈소스 활용/공개
            - DeltaLake + DeltaSharing(at DataBricks)
        - 주요 기능
            - 실시간 빅데이터 쿼리
            - 데이터 관리(접근 제어)

## DeltaSync

- 효율적인 데이터 수집/변환/저장 → DeltaSync
    - 데이터 파이프라인 구조
        - 기존 : Producer → Kafka → SparkStreaming → DeltaOnS3 → Spark/Trino : 대부분 JVM기반(Kafka는 page cache 최적화가 되어 있긴 함)
        - 개선 : Producer → Fluvio(분산 메시지 Q의 rust 버전) → DeltaSync → DeltaOnS3 → DeltaStore → [Arrow](https://arrow.apache.org/)(serialization, deserialization이 불필요함, 언어간 전송 때도 직렬화/역직렬화가 필요한데 Arrow를 쓰면 불필요함)
            - 적은 자원으로 빠르게 처리
            - Arrow 지원 FrameWork : Pandas/DuckDB(C++ StandAlone SQL engine)/Polars(Rust engine, SQL + DataFrame)
                - parquet → arrow → pandas > parquet → pandas : arrow는 multi thread 지원, row/column 으로 저장된 pandas를 더 빠르게 사용 가능
    - 오픈소스 활용/공개
        - kafka-delta-ingest(spark streaming → deltalake)
        - delta-rs, rdkafka
    - 주요 기능
        - 데이터 수집(Kafka/MQTT/Fluvio)
        - 데이터 변환
        - 데이터 저장(Delta/NoSQL/RDBMS)
    - 동작 원리
        - 데이터 수집
            - AutoLoader by Databricks(cloudfiles)
                - s3 data 쌓을 때 File을 직접 넣으면 autoloader가 읽어서 streaming해줌(s3 파일 추가 event를 확인하여 진행하는 방식, 비IT회사에서 다수 사용)
    - DeltaSync → DeltaStore
    - DeltaRS, DataFusion(spark → rust version embeding)
    - JVM은 변수(객체)에 대한 레퍼런스를 모니터링 하고 GC하는 구조, 객체가 많아지면 major GC, minor GC 등등이 있음
    - Rust는 scope 관리를 잘해서 레퍼런스 모니터링 없이도 메모리 관리
    
    # 태환님
    
    - time travel
    - CDC
    - key : path(partition column value), value : action value, from to 로 version 지원(메모리는 rocksDB에 있어서 변화 없음)
        - rocking이 row level rocking, file level rocking? → 동작 방식이 다름, 묶음 단위 parquet file 단위 rocking
        - OLAP용
    - Deletion Vector, 기존에는 parquet에 한 row만 제거하면 전체 다시 쓰는 것이었는데, 이 기능은 해당 부분이 삭제되었다고 알려주는 기능
    - deltalog를 안쓰면 parquet partitioning을 사용하는 것
    - clientside JS → presigned URL → parquet
    Client  RESTAPI server DeltaSharing
    
    # Spark Connect
    
    - pyspark도 JVM으로 실행됨(dataframe이 JVM위에)
    - grpc로 구현
    - 70개의 쌍으로 사용하는데, 70개를 하나의 spark 서버에서 사용 가능
    - Client : driver, server: executer

# NVMeF

- infini band(500Gi)
- AWS 고급 EBS

# NVMeOT

- TCP로 전송