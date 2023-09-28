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