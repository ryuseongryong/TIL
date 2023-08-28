# Address Binding
- https://docs.oracle.com/cd/E19455-01/806-1017/sockets-47146/index.html

- TCP와 UDP는 로컬IP주소, 로컬 포트번호, 외부 IP주소, 외부 포트번호의 4-튜플을 사용하여 주소를 지정한다. TCP는 이 4튜플이 고유해야 한다. UDP는 그렇지 않다. 호스트가 여러 네트워크에 존재할 수 있고 할당된 포트번호 집합에 사용자가 직접 액세스 할 수 없기 때문에 사용자 프로그램이 로컬 주소와 로컬 포트에 사용할 적절한 값을 항상 알고 있기를 기대하는 것은 비현실적이다. 이러한 문제를 방지하려면 주소의 일부를 지정하지 않은 채로 두었다가 필요할 때 시스템이 해당 부분을 적절하게 할당하도록 할 수 있다. 이러한 튜플의 다양한 부분은 소켓 API의 다양한 부분에서 지정할 수 있다.
- bind(3Socket) : Local address / Local port / Both
- connect(3Socket) : Foreign address and Foreign port
