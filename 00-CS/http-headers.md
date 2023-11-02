# HTTP headers
- https://www.geeksforgeeks.org/http-headers/

HTTP 헤더는 요청 및 응답 헤더를 통해 클라이언트와 서버 간에 추가 정보를 전달하는 데 사용됩니다. 모든 헤더는 대소문자를 구분하지 않으며, 헤더 필드는 콜론으로 구분되고, 키-값 쌍은 일반 텍스트 문자열 형식으로 표시됩니다. 헤더 섹션의 끝은 빈 필드 헤더로 표시됩니다. 코멘트를 포함할 수 있는 헤더 필드가 몇 가지 있습니다. 또한 일부 헤더에는 등호로 구분된 품질(q) 키-값 쌍이 포함될 수 있습니다.

컨텍스트에 따라 네 가지 종류의 헤더가 있습니다:
- General Header : 이 유형의 헤더는 요청 및 응답 헤더에 모두 적용되지만 데이터베이스 본문에는 영향을 미치지 않습니다.
- Request Header : 이 유형의 헤더에는 클라이언트가 가져온 요청에 대한 정보가 포함됩니다
- Response Header : 이 유형의 헤더에는 클라이언트가 요청한 소스의 위치가 포함됩니다.
- Entity Header : 이 헤더 유형에는 MIME 유형, 콘텐츠 길이와 같은 리소스 본문에 대한 정보가 포함됩니다.

프록시가 헤더를 처리하는 방식에 따라 헤더를 분류할 수도 있습니다:
- Connection
- Keep-Alive
- Proxy-Authenticate
- Proxy-Authorization
- TE
- Trailer
- Transfer-Encoding
- Authentication 
    - Authorization : 제한된 문서를 요청하는 데 사용됩니다.
    - Proxy-Autenticate : 인증 방법을 정의하여 리소스 파일에 대한 액세스 권한을 부여하는 응답 헤더입니다. 프록시 서버가 요청을 인증하여 추가 전송할 수 있도록 합니다.
    - Proxy-Authorization : 유형의 헤더입니다. 이 헤더에는 사용자 에이전트와 사용자가 지정한 서버 간에 인증하기 위한 자격 증명이 포함됩니다.
    - WWW-Authenticate : 인증 방법을 정의하는 응답 헤더입니다. 리소스에 대한 액세스 권한을 얻는 데 사용해야 합니다.
- Caching
    - Age : 응답 헤더입니다. 프록시 캐시에 있는 객체의 시간(초)을 정의합니다.
    - Cache-Control : 캐싱 메커니즘에 대한 지시문을 지정하는 데 사용되는 일반 유형 헤더입니다.
    - Clear-Site-Data : 응답형 헤더입니다. 이 헤더는 요청하는 웹사이트에 있는 브라우징 데이터를 삭제하는 데 사용됩니다.
    - Expires : 응답 유형 헤더로, 해당 시간 이후 사라질 날짜/시간을 정의하는 데 사용됩니다.
    - Pragma : 일반 유형 헤더이지만 응답 동작이 지정되지 않아 구현에 따라 다릅니다.
    - Warnings : 클라이언트에게 발생할 수 있는 문제를 알리는 데 사용되는 일반 유형 헤더입니다.
- Client hints
    - Accept-CH : 응답 유형 헤더입니다. 클라이언트가 후속 요청에 포함해야 하는 클라이언트 힌트 헤더를 지정합니다.
    - Accept-CH-Lifetime : Accept-CH 헤더 값의 지속성을 지정하는 데 사용되는 응답 타입 헤더입니다.
    - Content-DPR : 응답 유형 헤더입니다. 선택한 이미지 응답의 CSS 픽셀에 대한 물리적 픽셀 간의 비율을 정의하는 데 사용됩니다.
    - DPR : 응답형 헤더로, 디바이스의 현재 창의 CSS 픽셀에 대한 물리적 픽셀의 비율을 정의하는 데 사용됩니다.
    - Device-Memory : 클라이언트 디바이스에 남은 대략적인 램을 지정하는 데 사용됩니다.
    - Early-Data : 요청 유형 헤더입니다. 이 헤더는 요청이 초기 데이터로 전달되었음을 나타내는 데 사용됩니다.
    - Save-Data : 클라이언트 측에서 데이터 사용량을 줄이는 데 사용됩니다.
    - Viewport-Width : 레이아웃 뷰포트 너비를 CSS 픽셀 단위로 표시하는 데 사용됩니다.
    - Width : 요청 유형 헤더입니다. 이 헤더는 원하는 리소스 너비를 물리적 픽셀 단위로 표시하는 데 사용됩니다.
- Conditionals
    - Last-Modified : 마지막으로 수정된 응답 헤더는 요청된 소스의 마지막 수정 날짜를 지정하여 서버에서 전송하는 헤더입니다. 다음은 HTTP 헤더의 Last-Modified에 대한 공식적인 정의입니다.
    - ETag : 리소스의 특정 버전에 대한 식별자로 사용되는 응답 유형 헤더입니다.
    - If-Match : 요청 유형 헤더입니다. 요청을 조건부로 만드는 데 사용됩니다.
    - If-None-Match : 요청 유형 헤더입니다. 일반적으로 서버에서 엔티티 태그를 업데이트하는 데 사용됩니다. 먼저 클라이언트가 서버에 엔티티 태그(E-태그) 집합을 제공합니다.
    - If-Modified-Since : 요청 유형 헤더입니다. 이 헤더는 요청을 조건부로 만들고 지정된 날짜 이후에 엔티티가 수정된 경우 엔티티를 전송할 것으로 기대하는 데 사용됩니다.
    - If-Unmodified-Since : 요청 유형 헤더입니다. 이 헤더는 요청을 조건부로 만들고 지정된 날짜 이후에 엔티티가 수정되지 않은 경우 엔티티를 전송할 것으로 예상하는 데 사용됩니다.
    - Vary : 응답 유형 헤더입니다. 서버가 콘텐츠 협상 알고리즘에서 리소스의 표현을 선택할 때 사용한 헤더를 표시하는 데 사용됩니다.
- Connection management
    - Connection : 발신자 또는 클라이언트가 특정 연결에 원하는 옵션을 지정할 수 있는 일반 유형 헤더입니다.
    - Keep-Alive : 영구 연결이 열려 있어야 하는 기간을 알리는 데 사용되는 일반 유형 헤더입니다.
- Content negotiation 
    - Accept : 요청 유형 헤더입니다. Accept 헤더는 클라이언트가 MIME 유형으로 표현된 콘텐츠 유형을 이해할 수 있는지를 서버에 알리는 데 사용됩니다.
    - Accept-charset : 요청 유형 헤더입니다. 이 헤더는 서버의 응답에 허용되는 문자 집합을 나타내는 데 사용됩니다.
    - Accept-Encoding : 응답형 헤더입니다. 일반적으로 요청 헤더의 비교 알고리즘입니다. 모든 HTTP 클라이언트가 서버에 어떤 인코딩 또는 인코딩을 지원하는지 알려주는 데 사용됩니다.
    - Accept-Language : 클라이언트가 이해할 수 있는 모든 언어에 대해 서버에 알려주는 요청 유형 헤더입니다.
- Control
    - Expect : 요청 유형 헤더입니다. 서버가 클라이언트에 응답하기 위해 수행해야 하는 특정 동작 또는 기대치를 나타내는 데 사용됩니다. 일반적으로 헤더 필드에 정의된 기대값은 Expect: 100-continue가 유일합니다.
- Cookies
    - Cookie : 요청 유형 헤더입니다. 사용자가 서버로 보내는 요청에 사용되는 쿠키입니다.
    - Set-Cookie : 응답 헤더이며 서버에서 사용자 에이전트로 쿠키를 보내는 데 사용됩니다. 사용자 에이전트는 나중에 서버로 쿠키를 다시 전송하여 서버가 사용자를 감지할 수 있도록 합니다.
    - Cookie2 : 요청 유형 헤더입니다. 사용자가 서버로 보내는 요청에 사용되는 쿠키2입니다.
    - Set-Cookie2 : 응답 유형 헤더이며 더 이상 사용되지 않습니다. 클라이언트에서 서버로 상태 정보를 제공하고 검색하는 메커니즘을 제공하는 공급자입니다.
- CORS
    - Access-Control-Allow-Origin : 지정된 오리진의 요청 코드와 응답을 공유할 수 있는지 여부를 나타내는 데 사용되는 응답 헤더입니다.
    - Access-Control-Allow-Credentials : 응답 헤더입니다. Access-Control-Allow-Credentials 헤더는 요청의 자격 증명 모드 요청.credentials가 "include"일 때 브라우저에 프런트엔드 JavaScript 코드에 응답을 노출하도록 지시하는 데 사용됩니다.
    - Access-Control-Allow-Headers : 응답 헤더에 언급된 헤더를 노출하는 데 사용되는 응답 헤더입니다. 기본적으로 6개의 응답 헤더가 이미 노출되며, 이를 CORS 허용 목록 응답 헤더라고 합니다.
    - Access-Control-Allow-Methods : 리소스에 액세스할 때 허용되는 메소드를 지정하는 응답 유형 헤더입니다.
    - Access-Control-Expose-Headers : 노출할 수 있는 헤더를 나타내는 응답형 헤더입니다.
    - Access-Control-Max-Age : 특정 방법과 헤더를 사용하여 CORS 프로토콜이 이해되고 서버가 인지하고 있는지 확인하는 CORS 프리플라이트 요청의 결과를 캐시할 수 있는 시간을 알려주는 응답 헤더입니다.
    - Access-Control-Request-Headers : 요청 유형 헤더로, 실제 요청이 이루어질 때 어떤 HTTP 헤더가 사용될지 서버에 알려줍니다.
    - Access-Control-Request-Method : 요청 유형 헤더로, 실제 요청이 이루어질 때 어떤 HTTP 메서드가 사용될지 서버에 알려줍니다.
    - Origin : 경로 정보를 표시하지 않고 HTTP 요청을 시작하는 보안 컨텍스트를 나타내는 응답 HTTP 헤더입니다.
    - Timing-Allow-Origin : 응답 유형 헤더입니다. 리소스 타이밍 API의 기능을 통해 검색된 속성 값을 볼 수 있는 원본을 지정합니다.
- Do Not Track
    - DNT : 요청 유형 헤더입니다. 이를 통해 사용자는 개인화된 콘텐츠 대신 개인 정보를 선호하는지 여부를 표시할 수 있습니다.
    - TK : 응답 유형 헤더이며 추적 상태를 나타냅니다.
- Downloads
    - Content-Disposition : 본문에 대한 응답 유형 헤더입니다. 사용자가 전송된 리소스를 인라인으로 표시하거나 다운로드해야 함을 표시하고 '다른 이름으로 저장' 대화 상자를 표시할 수 있습니다.
- Message body information
    - Content-Length : 응답 유형 헤더입니다. 엔티티 바디의 크기를 소수점 이하 옥텟, 즉 바이트로 표시하여 수신자에게 전송하는 데 사용됩니다. 금지된 헤더 이름입니다.
    - Content-Type : 엔티티 유형 헤더입니다. 리소스의 미디어 유형을 나타내는 데 사용됩니다. 미디어 유형은 파일의 형식을 나타내는 파일과 함께 전송되는 문자열입니다.
    - Content-Encoding : 응답 유형 헤더입니다. 미디어 유형을 압축하는 데 사용됩니다. 사용자가 지원할 인코딩을 서버에 알려줍니다.
    - Content-Language : 엔티티 유형 헤더입니다. 문서가 어떤 언어 사용자를 대상으로 하는지 정의하는 데 사용됩니다. 문서의 언어는 정의하지 않습니다.
    - Content-Location : 반환되는 데이터의 다른 위치를 제공하고 직접 URL을 표시하여 리소스에 액세스하는 방법을 알려주는 엔티티 유형 헤더입니다.
- Proxies
    - Forwarded : 요청 유형 헤더입니다. 프록시가 요청 경로에 포함될 때 손실되는 프록시 서버의 클라이언트 측을 저장하는 데 사용됩니다.
    - X-Forwarded-For : 요청 유형 헤더로, 클라이언트가 HTTP 프록시 또는 로드밸런서를 통해 웹 서버에 연결할 때 원본 IP 주소를 식별하기 위해 사용되는 Forwarded 헤더의 대체 및 사실상의 표준 버전입니다.
    - X-Forwarded-Host : 요청 유형 헤더입니다. 호스트 HTTP 요청 헤더에서 클라이언트가 요청한 원본 호스트를 식별하는 데 사용됩니다.
    - X-Forwarded-Proto : 요청 유형 헤더입니다. 클라이언트가 프록시 또는 로드밸런서에 연결할 때 사용한 프로토콜을 식별하는 데 사용됩니다. HTTP 또는 HTTPS일 수 있습니다.
    - Via : 요청이 전송된 프록시를 서버에 알리는 데 사용되는 일반 유형 헤더입니다.
- Redirects
    - Location : 브라우저에 URL 리디렉션(상태 코드 3xx)을 요청하거나 새로 생성된 리소스(상태 코드 201)의 위치에 대한 정보를 제공하기 위해 두 가지 상황에서 사용되는 응답 헤더입니다.
- Request context
    - From : 요청하는 사용자 에이전트를 제어하는 사람의 인터넷 이메일 주소를 포함하는 데 사용되는 요청 유형 헤더입니다.
    - Host : 요청 유형 헤더입니다. 서버의 도메인 이름을 나타내는 데 사용됩니다. 서버가 사용하는 TCP(전송 제어 프로토콜) 포트 번호를 나타낼 수도 있습니다.
    - Referrer : 요청 유형 헤더입니다. 브라우저의 뒤로 가기 버튼이 작동할 수 있도록 이 새 페이지가 오는 이전 페이지 링크를 유지하는 데 사용됩니다.
    - Referrer-Policy : 응답 유형 헤더입니다. 요청에 얼마나 많은 리퍼러 정보를 포함해야 하는지 정의하는 데 사용됩니다.
    - User-Agent : 네트워크 프로토콜 피어가 웹 서버의 운영 체제 및 브라우저를 식별할 수 있는 특징적인 문자열을 허용하는 요청 헤더입니다.
- Range requests
    - Accept-Ranges : 응답 유형 헤더는 범위 시스템의 일부이기도 합니다. 이 헤더는 서버가 클라이언트의 부분 요청을 지원하기 위해 사용하는 마커 역할을 합니다.
    - Range : 서버에서 문서의 일부를 가져오는 데 사용되는 요청 유형 헤더입니다. 서버가 문서의 일부를 반환하는 경우 206(일부 콘텐츠) 상태 코드를 사용합니다.
    - If-Range : 요청 유형 헤더입니다. 범위 요청을 조건부로 만드는 데 사용됩니다.
    - Content-Range : 전신 마사지에서 부분 메시지가 속한 위치를 나타내는 응답 헤더입니다.
- Security
    - Cross-Origin-Resource-Policy : 응답 유형 헤더이며 브라우저가 지정된 리소스에 대한 노코어 교차 출처/사이트 간 요청을 차단한다는 것을 클라이언트에게 알립니다.
    - Content-Security-Policy : 웹 사이트 관리자가 리소스를 제어할 수 있도록 하는 데 사용되는 응답형 헤더입니다.
    - Content-Security-Policy-Report-Only : 웹 개발자가 정책의 효과를 주시하여 정책을 테스트할 수 있는 응답 헤더입니다.
    - Expect-CT : 사이트에 대해 잘못 발급된 인증서가 사용되는 것을 방지하고 눈에 띄지 않도록 하는 응답 헤더입니다.
    - Feature-Policy : 자체 프레임에서 기능의 사용을 허용하거나 거부하는 데 사용되는 응답 유형 헤더입니다.
    - Public-Key-Pins : 응답 헤더입니다. 특정 암호화 공개 키를 특정 웹 서버와 연결합니다.
    - Public-Key-Pins-Report-Only : 응답 유형 헤더입니다. report-uri에 보고하는 데 사용됩니다.
    - Strict-Transport-Security : 응답 유형 헤더입니다. 이는 악의적인 활동으로부터 웹사이트를 보호하고 사용자 에이전트와 웹 브라우저에 응답 헤더를 통해 연결을 처리하는 방법을 알려주는 웹 보안 정책 메커니즘입니다.
    - Upgrade-Insecure-Requests : 요청 유형 헤더입니다. 암호화되고 인증된 응답에 대한 클라이언트의 선호도를 나타내는 신호를 서버로 보냅니다.
    - X-Content-Type-Options : 응답 유형 헤더입니다. 콘텐츠 유형 헤더의 MIME 유형 헤더가 서버에 변경되지 않아야 함을 나타내는 마커 역할을 합니다.
    - X-Frame-Options : 응답 헤더입니다. 사이트의 클릭 재킹 공격을 방지하는 데 사용됩니다. 브라우저가 페이지를 <프레임>, <iframe>, <임베드> 또는 <객체>로 렌더링할 수 있도록 허용할지 여부를 정의합니다.
    - X-XSS-Protection : 응답형 헤더입니다. 사이트 간 스크립팅 필터링을 활성화하는 데 사용됩니다.
- Transfer coding
    - Transfer-Encoding : 홉별 헤더로 작동하는 응답 유형 헤더이며, 홉별 헤더 연결은 단일 전송 수준 연결이 재전송되지 않아야 합니다.
    - TE : 사용자 에이전트가 수락할 전송 인코딩을 지정하는 데 사용되는 요청 유형 헤더입니다.
    - Trailer : 청크 전송 코딩으로 인코딩된 메시지의 트레일러에 지정된 헤더 필드 집합이 있음을 나타내는 응답 헤더입니다.
- WebSockets
    - Sec-WebSocket-Accept : 응답형 헤더 카테고리입니다. 서버가 웹소켓 연결임을 이해하고 연결을 열 준비가 되었음을 클라이언트에게 알리기 위해 사용합니다.
- Other headers
    - Alt-Svc : 다른 방법으로 웹사이트에 접속하는 데 사용됩니다.
    - Date : HTTP 응답 또는 HTTP 요청과 함께 추가 정보를 전달하는 데 사용되는 일반 유형 헤더입니다.
    - Large-Allocation : 지원되는 브라우저(현재는 Firefox만)에 대용량 할당이 성공하고 일부 조각화되지 않은 메모리를 사용하여 새 프로세스를 시작할 수 있도록 메모리가 필요하다는 것을 알려주는 응답형 헤더입니다.
    - Link : HTTP 헤더에서 하나 이상의 링크를 직렬화하는 데 사용되는 엔티티 타입 헤더입니다.
    - Retry-After : HTTP 요청 또는 응답과 함께 추가 정보를 전달하는 데 사용되는 응답 유형 헤더입니다. HTTP 재시도 후 헤더는 다른 요청을 하기 전에 대기할 시간을 나타내는 HTTP 응답 헤더입니다.
    - Server-Timing : 응답 유형 헤더입니다. 이 헤더는 사용자 에이전트의 지정된 요청-응답 주기에 대해 둘 이상의 메트릭과 설명 간에 통신하는 데 사용됩니다.
    - SourceMap : 변환된 소스에서 원본 소스를 매핑하는 데 사용되는 응답 유형 헤더입니다. 예를 들어 자바스크립트 리소스는 실행 시점에 브라우저에 의해 원본에서 다른 소스로 변환됩니다.
    - X-DNS-Prefetch-Control : DNS 프리페칭을 제어하는 데 사용되는 응답 유형 헤더입니다.
