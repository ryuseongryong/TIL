# 인혁님
- 빅데이터지만 실시간 처리가 가능한 기술 등장(람다 아키텍쳐) -> 실시간 데이터는 DB, 과거 데이터는 빅데이터에 저장
- 새로운 기술이 등장 -> 필요한 부분은 임시 방편으로 보완 -> 또 새로운 기술이 등장
- 새로운 오픈소스가 빠르게 등장하는 중
- 블로그 내용
    - 카프카를 퍼블릭 클라우드에서 활용할 떄의 문제에 대해서 얘기함
    - 카프카는 신뢰성을 보장(프로듀서는 메시지를 쌓음, 컨슈머는 메시지를 소비, ack를 0으로 하면 안전하게 보관되었는지 확인되지 않지만, 빠르게 송신 가능, 반면 ack를 3, 5로 저장하면 3군데, 5군데 브로커에 저장된 것을 확인한 다음 송신)
    - 물리적으로 분리된 곳에 저장하는 것이 일반적 = 카프카의 경우 메시지 한 번 송신 때마다 존 간의 비용이 최소 2번 이상 발생
    - 프로듀서 -> 리더 브로커 -> 다른 존 브로커에 전달

- WarpStream : 카프카 프로듀서 구현 + S3 저장, 컨슈밍은 S3를 읽어서 진행. EC2 - S3 비용은 무료. S3 리플리케이션으로 안정적인 운영이 가능.
- 비용 절감은 가능, 레이턴시는 문제
- 카프카의 ACK 안정성 : 3개의 브로커의 페이지 캐시에 메시지 저장
- 카프카 서버 셧다운 시, 복구 가능(fsync를 주기적으로 실행)
- 42dot 실시간 데이터 엔지니어
- Postgres: a better message queue than kafka?
    - kafka 운영 인력 비용이 크기 때문에 큰 문제가 없으면 postgresql을 사용하라는 것.
    - ksql
- scyllaDB, cassandra와 API적으로 호환됨(OLAP용)
    - kafka없이 scyllaDB를 메시지 큐로 사용
- ceph vs seaweedfs

# rust
- 구조체(https://fluoridated-wholesaler-418.notion.site/60e0315e6d3e4f7099b775273e5cd721)
    - 메모리 관리를 위해서 내부적으로 copy가 발생하는 등 추가적인 부분이 있음
    - string from -> heap
    - peter string은 그대로, ref가 이동
    - into_iter는 ownership move가 발생, iter는 ref
    - enum : 다른 타입인데 똑같은 형식으로 사용 가능
        - error의 예시 : error의 형식에 enum을 사용하면 됨(string, structure 등 다 다른 경우에, superclass, subclass로 사용하는 것외 에도 위와 같은 경우도 동일함)
        - 메모리 해지자동, 데이터 처리, loop 단순
        - type = result 접근 시 항상 Error인지 확인해야 함
    - option
    - question marks : enum -> error type ? 적용
        - ? : err cascade / match + err와 같음, unwrap : err -> panic
    - collect, next : map return is iter - lazy evaluation(spark도 mapping할 때는 동일한 부분)

- scyllaDB 개발자들이 KVM(linux kernal hypervisor) 개발자임. kernal cpo polling 등 까지 개발해서 cassandra 대비 월등한 성능.