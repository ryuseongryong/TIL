use http::request::Request;
use server::Server;

mod server;
fn main() {
    let server = Server::new("127.0.0.1:8080".to_string());
    server.run();
}

mod http {
    pub mod request {
        use super::method::Method;
        pub struct Request {
            path: String,
            query_string: Option<String>,
            method: Method,
        }
    }
    
    pub mod method {
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
    }
}