### service
- 문자열
- 필수
- Envoy ext_authz HTTP 인증 서비스를 구현하는 서비스를 지정합니다. 형식은 [<네임스페이스>/]<호스트명>입니다. <네임스페이스> 지정은 서비스 레지스트리에서 서비스를 명확하게 확인할 수 없는 경우에만 필요합니다. <호스트명>은 쿠버네티스 서비스 또는 서비스엔트리에 의해 정의된 서비스의 정규화된 호스트 이름이다.
- 예시: "my-ext-authz.foo.svc.cluster.local" 또는 "bar/my-ext-authz.example.com".

### port
- UINT32
필수. 서비스의 포트를 지정합니다.

### timeout
- 초과 기간
- 프록시가 공급자의 응답을 기다리는 최대 기간입니다(기본 시간 제한: 600초). 이 시간 제한 조건이 충족되면 프록시는 권한 부여 서비스에 대한 통신을 실패로 표시합니다. 이 경우 클라이언트로 다시 전송되는 응답은 구성된 fail_open 필드에 따라 달라집니다.

### pathPrefix
- 문자열
- 권한 부여 요청 헤더 경로 값에 접두사를 설정합니다. 예를 들어 "/admin" 경로의 원래 사용자 요청에 대해 이 값을 "/check"로 설정하면 권한 확인 요청이 "/admin" 대신 "/check/admin" 경로의 권한 부여 서비스로 전송됩니다.

### failOpen
- 부울
- true이면 권한 부여 서비스와의 통신에 실패했거나 권한 부여 서비스에서 HTTP 5xx 오류를 반환한 경우에도 사용자 요청이 허용됩니다. 기본값은 거짓이며 요청은 "금지됨" 응답으로 거부됩니다.

### statusOnError
- 문자열
- 권한 부여 서비스에 네트워크 오류가 있을 때 클라이언트에 반환되는 HTTP 상태를 설정합니다. 기본 상태는 "403"(HTTP 금지됨)입니다.

### includeHeadersInCheck
- 문자열[]
- DEPRECATED : 대신 include_request_headers_in_check를 사용

### includeRequestHeadersInCheck 
- 문자열[]
- 권한 부여 서비스에 보내는 권한 부여 요청에 포함되어야 하는 클라이언트 요청 헤더 목록입니다. 여기에 지정된 헤더 외에도 다음 헤더가 기본적으로 포함됩니다:
    - Host, Method, Path 및 Content-Length는 자동으로 전송됩니다.
    - Content-Length는 0으로 설정되며 요청에는 메시지 본문이 없습니다. 그러나 권한 요청에는 버퍼링된 클라이언트 요청 본문이 포함될 수 있으므로(include_request_body_in_check 설정으로 제어) 권한 요청의 Content-Length 값은 해당 페이로드 크기의 크기를 반영합니다.
- 정확히, 접두사 및 접미사 일치가 지원됩니다(존재 일치(https://istio.io/latest/docs/reference/config/security/authorization-policy/#Rule)를 제외한 권한 부여 정책 규칙 구문과 유사):
    - 정확히 일치: "abc" 값에 대해 "abc"가 일치합니다.
    - 접두사 일치: "abc*"는 "abc" 및 "abcd" 값에서 일치합니다.
    - 접미사 일치: "*abc"는 "abc" 및 "xabc" 값에서 일치합니다.

### includeAdditionalHeadersInCheck
- map<string, string>
- 인증 서비스로 전송되는 인증 요청에 포함되어야 하는 추가 고정 헤더 집합입니다. 키는 헤더 이름이고 값은 헤더 값입니다. include_request_headers_in_check에 지정된 키와 동일한 헤더를 가진 클라이언트 요청은 재정의됩니다.

### includeRequestBodyInCheck
- EnvoyExternalAuthorizationRequestBody
- 설정하면 클라이언트 요청 본문이 권한 부여 서비스로 전송되는 권한 부여 요청에 포함됩니다.

### headersToUpstreamOnAllow 
- 문자열[]
- 권한 검사 결과가 허용될 때 원본 요청에 추가되거나 재정의되어 업스트림으로 전달되어야 하는 권한 부여 서비스의 헤더 목록입니다(HTTP 코드 200). 지정하지 않으면 원본 요청이 수정되지 않고 그대로 백엔드로 전달됩니다. 기존 헤더는 모두 재정의됩니다.

- 정확히, 접두사 및 접미사 일치가 지원됩니다(존재 일치(https://istio.io/latest/docs/reference/config/security/authorization-policy/#Rule)를 제외한 권한 부여 정책 규칙 구문과 유사):

    - 정확히 일치: "abc" 값에 "abc"가 일치합니다.
    - 접두사 일치: "abc*"는 "abc" 및 "abcd" 값에서 일치합니다.
    - 접미사 일치: "*abc"는 "abc" 및 "xabc" 값에서 일치합니다.

### headersToDownstreamOnDeny 
- 문자열[]
- 권한 검사 결과가 허용되지 않을 때 다운스트림으로 전달해야 하는 권한 부여 서비스의 헤더 목록입니다(200 이외의 HTTP 코드). 지정하지 않으면 권한(호스트)을 제외한 모든 권한 부여 응답 헤더가 다운스트림에 전달됩니다. 이 목록에 헤더가 포함되면 경로, 상태, 콘텐츠 길이, WWWAuthenticate 및 위치가 자동으로 추가됩니다. 인증 서비스의 본문은 항상 다운스트림에 대한 응답에 포함된다는 점에 유의하세요.

- 정확히, 접두사 및 접미사 일치가 지원됩니다(존재 일치(https://istio.io/latest/docs/reference/config/security/authorization-policy/#Rule)를 제외한 권한 부여 정책 규칙 구문과 유사):

    - 정확히 일치: "abc" 값에서 "abc"가 일치합니다.
    - 접두사 일치: "abc*"는 "abc" 및 "abcd" 값에서 일치합니다.
    - 접미사 일치: "*abc"는 "abc" 및 "xabc" 값에서 일치합니다.

### headersToDownstreamOnAllow 
- 문자열[]
- 권한 검사 결과가 허용될 때 다운스트림으로 전달해야 하는 권한 부여 서비스의 헤더 목록(HTTP 코드 200). 지정하지 않으면 원본 응답이 수정되지 않고 그대로 다운스트림으로 전달됩니다. 기존 헤더는 모두 재정의됩니다.

- 정확히, 접두사 및 접미사 일치가 지원됩니다(존재 일치(https://istio.io/latest/docs/reference/config/security/authorization-policy/#Rule)를 제외한 권한 부여 정책 규칙 구문과 유사):
    - 정확히 일치: "abc" 값에 "abc"가 일치합니다.
    - 접두사 일치: "abc*"는 "abc" 및 "abcd" 값에서 일치합니다.
    - 접미사 일치: "*abc"는 "abc" 및 "xabc" 값에서 일치합니다.
