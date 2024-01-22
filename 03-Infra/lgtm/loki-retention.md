- https://grafana.com/docs/loki/latest/operations/storage/retention/

# Retention
그라파나 로키의 보존은 테이블 관리자 또는 컴팩터를 통해 이루어집니다.

기본적으로 `table_manager.retention_deletes_enabled` 또는 `compactor.retention_enabled` 플래그가 설정되지 않은 경우, Loki로 전송된 로그는 영구 보존됩니다.

테이블 관리자를 통한 보존은 객체 저장소 TTL 기능에 의존하여 이루어지며, 볼트 저장소 및 청크/색인 저장소 모두에서 작동합니다. 그러나 압축기를 통한 보존은 boltdb-shipper 및 tsdb 저장소에서만 지원됩니다.

Compactor 보존은 기본값이 되며 장기적으로 지원됩니다. 테넌트별 및 스트림별 사용 사례에 대한 보다 세분화된 보존 정책을 지원합니다.

## Compactor

압축기는 인덱스 항목의 중복을 제거할 수 있습니다. 또한 세분화된 보존을 적용할 수도 있습니다. 압축기로 보존을 적용할 때는 테이블 관리자가 필요하지 않습니다.

`압축기를 싱글톤(단일 인스턴스)으로 실행합니다.`

압축과 보존은 비동기식입니다. 압축기가 다시 시작되면 중단된 지점부터 계속됩니다.

Compactor는 매 compaction_interval마다 또는 뒤처진 경우 가능한 한 빨리 압축 및 보존을 적용하기 위해 반복합니다.

인덱스를 업데이트하는 Compactor의 알고리즘입니다:

- 매일 각 테이블에 대해:
    - 테이블을 단일 인덱스 파일로 압축합니다.
    - 전체 인덱스를 트래버스합니다. 테넌트 구성을 사용해 제거해야 할 청크를 식별하고 표시합니다.
    - 인덱스에서 표시된 청크를 제거하고 그 참조를 디스크의 파일에 저장합니다.
    - 수정된 새 인덱스 파일을 업로드합니다.

보존 알고리즘이 인덱스에 적용됩니다. 보존 알고리즘을 적용하는 동안 청크는 삭제되지 않습니다. 청크는 스윕될 때 압축기에 의해 비동기적으로 삭제됩니다.

표시된 청크는 구성된 retention_delete_delay가 만료된 후에만 삭제됩니다:

- boltdb-shipper 인덱스는 특정 간격으로 이를 사용하는 구성 요소(쿼리어 및 룰러)의 공유 저장소에서 새로 고쳐집니다. 즉, 청크를 즉시 삭제하면 구성 요소가 여전히 이전 청크를 참조하게 되어 쿼리 실행에 실패할 수 있습니다. 지연이 있으면 컴포넌트가 저장소를 새로 고칠 수 있으므로 해당 청크에 대한 참조를 정상적으로 제거할 수 있습니다.

- 구성 실수가 발생한 경우 청크 삭제를 취소할 수 있는 짧은 시간을 제공합니다.

마커 파일(삭제할 청크가 포함된 파일)은 디스크가 유일한 참조가 되므로 영구 디스크에 저장해야 합니다.

### Retention Configuration
이 압축기 구성 예제는 보존을 활성화합니다.
```
compactor:
  working_directory: /data/retention
  shared_store: gcs
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150
schema_config:
    configs:
      - from: "2020-07-31"
        index:
            period: 24h
            prefix: loki_index_
        object_store: gcs
        schema: v11
        store: boltdb-shipper
storage_config:
    boltdb_shipper:
        active_index_directory: /data/index
        cache_location: /data/boltdb-cache
        shared_store: gcs
    gcs:
        bucket_name: loki
```

보존은 인덱스 기간이 24시간인 경우에만 사용할 수 있습니다.

`retention_enabled`를 `true`로 설정합니다. 이 설정이 없으면 압축기는 테이블만 압축합니다.

저장소에 액세스하기 위해 `schema_config`와 `storage_config`를 정의합니다.

인덱스 기간은 24시간이어야 합니다.

`working_directory`는 표시된 청크와 임시 테이블이 저장될 디렉토리입니다.

`compaction_interval`은 압축 및/또는 보존이 적용되는 빈도를 지정합니다. 압축이 늦어지면 압축 및/또는 보존이 가능한 한 빨리 수행됩니다.

`retention_delete_delay`는 압축기가 표시된 청크를 삭제하는 지연 시간입니다.

`retention_delete_worker_count`는 청크를 삭제하기 위해 인스턴스화된 고루틴 워커의 최대 수량을 지정합니다.

### 보존 기간 구성하기
보존 기간은 `limits_config` 구성 섹션에서 구성할 수 있습니다.

보존 정책을 설정하는 방법에는 두 가지가 있습니다:

`retention_period`: 전역적으로 적용됩니다.
선택기와 일치하는 청크에만 적용되는 `retention_stream`.
최소 보존 기간은 24시간입니다.

이 예는 전역 보존을 구성합니다:
```
...
limits_config:
  retention_period: 744h
  retention_stream:
  - selector: '{namespace="dev"}'
    priority: 1
    period: 24h
  per_tenant_override_config: /etc/overrides.yaml
...
```

참고: `retention_stream` 정의의 선택자 필드에서만 레이블 일치자를 사용할 수 있습니다. 임의의 LogQL 표현식은 지원되지 않습니다.

테넌트별 보존은 `/etc/overrides.yaml` 파일을 사용하여 정의할 수 있습니다. 예를 들어

```
overrides:
    "29":
        retention_period: 168h
        retention_stream:
        - selector: '{namespace="prod", container=~"(nginx|loki)"}'
          priority: 2
          period: 336h
        - selector: '{container="loki"}'
          priority: 1
          period: 72h
    "30":
        retention_stream:
        - selector: '{container="nginx", level="debug"}'
          priority: 1
          period: 24h
```

적용할 규칙은 이 목록에서 일치하는 첫 번째 규칙을 선택하면 됩니다:

- 테넌트별 retention_stream이 현재 스트림과 일치하는 경우 가장 높은 우선순위가 선택됩니다.
- 글로벌 retention_stream이 현재 스트림과 일치하면 가장 높은 우선순위가 선택됩니다.
- 테넌트별 retention_period이 지정되어 있으면 해당 기간이 적용됩니다.
- 일치하는 항목이 없는 경우 글로벌 retention_period이 선택됩니다.
- 글로벌 retention_period을 지정하지 않으면 기본값인 744시간(30일)의 보존 기간이 사용됩니다.

스트림 매칭은 Prometheus 라벨 매칭과 동일한 구문을 사용합니다:

- `=`: 제공된 문자열과 정확히 일치하는 레이블을 선택합니다.
- `!=`: 제공된 문자열과 같지 않은 레이블을 선택합니다.
- `=~`: 제공된 문자열과 정규식 일치하는 레이블을 선택합니다.
- `!~`: 제공된 문자열과 정규식 일치하지 않는 레이블을 선택합니다.

예제 구성은 이러한 규칙을 설정합니다:

- 개발 네임스페이스에서 29와 30을 제외한 모든 테넌트의 보존 기간은 24시간입니다.
- 개발 네임스페이스에 있지 않은 29와 30을 제외한 모든 테넌트의 보존 기간은 744시간입니다.
- 테넌트 29의 경우:
    - 컨테이너 로키 또는 네임스페이스 프로드에 있는 스트림을 제외한 모든 스트림의 보존 기간은 168시간(1주일)입니다.
    - prod 네임스페이스에 있는 모든 스트림은 컨테이너 레이블이 loki이더라도 prod 규칙의 우선순위가 더 높으므로 보존 기간이 336시간(2주)입니다.
    - 컨테이너 레이블이 loki이지만 네임스페이스 prod에 속하지 않는 스트림은 72시간의 보존 기간을 갖습니다.
- 테넌트 30의 경우:
    - 컨테이너 레이블이 nginx인 스트림을 제외한 모든 스트림은 재정의가 지정되지 않았으므로 글로벌 보존 기간이 744시간입니다.
    - nginx 레이블이 있는 스트림의 보존 기간은 24시간입니다.

## Table Manager
보존 지원을 사용하려면 삭제 및 보존 기간을 사용하도록 테이블 관리자를 구성해야 합니다. 사용 가능한 모든 옵션은 Loki 구성 참조의 table_manager 섹션을 참조하세요. 또는 table-manager.retention-period 및 table-manager.retention-deletes-enabled 명령줄 플래그를 사용할 수 있습니다. 제공된 보존 기간은 Prometheus 공통 모델 ParseDuration을 사용하여 구문 분석할 수 있는 문자열로 표현된 기간이어야 합니다. 예시 7D, 1W, 168H.

경고: 보존 기간은 period_config 블록에 구성된 인덱스 및 청크 테이블 기간의 배수여야 합니다. 자세한 내용은 테이블 관리자 설명서를 참조하세요.

참고: 보존 기간을 초과한 데이터의 쿼리를 방지하려면 chunk_store_config의 max_look_back_period 구성을 table_manager.retention_period에 설정된 값보다 작거나 같은 값으로 설정해야 합니다.

S3 또는 GCS를 사용하는 경우 청크를 저장하는 버킷에 만료 정책이 올바르게 설정되어 있어야 합니다. 자세한 내용은 S3의 설명서 또는 GCS의 설명서를 참조하세요.

현재 보존 정책은 전역적으로만 설정할 수 있습니다. 수집된 로그를 삭제하는 API가 포함된 테넌트별 보존 정책은 아직 개발 중입니다.

로키의 설계 목표는 로그를 저렴하게 저장하는 것이므로 볼륨 기반 삭제 API는 우선순위가 떨어집니다. 이 기능이 출시될 때까지는 수집된 로그를 갑자기 삭제해야 하는 경우, 개체 저장소에서 오래된 청크를 삭제할 수 있습니다. 그러나 이렇게 하면 로그 콘텐츠만 삭제되고 레이블 인덱스는 그대로 유지되며, 관련 레이블은 계속 볼 수 있지만 삭제된 로그 콘텐츠는 검색할 수 없다는 점에 유의하세요.

테이블 관리자 내부에 대한 자세한 내용은 테이블 관리자 설명서를 참조하세요.

### 구성 예시
보존 기간이 28일인 GCS를 사용한 구성 예시입니다:
```
schema_config:
  configs:
  - from: 2018-04-15
    store: bigtable
    object_store: gcs
    schema: v11
    index:
      prefix: loki_index_
      period: 168h

storage_config:
  bigtable:
    instance: BIGTABLE_INSTANCE
    project: BIGTABLE_PROJECT
  gcs:
    bucket_name: GCS_BUCKET_NAME

chunk_store_config:
  max_look_back_period: 672h

table_manager:
  retention_deletes_enabled: true
  retention_period: 672h
```