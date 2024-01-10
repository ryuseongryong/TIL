- https://betterstack.com/community/guides/logging/vector-explained/

# How to Colect, Process, and Ship Log Data with Vector

대부분의 시스템에서 로그는 시스템의 상태를 유지하고 문제를 해결하는 데 매우 중요한 역할을 합니다. 애플리케이션별 로그 기록은 유용하지만 포괄적인 인사이트를 얻기에는 부족한 경우가 많습니다. 보다 심층적인 이해를 위해서는 Docker 컨테이너, syslog, 데이터베이스 등 다양한 소스에서 로그를 수집하고 분석해야 합니다. 이때 로그 애그리게이터가 필요합니다. 로그 수집기는 다양한 소스에서 로그를 수집, 변환, 중앙 위치로 라우팅하여 효과적으로 분석하고 문제를 해결하는 능력을 향상시키도록 설계된 도구입니다. Vector, Fluentd, Filebeat 등 많은 로그 수집기를 사용할 수 있습니다. 하지만 이 글에서는 Vector에 초점을 맞추겠습니다.

Vector는 Datadog에서 개발한 강력한 오픈 소스 로그 수집기입니다. 여러 소스에서 로그를 원활하게 가져오고, 필요에 따라 데이터를 변환하고, 원하는 대상으로 라우팅하여 통합 가시성 파이프라인을 구축할 수 있도록 지원합니다. Vector는 메모리 관리 기능으로 유명한 프로그래밍 언어인 Rust로 구현되어 가벼운 무게, 뛰어난 속도, 메모리 효율성이 특징입니다.

Vector는 다양한 데이터 소스 및 대상과의 통합을 가능하게 하는 플러그인 지원, 실시간 모니터링, 강력한 보안 기능 등 로그 애그리게이터에서 흔히 볼 수 있는 풍부한 기능 세트를 제공합니다. 또한, Vector는 고가용성을 위해 구성할 수 있어 성능 저하 없이 상당한 양의 로그를 처리할 수 있습니다.

이 종합 가이드에서는 벡터를 활용하여 로그를 효과적으로 수집, 전달, 관리하는 방법을 살펴봅니다. 먼저 파일에 로그를 기록하는 샘플 애플리케이션을 구축하는 것으로 시작합니다. 그런 다음, 벡터를 사용하여 로그를 읽고 콘솔로 전달하는 방법을 안내합니다. 마지막으로 로그 변환, 중앙 집중화, 모니터링을 통해 벡터 기반 로그 관리 설정의 상태와 안정성을 보장하는 방법을 살펴봅니다.

## Prerequisites
이 튜토리얼을 완료하려면 sudo 권한이 있는 루트 사용자가 아닌 사용자가 있는 시스템이 필요합니다. 선택 사항으로 시스템에 Docker 및 Docker Compose를 설치할 수 있습니다. 로그 수집기가 익숙하지 않다면 이 문서에서 로그 수집기의 장점에 대해 자세히 알아볼 수 있습니다.

이러한 요구 사항을 충족한 후에는 애플리케이션, 구성 및 Docker파일을 저장할 루트 프로젝트 디렉터리를 만듭니다:

```
mkdir log-processing-stack

```

이 디렉토리는 튜토리얼을 진행하면서 프로젝트의 기초가 될 것입니다.

그런 다음 디렉터리로 이동합니다:

```
cd log-processing-stack

```

그런 다음 데모 애플리케이션 전용 디렉터리를 만듭니다. 그런 다음 새로 만든 디렉토리로 이동합니다:

```
mkdir logify && cd logify

```

## Developing a demo logging application
이 섹션에서는 일정한 간격으로 로그를 생성하는 샘플 Bash 스크립트를 만들 것입니다.

logify 디렉터리에서 원하는 텍스트 편집기를 사용하여 logify.sh라는 이름의 새 파일을 만듭니다:

```
nano logify.sh

```

logify.sh 파일에 다음 코드를 추가합니다:

```
#!/bin/bash
filepath="/var/log/logify/app.log"

create_log_entry() {
    local info_messages=("Connected to database" "Task completed successfully" "Operation finished" "Initialized application")
    local random_message=${info_messages[$RANDOM % ${#info_messages[@]}]}
    local http_status_code=200
    local ip_address="127.0.0.1"
    local emailAddress="user@mail.com"
    local level=30
    local pid=$$
    local ssn="407-01-2433"
    local time=$(date +%s)
    local log='{"status": '$http_status_code', "ip": "'$ip_address'", "level": '$level', "emailAddress": "'$emailAddress'", "msg": "'$random_message'", "pid": '$pid', "ssn": "'$ssn'", "time": '$time'}'
    echo "$log"
}

while true; do
    log_record=$(create_log_entry)
    echo "${log_record}" >> "${filepath}"
    sleep 3
done

```

create_log_entry() 함수는 HTTP 상태 코드, IP 주소, 임의의 로그 메시지, 프로세스 ID, 주민등록번호, 타임스탬프 등의 필드를 포함하는 JSON 형식의 로그 항목을 생성합니다. 그런 다음 스크립트는 이 함수를 반복적으로 호출하여 로그 항목을 생성하고 /var/log/logify 디렉터리에 있는 지정된 로그 파일에 추가하는 무한 루프에 들어갑니다.

이 예제에는 이메일 주소, 주민등록번호, IP 주소와 같은 개인 정보가 포함되어 있지만, 이는 주로 데모용이라는 점에 유의하세요. 벡터는 개인정보 필드를 제거하거나 삭제하여 민감한 데이터를 필터링할 수 있으며, 이는 데이터 프라이버시 및 보안을 유지하는 데 매우 중요합니다. 이를 구현하는 방법은 튜토리얼의 뒷부분에서 배우게 됩니다.

작업을 마치면 파일에 변경한 내용을 저장합니다. 다음 명령을 실행하여 스크립트를 실행합니다:

```
chmod +x logify.sh

```

그런 다음 애플리케이션이 로그를 저장할 /var/log/logify를 만듭니다:

```
sudo mkdir /var/log/logify

```

디렉터리 소유권을 현재 로그인한 사용자가 포함된 $USER 환경 변수에 지정된 사용자로 변경합니다:

```
sudo chown -R $USER:$USER /var/log/logify/

```

이제 마지막에 &를 추가하여 백그라운드에서 스크립트를 실행합니다:

```
./logify.sh &

```

bash 작업 제어 시스템은 프로세스 ID가 포함된 출력을 생성합니다:

```
[1] 2933

```

이 경우 프로세스 ID(이 경우 2933)는 나중에 스크립트를 종료하는 데 사용됩니다.

다음으로 tail 명령을 사용하여 로그 파일의 내용을 확인합니다:

```
tail -n 4 /var/log/logify/app.log

{"status": 200, "ip": "127.0.0.1", "level": 30, "emailAddress": "user@mail.com", "msg": "Task completed successfully", "pid": 12655, "ssn": "407-01-2433", "time": 1694551048}
{"status": 200, "ip": "127.0.0.1", "level": 30, "emailAddress": "user@mail.com", "msg": "Connected to database", "pid": 12655, "ssn": "407-01-2433", "time": 1694551051}
{"status": 200, "ip": "127.0.0.1", "level": 30, "emailAddress": "user@mail.com", "msg": "Initialized application", "pid": 12665, "ssn": "407-01-2433", "time": 1694551072}
{"status": 200, "ip": "127.0.0.1", "level": 30, "emailAddress": "user@mail.com", "msg": "Initialized application", "pid": 12665, "ssn": "407-01-2433", "time": 1694551075}

```

## Installing Vector

이제 로그를 생성할 수 있으므로 최신 버전의 Vector를 설치합니다. 이 글에서는 apt 패키지 관리자를 통해 Ubuntu 22.04에 Vector를 설치하겠습니다. 다른 시스템을 사용하는 경우 문서 페이지에서 운영 체제에 따라 적절한 옵션을 선택할 수 있습니다.

벡터 저장소를 추가하려면 다음 명령을 사용합니다:

```
curl -1sLf \
  'https://repositories.timber.io/public/vector/cfg/setup/bash.deb.sh' \
| sudo -E bash

```

다음 명령으로 벡터를 설치합니다:

```
sudo apt install vector

```

그런 다음 설치가 성공적으로 완료되었는지 확인합니다:

```
vector --version

vector 0.32.1 (x86_64-unknown-linux-gnu 9965884 2023-08-21 14:52:38.330227446)

```

벡터를 설치하면 시스템 서비스 형태로 백그라운드에서 자동으로 실행됩니다. 하지만 이 튜토리얼에서는 Vector를 수동으로 실행할 것이므로 서비스가 실행 중일 필요는 없습니다. 백그라운드 서비스가 실행되는 동안 벡터를 수동으로 실행하려는 경우 충돌이 발생할 수 있습니다.

Vector 서비스를 중지하려면 다음 명령을 사용합니다:

```
sudo systemctl stop vector

```

## How Vector works

https://imagedelivery.net/xZXo0QFi-1_4Zimer-T0XQ/147f8cb5-2295-48e9-a0dc-f47c222b2400/lg1x

벡터를 이해하려면 파이프라인으로 상상해 보세요. 한쪽 끝에서 Vector는 원시 로그를 수집하고 이를 통합 로그 이벤트 형식으로 표준화합니다. 로그 이벤트가 벡터를 통과하면서 '변환'을 통해 다양한 조작을 거쳐 내용을 조작하고 향상시킬 수 있습니다. 마지막으로 파이프라인의 마지막 단계에서 로그 이벤트는 저장 또는 분석을 위해 여러 대상으로 전송될 수 있습니다.

데이터 소스, 트랜스폼, 대상은 /etc/vector/vector.yaml에 있는 구성 파일에서 정의할 수 있습니다. 이 구성 파일은 다음과 같은 구성 요소로 구성되어 있습니다:

```
sources:
  <unique_source_name>:
    # source configuration properties go here

transforms:
  <unique_transform_name>:
    # transform configuration properties go here

sinks:
  <unique_destination_name>:
    # sink configuration properties go here

```

이 구조를 통해 특정 로그 집계 및 처리 요구 사항에 맞게 Vector를 구성하고 사용자 정의할 수 있습니다.

구성 요소를 분석해 보겠습니다:

- sources: 이 섹션에서는 벡터가 읽어야 하는 데이터 소스를 정의합니다.
- transforms: 데이터를 조작하거나 변환하는 방법을 지정합니다.
- sinks: 벡터가 데이터를 라우팅해야 하는 대상을 정의합니다.

각 컴포넌트마다 플러그인을 지정해야 합니다. 소스의 경우 사용할 수 있는 몇 가지 입력은 다음과 같습니다:

- File: 파일에서 로그를 가져옵니다.
- Docker 로그: Docker 컨테이너에서 로그를 수집합니다.
- Socket: 소켓 클라이언트를 통해 전송된 로그를 수집합니다.
- Syslog: Syslog에서 로그를 가져옵니다.

데이터를 처리할 때 유용하게 사용할 수 있는 몇 가지 변환은 다음과 같습니다:

- VRL로 다시 매핑: 데이터를 변환하도록 설계된 표현식 지향 언어입니다.

- Lua: Lua 프로그래밍 언어를 사용하여 로그 이벤트를 변환합니다.

- Filter: 지정된 조건에 따라 이벤트를 필터링합니다.

- Throttle: 로그 스트림의 속도를 제한합니다.

마지막으로, 벡터에서 사용할 수 있는 몇 가지 싱크에 대해 살펴봅시다:

- HTTP: 로그를 HTTP 엔드포인트로 전달합니다.
- WebSocket: 웹소켓 엔드포인트로 통합 가시성 데이터를 전달합니다.
- Loki: 로그를 Grafana Loki로 전달합니다.
- Elasticsearch: 로그를 Elasticsearch로 전달합니다.

다음 섹션에서는 파일 소스를 사용하여 파일에서 로그를 읽고 콘솔 싱크를 사용하여 콘솔로 레코드를 전달합니다.

## Getting started with Vector

이제 벡터의 작동 방식을 알았으니 /var/log/logify/app.log 파일에서 로그 레코드를 읽고 콘솔로 리디렉션하도록 구성할 수 있습니다.

etc/vector/vector.yaml 파일을 열고 필요한 수퍼유저 권한이 있는지 확인합니다:

```
sudo nano /etc/vector/vector.yaml

```

기존 콘텐츠를 모두 삭제하고 다음 줄을 추가합니다:

```
sources:
  app_logs:
    type: "file"
    include:
      - "/var/log/logify/app.log"

sinks:
  print:
    type: "console"
    inputs:
      - "app_logs"
    encoding:
      codec: "json"

```

소스 컴포넌트에서 파일에서 로그를 읽을 app_logs 소스를 정의합니다. 유형 옵션은 파일 소스를 지정하고, 포함 옵션은 읽을 파일의 경로를 포함하는 옵션을 정의합니다.

싱크 구성 요소에서는 로그를 전송할 대상을 지정하는 인쇄 싱크를 정의합니다. 로그를 콘솔로 리디렉션하려면 유형을 콘솔 싱크로 설정합니다. 다음으로 로그의 출처가 되는 소스 컴포넌트를 지정합니다(이 경우 app_logs 소스). 마지막으로 encoding.codec을 사용하여 로그가 JSON 형식이어야 함을 지정합니다.

이러한 구성을 완료했으면 파일을 저장하고 터미널에서 변경 사항을 확인합니다:

```
sudo vector validate /etc/vector/vector.yaml

√ Loaded ["/etc/vector/vector.yaml"]
√ Component configuration
√ Health check "print"
------------------------------------
                           Validated

```

이제 벡터를 실행할 수 있습니다:

```
sudo vector

```

시작하면 자동으로 구성 파일을 선택합니다.

vector.yaml을 다른 위치에 정의한 경우 구성 파일의 전체 경로를 전달해야 합니다:

```
sudo vector --config </path/to/vector.yaml>

```

Vector가 시작되면 시작되었음을 확인하는 출력이 표시됩니다:

```
2023-09-12T05:56:41.803796Z  INFO vector::app: Log level is enabled. level="vector=info,codec=info,vrl=info,file_source=info,tower_limit=info,rdkafka=info,buffers=info,lapin=info,kube=info"
2023-09-12T05:56:41.804202Z  WARN vector::app: DEPRECATED The openssl legacy provider provides algorithms and key sizes no longer recommended for use. Set `--openssl-legacy-provider=false` or `VECTOR_OPENSSL_LEGACY_PROVIDER=false` to disable. See https://vector.dev/highlights/2023-08-15-0-32-0-upgrade-guide/#legacy-openssl for details.
2023-09-12T05:56:41.805079Z  INFO vector::app: Loaded openssl provider. provider="legacy"
2023-09-12T05:56:41.805287Z  INFO vector::app: Loaded openssl provider. provider="default"
2023-09-12T05:56:41.806105Z  INFO vector::app: Loading configs. paths=["/etc/vector/vector.yaml"]
2023-09-12T05:56:41.809530Z  INFO vector::topology::running: Running healthchecks.
2023-09-12T05:56:41.810125Z  INFO vector: Vector has started. debug="false" version="0.32.1" arch="x86_64" revision="9965884 2023-08-21 14:52:38.330227446"
2023-09-12T05:56:41.810335Z  INFO vector::app: API is disabled, enable by setting `api.enabled` to `true` and use commands like `vector top`.
...

```

몇 초 후, 마지막에 JSON 형식의 로그 메시지가 표시되기 시작합니다:

```
{"file":"/var/log/logify/app.log","host":"vector-test","message":"{\"status\": 200, \"ip\": \"127.0.0.1\", \"level\": 30, \"emailAddress\": \"user@mail.com\", \"msg\": \"Task completed successfully\", \"pid\": 12655, \"ssn\": \"407-01-2433\", \"time\": 1694551048}","source_type":"file","timestamp":"2023-09-12T20:40:21.582883690Z"}
{"file":"/var/log/logify/app.log","host":"vector-test","message":"{\"status\": 200, \"ip\": \"127.0.0.1\", \"level\": 30, \"emailAddress\": \"user@mail.com\", \"msg\": \"Connected to database\", \"pid\": 12655, \"ssn\": \"407-01-2433\", \"time\": 1694551051}","source_type":"file","timestamp":"2023-09-12T20:40:21.582980072Z"}
...

```

출력 결과에서 벡터가 로그 파일을 성공적으로 읽고 로그를 콘솔로 라우팅할 수 있음을 확인할 수 있습니다. 벡터는 추가 컨텍스트를 위해 각 로그 항목에 파일, 호스트, 메시지, 소스 유형 및 타임스탬프와 같은 여러 필드를 자동으로 추가했습니다.

이제 CTRL + C를 눌러 Vector를 종료할 수 있습니다.

## Transforming the logs
로그를 어떤 식으로든 처리하지 않고 전송하는 경우는 드뭅니다. 중요한 필드로 로그를 보강하거나, 민감한 데이터를 삭제하거나, 일반 텍스트 로그를 기계가 구문 분석하기 쉬운 JSON과 같은 구조화된 형식으로 변환해야 하는 경우가 종종 있습니다.

벡터는 데이터 조작을 위한 강력한 언어인 벡터 리맵 언어(VRL)를 제공합니다. VRL은 데이터 변환을 위해 설계된 고성능 표현 지향 언어입니다. 데이터 구문 분석, 데이터 유형 변환을 위한 함수를 제공하며, 다른 기능 중에서도 조건문도 포함합니다.

이 섹션에서는 VRL을 사용하여 다음과 같은 방법으로 데이터를 처리합니다:

- JSON 로그 구문 분석.
- 필드 제거.
- 새 필드 추가.
- 타임스탬프 변환.
- 민감한 데이터 삭제.

### Vector Remap Language(VRL) dot operator
VRL로 로그를 변환하는 방법을 살펴보기 전에 효율적인 사용 방법을 이해하는 데 도움이 되는 몇 가지 기본 사항을 살펴보겠습니다.

구문에 익숙해지기 위해 벡터는 읽기-값-출력 루프(REPL)를 시작하는 `vector vrl` 하위 명령을 제공합니다. 이를 사용하려면 로그 이벤트가 포함된 JSON 파일을 받아들이는 `--input` 옵션을 함께 제공해야 합니다.

먼저 `log-processing-stack/logify`에 있는지 확인하고 `input.json` 파일을 만듭니다:

```
nano input.json
```

input.json 파일에 마지막 섹션의 출력에서 다음 로그 이벤트를 추가합니다:

```
{"file":"/var/log/logify/app.log","host":"vector-test","message":"{\"status\": 200, \"ip\": \"127.0.0.1\", \"level\": 30, \"emailAddress\": \"user@mail.com\", \"msg\": \"Task completed successfully\", \"pid\": 12655, \"ssn\": \"407-01-2433\", \"time\": 1694551048}","source_type":"file","timestamp":"2023-09-12T20:40:21.582883690Z"}

```
오류를 방지하기 위해 끝에 공백이 없는지 확인하세요.

그런 다음 REPL을 시작합니다:

```
vector vrl --input input.json

```

REPL 프롬프트에 점 하나를 입력합니다:

```
.
```

벡터가 input.json 파일에서 로그 이벤트를 읽으면 점 연산자는 다음을 반환합니다:

```
{ "file": "/var/log/logify/app.log", "host": "vector-test", "message": "{\"status\": 200, \"ip\": \"127.0.0.1\", \"level\": 30, \"emailAddress\": \"user@mail.com\", \"msg\": \"Task completed successfully\", \"pid\": 12655, \"ssn\": \"407-01-2433\", \"time\": 1694551048}", "source_type": "file", "timestamp": "2023-09-12T20:40:21.582883690Z" }

```

`.`은 들어오는 이벤트를 참조하며, 벡터가 처리하는 모든 이벤트는 점 표기법을 사용하여 액세스할 수 있습니다.

프로퍼티에 액세스하려면 다음과 같이 접두사 앞에 `.`을 붙입니다:

```
.host

"vector-host"

```

`.`의 값을 다른 속성에 재할당할 수도 있습니다:

```
. = .host

```

이제 다시 `.`을 입력합니다:

```
.
```

더 이상 원본 개체를 참조하지 않고 "호스트" 속성을 참조합니다:

```
"vector-host"

```

이제 exit를 입력하여 REPL을 종료할 수 있습니다:

```
exit

```

이제 점 연산자에 익숙해졌으므로 다음 섹션에서는 JSON 로그 구문 분석부터 시작하여 VRL에 대해 더 자세히 살펴보겠습니다.

### Parsing JSON logs using Vector

우선, 출력의 메시지 속성을 자세히 살펴보면 로그 항목이 원래 JSON 형식이었지만 벡터가 이를 문자열로 변환한 것을 확인할 수 있습니다:

```
{
  "file": "/var/log/logify/app.log",
  "host": "vector-test",
  "message": "{\"status\": 200, \"ip\": \"127.0.0.1\", \"level\": 30, \"emailAddress\": \"user@mail.com\", \"msg\": \"Task completed successfully\", \"pid\": 12655, \"ssn\": \"407-01-2433\", \"time\": 1694551048}",
  "source_type": "file",
  "timestamp": "2023-09-12T20:40:21.582883690Z"
}

```

하지만 우리의 목표는 벡터가 JSON 로그를 파싱하도록 하는 것입니다. 이를 위해 구성 파일을 다시 엽니다:

```
sudo nano /etc/vector/vector.yaml

```

그런 다음 트랜스폼을 정의하고 리매핑 트랜스폼을 사용하도록 설정합니다:

```
...
transforms:
  app_logs_parser:
    inputs:
      - "app_logs"
    type: "remap"
    source: |
      # Parse JSON logs
      ., err = parse_json(.message)

sinks:
  print:
    type: "console"
    inputs:
      - "app_logs_parser"
    encoding:
      codec: "json"

```

로그를 처리하기 위해 `app_logs_parser`라는 이름의 트랜스폼을 정의합니다. 이 구성 요소의 입력이 레코드를 읽는 소스(여기서는 `app_logs`)에서 제공되도록 지정합니다. 다음으로, 벡터 리매핑 언어(VRL)를 사용할 수 있는 `remap` 트랜스폼을 사용하도록 구성 요소를 구성합니다.

`source` 옵션에는 삼중 따옴표로 묶인 VRL 구문 `., err = parse_json(.message)`가 포함됩니다. VRL에서는 VRL 코드를 작성할 때마다 구문을 큰따옴표로 묶어야 합니다.

이전 섹션에서 살펴본 바와 같이, `.`은 벡터 프로세스 전체 객체를 나타냅니다. 객체 내에서 특정 속성을 선택하려면 필드 이름 앞에 점을 붙이면 됩니다. 다음은 벡터가 `., err = parse_json(.message)`를 실행하는 방식입니다:

`.message`: `message` 필드 내의 전체 문자열을 반환합니다.
`parse_json(.message)`: 이 메서드는 JSON 데이터를 구문 분석합니다.
`., err`: JSON 구문 분석에 성공하면 `.`이 `parse_json()` 메서드를 호출한 결과로 설정되고, 그렇지 않으면 `err` 변수가 초기화됩니다.
마지막으로 `sinks.print` 컴포넌트에서 `inputs`을 업데이트하여 이제 로그가 `transforms.app_logs_parser` 컴포넌트에서 가져오도록 지정합니다.

변경 사항을 저장합니다. 구성 파일을 종료하지 않고 다른 터미널로 전환하여 감시 모드로 Vector를 시작합니다:

```
sudo vector --watch-config

```

`--watch-config` 옵션은 설정 파일에 변경 사항을 저장하면 자동으로 Vector를 다시 시작합니다. 앞으로는 Vector를 수동으로 중지할 필요 없이 다른 터미널에서 설정을 조정할 수 있으므로 프로세스가 간소화됩니다.

Vector가 실행되면 로그 메시지가 성공적으로 파싱되는지 확인할 수 있습니다:

```
{"emailAddress":"user@mail.com","ip":"127.0.0.1","level":30,"msg":"Initialized application","pid":13611,"ssn":"407-01-2433","status":200,"time":1694551588}
...

```

이제 출력에서 객체가 구문 분석되었으며, Vector가 추가한 추가 필드는 더 이상 표시되지 않고 로그만 남아 있습니다. 벡터가 추가한 필드가 도움이 된다면 `., err = ...`을 `.message, err = .....` 로 바꿀 수 있습니다. 그러나 출력의 간결성을 위해 이 튜토리얼의 나머지 부분에서는 이러한 필드를 제거한 상태로 유지하겠습니다.

지금까지 JSON 로그를 파싱하는 방법을 살펴보았습니다. 하지만 벡터는 다음과 같은 다양한 다른 형식의 파서 함수도 제공합니다:

- `parse_csv`: CSV 로그 데이터 구문 분석에 유용합니다.
- `parse_logfmt`: Logfmt 형식의 구조화된 로그를 구문 분석하는 데 유용합니다.
- `parse_syslog`: Syslog 구문 분석에 적합합니다.
- `parse_grok`: 비정형 로그 데이터를 구문 분석하는 데 유용합니다.
이러한 구문 분석기는 다양한 로그 형식과 구조를 처리할 수 있는 유연성을 제공합니다.

구문 분석기 함수로 작업할 때는 잠재적인 런타임 오류를 해결하는 것이 좋습니다. 이 방법에 대한 자세한 내용은 벡터 웹사이트의 런타임 오류를 참조하세요.

### Adding and removing fields with Vector
이제 JSON 로그를 구문 분석할 수 있으므로 `emailAddress`와 같은 민감한 세부 정보를 제거합니다. 그런 다음 새 `environment` 필드를 추가하여 로그가 프로덕션 로그인지 개발 로그인지를 표시합니다.

`etc/vector/vector.yaml` 파일이 열려 있는 터미널로 돌아갑니다. 그런 다음 다음 줄로 소스 구성을 업데이트합니다:

```
transforms:
  app_logs_parser:
    ...
    source: |
      # Parse JSON logs
      ., err = parse_json(.message)

      # Remove emailAddress field
      del(.emailAddress)

      # Add an environment field
      .environment = "dev"

```

위의 코드 조각에서 `del()` 함수는 `emailAddress` 필드를 제거합니다. 그 후 새 `environment` 필드가 `dev`라는 값으로 JSON 객체에 추가됩니다. 필드가 이미 존재하는 경우 해당 값을 덮어씁니다.

Vector 구성 파일을 변경한 후 Vector가 자동으로 다시 시작되어야 합니다. 그렇지 않은 경우 수동으로 Vector를 다시 시작할 수 있습니다. 재시작하면 다음과 유사한 출력이 표시됩니다:

```
{"environment":"dev","ip":"127.0.0.1","level":30,"msg":"Connected to database","pid":13647,"ssn":"407-01-2433","status":200,"time":1694551695}
...

```

출력에서 볼 수 있듯이 `emailAddress` 필드가 삭제되고 새 `environment` 필드가 객체에 추가되었습니다.

`del()` 함수는 벡터에서 제공하는 경로 함수 중 하나입니다. 다른 유용한 함수는 다음과 같습니다:

- `exists`: 필드 또는 배열 요소가 존재하는지 확인하려는 경우에 유용합니다.

- `remove`: 경로를 모르는 필드를 제거하려는 경우에 유용합니다.

- `set`: 객체나 배열에 값을 동적으로 삽입할 때 유용합니다.

이렇게 하면 로그 이벤트의 속성을 수정할 수 있습니다. 다음 섹션에서는 벡터를 사용하여 날짜 서식을 지정하겠습니다.

### Formatting dates with Vector

이 애플리케이션은 1970년 1월 1일 00:00:00 UTC 이후 경과한 시간(초)을 나타내는 유닉스 타임스탬프 형식의 로그를 생성합니다. 타임스탬프를 사람이 읽을 수 있도록 하려면 타임스탬프를 읽을 수 있는 형식으로 변환해야 합니다.

구성 파일에 다음 줄을 추가합니다:

```
transforms:
  app_logs_parser:
    ...
    source: |
      # Parse JSON logs
      ., err = parse_json(.message)

      # Remove emailAddress field
      del(.emailAddress)

      # Add an environment field
      .environment = "dev"

      # Format date to the ISO format
      .time = from_unix_timestamp!(.time)
      .time = format_timestamp!(.time, format: "%+")

```

`from_unix_timestamp!()` 함수는 Unix 타임스탬프를 VRL 타임스탬프로 변환합니다. 이 함수의 반환 값은 시간 필드를 덮어쓰고, 이후 `format_timestamp!()` 함수의 값으로 다시 한 번 덮어씁니다. 이 함수는 `%+` 형식 지시어에 따라 ISO 형식으로 날짜의 형식을 지정합니다.

함수가 `!`로 끝나는 것을 볼 수 있습니다. 이는 함수에 오류가 있을 수 있으므로 오류 처리가 필요하다는 의미입니다.

구성 파일을 저장하면 벡터가 다시 로드되고 다음과 유사한 출력이 표시됩니다:

```
{"environment":"dev","ip":"127.0.0.1","level":30,"msg":"Connected to database","pid":13691,"ssn":"407-01-2433","status":200,"time":"2023-09-12T20:49:43+00:00"}
...

```

이제 날짜가 사람이 읽을 수 있는 ISO 형식으로 변환됩니다.

이 섹션에서 사용된 `from_unix_timestamp!()` 함수는 벡터가 제공하는 변환 함수 중 하나입니다. 다음 함수도 다양한 유형의 데이터를 변환할 때 유용하게 사용할 수 있습니다:

- `to_unix_timestamp`: 값을 유닉스 타임스탬프로 변환합니다.
- `to_syslog_facility`: 값을 Syslog 시설 코드로 변환할 때 유용합니다.
- `to_syslog_level`: 값을 Syslog 심각도 수준으로 강제 변환합니다.
로그의 날짜 서식을 더 잘 이해하려면 종합적인 로그 서식 지정 가이드를 참조하세요.

### Working with conditional statements

또한 VRL은 조건문을 제공하여 컴퓨터가 조건에 따라 결정하도록 지시합니다. 조건문은 JavaScript와 같은 다른 프로그래밍 언어와 유사하게 작동합니다. 이 섹션에서는 조건문을 사용하여 `status`가 `200`과 같은지 확인하고 조건이 참으로 평가되면 성공 필드를 추가합니다.

이를 수행하려면 다음 조건문을 추가합니다:

```
transforms:
  app_logs_parser:
    ...
    source: |
      # Parse JSON logs
      ., err = parse_json(.message)

      # Remove emailAddress field
      del(.emailAddress)

      # Add an environment field
      .environment = "dev"

      # Format date to the ISO format
      .time = from_unix_timestamp!(.time)
      .time = format_timestamp!(.time, format: "%+")

      if .status == 200 {
        .success = true
      }

```

`if` 문은 `status`가 `200`과 같은지 확인하고 새 `success` 필드를 추가합니다.

저장 후 벡터가 다시 로드되고 다음과 같은 출력이 표시됩니다:

```
{"environment":"dev","ip":"127.0.0.1","level":30,"msg":"Connected to database","pid":13722,"ssn":"407-01-2433","status":200,"success":true,"time":"2023-09-12T20:50:55+00:00"}

```

성공 필드가 객체에 성공적으로 추가되었습니다.

조건문으로 작업할 때는 타입 함수에 익숙해지면 도움이 됩니다:

- is_json: 값이 유효한 JSON인지 확인하고자 할 때 유용합니다.
- is_boolean: 값이 부울인지 확인하고자 할 때 유용합니다.
- is_string: 주어진 값이 문자열인지 확인하고자 할 때 유용합니다.

### Redacting sensitive data

로그 메시지에는 여전히 IP 주소 및 주민등록번호와 같은 민감한 필드가 포함되어 있습니다. 사적인 사용자 정보가 악의적인 사람의 손에 넘어가지 않도록 기록해서는 안 됩니다. 따라서 특히 필드를 완전히 제거할 수 없는 경우 민감한 데이터를 리댁트하는 것이 좋습니다. 이를 위해 벡터는 모든 데이터를 리댁트할 수 있는 redact() 함수를 제공합니다.

구성에서 다음 코드를 추가하여 IP 주소와 주민등록번호를 삭제합니다:

```
transforms:
  app_logs_parser:
    ...
    source: |
      # Parse JSON logs
      ., err = parse_json(.message)

      # Remove emailAddress field
      del(.emailAddress)

      # Add an environment field
      .environment = "dev"

      # Format date to the ISO format
      .time = from_unix_timestamp!(.time)
      .time = format_timestamp!(.time, format: "%+")

      if .status == 200 {
        .success = true
      }

      # Redact field values
      . = redact(., filters: ["us_social_security_number", r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$'])

```

redact() 메서드는 전체 객체를 가져와서 필터를 적용합니다. 필터는 정규식(정규 표현식) 또는 내장 필터일 수 있습니다. 현재 벡터에는 주민등록번호를 삭제할 수 있는 기본 제공 필터는 us_social_security_number 하나만 있습니다. 다른 민감한 정보의 경우 정규식을 사용해야 합니다. 이 예제에서 정규식 필터는 모든 IPV4 IP 주소를 일치시켜 삭제합니다.

변경 사항을 저장하면 다음과 같은 출력이 생성됩니다:

```
{"environment":"dev","ip":"[REDACTED]","level":30,"msg":"Connected to database","pid":13759,"ssn":"[REDACTED]","status":200,"success":true,"time":"2023-09-12T20:52:13+00:00"}
...

```

이제 Vector를 중지하고 구성 파일을 종료할 수 있습니다. logify.sh 스크립트를 중지하려면 다음 명령을 입력하여 프로세스 ID를 가져옵니다:

```
jobs -l | grep "logify"

[1]+  2933 Running                 ./logify.sh &

```

해당 프로세스 ID로 프로그램을 종료합니다:

```
kill -9 2933

```

이제 로그를 변환할 수 있게 되었으니, 벡터를 사용하여 여러 소스에서 레코드를 수집하고 중앙 위치로 전달할 수 있습니다.

## Collecting logs from Docker containers and centralizing logs

이 섹션에서는 Bash 스크립트를 컨테이너화하고 요청을 수신할 때마다 JSON 형식의 Nginx 로그를 생성하도록 사전 구성된 Nginx hello world Docker 이미지를 사용합니다. 그런 다음 Vector를 사용하여 두 컨테이너에서 로그를 수집하고 분석 및 모니터링을 위해 Better Stack에서 로그를 중앙 집중화합니다.

### Dockerizing the Bash script

이 섹션에서는 앞서 작성한 Bash 스크립트를 컨테이너화하기 위해 Docker파일을 생성합니다.

로그 프로세싱 스택/로그파이 디렉터리에 있는지 확인하세요. 다음으로, 컨테이너가 실행 중일 때 컨테이너에 포함되어야 할 내용을 지정하는 Docker파일을 만듭니다:

```
nano Dockerfile

```

도커파일에 지침을 추가합니다:

```
FROM ubuntu:latest

COPY . .

RUN chmod +x logify.sh

RUN mkdir -p /var/log/logify

RUN ln -sf /dev/stdout /var/log/logify/app.log

CMD ["./logify.sh"]

```

Docker파일에서 최신 Ubuntu 이미지를 지정하고, 로컬 디렉터리의 내용을 컨테이너에 복사하고, 스크립트를 실행 가능하게 만든 다음, 애플리케이션 로그를 저장할 전용 디렉터리를 만듭니다. 로그에 액세스할 수 있도록 하기 위해 심볼릭 링크를 사용하여 로그를 표준 출력(stdout)으로 리디렉션합니다. 마지막으로 컨테이너가 시작될 때 스크립트를 실행할 명령을 지정합니다.

이제 Bash 스크립트와 Nginx 서비스를 정의하는 docker-compose.yml 파일을 작성합니다.

먼저 디렉터리를 루트 프로젝트 디렉토리로 변경합니다:

```
cd ..

```

텍스트 편집기에서 docker-compose.yml을 생성합니다:

```
version: '3'
services:
  logify-script:
    build:
      context: ./logify
    image: logify:latest
    container_name: logify
  nginx:
    image: betterstackcommunity/nginx-helloworld:latest
    logging:
      driver: json-file
    container_name: nginx
    ports:
      - '80:80'

```

구성 파일에서 ./logify 디렉터리의 Docker파일을 기반으로 logify:latest라는 이름의 이미지를 빌드하는 logify-script 서비스를 정의합니다. 그런 다음 포트 80에서 들어오는 HTTP 요청을 수신 대기할 nginx 서비스를 정의합니다. 현재 포트 80에서 실행 중인 서비스가 있는 경우 해당 서비스를 종료해야 합니다.

이미지를 빌드하고 서비스를 생성하려면 docker-compose.yml 파일과 동일한 디렉터리에서 다음 명령을 실행합니다:

```
docker compose up -d

```

`-d` 플래그를 사용하면 컨테이너를 백그라운드에서 실행할 수 있습니다.

이 명령으로 컨테이너의 상태를 확인할 수 있습니다:

```
docker compose ps

NAME                COMMAND              SERVICE             STATUS              PORTS
logify              "./logify.sh"        logify-script       running
nginx               "/runner.sh nginx"   nginx               running             0.0.0.0:80->80/tcp, :::80->80/tcp

```

curl 명령을 사용하여 nginx 서비스에 5개의 요청을 보냅니다:

```
curl http://localhost:80/?[1-5]

```

그런 다음 Docker Compose 설정에서 컨테이너의 로그를 확인합니다:

```
docker compose logs

logify  | {"status": 200, "ip": "127.0.0.1", "level": 30, "emailAddress": "user@mail.com", "msg": "Task completed successfully", "pid": 1, "ssn": "407-01-2433", "time": 1695545456}
...
logify  | {"status": 200, "ip": "127.0.0.1", "level": 30, "emailAddress": "user@mail.com", "msg": "Operation finished", "pid": 1, "ssn": "407-01-2433", "time": 1695545462}
nginx  | {"timestamp":"2023-09-12T07:10:04+00:00","pid":"8","remote_addr":"172.19.0.1","remote_user":"","request":"GET /?1 HTTP/1.1","status": "200","body_bytes_sent":"11109","request_time":"0.000","http_referrer":"","http_user_agent":"curl/7.81.0","time_taken_ms":"1694502604.901"}
...
nginx  | {"timestamp":"2023-09-12T07:10:04+00:00","pid":"8","remote_addr":"172.19.0.1","remote_user":"","request":"GET /?2 HTTP/1.1","status": "200","body_bytes_sent":"11109","request_time":"0.000","http_referrer":"","http_user_agent":"curl/7.81.0","time_taken_ms":"1694502604.909"}

```

출력에는 nginx 및 logify 컨테이너의 모든 로그가 표시됩니다.

컨테이너가 실행되고 로그를 생성하고 있다면, 다음 단계는 이러한 로그를 읽고 중앙 집중화하기 위해 벡터 컨테이너를 설정하는 것입니다.

### Defining the Vector service with Docker Compose

이 섹션에서는 기존 컨테이너에서 수집하고 Better Stack에서 로그를 중앙 집중화하기 위해 Docker Compose 설정에서 Vector 서비스를 정의합니다. 또한 로그 레코드를 수집하고 처리하는 방법을 지정하는 Vector 구성 파일을 생성합니다.

루트 디렉토리에서 docker-compose.yml 파일을 엽니다:

```
nano docker-compose.yml

```

그런 다음 docker-compose.yml 파일에 다음 코드를 추가합니다:

```
version: '3'

services:
  ...
  vector:
    image: timberio/vector:0.32.1-debian
    volumes:
      - ./vector:/etc/vector
      - /var/run/docker.sock:/var/run/docker.sock
    command: ["-c", "/etc/vector/vector.yaml"]
    ports:
      - '8686:8686'
    container_name: vector
    depends_on:
      - logify-script
      - nginx

```

벡터 서비스 정의는 공식 timberio/vector 도커 이미지를 사용합니다. 또한 벡터 구성 파일이 포함된 벡터 디렉터리를 컨테이너에 마운트합니다.

다음으로 벡터 디렉토리를 생성하고 그 안으로 이동합니다:

```
mkdir vector && cd vector

```

그런 다음 다음 명령을 실행하여 Docker 이미지 이름을 얻습니다:

```
docker ps

CONTAINER ID   IMAGE                                          COMMAND              CREATED         STATUS         PORTS                               NAMES
fc30e4a4599f   betterstackcommunity/nginx-helloworld:latest   "/runner.sh nginx"   4 minutes ago   Up 4 minutes   0.0.0.0:80->80/tcp, :::80->80/tcp   nginx
7bf40ea91435   logify:latest             "./logify.sh"        4 minutes ago   Up 4 minutes                                       logify

```

vector.yaml 구성 파일을 만듭니다:

```
nano vector.yaml

```

아래 코드를 추가하고 include_images 옵션에 앞서 언급한 이미지 이름과 함께 이미지 이름을 포함해야 합니다:

```
sources:
  bash_logs:
    type: "docker_logs"
    include_images:
      - "logify:latest"

  nginx_logs:
    type: "docker_logs"
    include_images:
      - "betterstackcommunity/nginx-helloworld:latest"

  vector_logs:
    type: "internal_logs"

```

sources.bash_logs 구성 요소는 docker_logs 소스를 사용하여 Docker 컨테이너에서 로그를 읽습니다. include_images 옵션은 logify:latest 이미지로 빌드된 컨테이너에서 로그를 수집하도록 벡터에 지시합니다.

또한 sources.nginx_logs 구성 요소는 betterstackcommunity/nginx-helloworld:최신 이미지로 빌드된 Nginx Docker 컨테이너에서 로그를 읽습니다.

그 다음, sources.vector_logs 구성 요소는 내부 로그 소스를 사용하여 벡터가 로그를 생성하고 이를 읽고 대상으로 전달할 수 있도록 합니다.

다음으로 로그를 전달할 대상을 정의합니다. 한 곳에서 로그를 모니터링하고 분석할 수 있도록 Better Stack을 사용하여 기록을 중앙 집중화할 것입니다.

로그를 전달하기 전에 무료 Better Stack 계정을 만드세요. 로그인한 후 소스 링크를 클릭합니다:

https://imagedelivery.net/xZXo0QFi-1_4Zimer-T0XQ/bc78e436-70ae-4f99-3045-ecbcee5b0100/lg1x

더 나은 스택의 소스 페이지에서 소스 연결 버튼을 클릭합니다:

https://imagedelivery.net/xZXo0QFi-1_4Zimer-T0XQ/8e23363d-391d-4575-db47-c99d84cd7700/lg1x

그런 다음 원하는 소스 이름을 입력하고 플랫폼으로 '벡터'를 선택합니다:

https://imagedelivery.net/xZXo0QFi-1_4Zimer-T0XQ/10ed823d-df3d-4fba-829f-844176eab500/lg1x

소스를 생성한 후 소스 토큰 필드를 클립보드에 복사합니다:

https://imagedelivery.net/xZXo0QFi-1_4Zimer-T0XQ/41a01d8c-7421-4ae4-f5c6-d204d8d9dc00/lg1x

그런 다음 vector.yaml 파일로 돌아가서 로그를 Better Stack으로 리디렉션하는 싱크를 추가합니다:

```
...
sinks:
  better_stack_http_sink_bash:
    type: "http"
    method: "post"
    inputs:
      - "bash_logs"
    uri: "https://in.logs.betterstack.com/"
    encoding:
      codec: "json"
    auth:
      strategy: "bearer"
      token: "<your_bash_source_token>"

```

구성 파일을 저장하고 종료합니다.

루트 디렉토리로 돌아갑니다:

```
docker compose up -d

```

몇 초간 기다린 후 Better Stack으로 돌아와 로그가 성공적으로 전송되었는지 확인합니다:

https://imagedelivery.net/xZXo0QFi-1_4Zimer-T0XQ/c49796ec-a39c-42e3-9425-1eb2db45c800/lg1x

이제 Bash 스크립트 로그가 중앙 집중화되었으므로 유사한 단계에 따라 Nginx 및 Vector 로그에 대한 두 개의 소스를 추가로 만들 수 있습니다. 소스 토큰은 안전한 곳에 보관하세요. 성공적으로 완료되면 인터페이스는 다음과 같이 표시됩니다:

https://imagedelivery.net/xZXo0QFi-1_4Zimer-T0XQ/54ad430f-96dc-4440-91ef-1b9165d08c00/lg1x

그런 다음 vector.yaml 파일을 다시 엽니다:

```
nano vector/vector.yaml

```

두 개의 싱크를 추가하고 그에 따라 토큰을 업데이트하여 Nginx와 Vector의 로그가 Better Stack으로 올바르게 전송되도록 합니다:

```
...
sinks:
  better_stack_http_sink_bash:
  ...
  better_stack_http_sink_nginx:
    type: "http"
    method: "post"
    inputs:
      - "nginx_logs"
    uri: "https://in.logs.betterstack.com/"
    encoding:
      codec: "json"
    auth:
      strategy: "bearer"
      token: "<your_nginx_source_token>"

  better_stack_http_sink_vector:
    type: "http"
    method: "post"
    inputs:
      - "vector_logs"
    uri: "https://in.logs.betterstack.com/"
    encoding:
      codec: "json"
    auth:
      strategy: "bearer"
      token: "<your_vector_source_token>"

```

파일을 저장하고 명령을 다시 한 번 실행합니다:

```
docker compose up -d

```

이제 nginx 서비스에 다시 5개의 요청을 보냅니다:

```
curl http://localhost:80/?[1-5]

```

Nginx의 로그가 Better Stack에 성공적으로 업로드됩니다:

https://imagedelivery.net/xZXo0QFi-1_4Zimer-T0XQ/b2b31e84-7e96-4a4c-2a93-6f12f4385900/lg1x

벡터 로그가 업로드되고 있는지 확인하려면 모든 컨테이너를 중지하세요:

```
docker compose stop

```

컨테이너를 다시 시작합니다:

```
docker compose up -d

```

벡터 로그는 Better Stack에 업로드됩니다:

https://imagedelivery.net/xZXo0QFi-1_4Zimer-T0XQ/e171f99b-474a-4a3f-6a59-76b819cac300/lg1x

이를 통해 애플리케이션, Nginx 및 벡터 로그를 중앙 집중화할 수 있습니다.

## Monitoring Vector health with Better Stack
- https://betterstack.com/community/guides/logging/vector-explained/#monitoring-vector-health-with-better-stack

벡터는 Better Stack과 같은 툴이 주기적으로 확인할 수 있는 /health 엔드포인트를 제공합니다. Vector의 상태가 좋지 않거나 다운되면 전화나 이메일을 통해 알림을 보내도록 Better Stack을 구성하여 문제를 즉시 해결할 수 있습니다.

(생략)

## Final thoughts

이 포괄적인 글에서는 벡터에 대해 자세히 알아보고 벡터, Docker, Nginx, Better Stack을 사용하여 로그 처리 스택을 설정했습니다. Vector 구성 생성, Bash 스크립트와 Nginx의 도커화, Better Stack을 통한 로그 중앙 집중화 등 다양한 주제를 다루었습니다.

이제 문제 해결, 성능 향상, 애플리케이션 및 서비스 규정 준수 등 다양한 목적으로 로그를 효율적으로 관리할 준비가 되셨을 것입니다.

벡터에 대한 지식을 더 넓히려면 설명서를 참조하세요. Docker 및 Docker Compose에 대한 자세한 내용은 해당 문서 페이지를 참조하세요: Docker 및 Docker Compose.

읽어주셔서 감사드리며, 즐거운 로깅이 되시길 바랍니다!

