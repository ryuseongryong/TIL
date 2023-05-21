# Origin documentation
- https://martinheinz.dev/blog/91

# Cgroup - Deep Dive into Resource Management in Kubernetes
- 전체 k8s가 작동하기 위해서는 보이지 않는 곳에서 많은 '마법'이 일어난다. 그 중 하나는 리눅스 C그룹에 의해 수행되는 리소스 관리 및 리소스 할당이다.
- 이 글에서는 cgroup이 무엇이고 k8s가 노드 리소스를 관리하기 위해 어떻게 사용하는지, 그리고 파드에 리소스 요청과 제한을 설정하는 것 이상으로 이를 활용하는 방법에 대해 자세히 살펴본다.

## What are Cgroups?
- 컨트롤 그룹(줄여서 cgroups이라고 함)은 리소스 할당(CPU 시간, 메모리, 네트워크 대역폭, I/O), 우선순위 지정 및 계정(컨테이너가 얼마나 많이 사용하고 있는가?)을 처리하는 Linux 커널이다. 또한 cgroups은 Linux의 기본 요소이고, 컨테이너의 구성 요소이기도 하므로 cgroups이 없으면 컨테이너도 존재할 수 없다.
- 이름에서 알 수 있듯이 cgroups은 그룹이므로 부모-자식 계층 구조로 프로세스를 그룹화하여 트리를 형성한다. 따라서 예를 들어 부모 cgroup에 128Mi의 RAM이 할당된 경우 모든 자식 RAM 사용량 합계는 128Mi를 초과할 수 없다.
- 이 계층 구조는 cgroup 파일 시스템(cgroupfs)인 `/sys/fs/cgroup/`에 있다. 여기에는 모든 Linux 프로세스에 대한 하위 트리가 있다. 여기서는 k8s 파드에 assigned(변수/메모리 등에 값을 저장하는 것)/allocated(특정 목적을 위해 메모리/리소스 블록을 설정, 예약하는 것)된 스케줄링과 리소스에 cgroup이 어떤 영향을 미치는지에 관심이 있으므로 우리가 관심 있는 부분은 `kubepods.slice/` 이다.

```
/sys/fs/cgroup/
└── kubepods.slice/
    ├── kubepods-besteffort.slice/
    │   └── ...
    ├── kubepods-guaranteed.slice/
    │   └── ...
    └── kubepods-burstable.slice/
        └── kubepods-burstable-pod<SOME_ID>.slice/
            ├── crio-<CONTAINER_ONE_ID>.scope/
            │   ├── cpu.weight
            │   ├── cpu.max
            │   ├── memory.min
            │   └── memory.max
            └── crio-<CONTAINER_TWO_ID>.scope/
                ├── cpu.weight
                ├── cpu.max
                ├── memory.min
                └── memory.max
```

- 모든 k8s cgroup은 각 QOS(서비스 품질) 유형에 대해 kubepods.slice/ 서브 디렉토리에 위치하며, 이 디렉토리에는 `kubepods-besteffort.slice/`, `kubepods-burstable.slice/` 및 `kubepods-guaranteed.slice/` 서브디렉토리가 추가로 존재한다.
- 각 레벨에는 이 그룹이 사용할 수 있는 특정 리소스의 양을 지정하는 `cpu.weight` 또는 `cpu.max`와 같은 파일이 있다. 명확하게 하기 위해, 위의 파일 트리에는 가장 깊은 수준의 파일만 표시되어 있다.
- 마지막으로 여기 트리의 잎사귀에는 각 컨테이너가 작업할 수 있는 메모리(memory.min, memory.max), CPU(cpu.weight, cpu.max) 또는 기타 리소스의 양을 설명하는 파일들이 있다. 이런 파일은 파드 메니페스트에 정의된 리소스 요청과 제한을 직접 변환한 것이다. 그러나 이 파일들을 살펴보면, 거기에서 발견할 수 있는 값들은 실제 request/limit과 관련이 없는 것처럼 보이는데 이 값은 무엇을 의미하고, 왜 그 값을 가리키는 것일까?

## How Does It Work?
- 파드 request, limit이 /sys/fs/... 의 파일로 어떻게 translated/propagated되는지 더 잘 이해하기 위해 모든 단계를 살펴보자.
- 메모리와 CPU request/limit을 포함하는 간단한 파드 정의이다.

    ```
    # kubectl apply -f pod.yaml
    apiVersion: v1
    kind: Pod
    metadata:
    labels:
        run: webserver
    name: webserver
    spec:
    containers:
    - image: nginx
        name: webserver
        resources:
        requests:
            memory: "64Mi"
            cpu: "250m"
        limits:
            memory: "128Mi"
            cpu: "500m"
    ```
- 이 파드 매니페스트를 생성/적용하면, 파드가 노드에 할당되고 노드의 kubelet은 이 파드 스펙을 가져와 컨테이너 런타임 인터페이스(CRI, container/CRIO)로 전달하여 생성될 컨테이너를 설명하는 하위 레벨 OCI JSON 스펙으로 변환한다.
    ```
    {
  "status": {
    "id": "d94159cf8228addd7a29beaa3f59794799e0f3f65e856af2cb6389704772ffee",
    "metadata": {
      "name": "webserver"
    },
    "image": {
      "image": "docker.io/library/nginx:latest"
    },
    "imageRef": "docker.io/library/nginx@sha256:ab589a3...c332a5f0a8b5e59db"
  },
  "info": {
    "runtimeSpec": {
      "hostname": "webserver",
      "linux": {
        "resources": {
          "memory": {
            "limit": 134217728,
            "swap": 134217728
          },
          "cpu": {
            "shares": 256,
            "quota": 50000,
            "period": 100000
          },
          "pids": { "limit": 0 },
          "hugepageLimits": [{ "pageSize": "2MB", "limit": 0 }],
          "unified":{
            "memory.high": "107374182",
            "memory.min": "67108864"
          }
        },
        "cgroupsPath":
          "kubepods-burstable-pod6910effd_ea14_4f76_a7de_53c333338acb.slice:crio:d94159cf8228addd7a29b...389704772ffee"
      }}}}
    ```
- 위에서 볼 수 있듯이 이 spec에는 cgroup 파일이 위치할 디렉토리인 cgroupsPath가 포함된다. 또한 이미 변환된 request, limit이 `info.runtimeSpec.linux.resources` 아래에 포함되어 있다.
- 그런 다음 이 spec은 하위 수준의 OCI 컨테이너 런타임(대부분 runc)으로 전달되며, 이 런타임은 systemd 범위 단위를 생성하는 systemd 드라이버와 통신하고 cgroupfs의 파일에 값을 설정한다.
- 먼저 systemd scope unit을 상세히 살펴보자.
    ```
    # Find the container ID:
    crictl ps
    CONTAINER      IMAGE  CREATED        STATE    NAME       ATTEMPT  POD ID         POD
    029d006435420  ...    6 minutes ago  Running  webserver  0        72d13807f0ab1  webserver

    # Find the slice and scope
    systemd-cgls --unit kubepods.slice --no-pager
    Unit kubepods.slice (/kubepods.slice):
    ├─kubepods-burstable.slice
    │ ├─kubepods-burstable-pod6910effd_ea14_4f76_a7de_53c333338acb.slice
    │ │ └─crio-029d0064354201e077d8155f2147907dfe8f18ef2ccead607273d487971df7e0.scope ...
    │ │   ├─6166 nginx: master process nginx -g daemon off;
    │ │   ├─6212 nginx: worker process
    │ │   └─6213 nginx: worker process
    │ ├─kubepods-burstable-pod3fee6bda_0ed8_40fa_95c8_deb824f6de93.slice
    │ └─ ...
    │   └─...
    │     └─...
    └─...
    └─...
        └─...
        └─...

    systemctl show --no-pager crio-029d0064354201e077d8155f2147907dfe8f18ef2ccead607273d487971df7e0.scope
    MemoryMin=0
    MemoryMin=67108864
    MemoryHigh=107374182
    MemoryMax=134217728
    MemorySwapMax=infinity
    MemoryLimit=infinity
    CPUWeight=10
    CPUQuotaPerSecUSec=500ms
    CPUQuotaPeriodUSec=100ms
    ...
    # More info https://github.com/opencontainers/runc/blob/main/docs/systemd.md
    ```
- 먼저 docker ps에 해당하는 CRI인 `crictl ps`를 사용하여 컨테이너 ID를 찾는다. 이 명령의 출력에서 우리는 파드 웹서버와 컨테이너 ID를 볼 수 있다. 그런 다음 control group 콘텐츠를 재귀적으로 표시하는 systemd-cgls를 사용한다. 출력에서 컨테이너의 ID가 `crio-029d006435420...` 인 그룹을 볼 수 있다. 마지막으로 `systemctl show --no-pager crio-029d006435420...`을 사용하여 cgroup 파일에서 값을 설정하는 데 사용된 systemd 속성을 제공한다.
- 그럼 다음 cgroups 파일 시스템 자체를 살펴보자.

    ```
    cd /sys/fs/cgroup/kubepods.slice/kubepods-burstable.slice/
    ls -l kubepods-burstable-pod6910effd_ea14_4f76_a7de_53c333338acb.slice
    ...
    -rw-r--r-- 1 root root 0 Dec  3 11:46 cpu.max
    -rw-r--r-- 1 root root 0 Dec  3 11:46 cpu.weight
    -r--r--r-- 1 root root 0 Dec  3 11:46 hugetlb.2MB.current
    -rw-r--r-- 1 root root 0 Dec  3 11:46 hugetlb.2MB.max
    -rw-r--r-- 1 root root 0 Dec  3 11:46 io.max
    -rw-r--r-- 1 root root 0 Dec  3 11:46 io.weight
    -rw-r--r-- 1 root root 0 Dec  3 11:46 memory.high
    -rw-r--r-- 1 root root 0 Dec  3 11:46 memory.low
    -rw-r--r-- 1 root root 0 Dec  3 11:46 memory.max
    -rw-r--r-- 1 root root 0 Dec  3 11:46 memory.min
    ...

    cat .../cpu.weight  # 10

    #                  $MAX  $PERIOD
    cat .../cpu.max  # 50000 100000

    cat .../memory.min  # 67108864

    cat .../memory.max  # 134217728

    ```
- systemd-cgls의 출력에 나열된 디렉토리인 `kubepods-burstable-pod6910effd_ea14_4f76_a7de_53c333338acb.slice`로 이동한다. 이것은 전체 웹 서버 파드의 cgroup 디렉토리이다. 여기서 개별 cgroup 파일을 찾는다. 우리가 주로 관심을 갖는 파일과 값은 `cpu.weight`, `cpu.max`, `memory.min`, `memory.max`인데 이는 파드의 CPU와 메모리 request/limit를 설명하는 파일들인데, 이 값들은 무엇을 의미할까?
    - `cpu.weight` : CPU request이다. 소위 weight(shares)로 변환된다. 1-10000 범위이며 다른 컨테이너와 비교하여 컨테이너가 얼마나 많은 CPU를 사용할지 설명한다. 시스템에 2개의 프로세스만 있고 하나는 2000개, 다른 하나는 8000개인 경우 전자는 CPU 사이클의 20%를, 후자는 80%를 차지한다. 이 경우 250m은 10개의 shares에 해당하므로, 450m의 CPU 요청으로 파드를 실행하면 18개의 shares를 얻게 된다.
    - `cpu.max` : CPU limit이다. 파일의 값은 그룹이 각 `$PERIOD` 기간에 최대 `$MAX`까지 사용할 수 있음을 나타낸다. 최대값은 제한이 없음을 나타낸다. 이 경우 50000/100000을 사용하므로 최대 0.5(500m) CPU를 사용한다.
    - `memory.min` : 메모리 request(byte)이다. 클러스터에서 메모리 QoS가 활성화된 경우에만 설정된다.
    - `memory.max` : 바이트 단위 메모리 사용량 hard limit이다. cgroup의 메모리 사용량이 이 제한에 도달하여 줄일 수 없는 경우, cgroup에서 OOM killer가 호출되고 컨테이너가 종료된다.
- 이 4개의 파일 외에도 많은 다른 파일들이 있지만, 현재 파드 매니페스트를 통해 설정할 수 있는 파일은 없다.
- 참고로 직접 찾아보고 싶다면 앞서 언급한 컨테이너 런타임 스펙에서 cgroupfs의 경로르 얻는 것이 이러한 값을 찾는 대안/빠른 방법일 수 있다.
    ```
    POD_ID="$(crictl pods --name webserver -q)"
    crictl inspectp -o=json $POD_ID | jq .info.runtimeSpec.linux.cgroupsPath -r
    # Output (a path to Pod's pause container):
    # kubepods-burstable-pod6910effd_..._53c333338acb.slice:crio:72d13807f0ab1a3860478d6053...745a50e5e296ddd7570e1fa9
    # Translates to
    ls -l /sys/fs/cgroup/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod6910effd_..._53c333338acb.slice/

    -rw-r--r-- 1 root root 0 Dec  3 11:46 cpu.max
    -rw-r--r-- 1 root root 0 Dec  3 11:46 cpu.weight
    -rw-r--r-- 1 root root 0 Dec  3 11:46 memory.high
    -rw-r--r-- 1 root root 0 Dec  3 11:46 memory.low
    -rw-r--r-- 1 root root 0 Dec  3 11:46 memory.max
    -rw-r--r-- 1 root root 0 Dec  3 11:46 memory.min
    ...
    ```

## Monitoring
- 리소스 할당을 강제하는 것 외에도 cgroups는 리소스 소비를 모니터링하는 데에도 사용된다. 이 작업은 kubelet에 포함된 cAdvisor 구성 요소에 의해 수행된다. cAdvisor 메트릭을 보면 cgroups 파일 값을 더 쉽게 볼 수 있다.
- cAdvisor 메트릭을 보려면 다음을 사용할 수 있다.
    ```
    # Directly on the node:
    curl -sk -X GET  "https://localhost:10250/metrics/cadvisor" \
    --key /etc/kubernetes/pki/apiserver-kubelet-client.key \
    --cacert /etc/kubernetes/pki/ca.crt \
    --cert /etc/kubernetes/pki/apiserver-kubelet-client.crt

    # Remotely using "kubectl proxy"
    kubectl proxy &
    # [1] 2933

    kubectl get nodes
    NAME        STATUS   ROLES           AGE   VERSION
    some-node   Ready    control-plane   7d    v1.25.4

    curl http://localhost:8001/api/v1/nodes/some-node/proxy/metrics/cadvisor

    ```
- 클러스터 노드에 대한 액세스 권한이 있는 경우, 위의 첫 번째 curl 명령을 사용하여 kubelet API에서 직접 메트릭을 가져올 수 있다. 또는 kubectl 프록시를 사용하여 Kubernetes API 서버에 액세스하고 경로에 있는 노드 중 하나를 지정하여 로컬에서 curl을 실행할 수 있다.
- 어떤 옵션을 사용하든, 이 샘플에서 보이는 방대한 메트릭 목록을 얻을 수 있다.
- 몇 가지 흥미로운 메트릭들이 있다.
  ```
  # Memory limit defined for that container (memory.max)
  container_spec_memory_limit_bytes{
    container="webserver",
    id="/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod691...38acb.slice/crio-d94159cf...04772ffee.scope",
    image="docker.io/library/nginx:latest",
    name="k8s_webserver_webserver_default_6910effd-ea14-4f76-a7de-53c333338acb_1",
    namespace="default",
    pod="webserver"} 1.34217728e+08

  # If the CPU limit is "500m" (500 millicores) for a container and
  # the "container_spec_cpu_period" is set to 100,000, this value will be 50,000.
  # cpu.max 1st value
  container_spec_cpu_quota{...} 50000

  # The number of microseconds that the scheduler uses as a window when limiting container processes
  # cpu.max 2nd value
  container_spec_cpu_period{...} 100000

  # CPU share of the container
  # cpu.weight
  container_spec_cpu_shares{...} 237

  ```
- 파드 매니페스트에서 cgroupfs까지 전체 propagation과 translation에 대한 최종 요약은 아래 표와 같다.

|     Pod Spec    |  Systemd           | Cgroups FS | Cadvisor Metric                    |
|-----------------|--------------------|------------|------------------------------------|
| requests.memory |	MemoryMin          | memory.max | container_spec_memory_limit_bytes  |
| limits.memory   | MemoryMax          | memory.max | container_spec_memory_limit_bytes  |
| requests.cpu    |	CPUWeight          | cpu.weight | container_spec_cpu_shares          |
| limits.cpu      |	CPUQuotaPerSecUSec | cpu.max    | container_spec_cpu_quota (_period) |

## Why should you care?
- Kubernetes의 cgroups에 대한 모든 새로운 지식을 습득하고 나면 "Linux와 Kubernetes가 모든 작업을 자동으로 처리해 주는데 왜 굳이 이것을 배워야 하는지"라는 의문이 들 수 있다.
- 그 이유는 더 깊이 이해하는 것이 항상 도움이 되고, 디버깅을 위해 이 지식이 언제든 필요할 수 있다는 것이다. 그리고 더 중요한 것은 작동 방식을 알면 몇 가지 고급 기능을 구현하고 활용할 수 있다는 것이다.
  - 예를 들어 앞에서 간략하게 언급했던 메모리 QoS가 있다. 대부분의 사람들이 이 사실을 모르지만, 쿠버네티스 v1.26 기준 파드 매니페스트의 메모리 Request는 컨테이너 런타임에 의해 고려되지 않으므로 사실상 무시된다.
  - 또한 메모리 사용량을 조절할 수 있는 방법이 없고 컨테이너가 메모리 제한에 도달하면 단순히 OOM이 종료된다. 현재 알파 버전에 있는 메모리 QoS 기능의 도입으로 쿠버네티스는 컨테이너를 바로 종료하는 대신 추가적인 cgroup 파일 `memory.min` 및 `memory.high`를 활용하여 컨테이너를 스로틀링 할 수 있다. (앞의 예제에서는 `memory.min` 값은 클러스터에서 메모리 QoS가 활성화되었기 때문에 채워져 있다.)
  - logging sidecar가 있는 파드가 메모리 사용량 제한에 도달하면 사이드카의 메모리 소비로 인해 파드의 메인 컨테이너가 종료될 수 있다. container-aware OOM killer(https://www.scrivano.org/posts/2020-08-14-oom-group/)를 사용하면 이론적으로 메모리 제한에 도달하면 사이드카가 먼저 종료되도록 파드를 구성할 수 있다.
  - cgroups 덕분에 보안에 매우 유용한 rootless모드(https://kubernetes.io/docs/tasks/administer-cluster/kubelet-in-userns/)에서 kubelet 또는 CRI와 같은 Kubernetes 구성 요소를 실행할 수 있다.
  - 마지막으로 JDK(https://bugs.openjdk.org/browse/JDK-8230305)는 사용가능한 CPU 및 메모리 양을 파악하기 위해 cgroup 파일을 살펴 보기 때문에 Java 개발자라면 cgroup에 대해 어느 정도 알고 있는 것이 좋다.

- 이것들은 빙산의 일각에 불과하다. cgroups가 우리를 도울 수 있는 더 많은 것이 있고, 향후에는 디스크 스로틀링, 네트워크 IO 또는 리소스 압력(PSI)과 같은 다른 유형의 리소스 관리를 위해 더 많은 리소스 관리 기능이 Kubernetes에 추가될 가능성이 높다.

## 나가며
- Kubernetes의 많은 것들이 마법처럼 보일 수 있지만, 자세히 살펴보면 실제로는 핵심 Linux 구성 요소와 기능을 영리하게 사용한 것일 뿐이며, 이 글에서 살펴본 것처럼 리소스 관리도 예외는 아니다.
- 클러스터 운영자와 사용자의 관점에서는 cgroups가 구현 세부 사항처럼 보일 수 있지만, 작동 방식을 이해하면 어려운 문제를 해결하거나 이전 섹션에서 설명한 것과 같은 고급 기능을 사용할 때 유용하게 사용할 수 있다.