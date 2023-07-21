fn main() {
    let server = server::Server::new("127.0.0.1:8080".to_string());
    server.run();
}

mod server {
    pub struct Server {
        addr: String,
    }
    
    impl Server {
        pub fn new(addr: String) -> Self {
            Self {
                addr
            }
        }
    
        pub fn run(self) {
            println!("Listening on {}", self.addr)
        }
    }

}

struct Request {
    path: String,
    query_string: Option<String>,
    method: Method,
}

enum Method {
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

/*
GET /user?id=10 HTTP/1.1\r\n
HEADERS \r\n
BODY
 */