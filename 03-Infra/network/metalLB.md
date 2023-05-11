# MetalLB

## MetalLB with L2
- Speaker -> ARP req에 대한 res를 통해 LB 구현
    - 서비스의 endpoint(pod) -> node speaker가 ARP요청에 응답
    - 서비스의 endpoint가 2개 이상인 경우 하나의 노드에서 모든 요청 처리

```
metalLB를 설치하면 daemon 형태로 스피커가 설치돼요, daemonset이니까 모든 노드에 스피커 파드가 하나씩 설치가 돼요. L2 모드로 사용하면 어떻게 동작하냐면 스피커가 ARP request를 일종의 hijacking, intercepting을 해요. 

기본적으로 networking이 이루어지는 과정을 간단하게 요약하면, 클라이언트에서 240번으로 패킷을 보내려고 하면, 240번은 IP이다. IP networking을 위한 것이고, 실질적으로 패킷을 보내기 위해서는 MAC주소(L2주소)가 필요하다. 그러면 240번, 그러니까 같은 네트워크 대역, 우리가 IP 설정하면, 192.168.0.240을 설정하고, netmask를 설정한다. 255.255.255.0. 그래서 클라이언트와 서버가 같은 네트워크 주소 안에 있으면 서버의 MAC 주소를 알려달라는 것이 ARP 요청이다.

만약에 다른 네트워크에 있으면 라우터의 MAC 주소를 요청한다. 그래서 ARP로, default 라우터가 1번이면 1번의 MAC 주소를 알려달라고 한다. 그래서 실질적으로 패킷을 전달하는 것은 ARP 요청을 전달해서(요청을 날려서, broadcasting 해서) 응답을 해주는 놈의 MAC 주소로 패킷을 전달하는 것이다.

그래서 동작원리는 간단하다. 

K8S의 External IP는 서비스에 이미 할당 되어 있다. 

우리 같은 경우에는 IP range를 정해놓고, LB를 Static IP로 잡고 있다. 재설치할 때마다 바뀌면 안되기 때문에. 이 부분은 상황에 따라 다른 것이다.

(클라이언트가 이미 해당하는 서비스, 예를 들면 카프카 브로커 서비스에 접근하려고 하는 카프카 브로커 0번이)
클라이언트가 접근하려고 하는 kafka-broker service 0번이 노드 1번에 있다는 것을 이미 알고 있고, external IP가 240번이라는 것을 이미 알고 있으면 바로 240번으로 접근하면 된다. 그러면 같은 네트워크 대역 안에 있으니까, 240번으로 보내려고 클라이언트가 ARP request를 날릴 것이다. 그럼 240번의 MAC 주소달라는 요청을 할 것이고, MetalLB의 스피커가 노드 1번에 있는 것이 파드 3라는 것을 알고, 노드 1번에 있는 스피커가 ARP reply를 하고, 노드 1번의 MAC 주소가 클라이언트에게 전달된다. 이후 클라이언트는 노드1번의 MAC 주소로 요청을 보낼 것이다. 이렇게 동작하는 것이 L2모드이다. 말 그대로 ARP 패킷을 조작해서 우리가 원하는 목적을 달성하는 것이다. 

L2모드의 문제점은, 서비스에 파드 1개만 있는 것이 아니라, 하나의 서비스와 연결된 파드가 여러 개 설정되어 있을 것이다. 그러면 ARP request가 들어왔을 때 2~3가 동시에 reply할 수는 없다. 그래서 MetalLB L2는 2개 이상일 경우에 리더를 선출한다. 리더로 선출된 노드가 ARP reply를 한다. 문제는 리더에게만 패킷을 보내기 때문에 리더가 있는 노드를 무조건 거치게 되어있다. 따라서 네트워크 사용량이 일시적으로 증가하는 경우 트래픽을 모두 감당하지 못할 수 있다. 즉 load balancing은 되지 않는다고 볼 수 있다.
```

- 이런 문제를 해결하기 위해서 나온 것이 BGP모드.

## References
- https://metallb.universe.tf/concepts/layer2/
- https://en.wikipedia.org/wiki/Hop_(networking)
- https://medium.com/dataplatform-lab/k8s-kafka-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC-%EC%B5%9C%EC%A0%81%ED%99%94-metallb-fa59729086ea
- https://malwareanalysis.tistory.com/271