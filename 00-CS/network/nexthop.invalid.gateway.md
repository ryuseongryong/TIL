- https://access.redhat.com/solutions/7001170

# Why unable to add gateway using ip route shows Error: Nexthop has invalid gateway.

```
$ sudo ip route add 192.168.1.0/24 via 192.168.1.1 dev eno1
Error: Nexthop has invalid gateway.
```
### 해결법
- 네트워크 인터페이스의 IP 주소와 서브넷 마스크를 확인하고 게이트웨이 IP 주소가 동일한 서브넷 내에 있는지 확인합니다. 자세한 내용은 진단 단계를 참조하세요.
### 핵심 원인
- 다른 네트워크에서 게이트웨이를 추가하면 호스트에서 게이트웨이 주소에 연결할 수 없기 때문에 실패합니다. 따라서 iproute 명령을 사용하여 경로를 생성하는 동안 "넥스톱에 잘못된 게이트웨이가 있습니다."라는 오류가 발생합니다.
