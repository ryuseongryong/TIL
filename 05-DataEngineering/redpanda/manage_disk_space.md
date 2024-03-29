- https://docs.redpanda.com/current/manage/cluster-maintenance/disk-utilization/

# Manage Disk Space
레드판다는 클러스터의 프로덕션 안정성을 보장하기 위해 디스크 공간을 관리하는 몇 가지 방법을 제공합니다. 할 수 있습니다:

- 메시지 보존 및 로그 정리 정책을 구성합니다.

- 스토리지 임계값 속성을 구성하고 디스크 여유 공간이 특정 임계값에 도달하면 알려주는 알림을 설정합니다.

- 지속적인 데이터 밸런싱을 사용해 노드 간에 파티션을 자동으로 분산하여 디스크 사용량을 보다 균형 있게 관리하세요.

- 밸러스트 파일을 생성하여 디스크 부족에 대비한 버퍼 역할을 하세요.

디스크 여유 공간이 매우 낮은 수준에 도달하면 Redpanda는 클라이언트의 제작을 차단합니다.

Redpanda 노드는 디스크 공간이 부족해지면 종료됩니다. 이로 인해 리더 재할당과 복제 및 리밸런싱이 발생하여 성능에 영향을 미칩니다. 클러스터에서 더 많은 노드가 가득 차서 종료되면 트래픽이 더 적은 수의 노드에 집중되어 성능에 영향을 미칩니다.

## Configure message retention
기본적으로 자체 호스팅 Redpanda 클러스터의 모든 주제는 로컬 디스크에 24시간 동안 데이터를 보관하는 반면, Redpanda 클라우드 주제는 6시간 동안 데이터를 보관합니다. Redpanda는 디스크 공간을 절약하기 위해 동적 공간 관리 전략을 사용합니다. 그러나 데이터가 충분히 빠르게 쓰여지면 계층형 스토리지를 사용하는 경우에도 로컬 디스크 공간이 소진될 수 있습니다. 사용 사례에 맞게 메시지 보존 속성을 적절히 구성하면 이러한 상황을 방지하는 데 도움이 됩니다.

보존 속성은 메시지가 삭제되거나 압축되기 전에 디스크에 보관되는 최소 기간을 제어합니다. 메시지 보존 속성을 설정하는 것이 디스크가 꽉 찰 정도로 오래된 메시지가 디스크에 쌓이는 것을 방지하는 가장 좋은 방법입니다. 다음 조건에 따라 메시지를 삭제하도록 보존 속성을 구성할 수 있습니다:

- 메시지 보관 기간이 초과되었습니다.

- 토픽의 총 메시지 크기가 초과되었습니다.

- 메시지 연한과 집계 크기의 조합으로, 둘 중 하나가 초과되면 트리거됩니다.

보존 속성은 주제 수준 또는 클러스터 수준에서 설정할 수 있습니다. 주제에 대해 값을 지정하지 않으면 주제는 클러스터의 값을 사용합니다. 클러스터 수준 속성 이름은 대/소문자를 구분하는 반면, 주제 수준 속성은 점을 구분합니다.

보존 정책은 클러스터 또는 토픽 수준에서 설정되지만 토픽의 각 파티션에 독립적으로 적용됩니다. 파티션 내에서는 닫힌 세그먼트만 삭제 또는 압축할 수 있습니다. 시간 기반 정책을 설정하면 세그먼트 내의 모든 메시지가 설정된 제한을 초과해야 합니다. 예를 들어, 한 토픽의 retention.ms가 300,000ms(5분)라고 가정합니다. 세그먼트.ms가 1,800,000ms(30분)인 경우 메시지가 포함된 세그먼트가 열려 있는 동안 메시지는 최소 30분 동안 유지됩니다. 이 시나리오에서는 새 세그먼트가 시작된 후 5분이 지나면 보존 정책에 따라 닫힌 세그먼트가 삭제됩니다.

객체 저장소에서 데이터는 retention.ms 및 retention.bytes에 따라 만료됩니다. 예를 들어 retention.bytes가 10기가바이트로 설정되어 있으면 토픽의 모든 파티션에 10기가바이트의 스토리지 제한이 적용됩니다. 개체 스토리지의 데이터로 인해 retention.bytes가 초과되면 retention.ms가 아직 초과되지 않았더라도 개체 스토리지의 데이터가 잘립니다. 계층형 스토리지를 활성화한 경우, 데이터는 retention.local.target.ms 또는 retention.local.target.bytes에 따라 로컬 스토리지에서 만료됩니다.

보존 정책은 닫힌 세그먼트를 삭제하거나 압축하는 방식으로 작동합니다. 세그먼트 수명 및 세그먼트 크기 구성은 각 파티션 내에서 새 세그먼트가 정기적으로 생성되도록 하는 데 도움이 됩니다. 이 그림은 Redpanda가 크기와 시간에 따라 새 세그먼트를 생성하는 방법을 보여줍니다. 크기 기반이든 시간 기반이든 세그먼트의 제한에 도달하면 Redpanda는 세그먼트를 닫고 새 세그먼트를 채우기 시작합니다. 제한을 너무 높게 설정하면 세그먼트가 닫히기 전에 사용 가능한 디스크 공간을 모두 채우므로 삭제 또는 압축이 불가능할 수 있습니다. 값을 너무 낮게 설정하면 파티션에 삭제 또는 압축 프로세스가 실행될 때마다 확인해야 하는 세그먼트 수가 많아져 시스템 리소스 사용률에 악영향을 미칠 수 있습니다.

크기 기반 보존 정책과 시간 기반 보존 정책이 동시에 적용됩니다. 크기 기반 속성이 시간 기반 속성을 재정의하거나 그 반대의 경우도 가능합니다. 예를 들어 크기 기반 속성에서 세그먼트 하나를 제거해야 하고 시간 기반 속성에서 세그먼트 세 개를 제거해야 하는 경우 세그먼트 세 개가 제거됩니다. 크기 기반 속성은 한도를 초과하지 않고 최대한 최대 크기에 가깝게 디스크 공간을 확보합니다.

Redpanda는 이러한 정책 설정을 적용하기 위해 백그라운드에서 로그 정리 프로세스를 실행합니다. 디스크 공간이 부족해지기 시작하면 보존 속성을 조정하면 디스크 공간 사용량을 줄일 수 있습니다.

### Set time-based retention
메시지가 로그_보존기간(클러스터 수준 속성) 또는 retention.ms(토픽 수준 속성)에 지정된 값을 초과하면 삭제할 수 있습니다. 닫힌 세그먼트만 삭제할 수 있으며 닫힌 세그먼트의 모든 메시지가 보관 기간 제한을 초과해야 Redpanda가 세그먼트를 정리 대상으로 간주합니다. retention.ms가 토픽 수준에서 설정되지 않은 경우, 토픽은 log_retention_ms 설정을 상속합니다.

기본적으로 시간 기반 보존은 각 메시지의 브로커_타임스탬프 필드를 기반으로 합니다. 이 타임스탬프는 메시지를 처음 수신할 때 브로커에 의해 채워집니다. 각 세그먼트는 해당 세그먼트에 포함된 최대 브로커 타임스탬프를 세그먼트 인덱스의 배치 타임스탬프로 추적합니다. 세그먼트는 파티션 리더십이 변경되거나 세그먼트 크기 제한에 도달하면 닫힙니다. 닫힌 세그먼트는 시스템 시간과 배치 타임스탬프의 차이가 구성된 보존 시간을 초과하면 삭제됩니다.

단일 토픽에 대한 보존 시간을 설정하려면 log_retention_ms를 재정의하는 retention.ms를 사용합니다.

- retention.ms - 메시지가 삭제되기 전에 디스크에 보관되는 기간을 지정하는 토픽 수준 속성입니다.

    디스크 오류 가능성을 최소화하려면 retention.ms를 하루인 86400000 로 설정하세요. 기본값은 없습니다.

    개별 주제에 대해 retention.ms를 설정하려면 다음과 같이 하세요: `rpk topic alter-config <topic> --set retention.ms=<retention_time>`

- log_retention_ms - 메시지가 삭제되기 전에 디스크에 보관되는 기간을 지정하는 클러스터 수준 속성입니다.

    디스크 부족으로 인한 중단 가능성을 최소화하려면 log_retention_ms를 하루인 86400000 로 설정하세요. 기본값은 604800000, 즉 1주일입니다.

계층형 스토리지와 함께 원격 쓰기를 사용하여 세그먼트를 오브젝트 스토리지에 업로드하는 경우가 아니라면 log_retention_ms를 -1로 설정하지 마세요. 이 값을 -1로 설정하면 디스크 공간을 가득 채울 수 있는 무기한 보존이 구성됩니다.

### Set size-based retention
메시지가 포함된 파티션의 저장소 크기가 retention_bytes(클러스터 수준 속성) 또는 retention.bytes(토픽 수준 속성)에 지정된 값을 초과하면 메시지를 삭제할 수 있습니다. retention.bytes가 토픽 수준에서 설정되지 않은 경우 토픽은 retention_bytes 설정을 상속합니다. 세그먼트는 파티션이 지정된 크기 제한 이하로 돌아올 때까지 시간 순서대로 삭제됩니다.

- retention.bytes - 파티션의 최대 크기를 지정하는 토픽 수준 속성입니다. 기본값은 없습니다.

    retention.bytes를 설정하려면 다음과 같이 하세요: `rpk topic alter-config <topic> --set retention.bytes=<retention_size>`

- retention_bytes - 파티션의 최대 크기를 지정하는 클러스터 수준 속성입니다.

    디스크 용량보다 작은 값으로 설정하거나 주제당 파티션 수에 따라 디스크 용량의 일부로 설정합니다. 예를 들어, 파티션이 1개인 경우 retention_bytes는 디스크 크기의 80%가 될 수 있습니다. 파티션이 10개인 경우에는 디스크 크기의 80%를 10으로 나눈 값일 수 있습니다. 기본값은 null이며, 이는 토픽 크기에 따른 보존이 비활성화됨을 의미합니다.

    retention_bytes를 설정하려면 다음과 같이 하세요: `rpk cluster config set retention_bytes <retention_size>`

## Configure offset retention
레드판다는 정기적인 오프셋 만료와 카프카 오프셋 삭제 API를 통해 소비자 그룹 오프셋 유지를 지원합니다.

정기 오프셋 만료의 경우, 소비자 그룹 오프셋의 보존 기간과 확인 기간을 설정합니다. Redpanda는 만료된 오프셋을 식별하고 이를 제거하여 스토리지를 회수합니다. 소비자 그룹의 경우, 모든 소비자를 잃어서 그룹이 비어있는 시점부터 보존 시간 제한이 시작됩니다. 독립형 소비자의 경우, 보존 타임아웃은 마지막 커밋 시점부터 시작됩니다. 이 시간이 경과하면 오프셋은 만료된 것으로 간주되어 삭제됩니다.

레드판다는 rpk 그룹 오프셋 삭제 명령어를 통해 카프카 오프셋 삭제 API로 그룹 오프셋 삭제를 지원합니다. 오프셋 삭제 API는 소비자 오프셋 컬링을 보다 세밀하게 제어할 수 있습니다. 예를 들어, __consumer_groups 주제 내에서 Redpanda가 추적하는 오프셋을 수동으로 제거할 수 있습니다. 제거가 요청된 오프셋은 해당 그룹이 데드 상태이거나 삭제되는 파티션에 활성 구독이 없는 경우에만 제거됩니다.

## Configure segment size
log_segment_size 속성은 파티션 내 각 로그 세그먼트의 크기를 지정합니다. 이 크기를 초과하고 메시지가 새 세그먼트를 채우기 시작하면 Redpanda는 세그먼트를 닫습니다.

log_segment_size를 설정합니다: `rpk cluster config set log_segment_size <segment_size>`

어떤 주제에 더 많은 데이터를 받을지 알고 있다면 각 주제의 크기를 지정하는 것이 가장 좋습니다.

토픽의 로그 세그먼트 크기를 구성하려면 다음과 같이 하세요: `rpk topic alter-config <topic> --set segment.bytes=<segment_size>`

### Segment size for compacted topics

압축 또는 키 기반 보존은 토픽 파티션의 로그 내에서 메시지 키에 대해 최소한 가장 최근의 값을 유지하고 오래된 값은 삭제하여 공간을 절약합니다. 압축은 백그라운드에서 최선을 다하는 방식으로 주기적으로 실행되며, 키당 중복된 값이 없다는 것을 보장하지는 않습니다.

압축이 구성되면 토픽은 compacted_log_segment_size에서 크기를 가져옵니다. 압축된 토픽에는 log_segment_size 속성이 적용되지 않습니다.

압축이 실행되면 하나 이상의 세그먼트가 하나의 새로운 압축 세그먼트로 병합됩니다. 이전 세그먼트는 삭제됩니다. 초기 세그먼트의 크기는 segment.bytes에 의해 제어됩니다. max_compacted_log_segment_size 속성은 병합되는 세그먼트 수를 제어합니다. 예를 들어 segment.bytes를 128MB로 설정하고 max_compacted_log_segment_size를 5GB로 두면, 새 세그먼트는 128MB이지만 병합된 세그먼트는 압축 후 최대 5GB까지 커질 수 있습니다.

Redpanda는 백그라운드에서 주기적으로 압축을 수행합니다. 압축 주기는 클러스터 속성 log_compaction_interval_ms로 구성됩니다.

매우 큰 세그먼트는 압축을 지연시키거나 압축을 방해할 수 있다는 점에 유의하세요. 매우 큰 활성 세그먼트는 닫힐 때까지 정리하거나 압축할 수 없으며, 매우 큰 닫힌 세그먼트는 압축을 위해 처리하는 데 상당한 메모리와 CPU가 필요합니다. 매우 작은 세그먼트는 압축 및 리소스 제한을 적용하기 위한 처리 빈도를 증가시킵니다. 세그먼트 크기의 상한을 계산하려면 디스크 크기를 파티션 수로 나눕니다. 예를 들어 128GB 디스크와 1000개의 파티션이 있는 경우 세그먼트 크기 상한은 134217728 입니다. 기본값은 1073741824 입니다.

### Log rolling
토픽에 대한 데이터 쓰기는 일반적으로 여러 로그 세그먼트에 걸쳐 이루어집니다. 토픽의 활성 세그먼트는 기록 중인 로그 세그먼트를 말합니다. 토픽의 데이터가 쓰여지고 활성 세그먼트가 가득 차면(log_segment_size에 도달하면) 해당 세그먼트가 닫히고 읽기 전용 모드로 변경됩니다. 새 세그먼트가 생성되고 읽기-쓰기 모드로 설정되면 이 세그먼트가 활성 세그먼트가 됩니다. 로그 롤링은 새로운 활성 세그먼트를 생성하기 위해 세그먼트 간을 순환하는 것입니다.

구성 가능한 타임아웃으로 로그 롤링을 트리거할 수도 있습니다. 이는 알려진 고정 기간 내에 토픽 보존 제한을 적용할 때 유용합니다. 로그 롤링 타임아웃은 활성 세그먼트에 대한 첫 번째 쓰기부터 시작됩니다. 세그먼트가 가득 차기 전에 타임아웃이 경과하면 세그먼트가 롤링됩니다. 시간 제한은 클러스터 수준 및 토픽 수준 속성으로 구성됩니다:

- log_segment_ms(또는 log.roll.ms)는 클러스터의 모든 토픽에 대한 기본 세그먼트 롤링 시간 제한을 구성하는 클러스터 속성입니다.

    클러스터의 모든 토픽에 대해 밀리초 단위의 기간 동안 log_segment_ms를 설정하려면 다음과 같이 하세요: `rpk cluster config set log_segment_ms <segment_ms_duration>`

- segment.ms는 하나의 토픽에 대한 기본 세그먼트 롤링 시간 초과를 구성하는 토픽 수준 속성입니다. 기본적으로 설정되어 있지 않습니다. 설정하면 log_segment_ms를 재정의합니다.

    토픽에 대해 segment.ms를 설정하려면 다음과 같이 하세요: `rpk topic alter-config <topic> --set segment.ms=<segment_ms_duration>`

## Space management
Redpanda는 디스크 스토리지를 여러 카테고리로 나누어 공간을 유연하게 구성할 수 있습니다:

- 예약된 디스크 공간(디스크_예약_퍼센트): 이 오버헤드 예약은 Redpanda가 사용하지 않는 디스크 공간입니다.

    - 캐시 스토리지와 로그 스토리지가 사용하는 디스크 공간이 목표 크기로 확장됨에 따라 디스크 여유 공간 경고를 피할 수 있는 버퍼 공간을 제공합니다.

    - 용량에 가깝게 실행되는 SSD는 성능 저하를 경험할 수 있으므로, 이는 장치가 용량으로 실행되는 것을 방지하기 위해 버퍼 공간을 제공합니다.

- 캐시 스토리지(cloud_storage_cache_size_percent 또는 cloud_storage_cache_size): 계층형 스토리지가 활성화된 경우 사용되는 디스크 캐시의 최대 크기입니다. 캐시가 한계에 도달하면 캐시에 새 데이터가 추가되면 캐시에서 이전 데이터가 제거됩니다.

- 로그 저장소(retention_local_target_capacity_percent 또는 retention_local_target_capacity_bytes): 이 로그 데이터 예약은 사용자 데이터와 제어 로그와 같은 Redpanda 내부 주제에 대한 목표 최대 크기로 사용되는 디스크 공간입니다. 일반적으로 전체 디스크 공간의 70~80% 정도입니다.

로그 데이터 사용량이 로그 스토리지의 목표 크기에 근접하기 시작하면 클러스터 수준 및 토픽 수준 보존 설정을 따르는 퇴거 정책에 따라 로컬 디스크에서 데이터가 제거됩니다. 로그 데이터 사용량이 구성된 목표 크기를 초과하면 Redpanda는 제거할 데이터를 선택하여 사용량을 목표 크기 미만으로 되돌립니다. Redpanda는 세그먼트를 제거할 수 있는 파티션에서 세그먼트를 한 번에 한 번씩 라운드 로빈으로 제거하여 공정성을 유지하려고 시도합니다. 데이터 제거는 각 단계에서 이루어집니다. 스토리지 사용량이 목표 이하로 떨어지면 데이터 제거 프로세스가 종료됩니다.

### Phases of data removal

#### 1: Follow retention policy

Redpanda의 정기적인 관리 작업은 압축을 수행하고 보존 정책에 따라 만료된 데이터를 제거합니다. 이 프로세스는 계층형 스토리지와 비계층형 스토리지 주제 모두에 적용됩니다. 목표 크기에 도달하면 Redpanda는 압축보다 만료된 데이터 제거를 선호하며, 가장 많은 양의 데이터를 제거하는 순서대로 파티션에 보존을 적용하려고 시도합니다.

- retention_local_strict가 false(기본값)인 경우, 하우스키핑 프로세스는 구성된 소모성 보존을 초과하는 데이터를 제거합니다. 즉, 데이터 사용량이 로그 데이터 예약을 더 많이 차지하도록 확장할 수 있습니다.

- retention_local_strict가 true인 경우, 하우스키핑 프로세스는 로컬 보존 설정을 사용하여 제거할 데이터를 선택합니다.

#### 2: Trim to local retention
이 단계에서는 토픽에 적용된 명시적 로컬 보존 설정과 계층형 스토리지 토픽에 적용된 기본 로컬 보존 설정을 포함하여 유효 로컬 보존 정책을 초과한 데이터를 제거합니다. 기본 로컬 보존은 명시적인 주제 수준 재정의가 없는 모든 파티션에 할당된 로컬 보존입니다.

- retention_local_strict가 거짓(기본값)인 경우, 이전 단계에서 로컬 보존 정책이 충족되었으므로 Redpanda는 추가 데이터를 제거하지 않습니다.

- retention_local_strict가 참이면 Redpanda는 각 토픽이 로컬 보존에 도달할 때까지 모든 토픽에서 데이터를 공정하게 제거합니다.

이 단계가 끝나면 모든 파티션은 효과적인 로컬 보존을 반영하는 크기로 작동해야 합니다. 다음 단계에서는 더 많은 데이터를 제거하기 위해 로컬 보존 설정을 재정의하기 시작합니다.

#### 3: Trim data with default local retention settings
기본 로컬 보존 설정이 있는 주제의 경우, 이 단계에서는 데이터를 낮은 공간 수준까지 제거합니다.

낮은 공간 수준은 파티션 작업을 위한 최소한의 공간을 제공하는 구성된 크기(두 개의 세그먼트)입니다. Redpanda는 클라우드에 안전하게 보관된 데이터만 트리밍을 고려합니다.

#### 4: Trim data with explicitly-configured retention settings
명시적으로 보존 설정이 구성된 주제의 경우, 이 단계에서는 데이터를 낮은 공간 수준까지 제거합니다.

#### 5: Trim to active (latest) segment
이 단계에서는 모든 토픽이 마지막 활성 세그먼트까지 잘립니다. (활성 세그먼트의 데이터는 제거할 수 없습니다.) 데이터가 최대 크기에 도달하거나 세그먼트.ms 시간이 만료될 때까지 활성 세그먼트에서 데이터를 회수할 수 없습니다.

## Monitor disk space
메트릭을 확인하여 총 디스크 크기와 여유 공간을 확인할 수 있습니다:

- redpanda_storage_disk_total_bytes

- REDPANDA_STORAGE_DISK_FREE_BYTE

레드팬더는 디스크 공간을 모니터링하고 전체 디스크 경고 임계값에 따라 이러한 메트릭과 스토리지_공간_경고 상태를 업데이트합니다. redpanda_storage_disk_free_space_alert 메트릭으로 경고 상태를 확인할 수 있습니다. 경고 값은 다음과 같습니다:

- 0 = 경고 없음

- 1 = 여유 공간 부족 경고

- 2 = 공간 부족(성능 저하, 외부 쓰기 거부)

## Set free disk space alert
최소 디스크 여유 공간 알림에 대한 소프트 제한을 설정할 수 있습니다. 이 소프트 제한은 오류 메시지를 생성하고 redpanda_storage_disk_free_space_alert 메트릭의 값에 영향을 줍니다. 이 경고는 다음 구성 속성과 함께 작동하며, 모든 데이터 디스크(노드당 하나의 드라이브)에 설정할 수 있습니다:

알림 임계값은 바이트 또는 전체 공간의 백분율로 설정할 수 있습니다. 한 임계값을 비활성화하고 다른 임계값을 사용하려면 0으로 설정합니다.

디스크가 설정된 임계값을 초과하면 redpanda_storage_disk_free_space_alert가 업데이트되고 오류 메시지가 Redpanda 서비스 로그에 기록됩니다.

## Handle full disks
디스크 공간 부족 임계값을 초과하면 Redpanda는 클라이언트가 생성하지 못하도록 차단합니다. 이 상태에서 Redpanda는 외부 작성자에게 오류를 반환하지만, 복제 및 리밸런싱과 같은 내부 쓰기 트래픽은 계속 허용합니다.

이 쓰기 거부에 대한 디스크 공간 임계값(하드 제한)을 설정하는 조정 가능한 구성 속성인 storage_min_free_bytes는 이 쓰기 거부에 대한 낮은 디스크 공간 임계값을 설정합니다. 기본값은 5기가바이트이며, 이는 브로커의 여유 공간이 5기가바이트 미만으로 떨어지면 Redpanda가 모든 브로커에 대한 쓰기를 거부한다는 의미입니다.

## Create a ballast file
밸러스트 파일은 디스크 공간을 차지하는 빈 파일입니다. Redpanda의 디스크 공간이 부족하여 사용할 수 없는 경우, 최후의 수단으로 밸러스트 파일을 삭제할 수 있습니다. 이렇게 하면 일부 공간이 확보되어 주제나 레코드를 삭제하고 보존 속성을 변경할 수 있는 시간을 확보할 수 있습니다.

밸러스트 파일을 만들려면 redpanda.yaml 파일의 rpk 섹션에서 다음 속성을 설정하세요:

```yaml
rpk:
  tune_ballast_file: true
  ballast_file_path: "/var/lib/redpanda/data/ballast"
  ballast_file_size: "1GiB"
```

rpk를 실행하여 밸러스트 파일을 생성합니다: `rpk redpanda tune ballast_file`