# Differences in between AWS CLB, ALB and NLB

- ALB, NLB, CLB(ELB) 사이의 차이점

## 공통 기능
- Health Checks
- 들어오는 요청들을 EC2 인스턴스 또는 도커 컨테이너가 될 수 있는 여러 대상에 배포
- 몇 분 안에 확장 또는 축소가 가능한 HA, Elastic(탄력성)
- TLS termination, 인터넷 연결과 내부 연결 사이에 전환
- 유용한 메트릭을 CloudWatch로 보내고, 관련 정보를 CloudWatch 로그에 기록할 수 있음

## CLB(ELB) 기능
- L4(TCP), L7(HTTP)에서 모두 작동
- 오래된 AWS계정이면 EC2-Classic에서만 작동
- application-defined sticky session cookies(애플리케이션 정의 스티키 세션 쿠키)를 지원하지만, ALB의 쿠키는 사용자가 제어할 수 없음
- SSL이 있는 한 TLS 트래픽을 종료하고 트래픽을 다시 암호화 할 수 있음(end-to-end 암호화는 많은 프로그램에서 요구되는 일반적인 사항)
- 추가 보안을 위해 대상에서 제공한 TLS인증서를 확인하도록 ELB를 구성할 수 있음

## CLB 단점
- Fargate에서 실행되는 EKS 컨테이너와 호환되지 않음
- 인스턴스당 하나 이상의 포트에서 트래픽을 포워딩 X
- IP 주소로 포워딩을 지원 X
- ECS 또는 EKS의 명시적 EC2 인스턴스 또는 컨테이너로만 포워딩 할 수 있음
- ELB는 웹 소켓을 지원하지 않으며, L4를 사용하여 이 제한을 해결 할 수 있음
- AWS에서는 추천하지 않지만 ELB가 필요한 시나리오
    - EC2-Classic에서 실행하는 경우
    - 자체 스티키 세션 쿠키를 사용해야 하는 경우

## ALB 기능
- 호스트 이름, 경로, 쿼리 문자열 매개변수, HTTP 매서드, HTTP 헤더, 소스 IP 또는 포트 번호를 기반으로 들어오는 요청에 대한 광범위한 라우팅 규칙이 있음. 요청을 Lambda 함수로 라우팅할 수 있음
    - ELB의 경우 포트 번호에 기반한 라우팅만 허용
- 고정 응답 또는 리디렉션을 반환하도록 구성할 수 있음
- HTTP/2 및 웹 소켓 지원
- 서버 이름 표시(SNI)를 지원하여 기본 인증서를 더한 최대 25개의 인증서로 제한하여 많은 도메인 이름을 서비스할 수 있음
    - ELB는 하나의 도메인 이름만 허용
- OIDC, SAML, LDAP, MS AD, Facebook, Google 같이 잘 알려진 소셜 ID 공급자를 포함한 다양한 방법을 통해 사용자 인증을 지원함. 애플리케이션의 사용자 인증 부분을 로드밸런서로 오프로드 하는 데 도움이 될 수 있음.

### 용도
- 일반적으로 웹 애플리케이션에 사용
- 마이크로서비스의 경우, 특정 서비스를 구현하는 EC2 또는 도커 컨테이너 앞의 내부 로드밸런서로 사용할 수 있음
- REST API를 구현하는 애플리케이션 앞에서 사용할 수 있으나 AWS API Gateway가 더 나은 선택임.

## NLB 기능
- L4에서만 작동하며 TCP, UDP는 물론 TLS를 사용한 TCP 연결을 모두 처리할 수 있음
- 매우 높은 성능
- 고정 IP 주소를 사용하며 ALB와 ELB는 할당할 수 없는 EIP를 할당할 수 있음
- NLB는 기본적으로 TCP/UDP 패킷의 소스 IP주소를 보존하지만, ALB와 ELB는 포워딩 정보가 포함된 HTTP 헤더를 추가하도록 구성할 수 있으며, 애플리케이션에서 이를 올바르게 구문 분석해야 함.

### 용도
- ALB가 작동하지 않을 때
- 실시간에 가까운 데이터 스트리밍 서비스(동영상, 주식 시세 등)
- 애플리케이션이 비HTTP 프로토콜을 사용하는 경우
- 가격은 비슷해서 일반적으로 L7 로드밸런싱에는 ALB를 사용하고 그 외에서는 NLB를 사용하는 것이 좋음.

# 요약 table

feature         | ALB    | NLB    | ELB
--------------- |--------|--------|--------
분산 부하         | Yes    | Yes       | Yes 
상태 확인 성능     | Yes    | Yes       | Yes 
HA              | Yes    | Yes       | Yes 
Elastic         | Yes    | Yes       | Yes 
TLS termination | Yes    | Yes       | Yes 
Performance     | Good   | Very High | Good
CloudWatch      | Yes    | Yes       | Yes 
L4(TCP)         | No     | Yes       | Yes 
L7(HTTP)        | Yes    | No        | Yes 
Running Cost    | Low    | Low       | Low


### Reference
- https://medium.com/paul-zhao-projects/difference-in-between-aws-alb-nlb-and-clb-19b6048b3e6d