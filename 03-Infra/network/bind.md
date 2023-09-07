# Address Binding
- https://docs.oracle.com/cd/E19455-01/806-1017/sockets-47146/index.html

- TCP와 UDP는 로컬IP주소, 로컬 포트번호, 외부 IP주소, 외부 포트번호의 4-튜플을 사용하여 주소를 지정한다. TCP는 이 4튜플이 고유해야 한다. UDP는 그렇지 않다. 호스트가 여러 네트워크에 존재할 수 있고 할당된 포트번호 집합에 사용자가 직접 액세스 할 수 없기 때문에 사용자 프로그램이 로컬 주소와 로컬 포트에 사용할 적절한 값을 항상 알고 있기를 기대하는 것은 비현실적이다. 이러한 문제를 방지하려면 주소의 일부를 지정하지 않은 채로 두었다가 필요할 때 시스템이 해당 부분을 적절하게 할당하도록 할 수 있다. 이러한 튜플의 다양한 부분은 소켓 API의 다양한 부분에서 지정할 수 있다.
- bind(3Socket) : Local address / Local port / Both
- connect(3Socket) : Foreign address and Foreign port

- accept(3SOCKET)을 호출하면 외국 클라이언트로부터 연결 정보를 가져오기 때문에 (accept(3SOCKET) 호출자가 아무것도 지정하지 않았음에도 불구하고) 로컬 주소와 포트가 시스템에 지정되고 외국 주소와 포트가 반환됩니다.

- listen(3SOCKET)을 호출하면 로컬 포트가 선택될 수 있습니다. 로컬 정보를 할당하기 위해 명시적으로 bind(3SOCKET)를 수행하지 않은 경우, listen(3SOCKET)은 임시 포트 번호를 할당합니다.

- 특정 포트에 상주하지만 어떤 로컬 주소가 선택되든 상관하지 않는 서비스는 bind(3SOCKET) 자체를 해당 포트에 연결하고 로컬 주소를 지정하지 않을 수 있습니다(<netinet/in.h>에서 상수 값을 갖는 변수인 in6addr_any로 설정). 로컬 포트를 고정할 필요가 없는 경우 listen(3SOCKET)을 호출하면 포트가 선택됩니다. IN6ADDR_ANY 주소 또는 포트 번호 0을 지정하는 것을 와일드카드라고 합니다. (AF_INET의 경우, in6addr_any 대신에 INADDR_ANY가 사용됩니다.)

- 와일드카드 주소는 인터넷 제품군에서 로컬 주소 바인딩을 단순화합니다. 아래 샘플 코드는 특정 포트 번호인 MYPORT를 소켓에 바인딩하고 로컬 주소는 지정하지 않은 채로 둡니다.

```
Example 2-17 Bind Port Number to Socket

#include <sys/types.h>
#include <netinet/in.h>
...
struct sockaddr_in6 sin;
...
		s = socket(AF_INET6, SOCK_STREAM, 0);
		bzero (&sin6, sizeof (sin6));
		sin.sin6_family = AF_INET6;
		sin.sin6_addr.s6_addr = in6addr_any;
		sin.sin6_port = htons(MYPORT);
		bind(s, (struct sockaddr *) &sin, sizeof sin);

```

- 호스트의 각 네트워크 인터페이스에는 일반적으로 고유한 IP 주소가 있습니다. 와일드카드 로컬 주소가 있는 소켓은 지정된 포트 번호로 향하는 메시지를 수신하여 호스트에 할당된 가능한 모든 주소로 보낼 수 있습니다. 예를 들어 호스트에 주소가 128.32.0.4 및 10.0.0.78인 인터페이스가 두 개 있고 예제 2-17에서와 같이 소켓이 바인딩된 경우 프로세스는 128.32.0.4 또는 10.0.0.78로 주소가 지정된 연결 요청을 수락할 수 있습니다. 특정 네트워크의 호스트만 연결할 수 있도록 서버는 해당 네트워크의 인터페이스 주소를 바인딩합니다.

- 마찬가지로 로컬 포트 번호를 지정하지 않을 수 있으며(0으로 지정), 이 경우 시스템에서 포트 번호를 선택합니다. 예를 들어 특정 로컬 주소를 소켓에 바인딩하되 로컬 포트 번호는 지정하지 않을 수 있습니다:



