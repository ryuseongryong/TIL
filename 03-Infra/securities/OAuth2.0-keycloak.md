# How to architect OAuth 2.0 authorization using Keycloak

- https://www.redhat.com/architect/oauth-20-authentication-keycloak

- Keycloak은 안정적이고 편리한 ID 및 액세스 관리 서비스를 애플리케이션에 구축하는 데 도움이 되는 오픈 소스 도구이다.
- 소프트웨어 프로젝트의 로그인 서비스를 설계할 때 사용자 지정 솔루션을 만들거나 Keycloak과 같은 기성품 옵션을 선택할 수 있다. 다음과 같은 몇 가지 이유로 Keycloak을 선택해야 한다.
    - Keycloak은 오픈 소스 ID 및 액세스 관리(IAM) 도구이다.
    - 제품이나 모듈의 거의 모든 측면을 덮어쓰고 사용자 지정할 수 있다.
    - OAuth 2.0, OpenID, SAML을 포함한 거의 모든 표준 IAM 프로토콜을 구현한다.
    - 커뮤니티가 탄탄한 견고한 제품이다.
- OAuth 2.0은 업계 표준 인증 프로토콜이지만, 처음에는 거대하고 복잡하며 약간 무섭기도 하다. 하지만 지난 2년간 마이크로서비스 아키텍처를 구축하면서 배운 것처럼 Keycloak을 사용하면 OAuth2를 마스터할 수 있다.

## How Keycloak authorization works
- Google 드라이브에서 사진을 다운로드하려고 한다고 가정해 본다. 사진을 다운로드할 수 있는 권한이 있는지 확인하기 위해 웹 클라이언트 포털에서 인증 서비스로 리디렉션된다. 이 서비스는 사용자 이름과 비밀번호를 입력하는 로그인 페이지를 열고 이 사진을 다운로드할 수 있는 권한이 있는지 확인한다.

- 성공적으로 인증 + 토큰 발급 : 포털 -> 리소스 서버로 이동, 리소스 서버는 모든 비즈니스 로직이 발생하는 MSA
- 사진 파일을 가져오려면 해당 MSA의 API를 호출해야 함. 하지만 MSA는 요청에 토큰이 포함되어 있어도 아무에게나 API를 제공해서는 안 됨. 토큰이 인증 서비스(e.g. keycloak)에 의해 서명되었는지 확인해야함
- 따라서 MSA 키 ID를 사용하여 토큰 서명의 유효성을 검사하는 데 사용되는 키 집합인 JSON 웹 키 집합(JWKS)을 요청한다. 서명이 유효하면 프로세스는 응답을 반환한다.

## Understanding Keycloak users, clients, services, and realms
- user : resource owner
  client application : web portal
  authorization service : keycloak
  resource server : MSA 
- 여러 상점이 있는 대형 쇼핑몰에 들어갔다고 상상해보자. 이 쇼핑몰은 keycloak이고, 상점들은 여러분의 영역이다. 모든 행동은 이 영역 안에서 이루어진다. 쇼핑몰의 모든 장소는 하나의 부서이며, 쇼핑몰에 들어서자마자 여러분은 "입구 부서"에 있는 것이다.
- 이러한 부서는 여러분의 고객이다. Keycloak에 로그인하면 특정 클라이언트에 로그인하는 것이다. (쇼핑몰에 비유하자면 소매 부서의 특정 섹션에 들어온 것이다.)

- 또한 물건을 구매하고, 계산대에서 일하고, 고객에게 서비스를 제공하는 등의 사용자도 있다. 이를 역할이라고 하며, Keycloak을 사용하면 역할을 관리할 수 있다. 계산원에게는 한 가지 역할이 있고 고객에게는 다른 역할이 있다. 따라서 부서별, 매장별로 사용자를 차별화해야 한다. 예를 들어, 매장 1에서 무료로 물건을 가져갈 수 있다고 해서 매장 2에서도 무료로 물건을 가져갈 수 있는 것은 아니다.

## Build a microservices architecture
- MSA를 구축할 때는 아키텍처를 만드는 것부터 시작된다. 다음은 keycloak과 상호 작용하는 방법을 포함한 MSA의 최상위 다이어그램이다.

- Keycloak에는 realms, users, groups, clients 및 roles이 있다. 이 모든 메타데이터를 PostgreSQL 데이터베이스에 저장한다. 대규모 SaaS 플랫폼의 대규모 엔터프라이즈 프로젝트에는 많은 데이터가 있으므로 비관계형 데이터베이스(예: MongoDB)에 보관하는 것이 좋다. 하지만 메타데이터를 Keycloak 엔티티에 저장하는 것은 현명하지 않다. 대신 모든 데이터를 분리하여 단일 책임을 고수하는 것이 좋다.

- Keycloak과 통신할 사용자 정의 마이크로서비스 또는 마이크로서비스 집합을 작성해야 한다. 이렇게 하면 특정 URL을 사용하여 액세스할 수 있다. 영역을 만들려면 포스트 요청이 되고, 업데이트하려면 풋 요청이 된다. 따라서 Keycloak에 접속할 때 사용자 정의 로직을 수행할 수 있는 API를 제공하는 마이크로서비스가 필요하다.

- Keycloak에는 API를 바로 처리할 수 있는 솔루션이 없기 때문에 필요에 따라 마이크로서비스에 연결할 수 있는 소프트웨어 개발 키트(SDK)를 개발해야 한다. 이렇게 하면 웹 클라이언트를 통하지 않고 SDK에 구현된 기성 메소드를 사용하여 Keycloak에 HTTP 요청을 할 수 있다.
