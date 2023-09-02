# Access logging
- https://www.envoyproxy.io/docs/envoy/latest/configuration/observability/access_log/usage#config-access-log-format-strings

## Configuration
- Access logs are configured as part of the HTTP connection manager config, TCP Proxy, UDP Proxy or Thrift Proxy.
    - v3 API reference

## Format Rules
- 액세스 로그 형식에는 관련 데이터를 추출하여 삽입하는 명령 연산자가 포함되어 있다. 두 가지 형식을 지원한다. "format strings", "format dictionaries". 두 경우 모두 명령 연산자를 사용하여 관련 데이터를 추출한 다음 지정된 로그 형식에 삽입한다. 한 번에 하나의 액세스 로그 형식만 지정할 수 있다.

## Format Strings
- 서식 문자열은 일반 문자열로, 서식 키를 사용하여 지정한다. 여기에는 명령 연산자 또는 일반 문자열로 해석되는 다른 문자가 포함될 수 있다. 액세스 로그 포맷터는 새 줄 바꿈에 대해 어떤 가정도 하지 않으므로 형식 문자열의 일부로 지정해야 한다. 예는 default format을 참조해라.

## Default Format String
- 사용자 지정 형식 문자열을 지정하지 않으면 Envoy는 다음 기본 형식을 사용합니다:
- ```
    [%START_TIME%] "%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%"
    %RESPONSE_CODE% %RESPONSE_FLAGS% %BYTES_RECEIVED% %BYTES_SENT% %DURATION%
    %RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)% "%REQ(X-FORWARDED-FOR)%" "%REQ(USER-AGENT)%"
    "%REQ(X-REQUEST-ID)%" "%REQ(:AUTHORITY)%" "%UPSTREAM_HOST%"\n
  ```