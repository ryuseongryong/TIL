- https://taisho6339.gitbook.io/grafana-loki-deep-dive/query-process/split-a-query-into-someones
# Query splitting

## Overview
쿼리 프런트엔드는 쿼리 요청을 받아 쿼리를 여러 개로 분할합니다.

쿼리를 분할하는 이유는 쿼리 병렬성을 높이고 더 많은 쿼리어를 병렬로 처리하기 때문입니다. 이를 통해 성능이 향상됩니다.

분할에는 크게 두 가지 전략이 있습니다.

- 시간 범위로 분할

- 샤드 번호로 분할

## Split by time range
이 설정은 "split_queries_by_interval" 파라미터로 설정할 수 있습니다.

이 매개변수가 15m라고 가정하면 쿼리가 15m 단위로 분할된다는 뜻입니다.

예를 들어, 한 시간 동안 로그를 검색하는 쿼리는 이 매개변수로 인해 4개의 쿼리로 분할됩니다.

이것이 바로 쿼리를 병렬로 처리하는 방법입니다.

## Split by shard number
쿼리 프로세스에서 쿼리자는 반전된 인덱스를 사용하여 로그를 검색합니다.

반전된 인덱스는 수집 프로세스에서 미리 샤드 번호별로 분할됩니다.

따라서 쿼리 프로세스에서 쿼리 프론트엔드는 쿼리를 여러 개로 분할하고 각 쿼리에 자동으로 샤드 번호를 추가하여 쿼리가 여러 쿼리러에 의해 병렬로 처리되도록 합니다.

```
service=keystone, hostname=host1 ----> service=keystone, hostname=host1, shard=0_of_4
                                 ----> service=keystone, hostname=host1, shard=1_of_4
                                 ----> service=keystone, hostname=host1, shard=2_of_4
                                 ----> service=keystone, hostname=host1, shard=3_of_4
```

이는 각 쿼리에서 결정되는 일치하는 청크가 분할 전보다 적다는 것을 의미합니다.

병렬 쿼리 처리에 대한 자세한 내용은 추가 섹션을 참조하세요.

