# Configuring for use with the Nginx auth_request directive
- https://oauth2-proxy.github.io/oauth2-proxy/docs/configuration/overview/#configuring-for-use-with-the-nginx-auth_request-directive

- Nginx auth_request 지시문을 사용하면 Nginx가 요청을 프록시하지 않고 202 허용됨 응답 또는 401 권한 없음 응답만 반환하는 oauth2-proxy의 /auth 엔드포인트를 통해 요청을 인증할 수 있습니다. 예를 들어

- 쿠버네티스에서 ingress-nginx를 사용하는 경우, 인그레스에 대해 반드시 kubernetes/ingress-nginx(Lua 모듈 포함)와 다음 구성 스니펫을 사용해야 합니다. auth_request_set으로 설정된 변수는 위치가 proxy_pass를 통해 처리될 때 일반 nginx 구성에서 설정할 수 없으며 Lua에서만 처리될 수 있습니다. nginxinc/kubernetes-ingress에는 Lua 모듈이 포함되어 있지 않다는 점에 유의하세요.

- 대규모 세션/OIDC 토큰이 예상되는 경우(예: MS Azure 사용) --session-store-type=redis를 사용하는 것이 좋습니다.

- 이름 대신 --cookie-name 매개변수를 통해 구성한 실제 쿠키 이름으로 대체해야 합니다. 사용자 지정 쿠키 이름을 설정하지 않은 경우 변수는 "$upstream_cookie_name_1" 대신 "$upstream_cookie__oauth2_proxy_1"이 되어야 하며 새 쿠키 이름은 "name_1=" 대신 "_oauth2_proxy_1="가 되어야 합니다.

