- https://www.crowdstrike.com/guides/kafka-logging/
# Kafka logging guide: the basics

Apache Kafka는 오픈소스 이벤트 스트리밍 플랫폼으로, 데이터를 이벤트로 취급하여 분산된 내결함성 방식으로 순서화된 레코드 시퀀스로 저장합니다. 오늘날의 애플리케이션은 작업을 수행하기 위해 끊임없이 동적 정보에 의존하고 있기 때문에, Kafka를 사용하면 애플리케이션 서비스와 사용자가 지연 시간 없이 원활하게 데이터에 액세스할 수 있습니다.

이 글은 카프카 로깅에 대한 시리즈 중 1부입니다. 1부에서는 기본 사항을 다룹니다. Kafka와 아키텍처, 주요 구성 요소에 대한 간략한 개요를 제공합니다. 그런 다음 메시지를 조작하고 카프카 생태계 내에서 데이터가 어떻게 흐르는지 추적하는 데 사용되는 주요 명령어를 다룹니다.

## Overview of Kafka Architecture
Kafka는 로그라는 정렬된 데이터 구조에 메시지를 저장합니다. 이는 익숙한 기존 로그와는 다릅니다. 대신, Kafka 로그는 서버에 분산되어 불변의 방식으로 레코드를 보관하는 네임드 구조입니다. 이러한 명명된 구조를 토픽이라고 합니다. 로그는 Kafka 클러스터의 모든 노드에 복제되고 파티션화되어 소비자들이 그에 따라 구독하고 항상 데이터를 사용할 수 있도록 합니다.
https://www.crowdstrike.com/wp-content/uploads/2022/12/apache-kafka-example-architecture.png

### Kafka Components
위의 다이어그램에서는 단일 클러스터 환경에서 카프카 생태계를 구성하는 모든 주요 구성 요소를 관찰할 수 있습니다.

Brokers
브로커는 스토리지 디스크가 있는 단일 노드로, 레코드를 올바른 순서로 저장하고 서비스에서 액세스할 수 있도록 데이터를 노출하는 역할을 담당합니다. 브로커는 카프카 서버라고도 하며, 자체적인 상태를 갖지 않습니다.

Producers
프로바이더는 이벤트를 카프카 서버로 전송하는 엔티티입니다. 프로듀서는 애플리케이션, 서비스 또는 타사 도구가 될 수 있으며, 프로듀서 API를 사용하여 카프카 클러스터와 상호 작용합니다.
서버와 상호 작용하도록 프로듀서가 초기화되면, 프로듀서 ID(PID)라는 고유 식별자가 할당됩니다. PID는 0에서 시작하여 메시지가 게시될 때마다 증가하는 고유 카운터 변수입니다. 이는 데이터에서 발생하는 중복 문제를 해결하는 편리한 속성입니다.

Consumers
소비자는 소비자 API를 사용하여 올바른 키를 제공함으로써 Kafka 서버에서 이벤트 로그를 가져오는 엔티티입니다.

Topics
Kafka 노드에서 수신된 레코드는 정렬된 추가 전용 큐에 배치됩니다.

https://www.crowdstrike.com/wp-content/uploads/2022/12/Overview-of-inserting-a-record-in-a-log.png

실제 비즈니스 애플리케이션에서는 레코드에 지속적으로 액세스하는 많은 프로세스와 서비스가 있으며, 이로 인해 추가 전용 대기열을 처리할 때 성능 저하와 같은 문제가 발생할 수 있습니다. 이 문제를 완화하기 위해 Kafka에서는 각 로그에 고유 식별자를 할당하여 유사한 데이터를 그룹화할 수 있는 다양한 사용 사례에 대한 여러 개의 로그를 생성할 수 있습니다. 이렇게 이름이 지정된 로그를 토픽이라고 합니다.

https://www.crowdstrike.com/wp-content/uploads/2022/12/apache-kafka-Topics-overview.png

각 Kafka 토픽의 로그는 둘 이상의 소비자가 하나의 로그를 구독할 수 있도록 분할되어 있습니다. 이렇게 하면 카프카는 특정 토픽을 구독한 사용자에게만 레코드를 전송합니다. 특정 레코드를 가져오려면 파티션의 오프셋과 특정 토픽에 대한 레코드의 조합인 키를 제공하면 됩니다.

다음 예를 살펴보세요:

https://www.crowdstrike.com/wp-content/uploads/2022/12/Demonstration-of-keys-used-by-individual-records.png

Id가 612인 프로듀서는 값이 3인 시퀀스 카운터를 사용하여 첫 번째 파티션에 레코드(h,a)를 보냅니다. 그러면 브로커는 프로듀서 ID를 시퀀스 번호와 결합하여 파티션된 토픽에 씁니다.

소비자는 키 [12]를 사용하여 두 번째 파티션에서 레코드를 가져옵니다. 첫 번째 요소는 파티션 번호이고, 두 번째 문자는 읽을 메시지의 오프셋입니다.

이를 통해 카프카는 분산 아키텍처에서 원자성을 달성합니다.

## Working with Kafka Logs
### Data Relevance
보시다시피, Kafka는 로그에 지속적으로 데이터를 추가하고 있습니다. 개발자와 테스터가 버그나 디버그 메시지와 같은 특정 정보를 추적하기 위해 모든 레코드를 스크롤하는 것은 지루한 일입니다. 토픽을 최대한 깔끔하게 유지하려면 어떤 정보를 게시하거나 무시해야 하는지에 대한 강력한 제어가 필요합니다.

아래 서비스의 로그 파일을 생각해 보세요:
```
178.62.253.136 - - [10/Sep/2022:22:53:52 +0800] "Server 01 is ready to peer"
178.62.253.136 - - [10/Sep/2022:22:53:52 +0800] "Server 01 is ready to peer"
134.122.184.26 - - [10/Sep/2022:23:02:28 +0800] "Server 05 is ready to peer "-" "<title>(.*?)</title>"
172.104.229.176 - - [10/Sep/2022:23:05:41 +0800] "Server 01 is ready to peer94 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
70.35.198.178 - - [10/Sep/2022:23:21:22 +0800] "Server 01 is ready to peer.4322)"
104.248.51.8 - - [10/Sep/2022:23:27:41 +0800] "Server 02 is ready to peer Firefox/79.0"
46.19.141.122 - - [10/Sep/2022:23:37:03 +0800] "Server 01 is ready to peer Firefox/77.0"
74.208.182.71 - - [10/Sep/2022:23:54:47 +0800] "Server 01 connected "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"
179.60.150.88 - - [10/Sep/2022:23:56:36 +0800] "\x03\x00\x00/*\\x00Cookie: mstshash=Administr" 400 182 "-" "-"
88.208.199.38 - - [11/Sep/2022:00:01:16 +0800] "Server 01 disconnected Firefox/63.0"
192.241.220.53 - - [11/Sep/2022:00:10:01 +0800] "Server 01 is ready to peer" 400 280 "-" "Mozilla/5.0 zgrab/0.x"
```
"서버 01이 피어링할 준비가 되었습니다."라는 메시지는 애플리케이션 로그와 무관할 수 있으며 Kafka 주제에 저장할 필요가 없습니다.

### Retention Policies
여러 생산자로부터 레코드가 계속 흘러나오기 때문에 Kafka 로그의 크기는 계속 커질 것입니다. 짧은 기간 내에 로그는 디스크 공간을 차지하게 되고, 저장 용량을 늘리지 않는 한 새로운 메시지를 저장하는 것은 번거로운 일이 됩니다.

물론 이것은 비용 효율적이지 않습니다. 시간이 지날수록 오래된 데이터는 덜 중요해지기 때문에 그냥 없애버리고 싶을 것입니다. 이를 위해 Kafka는 일정 기간(기본값 168시간) 동안 로그를 보존하는 시간 기반 정책과 같은 보존 정책을 제공합니다.

### Enabling Logs
Kafka는 각각 다른 사용 사례를 처리하도록 설계된 8개의 로깅 레벨이 있는 Log4j 2 로깅 서비스를 사용합니다. 로깅을 활성화하려면 Log4j 속성을 업데이트하기만 하면 됩니다.

```
log4j.rootLogger=Trace, kafka
log4j.appender.kafka=com.cloudera.kafka.log4jappender.KafkaLog4jAppender
log4j.appender.stdout=org.apache.log4j.ConsoleAppender
log4j.appender.stdout.Target=System.out
```

## Kafka Commands to Manipulate Records
Kafka는 다양한 API와 인터페이스를 통해 클러스터를 조작할 수 있는 많은 명령어를 제공합니다. Kafka 로그부터 시작하기 위해 사용할 수 있는 주요 명령어를 살펴보겠습니다.

### Create a Kafka Topic
카프카 토픽을 만들려면 카프카가 설치된 서버에서 카프카 토픽 API를 호출하면 됩니다. flag 명령을 사용하는 것 외에도 다음 매개 변수를 포함해야 합니다:
- --topic NAME 토픽의 이름을 지정
- --partition NUMBER 파티션의 개수를 지정
- --replication NUMBER 카프카가 유지해야 하는 복사본 수를 지정
- --bootstrap-server ADDRESS 카프카 클러스터에 처음 연결할 때 사용되는 노드 주소를 지정

다음 명령은 두 개의 파티션과 각 파티션의 복제본 두 개가 있는 ls-topic이라는 토픽을 생성하며, 처음에는 로컬 호스트의 포트 9062에서 수신 대기 중인 서버에 연결합니다.
```
sh kafka-topics.sh --create --topic ls-topic --partitions 2 --replication-factor 2 --bootstrap-server localhost:9062
```

### List all Kafka Topics
모든 Kafka 토픽을 나열하려면 --listcommand를 사용하고 --bootstrap-server를 사용하여 Kafka 클러스터 연결 주소를 지정하면 됩니다. 또한 --exclude-internal을 사용하여 Kafka에서 생성한 내부 토픽을 숨길 수 있습니다.

```
sh kafka-topics.sh --list --exclude-internal --bootstrap-server localhost:9062
```

### Delete a Kafka Topic
카프카 토픽을 삭제하려면 --deleteflag를 사용합니다.
```
sh kafka-topics.sh --delete --topic ls-topic --bootstrap-server localhost:9062
```

### Read all records from a Kafka Topic
특정 카프카 토픽의 모든 메시지를 읽으려면 소비자 API에 --from-beginningflag 매개변수를 지정하세요.

### Publish to a Kafka Topic
Kafka 토픽에 레코드를 게시하려면, 게시할 레코드와 함께 --topic 및 --bootstrap-server를 지정하는 프로듀서 API를 사용하면 됩니다.


