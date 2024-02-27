use std::str::FromStr;
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




impl FromStr for Method {
    type Err = MethodError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "GET" => Ok(Self::GET),
            "DELETE" => Ok(Self::DELETE),
            "POST" => Ok(Self::POST),
            "PUT" => Ok(Self::PUT),
            "HEAD" => Ok(Self::HEAD),
            "CONNECT" => Ok(Self::CONNECT),
            "OPTIONS" => Ok(Self::OPTIONS),
            "TRACE" => Ok(Self::TRACE),
            "PATCH" => Ok(Self::PATCH),
            _ => Err(MethodError),
        }
    }
}

pub struct MethodError;