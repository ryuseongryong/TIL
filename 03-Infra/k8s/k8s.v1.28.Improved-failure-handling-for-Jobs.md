- https://kubernetes.io/blog/2023/08/21/kubernetes-1-28-jobapi-update/

이 블로그에서는 배치 사용자의 작업을 개선하기 위한 쿠버네티스 1.28의 두 가지 새로운 기능에 대해 설명한다: 파드 교체 정책과 인덱스당 백오프 제한이다.

이 기능들은 잡에서 파드 장애 처리를 개선하기 위해 파드 장애 정책에서 시작된 노력을 이어간다.

## Pod replacement policy
기본적으로, 파드가 종료 상태에 들어가면(예: 선점 또는 퇴거로 인해) 쿠버네티스는 즉시 대체 파드를 생성한다. 따라서 두 파드가 동시에 실행된다. API 용어로, 파드가 삭제 타임스탬프가 있고 페이즈가 보류 중 또는 실행 중일 때 종료되는 것으로 간주한다.

주어진 시간에 두 개의 파드가 동시에 실행되는 시나리오는 주어진 인덱스에 대해 최대 하나의 파드만 동시에 실행해야 하는 TensorFlow 및 JAX와 같은 일부 인기 있는 머신 러닝 프레임워크에서 문제가 됩니다. 주어진 인덱스에 대해 두 개의 파드가 실행 중인 경우 Tensorflow는 다음과 같은 오류를 발생시킵니다.

``` /job:worker/task:4: Duplicate task registration with task_name=/job:worker/replica:0/task:4
```

이전 파드가 완전히 종료되기 전에 대체 파드를 생성하면 리소스가 부족하거나 예산이 부족한 클러스터에서 문제가 발생할 수도 있습니다:

- 기존 파드가 완전히 종료될 때까지 쿠버네티스가 사용 가능한 노드를 찾는 데 시간이 오래 걸릴 수 있으므로 스케줄링 대기 중인 파드에 대한 클러스터 리소스를 확보하기 어려울 수 있다.
- 클러스터 오토스케일러가 활성화된 경우, 대체 파드가 원치 않는 스케일업을 생성할 수 있다.

### How can you use it? 
이 기능은 알파 기능으로, 클러스터에서 JobPodReplacementPolicy 기능 게이트를 켜서 활성화할 수 있습니다.

클러스터에서 이 기능이 활성화되면, 여기에 표시된 것처럼 podReplacementPolicy 필드를 지정하는 새 Job을 생성하여 이 기능을 사용할 수 있습니다:

```kind: Job
metadata:
  name: new
  ...
spec:
  podReplacementPolicy: Failed
  ...
```

해당 잡에서, 파드는 종료 중이 아니라 실패 단계에 도달했을 때만 교체됩니다.

또한, 잡의 `.status.terminating` 필드를 검사할 수 있다. 이 필드의 값은 현재 종료 중인 잡이 소유한 파드의 수입니다.

```kubectl get jobs/myjob -o=jsonpath='{.items[*].status.terminating}'
```

```3 # three Pods are terminating and have not yet reached the Failed phase
```

이는 현재 종료되는 잡에서 리소스가 회수될 때까지 잡의 실행 중인 파드에서 할당량을 추적하는 Kueue와 같은 외부 큐잉 컨트롤러에 특히 유용할 수 있습니다.

참고로, 파드리플레이스먼트폴리시: Failed는 커스텀 파드 장애 정책을 사용할 때 기본값이다.

## Backoff limit per index
기본적으로, 인덱싱된 잡에 대한 파드 실패는 .spec.backoffLimit으로 표시되는 글로벌 재시도 횟수 제한에 포함된다. 즉, 지속적으로 실패하는 인덱스가 있으면 한도를 소진할 때까지 반복적으로 다시 시작된다. 제한에 도달하면 전체 작업이 실패로 표시되고 일부 인덱스는 시작조차 하지 못할 수도 있습니다.

이는 모든 인덱스에 대한 파드 장애를 독립적으로 처리하려는 사용 사례에서 문제가 된다. 예를 들어, 각 인덱스가 테스트 스위트에 해당하는 통합 테스트를 실행하기 위해 인덱싱된 작업을 사용하는 경우이다. 이 경우, 스위트당 1~2번의 재시도를 허용하는 플레이크 테스트 가능성을 고려해야 할 수 있다. 일부 버그가 있는 테스트 스위트가 있어서 해당 인덱스가 지속적으로 실패할 수 있습니다. 이 경우 버그가 있는 테스트 모음에 대한 재시도는 제한하되 다른 모음은 완료할 수 있도록 허용하는 것이 좋습니다.

이 기능을 사용하면 다음을 수행할 수 있습니다:
- 일부 인덱스가 실패하더라도 모든 인덱스의 실행을 완료할 수 있습니다.
- 지속적으로 실패하는 인덱스에 대한 불필요한 재시도를 방지하여 컴퓨팅 리소스를 더 잘 활용할 수 있습니다.

### How can you use it?
이 기능은 알파 기능으로, 클러스터에서 `JobBackoffLimitPerIndex` 기능 게이트를 켜서 활성화할 수 있습니다.

클러스터에서 이 기능이 활성화되면 `.spec.backoffLimitPerIndex` 필드를 지정하여 인덱싱된 작업을 생성할 수 있습니다.

### Example
다음 예제에서는 이 기능을 사용하여 작업이 모든 인덱스를 실행하고(`activeDeadlineSeconds` 시간 제한에 도달하거나 사용자가 수동으로 삭제하는 등 작업이 조기 종료되는 다른 이유가 없는 경우) 인덱스별로 실패 횟수를 제어하는 방법을 보여 줍니다.

```apiVersion: batch/v1
kind: Job
metadata:
  name: job-backoff-limit-per-index-execute-all
spec:
  completions: 8
  parallelism: 2
  completionMode: Indexed
  backoffLimitPerIndex: 1
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: example # this example container returns an error, and fails,
                      # when it is run as the second or third index in any Job
                      # (even after a retry)        
        image: python
        command:
        - python3
        - -c
        - |
          import os, sys, time
          id = int(os.environ.get("JOB_COMPLETION_INDEX"))
          if id == 1 or id == 2:
            sys.exit(1)
          time.sleep(1)          
```

이제 작업이 완료된 후 파드를 검사합니다:
```kubectl get pods -l job-name=job-backoff-limit-per-index-execute-all
```
이와 유사한 출력을 반환합니다:
```NAME                                              READY   STATUS      RESTARTS   AGE
job-backoff-limit-per-index-execute-all-0-b26vc   0/1     Completed   0          49s
job-backoff-limit-per-index-execute-all-1-6j5gd   0/1     Error       0          49s
job-backoff-limit-per-index-execute-all-1-6wd82   0/1     Error       0          37s
job-backoff-limit-per-index-execute-all-2-c66hg   0/1     Error       0          32s
job-backoff-limit-per-index-execute-all-2-nf982   0/1     Error       0          43s
job-backoff-limit-per-index-execute-all-3-cxmhf   0/1     Completed   0          33s
job-backoff-limit-per-index-execute-all-4-9q6kq   0/1     Completed   0          28s
job-backoff-limit-per-index-execute-all-5-z9hqf   0/1     Completed   0          28s
job-backoff-limit-per-index-execute-all-6-tbkr8   0/1     Completed   0          23s
job-backoff-limit-per-index-execute-all-7-hxjsq   0/1     Completed   0          22s
```

또한 해당 작업의 상태를 살펴볼 수도 있습니다:
```kubectl get jobs job-backoff-limit-per-index-fail-index -o yaml
```

출력은 다음과 유사한 상태로 종료됩니다:

```  status:
    completedIndexes: 0,3-7
    failedIndexes: 1,2
    succeeded: 6
    failed: 4
    conditions:
    - message: Job has failed indexes
      reason: FailedIndexes
      status: "True"
      type: Failed
```

여기서는 인덱스 1과 2가 모두 한 번씩 재시도되었습니다. 두 번째 실패 후 각 인덱스에서 지정된 `.spec.backoffLimitPerIndex`가 초과되었으므로 재시도가 중지되었습니다. 비교를 위해, 인덱스별 백오프를 비활성화한 경우, 버그가 있는 인덱스는 전역 `backoffLimit`을 초과할 때까지 재시도한 다음, 일부 상위 인덱스가 시작되기 전에 전체 작업이 실패로 표시될 것입니다.

