- 240907

- Istio Ambient Mode 분석
    - 최근 공개된 베타 버전 기준으로 자세한 내용을 소개
- VM 기반의 KaaS (Kubernetes as a Service) 프로비저닝 툴 구축기

tesla linux quity(QT)

# Istio AmbientMesh
## 기존 방식(Sidecar Injection)
- 모든 파드에 컨테이너가 삽입되는 방식
    - envoy proxy 파드
- 모든 파드에 대한 정책을 유지하는 방식

## 개선 방식(AmbientMesh)
### 오버레이 네트워크(ztunnel)
- 모든 IO이 envoy를 거치게 된 것이 노드에 있는 ztunnel로 대체되었다고 볼 수 있음
    - L4까지 처리(서비스)
### 네임스페이스 프록시(waypoint)
- Waypoint는 envoy를 동일하게 사용
- L7 정책 처리(envoy)
- destination 기반 정책
- namespace별로 하나씩 설치

## 동작과정
- VETH -> 리눅스 컨테이너 구현 시 네임스페이스 - jl network과 host network는 분리(커널은 하나지만) - 물리 eth카드를 갖고 있는 것이 아니기 때문에 물리를 거치려면 host를 거쳐야하는데, 그 때 사용하는 것이 Virtual network device -> host network interface를 쓸 때는 필요없는 개념

- message queue같은 IPC 역할
- netfilter를 사용하여 linux level에서 network stack
- k8s cni network device 앞 뒤 단을 잡음
- netfilter에서 network device로 패킷을 보내기 위한 Egress callback
- Ingress callback
    - I/Egress -> netfilter 동작
    - Ingress : 들어오는 모든 패킷
    - Egress : 타켓으로 나가는 모든 패킷
- host level에서 처리(veth0 -> veth1)

- istio ebpf 가 삭제된 이유 -> EKS 등 설치가 안되는 경우 지원이 안됨
    - license issue도 있음
    - cilium은 AWS, cilium에서 미리 작업해 놓은 것
    - istio - cilium가 같이 ebpf 함수 호출 순서에 따라 문제가 발생한 경우가 있음

- 다른 ebpf를 사용하는 경우 개발자가 확인하여 사용해야 함

- mesh를 사용하는 경우가 더 빠른 게 있음
    - 분석한 글(https://thenewstack.io/ambient-mesh-can-sidecar-less-istio-make-applications-faster/)
    - https/multi-flexing + TCP NOdelay
* zero trust 관련 궁금증
- https://community.renesas.com/mcu-mpu/embedded-system-platform/f/forum/29025/difference-in-packet-size-for-http-and-https-server
- 현상, 문제정의, 가설, 검증

---
- compiler vs kernel : compiler는 계속해서 시장이 생김
- GCC vs 사용컴파일러
- JAVA runtime 최적화 JIT
- Web Assembly 최적화
    - LLVM은 runtime에 무거울 수 있음
    - 최적화 + 속도 향상 -> 새로운 compiler
- AI(model싸움 -> Runtime 싸움)
    - vLLM의 핵심 근간은 컴파일러

# k8s-tug
- VM 기반 k8s, KaaS
- kubespray 걷어내기
    - infra setting - VM image(Golden Image) -> Packer
    - k8s -> cloud-init(가상머신 최초 실행 스크립트에 join 명령어 등)
    - add-on -> helm

- EKS
    - etcd event lease (event storm) 발생 시 etcd 용량이 차면 연락이 옴
    - EKS nodeadm
    - 가상머신 이미지는 native에 안됨

---
VPC VM

MCU - 캔, 린
이더넷(SDB OS -> Bluechi, IBI OS -> AAOS, 할)
CCOS에서 전환중