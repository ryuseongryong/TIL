- https://grafana.com/docs/loki/latest/configure/#ingester_config

# 그라파나 로키 구성 매개변수
그라파나 로키는 로키가 실행되는 모드에 따라 로키 서버 및 개별 구성 요소에 대한 정보가 포함된 YAML 파일(일반적으로 loki.yaml이라고 함)로 구성됩니다.

## 런타임에 Loki 구성 인쇄
로키에 -print-config-stderr 또는 -log-config-reverse-order 플래그를 전달하면(또는 -print-config-stderr=true) 로키는 기본 제공 기본값에서 생성한 전체 구성 개체를 구성 파일의 오버라이드로 먼저 덤프하고, 플래그의 오버라이드로 두 번째로 덤프합니다.

결과는 Loki 구성 구조의 모든 구성 개체에 대한 값으로, 매우 큰...

사용하지 않거나 정의하지 않은 스토리지 구성과 같은 많은 값이 설치와 관련이 없을 수 있는데, 이는 모든 옵션이 사용 중인지 여부에 따라 기본값이 있기 때문에 예상되는 현상입니다.

이 설정은 Loki가 실행할 때 사용하는 것으로, 설정과 관련된 문제를 디버깅하는 데 유용하며 특히 설정 파일과 플래그가 제대로 읽히고 로드되는지 확인하는 데 유용합니다.

./loki와 같이 Loki를 직접 실행할 때는 -print-config-stderr를 사용하면 전체 Loki 구성을 빠르게 출력할 수 있으므로 유용합니다.

-log-config-reverse-order는 모든 환경에서 Loki를 실행하는 플래그로, 구성 항목의 순서를 반대로 하여 Grafana의 Explore에서 볼 때 구성 순서가 위에서 아래로 올바르게 읽히도록 합니다.

## 런타임에 다시 로드
프롬테일은 런타임에 구성을 다시 로드할 수 있습니다. 새 구성이 제대로 구성되지 않은 경우 변경 사항이 적용되지 않습니다. 구성 로드는 Promtail 프로세스에 SIGHUP을 보내거나 /reload 엔드포인트에 HTTP POST 요청을 보내면 트리거됩니다( --server.enable-runtime-reload 플래그가 활성화된 경우).

## 구성 파일 참조
로드할 구성 파일을 지정하려면 명령줄에서 -config.file 플래그를 전달합니다. 이 값은 쉼표로 구분된 경로 목록일 수 있으며, 존재하는 첫 번째 파일이 사용됩니다. -config.file 인수를 지정하지 않으면 Loki는 현재 작업 디렉터리와 config/ 하위 디렉터리에서 config .yaml을 찾아서 이를 사용하려고 시도합니다.

파일은 아래 체계에 정의된 YAML 형식으로 작성됩니다. 괄호는 매개변수가 선택 사항임을 나타냅니다. 목록에 없는 매개변수의 경우 값이 지정된 기본값으로 설정됩니다.

### 구성에서 환경 변수 사용
참고: 이 기능은 Loki 2.1 이상에서만 사용할 수 있습니다.

구성 파일에서 환경 변수 참조를 사용하여 배포 중에 구성할 수 있는 값을 설정할 수 있습니다. 이렇게 하려면 -config.expand-env=true를 전달하고 사용하세요:

```
${VAR}
```
여기서 VAR은 환경 변수의 이름입니다.

각 변수 참조는 시작 시 환경 변수 값으로 대체됩니다. 대소문자를 구분하며 YAML 파일이 구문 분석되기 전에 대체됩니다. 정의되지 않은 변수에 대한 참조는 기본값이나 사용자 지정 오류 텍스트를 지정하지 않는 한 빈 문자열로 대체됩니다.

기본값을 지정하려면 다음을 사용합니다:

```
${VAR:-default_value}
```
여기서 default_value는 환경 변수가 정의되지 않은 경우 사용할 값입니다.

이 설정 방법을 사용하려면 명령줄에 -config.expand-env 플래그를 전달하세요.

### 일반 자리 표시자
<boolean> : a boolean that can take the values true or false
<int> : any integer matching the regular expression [1-9]+[0-9]*
<duration> : a duration matching the regular expression [0-9]+(ns|us|µs|ms|[smh])
<labelname> : a string matching the regular expression [a-zA-Z_][a-zA-Z0-9_]*
<labelvalue> : a string of unicode characters
<filename> : a valid path relative to current working directory or an absolute path.
<host> : a valid string consisting of a hostname or IP followed by an optional port number
<string> : a string
<secret> : a string that represents a secret, such as a password

