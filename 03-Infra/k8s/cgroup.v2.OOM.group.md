- https://www.scrivano.org/posts/2020-08-14-oom-group/

# cgroup v2 OOM group
- 컨테이너에 메모리 제한을 설정할 때 발생하는 한 가지 문제는 OOM killer kernel process가 일부 프로세스만 종료된 채로 컨테이너를 일관되지 않은 상태로 둘 수 있다는 것이다.
- 시스템 또는 cgroup의 메모리가 부족하면 OOM killer가 트리거되고 커널이 일부 메모리를 확보하려고 시도한다.
- 커널은 종료할 잠재적 프로세스, 즉 호스트의 모든 프로세스 또는 OOM이 cgroup에 로컬인 경우 cgroup에 있는 프로세스를 반복한다. 각 프로세스에 대해 badness 점수를 계산하여 가장 높은 점수를 받는 프로세스를 종료한다.
- badness heuristic은 여러 번 변경되었고, 현재 형태에서는 프로세스가 사용하는 메모리 양, 프로세스를 종료할 수 있는지 여부를 고려하고 사용자 공간에서 구성할 수 있는 값으로 점수를 조정한다.
- OOM killer는 전체 시스템의 메모리가 부족하거나 메모리 cgroup 제한이 위반되는 경우에도 비슷한 방식으로 작동한다. 차이점은 종료 대상으로 고려되는 프로세스 집합에 있다.
- cgroup이 메모리 제한에 도달하면 하나의 프로세스만 종료된다. 대부분의 경우 이 동작으로 인해 컨테이너가 일관되지 않은 상태로 남게 되며 나머지 프로세스는 계속 실행된다.
- 패치를 통해 cgroup v2에 새로운 knob가 추가됨
    ```
    commit 3d8b38eb81cac81395f6a823f6bf401b327268e6
    Author: Roman Gushchin <guro@fb.com>
    Date:   Tue Aug 21 21:53:54 2018 -0700

        mm, oom: introduce memory.oom.group

        For some workloads an intervention from the OOM killer can be painful.
        Killing a random task can bring the workload into an inconsistent state.

        ....
    ```
- `memory.oom.group`이 설정되어 있으면 전체 cgroup이 분할할 수 없는 단위로 죽는다.
- 현재 버전(2020-08-14)의 OCI 런타임 사양에는 이 설정을 지정할 수 있는 방법이 없기 때문에 OCI 컨테이너는 아직 이 기능을 활용할 수 없다.

## OCI container adoption
- 런타임 사양에 cgroup v2 지원을 추가하기 위한 논의는 아직 검토 중이다.(merge 됨 : https://github.com/opencontainers/runtime-spec/pull/1040)
- 일단 추가되면 컨테이너 런타임을 확장하여 원하는 동작이 될 때 구성을 설정할 수 있다.
- memory.oom.group 설정은 cgroup 계층 구조의 어느 수준에서나 지정할 수 있다.
- 쿠버네티스 세계에서는 컨테이너별 모드와 파드별 모드의 OOM 그룹 모드를 모두 지원할 수 있다. 컨테이너별 모드에서는 단일 컨테이너에 대한 프로세스만 OOM에서 종료된다. 대신 파드에 대해 설정이 구성된 경우, OOM 이벤트가 발생하면 프로세스를 남기지 않고 전체 파드가 종료된다.
- 두 번째 구성의 가장 큰 어려움은 일반적으로 파드 cgroup에서 실행 중인 shim 프로세스를 다른 곳으로 이동해야 하며, 그렇지 않으면 OOM 킬러 정리의 일부로 종료된다는 점이다.
