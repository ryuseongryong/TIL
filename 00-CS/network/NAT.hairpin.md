# EdgeRouter의 NAT 헤어핀에 대해서

## Intro
- 일반적으로 NAT port forwarding rule은 `네트워크 밖 -> 네트워크 안`으로 hostname / 라우터의 퍼블릭 주소를 통해서 사용됨.
- 하지만 같은 로컬 네트워크 내의 로컬 서버의 주소는 더 사용하기 쉬운 NAT 헤어핀이 적용됨.
- e.g. 사용자 노트북과 mail server가 같은 로컬 네트워크에 있는 경우, 혼란을 피하기 위해 같은 네트워크 내에 있을 때나 밖에 있을 때나 같은 서버명을 사용하는 것이 더 바람직한 경우가 있는데, 이 때 사용.
- NAT hairpin은 LAN에 있는 장치가 게이트웨이 라우터의 공용 IP 주소를 통해서 LAN의 다른 컴퓨터에 액세스 할 수 있는 기능이다.

## A.K.A.
- NAT hairpin
- NAT inside-to-inside
- NAT loopback
- NAT reflection

## How to
1. DNAT 설정(외부에서 들어오는 특정 address, port에 대한 요청을 특정 address, port로 변환)
2. NAT haripin 설정

## how to by mikrotik guide
1. DNAT 설정(일반적인 경우, 응답 서버가 다른 네트워크망에 있는 경우)
    1. client req: port443, src192.168.88.1 -> port443, dst172.16.16.1
    2. router DNAT: port443, src192.168.88.1 -> port443, **dst10.0.0.3**
    3. server res: src10.0.0.3 -> dst192.168.88.1
    4. router(determines packet is part of previous connection): **src172.16.16.1** -> dst192.168.88.1
2. 웹 서버와 동일한 네트워크에 있는 클라이언트가 웹 서버의 공용 IP 주소로 연결을 요청하면 문제 발생
    1. client req: src10.0.0.2 -> dst172.16.16.1
    2. router DNAT: src10.0.0.2 -> **dst10.0.0.3**
    3. server res: src10.0.0.3 -> **_dst router LAN interface(bridge1) 10.0.0.1_**
    4. router(determines packet is part of previous connection): **_src172.16.16.1_** -> **_dst10.0.0.3_**
3. NAT hairpin 설정
    1. client req: src10.0.0.2 -> dst172.16.16.1
    2. router DNAT + hairpin NAT: **_src router LAN interface(bridge1) 10.0.0.1_** -> **dst10.0.0.3**
    3. server res: src10.0.0.3 -> **_dst router LAN interface(bridge1) 10.0.0.1_**
    4. router(determines packet is part of previous connection): **_src172.16.16.1_** -> **_dst10.0.0.3_**


## References
- https://help.ui.com/hc/en-us/articles/204952134-EdgeRouter-NAT-Hairpin-Nat-Inside-to-Inside-Loopback-Reflection-
- https://docs.buf4.com/edgemax/edgerouter-configuration/_204952134-EdgeRouter-NAT-Hairpin-Nat-Inside-to-Inside-Loopback-Reflection-.html
- https://help.mikrotik.com/docs/display/ROS/NAT#NAT-HairpinNAT
