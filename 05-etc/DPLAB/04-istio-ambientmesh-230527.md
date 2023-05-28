# Istio AmbientMesh(발표자:haruband)
- https://medium.com/dataplatform-lab/k8s-istio-ambient-mesh-%EC%86%8C%EA%B0%9C-18cb17c2add4
- https://medium.com/dataplatform-lab/k8s-istio-ambientmesh-%EB%8F%99%EC%9E%91-%EA%B3%BC%EC%A0%95-%EB%B6%84%EC%84%9D-9c8975f3bd2a

## 기존방식(Sidecar Injection)
- 모든 파드에 컨테이너가 삽입되는 방식
    - 정확한 자원 사용량 예측 불가
    - 불필요한 자원 사용량 증가
- 모든 파드에 대한 정책을 유지하는 방식
    - 트래픽 관련 정책은 출발지 파드의 프록시에서 처리
    - 보안 관련 정책은 목적짖 파드의 프록시에서 처리
    - 다양한 문제 발생
        - 확장성 
            -> 모든 파드에서 전체 정책을 갖고 있어야 함
            -> 쿠버네티스 API server가 관리해야하는 것이 스케일이 커지면 로드가 커진다.
        - 보안성
        - 디버깅 -> 출발지 파드, 목적지 파드의 컨테이너에 대한 디버깅 시작점이 다르다.
- 기존에 서비스 mesh를 쓰겠다면 무조건 envoy container L7을 거쳐서 통신

## 개선방식(AmbientMesh)
- 오버레이 네트워크(Ztunnel)
    - L4 정책 처리
    - 터널링(HBONE on HTTP/2 Connect)
        - 웹소켓 개발에서 사용하는 것과 같음
    - ambientmesh를 위해 개발됨
    - 기존 envoy container L7을 무조건 거치는 것을 개선
    - L4 수준의 정책은 ztunnel에서 처리하고자 함
    - daemonset으로 노드별 설치 가능
    - ebpf사용, rust로 작성
    - 정책 처리 부분이 아직 개발중
- 네임스페이스 프록시(Waypoint)
    - L7 정책 처리(envoy)
- 노드간 통신이 증가한다는 단점(waypoint를 거치면서 2 hop이 증가)
- namespace별로 node에 하나씩 설치(daemonset)하여 해결할 수 있을 것

## Netfilter vs eBPF
- packet filter를 위한 byte code를 extended 한 것
- kernal에 코드를 넣을려면 모듈을 개발하는 것 밖에 없었음
- 꼭 커널 커뮤니티 검증이 필요하지 않는 방법이라 선호됨
- image(https://commons.wikimedia.org/wiki/File:Netfilter-packet-flow.svg)
- network traffic, security에서 많이 사용
- trace point, kernal에 포함된 함수를 실행하기 전, 후에 ebpf코드를 넣어서 진행할 수 있음, hooking trance point관련
- eBPF로 traffic 제어가 가능함
- eBPF byte code가 나오는 것을 생각하면 됨. x86, ARM 역할
- 양쪽 끝을 주로 수정해서 사용할 수 있음
- 왜 eBPF를 좋다고 하는가.
- iptable은 기본적인 kernal의 netfilter를 이용하는 것
- Netfilter linux network stack에 어떤 부분을 설정하면 NAT가능 등이 있는데, 이를 동작시키는 코드가 Netfilter. 이 무거운 것을 모두 거쳐야 했음
- eBPF는 필요한 것만 실행해서 진행할 수 있음. 제약사항이 존재함. e.g. loop가 몇 년전까지는 허용이 안 되었음.
- SKB TCP UDP header의 숫자만 바꾸면 됨. http를 eBPF로 처리하는 것은 어려움. L4정도로 사용중. 이 수준에서 traffic제어가 가능함.

## VirtualMachine vs Container
- VM
    - VMWare/KVM/Xen/Qemu
- Container
    - Namespace/CGroup

## 동작과정
- 트래픽 제어
    - 송신 패킷(pod입장에서 송신, eBPF를 삽입하기 위해서 eth0 egress or veth0 ingress)
        - ETH0 -> VETH0 ->
        - Ingress on VETH0
        - 그럼 왜 VETH0의 ingress를 만지는 것이냐? hostnetwork를 사용하기 때문에 같은 ns의 veth를 만지는 것이 수월하기 때문에(추가적인 이유는 뒤에서 설명)
        - 받고 나서 처리
    - 수신 패킷
        - -> VETH0 -> ETH0
        - Egress on VETH0
        - 보내기 전에 처리
    - VETH : pod에서 ztunnel과 통신할 때 netfilter routing을 거치지 않기 위해서 사용됨. ETH와 연결된 VETH로 바로 전달됨. 하나의 커널안에서 네임스페이스만 분리되어 있기 때문에 가능. 가상머신의 경우 IPC를 위해 RPC를 해야하기 때문에 불가능함.
- 터널링(HBONE)
    - Ztunnel <-> Waypoint
- j-pod -> n-pod로 접속하여 진행하는 것의 시나리오
    - ztunnel, ambientmesh가 없을 때는 eth0 -> veth0 -> ethX(physical) -> n-pod node의 반대순서로 진행
- 출발지, 목적지 주소 pairing, STCP port, DTCP port, IP header가 있음. S IP Addr, D IP Addr가 있음.

- eth0 -> veth0 -> ingress-A(ebpf, SKB의 ethernet dest 주소를 veth1(?의 physical ethernet주소)로 변경 + 강제로 veth1로 redirect) -> veth1 -> eth1 -> ip 주소가 다름, ingress-B(pod ns에 ebpf 삽입, ip가 내 ip가 아니기 때문에 **packet marking**을 하고 iproute table에 mark를 갖고있는 패킷의 경로를 변경, 100번으로 marking된 패킷을 local로 받으라고 설정, 그렇지 않으면 drop이 됨. router가 아니기 때문에 forwarding 설정이 안 됨. **port 번호를 변경**. 실제 ztunnel netstat을 검색하면 j-pod, n-pod가 있음)
- transparent proxy라고 함. j-pod입장에서는 목적지대로 진행하는 것인데, 중간에 껴서 진행함.
- default ns에 waypoint가 있는 경우 무조건 waypoint로 보내게 되어있음. 나중에 변경 될 수 있을 것.
- 목적지 주소가 waypoint 주소로 변경, 원래 주소는 HBONE의 http에 저장되어 있음. waypoint가 패킷을 받아서 header를 확인. waypoint가 받은 패킷의 출발지 주소는 j-pod의 주소. ztunnel에서 transparent를 지원하기 때문에 가능. waypoint는 transparent하게 동작하지 않음.
- 점선 : nginx 서비스 주소, 실선 : nginx의 pod 주소
- 수신에도 반대로 진행.
- 최종 수신 후 marking으로 bypass 처리함.

#### Q
- eth0 - veth0 IPC, MacAddress도 확인안하지만, 서로 전달할 때는 물리적 ip addr이 동일한지 확인하는 과정이 있고, 같지 않는 경우 drop함
- istio-d 에서 처리하는 부분(control plane)

### 왜 이렇게 자세히 설명하는지에 대한 이유
- 쿠버네티스는 단순히 스테이트 관리, 설정 및 정책 관리
- 실제로는 CRI, CNI에서 동작함.
- 이런 과정을 모르면 손을 쓸 수 없기 떄문에 자세한 설명을 진행함
- Cilium(CNI)와 AmbientMesh의 동작과정은 비슷해보임(Calico 등도 비슷함, eBPF network traffic 동작 과정이 비슷함)

- envoy : 트래픽 관련 처리를 위한 오픈소스, istio engress gateway, ingress gateway도 모두 envoy 기반
- ebpf : byte code. kernal 지원 byte code
        

# Rust
- trace + async 문법 오류가 나는 게 있음
    - syntax sugar가 안되어있어서 발생함(nightly에는 올라가 있는데 정식 버전에 반영이 안 되어있음)
