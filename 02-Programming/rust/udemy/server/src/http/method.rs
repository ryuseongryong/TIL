pub enum Method {
    GET,
    DELETE,
    POST, // = 5를 설정하여, variant 설정 가능, 이후로 1씩 증가된 값으로 설정됨,
    PUT, // 이를 응답코드에서 사용할 수 있음 404 Not Found
    HEAD,
    CONNECT,
    OPTIONS,
    TRACE,
    PATCH,
}
