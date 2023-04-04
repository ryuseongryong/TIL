- https://github.com/kubernetes-sigs/descheduler

# Descheduler for Kubernetes

쿠버네티스 스케줄링은 보류 중인 파드를 노드에 바인딩하는 프로세스이며, 쿠버네티스의 구성 요소인 kube-scheduler에 의해 수행된다. 스케줄러의 결정은 파드를 스케줄링 할 수 있는지 또는 스케줄링할 수 없는지 여부에 대한 구성 가능한 정책에 따라 이루어지며, 이는 predicates와 priorities라고 하는 rules set으로 구성된다. 스케줄러의 결정은 스케줄링을 위해 새 파드가 나타나는 시점의 쿠버네티스 클러스터에 대한 view에 영향을 받는다. 쿠버네티스 클러스터는 매우 동적이며 시간이 지남에 따라 상태가 변하기 때문에, 여러 가지 이유로 이미 실행 중인 파드를 다른 노드로 이동하고 싶을 수 있다.

`여러가지 이유`
- 일부 노드의 사용량이 부족하거나 과도하게 사용되는 경우
- 노드에 taint(노드가 파드를 제외시키는 정책) 또는 레이블이 추가되거나 노드에서 제거되고, 파드/노드 affinity 요구사항이 더 이상 충족되지 않아, 원래의 스케줄링 결정이 더 이상 유효하지 않는 경우
- 일부 노드가 실패하여 해당 파드가 다른 노드로 이동하는 경우
- 클러스터에 새 노드가 추가되는 경우

따라서 클러스터에서 원하지 않는 노드에 여러 개의 파드가 스케줄링되어 있을 수 있다. 디스케줄러는 정책에 따라 이동할 수 있는 파드를 찾아서 evict한다. 현재 구현에서 디스케줄러는 evicted 파드의 교체일정을 예약하지 않고 기본 스케줄러에 의존한다는 점에 유의하라.

## Quick Start
스케줄러는 쿠버네티스 클러스터 내에서 Job, CronJob, Deployment로 실행할 수 있다. 사용자 개입 없이 여러 번 실행할 수 있다는 장점이 있다. 스케줄러 파드는 자체적 또는 kubelet에 의해 evict 되지 않도록 하기 위해 kube-system 네임스페이스 내에서 critical 파드로 실행된다.

## User Guide

### Policy, Default Evictor and Strategy plugins
스케줄러 정책은 구성할 수 있으며 활성화 또는 비활성화할 수 있는 기본 전략 플러그인이 포함되어 있다. 여기에는 최상위 레벨의 일반적인 eviction 구성과 evictor plugin(별도 지정하지 않은 경우 기본 evictor). 최상위 수준 구성과 evictor plugin 구성은 모든 eviction에 적용됨.

### Top Level configuration
- nodeSelector
- maxNoOfPodsToEvictPerNode
- maxNoOfPodsToEvictPerNamespace

### Evictor Plugin configuration (Default Evictor)
디폴트 Evictor Plugin은 기본적으로 전략 플러그인에서 처리하기 전에 파드를 필터링하거나 evict하기 전에 파드를 PreEvictionFilter를 적용하는 데 사용됨. 자신만의 Evictor 플러그인을 생성하거나 디스케줄러에서 제공하는 기본 플러그인을 사용할 수도 있음. 다른 기준별로 파드를 정렬, 필터링, 유효성 검사, 그룹화 할 수 있고, 이것이 바로 최상위 구성에서 구성하지 않고 플러그인에서 처리하는 이유이다.
- nodeSelector
- evictLocalStoragePods
- evictSystemCriticalPods
- ignorePvcPods
- evictFailedBarePods
- labelSelector
- priorityThreshold
- nodeFit