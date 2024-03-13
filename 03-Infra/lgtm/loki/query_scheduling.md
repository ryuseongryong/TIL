- https://taisho6339.gitbook.io/grafana-loki-deep-dive/query-process/schedule-queries-to-queriers

# Query scheduling

## Overview

분할된 쿼리는 쿼리 프런트엔드에 의해 요청 대기열에 큐에 대기됩니다.

양방향 gRPC를 통해 쿼리 프런트엔드에 연결된 일부 쿼리어는 쿼리를 가져와 처리합니다.

또한 쿼리어는 일부 쿼리를 병렬로 처리할 수 있도록 각 쿼리에 대해 고루틴을 생성합니다.

쿼리가 완료되면 gRPC를 통해 쿼리 프런트엔드에 결과를 반환합니다.

대기 중인 쿼리 요청에는 올바른 인스턴스로 반환할 수 있도록 원래 쿼리 프런트엔드 주소가 있습니다.

다음은 쿼리 처리를 위한 전체 그림입니다.

1. query request 수신                -   쿼리 프론트엔드에 의해 queue에 저장
2. split by time interval           -
3. split by shard                   -
4. Enqueue                          -
5. Pull query via gRPC              -   양방향 gRPC를 통해 쿼리 프론트엔드에 연결된 일부 쿼리어는 쿼리를 가져와 처리함
6. Process each query in parallel   -   쿼리어는 일부 쿼리를 병렬로 처리할 수 있도록 각 쿼리에 대해 고루틴을 생성함
7. Return query result              -   쿼리가 완료되면 gRPC를 통해 쿼리 프론트엔드에 결과를 반환함 :: number of streams up to querier.worker-parallelism or querier.max-concurrent / number of frontend will be executed in parallel. They each retrieve a query from a queue and execute it.
8. Aggregate results                -   

결론적으로, 이 아키텍처에는 나열된 몇 가지 장점이 있습니다.

쿼리 프런트엔드별로 쿼리를 분할하면 쿼리어가 쿼리를 병렬로 처리할 수 있습니다.

쿼리 프런트엔드는 쿼리를 큐에 대기시키고 쿼리어는 큐에서 쿼리를 가져와 쿼리어가 스스로 쿼리를 처리할 시기를 결정할 수 있습니다.

이것이 쿼리러를 효율적으로 사용하는 방법입니다.

## What is query-scheduler

2.4.0 최신 버전에서는 쿼리 스케줄러가 출시되었습니다.

이것은 쿼리 프런트엔드에서 쿼리 요청 대기열을 잘라내는 구성 요소입니다.

작동 방식은 다음과 같습니다.

- Query Frontend
    HTTP Server -> Query1 / Query2 / ... :: Enqueue query request -> Get item from queue -> scheduler Worker1 / scheduler Worker2 / ... -> Query Scheduler
- Query Scheduler
    Scheduler Worker -> Enqueue via bidrectional gRPC -> gRPC Server -> Query1 / Query2
    Querier -> Fetch queue item -> gRPC Server -> Return each result


쿼리 스케줄러에는 각 요청 큐가 있습니다.

먼저 쿼리 프런트엔드에서 쿼리 요청을 수신하여 요청 대기열에 큐에 대기시킵니다.

그런 다음 요청이 쿼리 스케줄러로 전송되어 해당 쿼리 스케줄러에 큐에 대기합니다.

모든 쿼리어는 'query.worker-parallelism'에 따라 쿼리 스케줄러의 큐를 관찰하고, 쿼리 스케줄러로부터 쿼리를 받아 처리합니다.

이렇게 해서 쿼리 프론트엔드와 쿼리러 사이의 종속성이 사라졌습니다.

## Why do we need the query-scheduler?

이전 아키텍처에서는 확장에 문제가 있습니다.

각 쿼리에는 쿼리 프런트엔드에 대한 연결 수가 구성되어 있습니다.

이는 "querier.worker-parallelism" 또는 "querier.max-concurrent"로 구성됩니다.

즉, 쿼리 프런트엔드는 이 매개변수보다 더 많이 확장할 수 없습니다.

그러나 쿼리 스케줄러가 포함된 새로운 아키텍처에서는 쿼리어에 관계없이 쿼리 프런트엔드를 확장할 수 있습니다.

쿼리 프런트엔드는 더 이상 쿼리어에 의존하지 않습니다.

