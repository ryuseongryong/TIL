# DeltaQuery Optimization (vs Spark/Trino)
- Benchmark(DQ vs Spark)
- Rust (vs JVM with GC)
- Compiler Optimization
- Standalone Computing (vs Distributed Computing)


spark : batch based pipeline 를 대체하기 위한 것

FDAP stack by InfluxDB(시계열 데이터)
- FlightSQL
- Data Fusion
- Arrow
- Parquet

DeltaQuery -> OSS 버전은 DuckDB, Imbeding가능한 것은 python C++ JAVA RUST 개발 시 Libraray로 넣어서 사용하는 것이 Imbeding Query engine

duckdb c++ >> 데이터 량이 적을 때
datafusion rust >> 최적화 여지가 많은 것이 유리
polas 도 있으나 위에 선에서 가능

duckdb + delta lake??로 사용해야하기 때문에 data fusion

duckdb - datafusion은 DB query가 달라질 수 있음

cf. storage engine은 delta lake 기반
쿼리의 대상이 되는 데이터만 필터링하는 역할, data file들만 걸러내기
delta lake == parquet + transaction log
기존에는 parquet + partitioning만 함

parquet파일
기존에는 metadata - row그룹, 각 column의 minmax 통계 값을 읽어서 필터링
delta lake는 별도 필터링 용 로그만 읽어서 필터링

## Rust
- 2~3년전부터 JAVA app -> Rust app으로 성능 100배 향상
- JVM with GC 문제점
    - 메모리 사용량 제어 불가
        - 메모리 반환 후 GC에 의해 수거
        - 8G할당, 8G해제 -> 다시 8G 사용 X -> GC이후 사용가능(eventually 반환은 가능하지만, 일정시간 메모리 사용량이 늘어나고, GC를 바로하게되면 오버헤드가 계속 증가함)
    - 메모리 한도를 늘릴수록 GC 오버헤드 커짐
        - GC에 의해 관리되는 영역이 넓어짐
    - GraalVM으로 최적화할 수 있긴하지만 GC 문제 자체를 없애기 어려움
    - SK hynix에서 JAVA 메모리 문제 때문에 임팔라 사용한 사례
- Rust
    - raw vectorization 지원
    - Memory-Safe mechanism without GC(ownershop, borrowing)
    - 효율적인 물리 메모리와 스왑 메모리 사용 가능
    - cargo debug모드는 최적화하지 않음, release모드는 최적화 진행

## Standalone Computing(vs Distributed Computing)
- 대규모 클러스터 문제점
    - 구축/유지 비용(장비 + 인력)
    - 실시간 응답성 지원 불가
    - 대용량 네트워크 트래픽 발생
    - 비효율적인 소프트웨어 아키텍처 (분산 처리)
- 소규모 클러스터 가능성 (서버 1대~)
    - 물리 서버 발전
        - 멀티코어(100~)
        - 메모리(CXL, Swap on NVMe)
            - 메인메모리 -> CPU에 바로 붙어있어서 더 늘리기 어려움
            - CXL은 PCIe에 붙어있어서 무한히 확장 가능성
        - 스토리지(NVMe)
    - 런타임 환경 개선(러스트)
        - 벡터 연산 지원(SIMD)
        - 메모리 한계 극복(물리 메모리 + 스왑 메모리)

## Distrubuted Filesystem
CPU 에서 멀어질 수록 느려짐
- L1 L2 L3 cache
- memoery
- CXL
- NVMe
- SSD
- HDD
- Network

data object에서 긁어오는 것이 젤 느림

- DeltaQuery with JuiceFS : client side caching + partitioning data writing with automatic renaming
               |      <client side caching>       | < JuiceFS입장에서는 OSD로 취급>
    DeltaQuery - Gateway(S3) - MDS(redis)
                             - OSD(localfs)
                             - Object Storage(S3) - Gateway(S3) - MDS
                                                                - OSD
MDS : inode, directory entry, super block... file 메타데이터 서버
OSD : 실제 데이터 블록을 갖고 있는 데몬
    - 모든 저장소에서 실제 파일은 block으로 쪼개서 지정된 사이즈 단위(메모리 - 페이지, 스토리지- 블록(청크) 쌓도록 되어 있음)
    - 빅데이터도 블록 사이즈 설정이 중요함
- cache hit율이 높으면 사용, 낮으면 사용하지 않는 게 좋음(일반적으로 높을 수 밖에 없음)
- sk hynix에서 8PB NVMe 구성한 사례는 L3 cache를 수십GB로 구성한 것과 비슷함
- S3는 automic renaming이 안됨
    - delta lake는 (partitioned)parquet files + transaction log 저장하는 것 [commoditi fs에서 transaction 보장]
    - 여러개 파일을 한 번에 저장, 100개 써야하는데 다른 애가 읽으면 50개만 읽게 됨(transaction)
    - 일반적인 fs에서 DBMS 등과 달리 transaction 보장이 되는 방법은 file을 쓸 때 안전하게 보장받는것.
    - 하나의 file이 하나의 transaction, log가 0, 1, 2, 3, ...씩 증가함, data file은 존재하지만, log가 없으면 읽지 못함
    - s3는 이를 지원하지 않음
    - 여러 대로 pipelining하게되면 중복될 수 있는데 이를 juiceFS로 해결 가능
- SideCar posix?
- page cache

## Columnar(vs Row Oriented)
- 컬럼 기반 데이터
    - 스토리지 포맷(Parquet)
    - 메모리 포맷(Arrow)
    - 네트워크 프로토콜(FlightSQL)

- 기존 DB는 행기반
- 빅데이터는 열기반

         < row기반 >                       < column 기반으로 변경 >
- Python - DBAPI - DBAPI driver(postgres)      | - Postgres
                 - DBAPI driver(trino)         | - trino - delta - s3(parquet: column based)

        < row기반 유지 >            < driver DB 통합 >
- Java/Python/ - ADBC - ADBC driver(flightSQL) | - postgresql/mongodb/...
                                               | - deltaquery - delta - s3

- 직렬화, 역질렬화 과정 제거되는 장점이 있음

## Qeury Optimization
- 예졔 쿼리(집계)
    [sql] select data,hour,sum(score) from delta.datafusion.local group by date,hour
    [logical plan]
        plan=Projection; delta.datafusion.local.date, delta.datafusion.local.hour, SUM(delta.datafusion.local.score)
            Aggregate: groupBy=[delta.datafusion.local.date, delta.datafusion.local.hour], aggr=[SUM(delta.datafusion.local.score)]
                TableScan: delta.datafusion.local
    [physical plan 0]
        AggregateExec(FinalPartitioned, GroupBy(date, hour))
            RepartitionExec(Hash(date, hour))
                RepartitionExec(RoundRobin(10))
                    AggregateExec(Partial, GroupBy(date, hour))
                        ParquetExec()
    [physical plan 1]
        AggregateExec(SinglePartitioned, GroupBy(date, hour))
            RepartitionExec(Hash(date, hour))
                RepartitionExec(RoundRobin(10))
                    ParquetExec()
- spark cost estimation, logical plan을 physical plan으로 어떻게 바꿀지 1안, 2안, 3안, 4안 만들어서 각 비용을 estimation : 
- group by는 cardinality가 낮다면 1개의 데이터를 파티셔닝하는 것이 효율적, 극단적으로 높다면 파티셔닝하는 것이 비효율적
    - 1억개 -> 300G - 400G 메모리 사용