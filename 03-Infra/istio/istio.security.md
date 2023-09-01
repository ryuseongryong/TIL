### Ref
- https://istio.io/latest/docs/concepts/security/

- https://blog.devgenius.io/sidecar-and-service-mesh-101-134d342bdad9

- https://istio.io/v1.16/blog/2022/merbridge/

- https://elastisys.com/istio-and-oauth2-proxy-in-kubernetes-for-microservice-authentication/

- https://wiki.onap.org/display/DW/Oauth2-Proxy+implementation+and+configuration

- https://www.howtogeek.com/devops/how-to-add-http-basic-authentication-to-a-kubernetes-nginx-ingress/

# Security
- 모놀리식 애플리케이션을 아토믹 서비스로 세분화하면 민첩성 향상, 확장성 개선, 서비스 재사용 능력 향상 등 다양한 이점을 얻을 수 있다. 하지만 마이크로서비스에는 특별한 보안 요구 사항도 있다.
    - 중간자 공격을 방어하려면 트래픽 암호화가 필요하다.
    - 유연한 서비스 접속 제어를 제공하려면 상호 TLS와 세분화된 접속 정책이 필요하다.
    - 누가 언제 무엇을 했는지 확인하려면 auditing 도구가 필요하다.
- istio security는 이러한 문제를 해결하기 위해 포괄적인 보안 솔루션을 제공한다. 이 페이지에서는 istio 보안 기능을 사용하여 서비스를 실행하는 모든 곳에서 서비스를 보호하는 방법에 대한 개요를 제공한다. 특히 istio 보안은 데이터, 엔드포인트, 커뮤니케이션 및 플랫폼에 대한 내부 및 외부 위협을 모두 완화한다.
- istio 보안 기능은 강력한 ID, 강력한 정책, 투명한 TLS 암호화, 인증, 권한 부여 및 감사(AAA) 도구를 제공하여 서비스 및 데이터를 보호한다. istio 보안의 목표는 다음과 같다.
    - 기본 보안 : 애플리케이션 코드와 인프라를 변경할 필요 없음
    - 심층 방어 : 기존 보안 시스템과 통합하여 여러 계층의 방어를 제공
    - zero-trust 네트워크 : 신뢰할 수 없는 네트워크에 보안 솔루션 구축
- 배포된 서비스에서 istio 보안 기능을 사용하려면 상호 TLS 마이크레이션 문서를 참조하라. 보안 기능을 사용하기 위한 자세한 지침은 보안 작업을 참조하라.

## High-level architecture
- istio 보안에는 여러 구성 요소가 포함됨
    - 키 및 인증서 관리를 위한 인증 기관(CA)
    - 구성 API 서버가 프록시에 배포됨
        - 인증 정책
        - 권한 부여 정책
        - 보안 이름 지정 정보
    - 사이드카 및 경계 프록시는 클라이언트와 서버 간의 통신을 보호하기 위해 정책 적용 지점(PEP)으로 작동함
    - 원격 분석 및 감사를 관리하기 위한 Envoy 프록시 확장 세트
- 컨트롤 플레인은 API 서버에서 구성을 처리하고 데이터 플레인에서 PEP를 구성한다. PEP는 Envoy를 사용하여 구현된다. 
- https://istio.io/latest/docs/concepts/security/arch-sec.svg

## Istio identity
- ID는 모든 보안 인프라의 기본 개념이다. 워크로드 간 통신이 시작될 때 두 당사자는 상호 인증을 위해 신원 정보와 함께 자격 증명을 교환해야 한다. 클라이언트 측에서는 서버의 신원을 보안 명명 정보와 비교하여 서버가 워크로드의 권한이 있는 실행자인지 확인한다. 서버 측에서는 권한 부여 정책에 따라 클라이언트가 액세스할 수 있는 정보를 결정하고, 누가 어떤 시간에 어떤 정보에 액세스했는지 감사하고, 사용한 워크로드에 따라 클라이언트에게 요금을 청구하고, 요금을 지불하지 않은 클라이언트의 워크로드 액세스를 거부할 수 있다.
- isito ID 모델은 1급 서비스 ID를 사용하여 요청의 출처 ID를 결정한다. 이 모델은 서비스 ID가 사용자, 개별 워크로드 또는 워크로드 그룹을 나타낼 수 있는 뛰어난 유연성과 세분성을 제공한다. 서비스 ID가 없는 플랫폼에서는 서비스 이름과 같이 워크로드 인스턴스를 그룹화할 수 있는 다른 ID를 사용할 수 있다.
- 아래 목록은 다양한 플랫폼에서 사용할 수 있는 서비스 ID의 예시이다.
    - k8s : k8s service account
    - GCE : GCP serivce account
    - On-premises(non k8s) : user account, custom service account, service name, Istio service account, or GCP service account. 사용자 지정 서비스 계정은 고객의 ID 디렉터리에서 관리하는 ID와 마찬가지로 기존 서비스 계정을 의미한다.

## Identity and certificate management
- Istio는 X.509 인증서를 사용하여 모든 워크로드에 강력한 ID를 안전하게 프로비저닝한다. 각 Envoy 프록시와 함께 시작되는 istio 에이전트는 istiod와 함께 작동하여 키 및 인증서 로테이션을 대규모로 자동화한다.
- https://istio.io/latest/docs/concepts/security/id-prov.svg
- istio는 다음 플로우를 통해 키와 인증서를 프로비저닝한다.
    1. istiod는 인증서 서명 요청(CSR)을 받기 위해 gRPC 서비스를 제공한다.
    2. 시작되면 istio 에이전트는 개인 키와 CSR을 생성한 다음 서명을 위해 자격 증명이 포함된 CSR을 istiod로 보낸다.
    3. isitod의 CA는 CSR에 포함된 자격 증명을 검증한다. 유효성 검사에 성공하면 CSR에 서명하여 인증서를 생성한다.
    4. 워크로드가 시작되면 Envoy는 Envoy SDS(비밀 검색 서비스) API를 통해 동일한 컨테이너에 있는 istio 에이전트에 인증서와 키를 요청한다.
    5. istio 에이전트는 Envoy SDS API를 통해 istiod에서 받은 인증서와 개인 키를 Envoy로 보낸다.
    6. istio 에이전트는 워크로드 인증서의 만료를 모니터링한다. 인증서 및 키 로테이션을 위해 위 프로세스가 주기적으로 반복된다.

## Authentication
- istio는 두 가지 유형의 인증을 제공한다.
    - Peer authentication : 연결을 시도하는 클라이언트를 확인하기 위한 서비스 간 인증에 사용된다. istio는 서비스 코드를 변경할 필요 없이 사용할 수 있는 전송 인증을 위한 풀 스택 솔루션으로 상호 TLS를 제공한다.
        - 각 서비스에 각자의 역할을 나타내는 강력한 ID를 제공하여 클러스터와 클라우드 전반에서 상호 운용성을 지원한다.
        - 서비스 간 통신을 보호한다.
        - 키 및 인증서 생성, 배포, 로테이션을 자동화하는 키 관리 시스템을 제공한다.
    - Request authentication : 요청에 첨부된 자격 증명을 확인하기 위한 최종 사용자 인증에 사용된다. istio는 사용자 지정 인증 공급자 또는 OpenID Connect 공급자 등을 사용하여 JSON 웹 토큰(JWT) 유효성 검사를 통한 요청 수준 인증 및 간소화된 개발자 환경을 지원한다.
        - ORY Hydra
        - Keycloak
        - Auth0
        - Firebase Auth
        - Google Auth
    - 모든 경우에 isito는 사용자 정의 k8s API를 통해 istio 구성 저장소에 인증 정책을 저장한다. istio는 각 프록시에 대해 적절한 경우 키와 함께 최신 상태로 유지한다. 또한 istio는 허용 모드에서의 인증을 지원하여 정책 변경이 적용되기 전에 보안 태세에 어떤 영향을 미칠 수 있는지 이해할 수 있도록 도와준다.

### Mutual TLS authentication
- istio는 Envoy 프록시로 구현된 클라이언트 및 서버 측 PEP를 통해 서비스 간 통신을 터널링한다. 한 워크로드가 상호 TLS 인증을 사용하여 다른 워크로드에 요청을 보내면 요청은 다음과 같이 처리된다.
    1. istio는 클라이언트의 아웃바운드 트래픽을 클라이언트의 로컬 사이드카 Envoy로 다시 라우팅한다.
    2. 클라이언트 측 Envoy는 서버 측 Envoy와 상호 TLS 핸드셰이크를 시작한다. 핸드셰이크 중에 클라이언트 측 Envoy는 서버 인증서에 제시된 서비스 계정이 대상 서비스를 실행할 권한이 있는지 확인하기 위해 보안 명명 확인도 수행한다.
    3. 클라이언트 측 Envoy와 서버 측 Envoy는 상호 TLS 연결을 설정하고, istio는 클라이언트 측 Envoy에서 서버 측 Envoy로 트래픽을 전달한다.
    4. 서버 측 Envoy는 요청을 승인한다. 권한이 부여되면 로컬 TCP 연결을 통해 트래픽을 백엔드 서비스로 전달한다.
- istio는 클라이언트와 서버 모두에 대해 다음 암호 제품군을 사용하여 TLSv1_2를 최소 TLS 버전으로 구성한다.
    - ECDHE-ECDSA-AES256-GCM-SHA384
    - ECDHE-RSA-AES256-GCM-SHA384
    - ECDHE-ECDSA-AES128-GCM-SHA256
    - ECDHE-RSA-AES128-GCM-SHA256
    - AES256-GCM-SHA384
    - AES128-GCM-SHA256

#### Permissive mode
- istio 상호 TLS에는 허용 모드가 있어 서비스가 일반 텍스트 트래픽과 상호 TLS 트래픽을 동시에 허용할 수 있다. 이 기능은 상호 TLS 온보딩 경험을 크게 개선한다.
- 많은 비(非)Istio 클라이언트가 비(非)Istio 서버와 통신하는 경우, 해당 서버를 상호 TLS가 활성화된 Istio로 마이그레이션하려는 운영자에게 문제가 발생한다. 일반적으로 운영자는 모든 클라이언트에 동시에 Istio 사이드카를 설치할 수 없거나 일부 클라이언트에 설치할 수 있는 권한조차 없다. 서버에 Istio 사이드카를 설치한 후에도 운영자는 기존 통신을 중단하지 않고는 상호 TLS를 활성화할 수 없다.
- 허용 모드를 활성화하면 서버는 일반 텍스트 및 상호 TLS 트래픽을 모두 허용한다. 이 모드는 온보딩 프로세스에 더 큰 유연성을 제공한다. 서버에 설치된 Istio 사이드카는 기존 일반 텍스트 트래픽을 중단하지 않고 상호 TLS 트래픽을 즉시 수신한다. 따라서 운영자는 클라이언트의 Istio 사이드카를 점진적으로 설치 및 구성하여 상호 TLS 트래픽을 전송할 수 있다. 클라이언트 구성이 완료되면 운영자는 서버를 상호 TLS 전용 모드로 구성할 수 있다. 자세한 내용은 상호 TLS 마이그레이션 튜토리얼을 참조해라.

#### Secure naming
- 서버 ID는 인증서에 인코딩되지만 서비스 이름은 검색 서비스 또는 DNS를 통해 검색된다. 보안 이름 지정 정보는 서버 ID를 서비스 이름에 매핑한다. ID A를 서비스 이름 B에 매핑한다는 것은 "A는 서비스 B를 실행할 수 있는 권한이 있다"라는 의미이다. 컨트롤 플레인은 에이저를 감시하고 보안 네임 매핑을 생성한 후 이를 PEP에 안전하게 배포한다. 다음 예는 인증에서 보안 이름 지정이 중요한 이유를 설명한다.
- 서비스 데이터 저장소를 실행하는 합법적인 서버가 인프라 팀 ID만 사용한다고 가정한다. 악의적인 사용자가 테스트 팀 ID에 대한 인증서와 키를 가지고 있다. 악의적인 사용자는 서비스를 가장하여 클라이언트로부터 전송된 데이터를 검사하려고 한다. 악의적인 사용자가 테스트 팀 신원에 대한 인증서와 키가 있는 위조된 서버를 배포한다. 악의적인 사용자가 데이터 저장소로 전송된 트래픽을 성공적으로 하이재킹(DNS 스푸핑, BGP/라우트 하이재킹, ARP 스푸핑 등)하여 위조된 서버로 리디렉션했다고 가정한다.
- 클라이언트가 데이터스토어 서비스를 호출하면 서버의 인증서에서 테스트 팀 ID를 추출하고, 테스트 팀이 보안 네이밍 정보로 데이터스토어를 실행할 수 있는지 여부를 확인한다. 클라이언트는 테스트 팀이 데이터스토어 서비스를 실행할 수 없는 것을 감지하고 인증이 실패한다.
- HTTP/HTTPS가 아닌 트래픽의 경우, 보안 네이밍은 공격자가 서비스의 대상 IP를 수정하는 DNS 스푸핑으로부터 보호하지 못한다는 점에 유의해라. TCP 트래픽에는 호스트 정보가 포함되어 있지 않고 Envoy는 라우팅을 위해 대상 IP에만 의존할 수 있기 때문에 Envoy는 하이재킹된 IP의 서비스로 트래픽을 라우팅할 수 있다. 이러한 DNS 스푸핑은 클라이언트 측 Envoy가 트래픽을 수신하기 전에도 발생할 수 있다.

### Authentication architecture
- 피어 및 요청 인증 정책을 사용하여 Istio 메시에서 요청을 수신하는 워크로드에 대한 인증 요구 사항을 지정할 수 있다. 메시 운영자는 `.yaml` 파일을 사용하여 정책을 지정한다. 정책은 배포된 후 Istio 구성 스토리지에 저장된다. Istio 컨트롤러는 구성 저장소를 감시한다.
- 정책이 변경되면 새 정책이 적절한 구성으로 변환되어 PEP에 필요한 인증 메커니즘을 수행하는 방법을 알려준다. 컨트롤 플레인은 공개 키를 가져와서 JWT 유효성 검사를 위해 구성에 첨부할 수 있다. 또는 Istio 시스템이 관리하는 키 및 인증서의 경로를 제공하여 상호 TLS를 위해 애플리케이션 포드에 설치한다. 자세한 내용은 ID 및 인증서 관리 섹션에서 확인할 수 있다.
- Istio는 대상 엔드포인트에 구성을 비동기적으로 보낸다. 프록시가 구성을 받으면 새 인증 요건이 해당 포드에 즉시 적용된다.
- 요청을 전송하는 클라이언트 서비스는 필요한 인증 메커니즘을 따라야 할 책임이 있다. 요청 인증의 경우, 애플리케이션은 JWT 자격 증명을 획득하여 요청에 첨부할 책임이 있다. 피어 인증의 경우, Istio는 두 PEP 간의 모든 트래픽을 상호 TLS로 자동 업그레이드한다. 인증 정책에서 상호 TLS 모드를 비활성화하는 경우, Istio는 PEP 간에 일반 텍스트를 계속 사용한다. 이 동작을 재정의하려면 대상 규칙으로 상호 TLS 모드를 명시적으로 비활성화해라. 상호 TLS의 작동 방식에 대한 자세한 내용은 상호 TLS 인증 섹션에서 확인할 수 있다.
- https://istio.io/latest/docs/concepts/security/authn.svg
- Istio는 두 가지 인증 유형과 자격 증명의 다른 클레임(해당되는 경우)이 모두 포함된 ID를 다음 계층인 권한 부여로 출력한다.

### Authentication policies
- 이 섹션에서는 Istio 인증 정책의 작동 방식에 대해 자세히 설명한다. 아키텍처 섹션에서 기억하시겠지만, 인증 정책은 서비스가 수신하는 요청에 적용된다. 상호 TLS에서 클라이언트 측 인증 규칙을 지정하려면 DestinationRule에 TLSSettings를 지정해야 한다. 자세한 내용은 TLS 설정 참조 문서에서 확인할 수 있다.
- 다른 Istio 구성과 마찬가지로, `.yaml` 파일에 인증 정책을 지정할 수 있다. kubectl을 사용하여 정책을 배포한다. 다음 인증 정책 예시는 `app:reviews` 레이블이 있는 워크로드에 대한 전송 인증이 상호 TLS를 사용해야 한다고 지정한다.
- ```
    apiVersion: security.istio.io/v1beta1
    kind: PeerAuthentication
    metadata:
        name: "example-peer-policy"
        namespace: "foo"
    spec:
        selector:
            matchLabels:
                app: reviews
        mtls:
            mode: STRICT
  ```

#### Policy storage
- Istio는 루트 네임스페이스에 메시 범위 정책을 저장한다. 이러한 정책에는 메시의 모든 워크로드에 적용되는 빈 선택기가 있다. 네임스페이스 범위가 있는 정책은 해당 네임스페이스에 저장된다. 해당 네임스페이스 내의 워크로드에만 적용된다. 선택기 필드를 구성하는 경우 인증 정책은 구성한 조건과 일치하는 워크로드에만 적용된다.
- 피어 및 요청 인증 정책은 각각 PeerAuthentication 및 RequestAuthentication 종류별로 별도로 저장된다.

#### Selector field
- 피어 및 요청 인증 정책은 선택기 필드를 사용하여 정책이 적용되는 워크로드의 레이블을 지정한다.
- 선택기 필드에 값을 제공하지 않으면 Istio는 정책의 스토리지 범위에 있는 모든 워크로드에 정책을 일치시킨다. 따라서 선택기 필드는 정책의 범위를 지정하는 데 도움이 된다.
    - Mesh-wide policy: 선택기 필드가 없거나 비어 있는 루트 네임스페이스에 대해 지정된 정책이다.
    - Namespace-wide policy: 선택기 필드가 없거나 빈 선택기 필드가 있는 루트 네임스페이스가 아닌 네임스페이스에 대해 지정된 정책이다.
    - Workload-specific policy: 비어 있지 않은 선택기 필드가 있는 일반 네임스페이스에 정의된 정책이다.
- 피어 및 요청 인증 정책은 선택자 필드에 대해 동일한 계층 구조 원칙을 따르지만, Istio는 이를 약간 다른 방식으로 결합하여 적용한다.

- 메시 전체 피어 인증 정책은 하나만 있을 수 있고 네임스페이스 전체 피어 인증 정책은 네임스페이스당 하나만 있을 수 있다. 동일한 메시 또는 네임스페이스에 대해 여러 개의 메시 또는 네임스페이스 전체 피어 인증 정책을 구성하는 경우, Istio는 최신 정책을 무시한다. 둘 이상의 워크로드별 피어 인증 정책이 일치하는 경우, Istio는 가장 오래된 정책을 선택한다.

- Istio는 다음 순서를 사용하여 각 워크로드에 대해 가장 좁은 매칭 정책을 적용한다:
    - 워크로드별
    - 네임스페이스 전체
    - 메시 전체
- Istio는 일치하는 모든 요청 인증 정책을 결합하여 마치 단일 요청 인증 정책에서 나온 것처럼 작동할 수 있다. 따라서 메시 또는 네임스페이스에 여러 개의 메시 전체 또는 네임스페이스 전체 정책을 가질 수 있다. 그러나 메시 전체 또는 네임스페이스 전체 요청 인증 정책을 여러 개 두는 것은 피하는 것이 좋다.

#### Peer authentication
- 피어 인증 정책은 Istio가 대상 워크로드에 적용하는 상호 TLS 모드를 지정한다. 지원되는 모드는 다음과 같다
    - PERMISSIVE: 워크로드가 상호 TLS와 일반 텍스트 트래픽을 모두 허용한다. 이 모드는 사이드카가 없는 워크로드가 상호 TLS를 사용할 수 없는 마이그레이션 중에 가장 유용하다. 사이드카 인젝션으로 워크로드를 마이그레이션한 후에는 모드를 STRICT로 전환해야 한다.
    - STRICT: 워크로드는 상호 TLS 트래픽만 허용한다.
    - DISABLE: 상호 TLS가 비활성화된다. 보안 관점에서 자체 보안 솔루션을 제공하지 않는 한 이 모드를 사용해서는 안 된다.
- 모드가 설정되지 않은 경우 상위 범위의 모드가 상속된다. 모드가 설정되지 않은 메시 전체 피어 인증 정책은 기본적으로 허용 모드를 사용한다.
- 다음 피어 인증 정책은 네임스페이스 foo의 모든 워크로드가 상호 TLS를 사용하도록 요구한다.
    - ```
        apiVersion: security.istio.io/v1beta1
        kind: PeerAuthentication
        metadata:
            name: "example-policy"
            namespace: "foo"
        spec:
            mtls:
                mode: STRICT

      ```

- 워크로드별 피어 인증 정책을 사용하면 포트마다 서로 다른 상호 TLS 모드를 지정할 수 있다. 포트 전체 상호 TLS 구성에는 워크로드가 클레임한 포트만 사용할 수 있다. 다음 예에서는 `app:example-app` 워크로드에 대해 포트 80에서 상호 TLS를 사용하지 않도록 설정하고 다른 모든 포트에 대해 네임스페이스 전체 피어 인증 정책의 상호 TLS 설정을 사용한다.
    - ```
        apiVersion: security.istio.io/v1beta1
        kind: PeerAuthentication
        metadata:
            name: "example-workload-policy"
            namespace: "foo"
        spec:
            selector:
                matchLabels:
                    app: example-app
        portLevelMtls:
            80:
                mode: DISABLE

      ```

- 위의 피어 인증 정책은 아래의 서비스 구성이 예제 앱 워크로드의 요청을 예제 서비스의 포트 80으로 바인딩했기 때문에 작동한다.
    - ```
        apiVersion: v1
        kind: Service
        metadata:
        name: example-service
        namespace: foo
        spec:
        ports:
        - name: http
            port: 8000
            protocol: TCP
            targetPort: 80
        selector:
            app: example-app

      ```

#### Request authentication
- 요청 인증 정책은 JSON 웹 토큰(JWT)의 유효성을 검사하는 데 필요한 값을 지정한다. 이러한 값에는 특히 다음이 포함된다.
    - 요청에서 토큰의 위치
    - 발급자 또는 요청
    - 공개 JSON 웹 키 세트(JWKS)
- Istio는 제시된 토큰이 요청 인증 정책의 규칙과 일치하는지 확인하고 유효하지 않은 토큰이 포함된 요청을 거부한다. 요청에 토큰이 없는 경우 기본적으로 요청이 수락된다. 토큰이 없는 요청을 거부하려면 특정 작업(예: 경로 또는 작업)에 대한 제한을 지정하는 권한 부여 규칙을 제공해라.

- 요청 인증 정책은 각각 고유한 위치를 사용하는 경우 둘 이상의 JWT를 지정할 수 있다. 둘 이상의 정책이 워크로드와 일치하는 경우, Istio는 모든 규칙을 단일 정책으로 지정된 것처럼 결합한다. 이 동작은 다른 공급자의 JWT를 수락하도록 워크로드를 프로그래밍하는 데 유용하다. 그러나 둘 이상의 유효한 JWT가 있는 요청은 이러한 요청의 출력 주체가 정의되지 않았기 때문에 지원되지 않는다.

#### Principals
- 피어 인증 정책 및 상호 TLS를 사용하는 경우, Istio는 피어 인증에서 `source.principal`로 ID를 추출한다. 마찬가지로 요청 인증 정책을 사용하는 경우 Istio는 JWT의 ID를 `request.auth.principal`에 할당한다. 이러한 주체를 사용하여 인증 정책을 설정하고 원격 분석 출력으로 사용한다.

### Updating authentication policies
- 인증 정책은 언제든지 변경할 수 있으며, Istio는 거의 실시간으로 새 정책을 워크로드에 푸시한다. 하지만 모든 워크로드가 동시에 새 정책을 받는다고 보장할 수는 없다. 다음 권장 사항은 인증 정책을 업데이트할 때 중단을 방지하는 데 도움이 된다.
    - 허용 모드를 비활성화에서 엄격으로 또는 그 반대로 변경할 때는 허용 모드를 사용하여 중간 피어 인증 정책을 사용한다. 모든 워크로드가 원하는 모드로 성공적으로 전환되면 최종 모드로 정책을 적용할 수 있다. Istio 원격 측정을 사용하여 워크로드가 성공적으로 전환되었는지 확인할 수 있다.
    - 한 JWT에서 다른 JWT로 요청 인증 정책을 마이그레이션할 때는 이전 규칙을 제거하지 않고 새 JWT에 대한 규칙을 정책에 추가한다. 그러면 워크로드가 두 가지 유형의 JWT를 모두 수락하고 모든 트래픽이 새 JWT로 전환될 때 이전 규칙을 제거할 수 있다. 그러나 각 JWT는 다른 위치를 사용해야 한다.

## Authorization
- Istio의 권한 부여 기능은 메시에서 워크로드에 대한 메시, 네임스페이스 및 워크로드 전체 액세스 제어 기능을 제공한다. 이러한 수준의 제어는 다음과 같은 이점을 제공한다.
    - 워크로드 간 및 최종 사용자 간 권한 부여
    - A simple API: 사용 및 유지 관리가 쉬운 단일 AuthorizationPolicy CRD가 포함되어 있습니다.
    - Flexible semantics: 운영자는 Istio 속성에 대한 사용자 지정 조건을 정의하고 CUSTOM, DENY, ALLOW 작업을 사용할 수 있습니다.
    - High performance: Istio 권한 부여(허용 및 거부)는 Envoy에서 기본적으로 적용됩니다.
    - High compatibility: gRPC, HTTP, HTTPS, HTTP/2는 물론 모든 일반 TCP 프로토콜을 기본적으로 지원한다.

### Authorization architecture
- 권한 부여 정책은 서버 측 Envoy 프록시에서 인바운드 트래픽에 대한 액세스 제어를 시행한다. 각 Envoy 프록시는 런타임에 요청을 승인하는 권한 부여 엔진을 실행한다. 프록시로 요청이 들어오면 권한 부여 엔진은 현재 권한 부여 정책에 대해 요청 컨텍스트를 평가하고 ALLOW 또는 DENY 중 하나의 권한 부여 결과를 반환한다. 운영자는 `.yaml` 파일을 사용하여 Istio 권한 부여 정책을 지정한다.
- https://istio.io/latest/docs/concepts/security/authz.svg

### Implicit enablement
- Istio의 인증 기능을 명시적으로 활성화할 필요는 없고, 설치 후에 가능하다. 워크로드에 대한 액세스 제어를 적용하려면 권한 부여 정책을 적용하면 된다.
- 권한 부여 정책이 적용되지 않은 워크로드의 경우, Istio는 모든 요청을 허용한다.
- 권한 부여 정책은 ALLOW, DENY 및 CUSTOM 작업을 지원한다. 워크로드에 대한 액세스를 보호하기 위해 필요에 따라 각각 다른 동작을 가진 여러 정책을 적용할 수 있다.
- Istio는 이 순서대로 계층별로 일치하는 정책을 확인한다: CUSTOM, DENY, ALLOW 순으로 일치하는 정책을 확인한다. 각 작업 유형에 대해 Istio는 먼저 해당 작업이 적용된 정책이 있는지 확인한 다음 요청이 정책의 사양과 일치하는지 확인한다. 요청이 한 계층의 정책과 일치하지 않으면 다음 계층으로 계속 확인한다.

- 다음 그래프는 정책 우선순위를 자세히 보여준다: https://istio.io/latest/docs/concepts/security/authz-eval.png
- 동일한 워크로드에 여러 권한 부여 정책을 적용하는 경우, Istio는 이를 추가적으로 적용한다.

### Authorization policies
- 권한 부여 정책을 구성하려면 AuthorizationPolicy 사용자 지정 리소스를 만든다. 권한 부여 정책에는 선택기, 작업 및 규칙 목록이 포함된다.
    - 선택기 필드는 정책의 대상을 지정한다.
    - 작업 필드는 요청을 허용할지 거부할지 지정한다.
    - 규칙은 동작을 트리거할 시기를 지정한다.
        - 규칙의 발신자 필드는 요청의 출처를 지정한다.
        - 규칙의 to 필드는 요청의 작업을 지정한다.
        - 언제 필드는 규칙을 적용하는 데 필요한 조건을 지정한다.
- 다음 예제에서는 전송된 요청에 유효한 JWT 토큰이 있을 때 두 개의 소스, 즉 `cluster.local/ns/default/sa/sleep` 서비스 계정과 dev 네임스페이스가 앱으로 워크로드에 액세스할 수 있도록 허용하는 권한 부여 정책을 보여준다(전송된 요청에 유효한 JWT 토큰이 있을 때 foo 네임스페이스의 httpbin 및 version: v1 레이블).
    - ```
        apiVersion: security.istio.io/v1
        kind: AuthorizationPolicy
        metadata:
         name: httpbin
         namespace: foo
        spec:
         selector:
           matchLabels:
             app: httpbin
             version: v1
         action: ALLOW
         rules:
         - from:
           - source:
               principals: ["cluster.local/ns/default/sa/sleep"]
           - source:
               namespaces: ["dev"]
           to:
           - operation:
               methods: ["GET"]
           when:
           - key: request.auth.claims[iss]
             values: ["https://accounts.google.com"]
    
      ```
- 다음 예는 소스가 foo 네임스페이스가 아닌 경우 요청을 거부하는 권한 부여 정책을 보여준다.
    - ```
        apiVersion: security.istio.io/v1
        kind: AuthorizationPolicy
        metadata:
         name: httpbin-deny
         namespace: foo
        spec:
         selector:
           matchLabels:
             app: httpbin
             version: v1
         action: DENY
         rules:
         - from:
           - source:
               notNamespaces: ["foo"]

      ```

- 거부 정책이 허용 정책보다 우선한다. 허용 정책과 일치하는 요청이 거부 정책과 일치하면 거부될 수 있다. Istio는 거부 정책을 먼저 평가하여 허용 정책이 거부 정책을 우회할 수 없도록 한다.

#### Policy Target
- 메타데이터/네임스페이스 필드와 선택적 선택기 필드를 사용하여 정책의 범위 또는 대상을 지정할 수 있다. 메타데이터/네임스페이스 필드에 있는 네임스페이스에 정책이 적용된다. 값을 루트 네임스페이스로 설정하면 메시의 모든 네임스페이스에 정책이 적용된다. 루트 네임스페이스의 값은 구성할 수 있으며 기본값은 istio-system이다. 다른 네임스페이스로 설정하면 정책이 지정된 네임스페이스에만 적용된다.

- 선택기 필드를 사용하여 특정 워크로드에 적용하도록 정책을 추가로 제한할 수 있다. 선택기는 레이블을 사용하여 대상 워크로드를 선택한다. 선택기에는 {키: 값} 쌍의 목록이 포함되며, 여기서 키는 레이블의 이름이다. 설정하지 않으면 권한 부여 정책이 권한 부여 정책과 동일한 네임스페이스에 있는 모든 워크로드에 적용된다.

- 예를 들어, 읽기 허용 정책은 기본 네임스페이스에서 `app: products` 레이블이 있는 워크로드에 대한 "GET" 및 "HEAD" 액세스를 허용한다.
    - ```
        apiVersion: security.istio.io/v1
        kind: AuthorizationPolicy
        metadata:
          name: allow-read
          namespace: default
        spec:
          selector:
            matchLabels:
              app: products
          action: ALLOW
          rules:
          - to:
            - operation:
                 methods: ["GET", "HEAD"]

      ```

#### Value matching
- 권한 부여 정책의 대부분의 필드는 다음과 같은 일치하는 스키마를 모두 지원한다:
    - 정확히 일치: 정확한 문자열 일치.
    - 접두사 일치: 끝이 "*"인 문자열. 예를 들어, "test.abc.*"는 "test.abc.com", "test.abc.com.cn", "test.abc.org" 등과 일치한다.
    - 접미사 일치: 시작이 "*"인 문자열입니다. 예를 들어, "*.abc.com"은 "eng.abc.com", "test.eng.abc.com" 등과 일치한다.
    - 현재 위치 일치: * 는 비어 있지 않은 모든 것을 지정하는 데 사용된다. 필드가 반드시 존재하도록 지정하려면 필드명: ["*"]형식을 사용한다. 이는 필드를 지정하지 않은 상태로 두는 것과 다르며, 비어 있는 것을 포함하여 무엇이든 일치시키는 것을 의미한다.

- 몇 가지 예외가 있다. 예를 들어 다음 필드는 정확히 일치하는 항목만 지원한다:
    - 언제 섹션 아래의 키 필드
    - source 섹션 아래의 ipBlocks
    - to 섹션 아래의 포트 필드
- 다음 예제 정책은 `/test/*` 접두사 또는 `*/info` 접미사가 있는 경로에 대한 액세스를 허용한다.
    - ```
        apiVersion: security.istio.io/v1
        kind: AuthorizationPolicy
        metadata:
          name: tester
          namespace: default
        spec:
          selector:
            matchLabels:
              app: products
          action: ALLOW
          rules:
          - to:
            - operation:
                paths: ["/test/*", "*/info"]
        
      ```

#### Exclusion matching
- when 필드의 notValues, source 필드의 notIpBlocks, 대상 필드의 notPorts와 같은 음수 조건을 일치시키기 위해 Istio는 제외 매칭을 지원한다. 다음 예제에서는 요청 경로가 /healthz가 아닌 경우 JWT 인증에서 파생된 유효한 요청 주체가 필요하다. 따라서 이 정책은 JWT 인증에서 /healthz 경로에 대한 요청을 제외한다.
    - ```
        apiVersion: security.istio.io/v1
        kind: AuthorizationPolicy
        metadata:
          name: disable-jwt-for-healthz
          namespace: default
        spec:
          selector:
            matchLabels:
              app: products
          action: ALLOW
          rules:
          - to:
            - operation:
                notPaths: ["/healthz"]
            from:
            - source:
                requestPrincipals: ["*"]

      ```
- 다음 예에서는 요청 주체가 없는 요청에 대해 /admin 경로에 대한 요청을 거부한다.
    - ```
        apiVersion: security.istio.io/v1
        kind: AuthorizationPolicy
        metadata:
          name: enable-jwt-for-admin
          namespace: default
        spec:
          selector:
            matchLabels:
              app: products
          action: DENY
          rules:
          - to:
            - operation:
                paths: ["/admin"]
            from:
            - source:
                notRequestPrincipals: ["*"]

      ```