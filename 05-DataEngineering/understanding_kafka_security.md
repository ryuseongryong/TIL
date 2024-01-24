- https://sharebigdata.wordpress.com/2018/01/09/understanding-kafka-security/
# Understanding Kafka Security
실제 구현을 시작하기 전에 전반적인 보안 구조를 이해하는 데 도움이 되는 몇 가지 중요한 속성/용어를 설명합니다.

# 무엇을 인증하나요?

인증 대상을 설정할 수 있습니다:

- 브로커 서버: 한 브로커가 다른 브로커에 연결할 수 있어야 하는 경우. 인증은 다음을 사용하여 수행됩니다: SSL 또는/또는 SASL(일반/SCRAM/GSSAPI)
- 클라이언트 머신: 컴퓨터가 카프카 브로커에 연결할 수 있는 경우. 이 작업은 인증 기관에서 생성/서명해야 하는 SSL 인증서를 사용하여 수행됩니다.
- 클라이언트/사용자/생산자/소비자: 사용자가 Kafka에 연결할 수 있는 경우. 이는 다음을 사용하여 수행됩니다: SASL(일반/스크램/GSSAPI)

# 사용되는 인증은 어디서/어떻게 정의하나요?

브로커 서버: 
a) 카프카 브로커를 시작하면, 서버 속성에 정의된 security.inter.broker.protocol을 확인하여 브로커 간 통신 시 어떤 보안 프로토콜을 사용해야 하는지 확인합니다.유효한 값은 다음과 같습니다:
일반 텍스트: 일반 텍스트만 - 전송되는 데이터가 일반 텍스트(암호화되지 않음)입니다.
SSL: SSL만 - 전송되는 데이터가 암호화됩니다.
SASL_PLAINTEXT: 일반 텍스트 프로토콜을 통한 일부 SASL(SCRAM/PLAIN/GSSAPI) 프로토콜
SASL_SSL: 일부 SASL(SCRAM/PLAIN/GSSAPI) over SSL 프로토콜

Example:
```
security.inter.broker.protocol=PLAINTEXT    # Default
security.inter.broker.protocol=SSL
security.inter.broker.protocol=SASL_PLAINTEXT
security.inter.broker.protocol=SASL_SSL
```

b) 동시에, 브로커 간 인증에 사용되는 메소드/메커니즘을 확인하기 위해 sasl.mechanism.inter.broker.protocol이 사용됩니다. 이 속성은 : 브로커 간 통신에 사용되는 SASL 메커니즘입니다.

유효한 값은 다음과 같습니다:

일반: SASL/PLAIN은 보안 인증을 구현하기 위해 일반적으로 암호화를 위해 TLS와 함께 사용되는 간단한 사용자 이름/암호 인증 메커니즘으로, 사용자 이름은 ACL 등의 구성을 위해 인증된 주체로 사용됩니다.

SCRAM: 솔티드 챌린지 응답 인증 메커니즘(SCRAM)은 사용자 이름/비밀번호 인증을 수행하는 기존 메커니즘의 보안 문제를 해결하는 SASL 메커니즘 제품군으로, 사용자 이름은 ACL 등의 구성을 위해 인증된 주체로 사용됩니다. Kafka의 기본 SCRAM 구현은 SCRAM 자격 증명을 Zookeeper에 저장합니다.

GSSAPI: 우리가 모두 알고 있는 Kerberos.

Example:

```
sasl.mechanism.inter.broker.protocol=GSSAPI
sasl.mechanism.inter.broker.protocol=PLAIN
sasl.mechanism.inter.broker.protocol=SCRAM-SHA-256 (or SCRAM-SHA-512
```

c) 지금까지는 브로커가 SASL(일반/스크램/GSSAPI)을 사용해야 한다고 정의했습니다. 이제 브로커가 이 SASL 인증에 어떤 자격 증명을 사용할지 알려줄 차례입니다. 따라서 이러한 자격 증명을 사용하기 시작한 브로커는 클러스터에 참여할 수 있습니다(자세한 방법 참조). 보안 메커니즘에 대한 이러한 자격 증명 관련 세부 정보는 $KAFKA_HOME/config/jaas.conf 파일에 정의됩니다.
이 파일은 하나 이상의 인증 방법(우리가 사용하려는)으로 만들어집니다.

왜 하나 이상의 방법이 필요한가요?
이는 카프카 인터 브로커 인증과는 아무런 관련이 없습니다. 브로커는 'sasl.mechanism.inter.broker.protocol'에 정의된 하나의 방법만 선택합니다. 그러나 클라이언트/사용자 인증에 동시에 여러 메커니즘을 사용할 수 있습니다(나중에 참조).

아래는 3개의 SASL을 모두 정의하고 있지만, 'sasl.mechanism.inter.broker.protocol'의 값에 따라 브로커 인증에는 하나만 사용됩니다.

$KAFKA_HOME/config/jaas.conf

```
KafkaServer {
 org.apache.kafka.common.security.scram.ScramLoginModule required
 username="admin"
 password="admin-secret";

org.apache.kafka.common.security.plain.PlainLoginModule required
 username="admin"
 password="admin-secret"
 user_admin="admin-secret"
 user_alice="alice-secret"
 user_nrsh13="nrsh13-secret";

com.sun.security.auth.module.Krb5LoginModule required
 useKeyTab=true
 storeKey=true
 keyTab="/etc/security/keytabs/kafka_server.keytab"
 principal="kafka/kafka1.hostname.com@EXAMPLE.COM";
};

```

Kafka 프로세스가 시작되기 전에 환경 변수(예: .bashrc)에 $KAFKA_HOME/config/jaas.conf 파일이 전달됩니다. Kafka는 jaas 파일을 읽고 필요한 인증을 활성화합니다.
따라서 클러스터에 참여하고자 하는 모든 브로커는 jaas.conf로 시작해야 하며, 그렇지 않으면 인증에 실패하여 클러스터에 참여할 수 없습니다.

```
export KAFKA_HOME=/usr/local/kafka
export KAFKA_PLAIN_PARAMS="-Djava.security.auth.login.config=/usr/local/kafka/config/jaas.conf"
export KAFKA_OPTS="$KAFKA_PLAIN_PARAMS $KAFKA_OPTS"
export PATH="$PATH:$ZOOKEEPER_HOME/bin:$KAFKA_HOME/bin"

```

클라이언트 머신 및 사용자: 생산자/소비자 실행을 위해 특정 머신을 사용할 수 있는지 여부를 의미합니다. SSL이 활성화된 경우, 클라이언트 머신은 생산자/소비자를 실행하는 동안 client.properties에 키 저장소/트러스트 저장소 관련 세부 정보(생산자/소비자 실행 중 -producer.config 또는 -consumer.config 매개변수 값에 사용됨)를 제공하여 자신을 인증해야 하며, 동시에 'sasl.enabled.mechanisms' 아래에 정의된 SASL 인증 메커니즘에 따라 사용자별 세부 정보가 전달됩니다. 이 값은 jaas.conf에 정의된 모든 SASL 인증 메커니즘에 따라 SCRAM-SHA-256,PLAIN,GSSAPI(쉼표로 구분)와 같은 여러 값을 가질 수 있습니다.
이 속성과 jaas.conf는 사용자에게 클러스터에서 어떤 인증 메커니즘을 사용할 수 있는지 알려주며, 사용자/프로듀서/소비자 누구나 사용할 수 있습니다.

예시: 아래에서는 SASL(SCRAM) + SSL로 사용자를 인증하고 싶다는 client.properties를 사용하고 있습니다.

```
# Remove below 5 lines if NO SASL is required/enabled
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
 username="hduser" \
 password="hduser-secret";
security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-256

ssl.keystore.location=/tmp/apache-kafka.abc.com/node.ks
ssl.keystore.password=password
ssl.key.password=password
#security.protocol=SSL # Include if NO SASL is enable/required
ssl.truststore.location=/tmp/apache-kafka.abc.com/node.ts
ssl.truststore.password=password

```

또는 SASL(일반) + SSL의 경우:

```
# Remove below 5 lines if NO SASL is required/enabled
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required \
 username="nrsh13" \
 password="nrsh13-secret";
security.protocol=SASL_PLAINTEXT
sasl.mechanism=PLAIN

ssl.keystore.location=/tmp/apache-kafka.abc.com/node.ks
ssl.keystore.password=password
ssl.key.password=password
#security.protocol=SSL # Include if NO SASL is enable/required
ssl.truststore.location=/tmp/apache-kafka.abc.com/node.ts
ssl.truststore.password=password

```

또는 SASL(GSSAPI) + SSL의 경우:

```
# Remove below 5 lines if NO SASL is required/enabled
sasl.jaas.config=com.sun.security.auth.module.Krb5LoginModule required \
 useKeyTab=true \
 storeKey=true \
 keyTab="/apphome/hduser/hduser.keytab"
 principal="hduser@EXAMPLE.COM";

ssl.keystore.location=/tmp/apache-kafka.abc.com/node.ks
ssl.keystore.password=password
ssl.key.password=password
#security.protocol=SSL # Include if NO SASL is enable/required
ssl.truststore.location=/tmp/apache-kafka.abc.com/node.ts
ssl.truststore.password=password

```

Listeners 속성 및 사용 가능한 값은 무엇인가요? Listeners 속성은 프로토콜, SASL, 호스트 이름, 포트와 같은 카프카 브로커 세부 정보의 조합으로, 사용 가능한 값은 다음과 같습니다:

```
# No Authentication. DEFAULT
Listeners=PLAINTEXT://apache-kafka.abc.com:9092
# SSL is enabled 
listerners=SSL://apache-kafka.abc.com:9092
# Any SASL is enabled but not SSL
listeners=SASL_PLAINTEXT://apache-kafka.abc.com:9092
# Any SASL with SSL 
listeners=SASL_SSL://apache-kafka.abc.com:9092

```