- https://docs.fluentbit.io/manual/pipeline/filters/kubernetes

Fluent Bit 쿠버네티스 필터는 쿠버네티스 메타데이터로 로그 파일을 보강할 수 있게 해줍니다.
Fluent Bit가 컨테이너에서 로그 파일을 읽도록 구성(꼬리 또는 systemd 입력 플러그인 사용)되어 있고 데몬셋으로 Kubernetes에 배포된 경우, 이 필터는 다음 작업을 수행하는 것을 목표로 합니다:
- 태그를 분석하여 다음 메타데이터를 추출합니다:
    - 파드 이름
    - 네임스페이스
    - 컨테이너 이름
    - 컨테이너 ID
- 쿠버네티스 API 서버를 쿼리하여 해당 파드에 대한 추가 메타데이터를 얻습니다:
    - 파드 ID
    - 레이블
    - 어노테이션

데이터는 메모리에 로컬로 캐시되어 각 레코드에 추가됩니다.

### Configuration Parameters
플러그인은 다음 구성 매개변수를 지원합니다:
- Buffer_Size : 쿠버네티스 API 서버에서 응답을 읽을 때 HTTP 클라이언트의 버퍼 크기를 설정합니다. 값은 단위 크기 사양에 따라야 합니다. 값이 0이면 제한이 없으며 버퍼는 필요에 따라 확장됩니다. 파드 사양이 버퍼 제한을 초과하면 메타데이터를 검색할 때 API 응답이 삭제되고 일부 쿠버네티스 메타데이터가 로그에 삽입되지 않을 수 있다는 점에 유의하세요. (32k)
- Kube_URL : API Server end-point (https://kubernetes.default.svc:443)
- Kube_CA_File : CA certificate file (/var/run/secrets/kubernetes.io/serviceaccount/ca.crt)
- Kube_CA_Path : Absolute path to scan for certificate files ()
- Kube_Token_File : Token file (/var/run/secrets/kubernetes.io/serviceaccount/token)
- Kube_Tag_Prefix : 소스 레코드가 테일 입력 플러그인에서 제공되는 경우 이 옵션을 사용하면 테일 구성에 사용되는 접두사를 지정할 수 있습니다. (kube.var.log.containers.)
- Merge_Log : 이 기능을 활성화하면 로그 필드 콘텐츠가 JSON 문자열 맵인지 확인하고, 맵인 경우 해당 맵 필드를 로그 구조의 일부로 추가합니다. (Off)
- Merge_Log_Key : Merge_Log가 활성화되면 필터는 수신 메시지의 로그 필드가 JSON 문자열 메시지라고 가정하고 이를 맵의 로그 필드와 동일한 수준에서 구조화된 표현으로 만들려고 시도합니다. 이제 Merge_Log_Key(문자열 이름)가 설정되면 원래 로그 콘텐츠에서 가져온 모든 새 구조화된 필드가 새 키 아래에 삽입됩니다. ()
- Merge_Log_Trim : Merge_Log가 활성화된 경우 필드 값을 잘라냅니다(가능한 \n 또는 \r 제거). (On)
- Merge_parser : 로그 키에 포함된 데이터를 파싱하는 방법을 지정하는 선택적 파서 이름입니다. 개발자 또는 테스트용으로만 사용하는 것이 좋습니다. ()
- Keep_Log : Keep_Log를 비활성화하면 병합이 성공적으로 완료되면 수신 메시지에서 로그 필드가 제거됩니다(Merge_Log도 활성화해야 함). (On)
- tls.debug : 디버그 수준은 0(아무것도 없음)에서 4(모든 세부 사항) 사이입니다. (-1)
- tls.verify : 활성화하면 Kubernetes API 서버에 연결할 때 인증서 유효성 검사를 켭니다. (On)
- Use_Journal : 활성화하면 필터가 저널 형식으로 들어오는 로그를 읽습니다. (Off)
- Cache_Use_Docker_Id : 활성화하면 docker_id가 변경될 때 K8에서 메타데이터를 가져옵니다. (Off)
- Regex_Parser : 대체 파서를 설정하여 레코드 태그를 처리하고 pod_name, 네임스페이스_name, 컨테이너_name 및 docker_id를 추출합니다. 파서는 파서 파일에 등록되어 있어야 합니다(예시로 파서 필터-kube-test를 참조하세요).

- K8S-LOGGING.Parser : 쿠버네티스 파드가 사전 정의된 파서를 제안하도록 허용한다(자세한 내용은 쿠버네티스 어노테이션 섹션에서 읽어본다). (Off)
- K8S-Logging.Exclude : 쿠버네티스 파드가 로그 프로세서에서 로그를 제외하도록 허용한다(자세한 내용은 쿠버네티스 어노테이션 섹션에서 읽어본다). (Off)

- Labels : 추가 메타데이터에 쿠버네티스 리소스 레이블을 포함한다. (On)
- Annotations : 추가 메타데이터에 쿠버네티스 리소스 어노테이션을 포함하세요. (On)
- Kube_meta_preload_cache_dir : 설정하면, 이 디렉터리에 있는 JSON 형식의 파일에서 쿠버네티스 메타데이터를 캐시/사전 로드할 수 있으며, 이름은 namespace-pod.meta로 지정된다.
- Dummy_Meta : 설정된 경우, 더미 메타 데이터 사용(테스트/개발 목적) (Off)
- DNS_Retries : 네트워크가 작동하기 시작할 때까지 DNS 조회를 N번 시도합니다. (6)
- DNS_Wait_Time : 네트워크 상태 확인 사이의 DNS 조회 간격 (30)
- Use_Kubelet : 이것은 로그를 향상시키기 위해 Kube Server API를 호출하는 대신 kubelet에서 메타데이터 정보를 가져오는 선택적 기능 플래그입니다. 이렇게 하면 대규모 클러스터의 Kube API 트래픽 폭주 문제를 완화할 수 있습니다. (Off)
- Kubelet_Port : HTTP 요청에 사용하는 kubelet 포트는 Use_Kubelet이 켜짐으로 설정된 경우에만 작동합니다. (10250)
- Kubelet_Host : HTTP 요청에 사용하는 kubelet 호스트는 Use_Kubelet이 켜짐으로 설정된 경우에만 작동합니다. (127.0.0.1)
- Kube_Meta_Cache_TTL : K8 캐시 메타데이터에 대한 구성 가능한 TTL입니다. 기본적으로 이 값은 0으로 설정되어 있어 캐시 항목에 대한 TTL이 비활성화되고 용량에 도달하면 캐시 항목이 무작위로 퇴거됩니다. 이 옵션을 활성화하려면 이 숫자를 시간 간격으로 설정해야 합니다. 예를 들어 이 값을 60 또는 60초로 설정하면 60초 이상 생성된 캐시 항목이 퇴거됩니다. (0)
- Kube_Token_TTL : K8 토큰의 '유효 기간'을 설정할 수 있습니다. 기본적으로 600초로 설정되어 있습니다. 이 시간이 지나면, 토큰은 Kube_Token_File 또는 Kube_Token_Command에서 다시 로드됩니다. (600)
- Kube_Token_Command : 명령을 실행하여 쿠버네티스 인가 토큰을 가져옵니다. 기본적으로 NULL이며 토큰 파일을 사용하여 토큰을 가져옵니다. 토큰을 가져올 명령을 수동으로 선택하려면 여기에서 명령을 설정할 수 있습니다. 예를 들어, `aws-iam-authenticator -i your-cluster-name token --token-only`를 실행하여 토큰을 설정합니다. 이 옵션은 현재 Linux 전용입니다.

### Processing the 'log' value
쿠버네티스 필터는 로그 키에 포함된 데이터를 처리하는 여러 가지 방법을 제공하는 것을 목표로 한다. 다음 워크플로에 대한 설명은 parsers.conf에 정의된 원래 Docker 파서가 다음과 같다고 가정합니다:
```
[PARSER]
    Name         docker
    Format       json
    Time_Key     time
    Time_Format  %Y-%m-%dT%H:%M:%S.%L
    Time_Keep    On
```
- 플루언트 비트 v1.2부터는 데이터 유형 충돌을 피하기 위해 출력에 Elasticsearch 데이터베이스를 사용하는 경우 디코더(Decode_Field_As)를 사용하지 않는 것이 좋습니다.

로그 키 처리를 수행하려면 이 필터에서 Merge_Log 구성 속성을 활성화해야 하며, 그러면 다음과 같은 처리 순서가 수행됩니다:
    - 파드가 파서를 제안하는 경우, 필터는 해당 파서를 사용하여 로그 콘텐츠를 처리한다.
    - Merge_Parser 옵션이 설정되어 있고 파드가 파서를 제안하지 않은 경우, 구성에서 제안된 파서를 사용하여 로그 콘텐츠를 처리한다.
    - 파서가 제안되지 않았고 Merge_Parser가 설정되지 않은 경우, 콘텐츠를 JSON으로 처리해본다.

로그 값 처리에 실패하면 해당 값은 그대로 유지됩니다. 위의 순서는 연쇄적이지 않으므로 배타적이며 필터는 위의 옵션 중 하나만 시도하고 모두 시도하지 않습니다.

### Kubernetes Annotations
플루언트 비트 쿠버네티스 필터의 유연한 기능은 쿠버네티스 파드가 레코드를 처리할 때 로그 프로세서 파이프라인에 대해 특정 동작을 제안할 수 있도록 하는 것입니다. 현재 지원되는 기능은 다음과 같다:
- 사전 정의된 파서 제안
- 로그 제외 요청
다음과 같은 어노테이션을 사용할 수 있다:
- fluentbit.io/parser[_stream][-container] : 사전 정의된 구문 분석기를 제안합니다. 구문 분석기는 플루언트 비트에 의해 이미 등록되어 있어야 한다. 이 옵션은 플루언트 비트 구성(쿠버네티스 필터)에서 K8S-Logging.Parser 옵션을 활성화한 경우에만 처리된다. 이 옵션이 있는 경우, 스트림(stdout 또는 stderr)이 해당 특정 스트림을 제한합니다. 존재하는 경우, 컨테이너는 파드의 특정 컨테이너를 재정의할 수 있다.
- fluentbit.io/exclude[_stream][-container] : 파드에서 생성된 로그를 제외할지 여부를 플루언트비트에 요청한다. 이 옵션은 플루언트 비트 구성(쿠버네티스 필터)에서 K8S-Logging.Exclude 옵션을 활성화한 경우에만 처리된다.

### Annotation Examples in Pod definition
#### Suggest a parser
다음 파드 정의는 표준 출력으로 아파치 로그를 내보내는 파드를 실행하며, 어노테이션에서 미리 정의된 파서인 아파치를 사용하여 데이터를 처리해야 한다고 제안한다:
```
apiVersion: v1
kind: Pod
metadata:
  name: apache-logs
  labels:
    app: apache-logs
  annotations:
    fluentbit.io/parser: apache
spec:
  containers:
  - name: apache
    image: edsiper/apache_logs
```
#### Request to exclude logs
사용자가 로그 프로세서에게 해당 파드의 로그를 건너뛰도록 요청하고 싶은 특정 상황이 있습니다:
```
apiVersion: v1
kind: Pod
metadata:
  name: apache-logs
  labels:
    app: apache-logs
  annotations:
    fluentbit.io/exclude: "true"
spec:
  containers:
  - name: apache
    image: edsiper/apache_logs
```
주석 값은 참 또는 거짓을 취할 수 있는 부울이며 따옴표로 묶어야 합니다.

### Workflow of Tail + Kubernetes Filter
쿠버네티스 필터는 Tail 또는 Systemd 입력 플러그인에 의존하여 쿠버네티스 메타데이터로 레코드를 처리하고 보강한다. 여기서는 Tail의 워크플로우와 그 구성이 Kubernetes 필터와 어떻게 연관되는지 설명하겠습니다. 다음 구성 예제를 살펴보세요(프로덕션이 아닌 데모용):
```
[INPUT]
    Name    tail
    Tag     kube.*
    Path    /var/log/containers/*.log
    Parser  docker

[FILTER]
    Name             kubernetes
    Match            kube.*
    Kube_URL         https://kubernetes.default.svc:443
    Kube_CA_File     /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    Kube_Token_File  /var/run/secrets/kubernetes.io/serviceaccount/token
    Kube_Tag_Prefix  kube.var.log.containers.
    Merge_Log        On
    Merge_Log_Key    log_processed
```
입력 섹션에서 Tail 플러그인은 경로 /var/log/containers/에서 .log로 끝나는 모든 파일을 모니터링합니다. 모든 파일에 대해 모든 줄을 읽고 도커 파서를 적용합니다. 그런 다음 레코드는 확장 태그와 함께 다음 단계로 전송됩니다.
꼬리는 태그 확장을 지원하므로, 태그에 별표 문자(*)가 있는 경우 파일 이름과 경로가 있는 경우 해당 값을 모니터링되는 파일의 절대 경로로 대체합니다:
```
/var/log/container/apache-logs-annotated_default_apache-aeeccc7a9f00f6e4e066aeff0434cf80621215071f1b20a51e8340aa7c35eac6.log
```
를 입력하면 해당 파일의 모든 레코드에 대한 태그가 됩니다:
```
kube.var.log.containers.apache-logs-annotated_default_apache-aeeccc7a9f00f6e4e066aeff0434cf80621215071f1b20a51e8340aa7c35eac6.log
```
- 슬래시는 점으로 대체된다는 점에 유의하세요.

Kubernetes 필터가 실행되면, kube로 시작하는 모든 레코드를 일치시키려고 시도합니다. (끝나는 점에 유의), 위에서 언급한 파일의 레코드가 일치 규칙에 맞으면 필터가 레코드를 보강하려고 시도합니다.
Kubernetes 필터는 로그의 출처가 어디인지는 신경 쓰지 않지만, 모니터링되는 파일의 절대 이름은 신경 쓰는데, 그 이유는 이 정보에 Kubernetes 마스터/API 서버에서 실행 중인 파드와 관련된 메타데이터를 검색하는 데 사용되는 파드 이름과 네임스페이스 이름이 포함되어 있기 때문입니다.
- 파드 사양이 큰 경우(많은 수의 환경 변수 등으로 인해 발생할 수 있음), kubernetes 필터의 Buffer_Size 파라미터를 늘려야 한다. 오브젝트 크기가 이 버퍼를 초과하면 일부 메타데이터가 로그에 삽입되지 않을 수 있습니다.

구성 속성 Kube_Tag_Prefix가 구성된 경우(Fluent Bit >= 1.1.x에서 사용 가능), 해당 값을 사용하여 이전 입력 섹션의 태그에 추가된 접두사를 제거합니다. 구성 속성의 기본값은 kube.var.logs.containers입니다. 로 설정되어 있으므로 이전 태그 콘텐츠가 변환됩니다:
```
kube.var.log.containers.apache-logs-annotated_default_apache-aeeccc7a9f00f6e4e066aeff0434cf80621215071f1b20a51e8340aa7c35eac6.log
```
to:
```
apache-logs-annotated_default_apache-aeeccc7a9f00f6e4e066aeff0434cf80621215071f1b20a51e8340aa7c35eac6.log
```
- 위의 변환은 원본 태그를 수정하지 않고 필터가 메타데이터 조회를 수행하기 위한 새로운 표현을 생성할 뿐입니다.

이 새 값은 필터에서 파드 이름과 네임스페이스를 조회하는 데 사용되며, 이를 위해 필터는 내부 정규식을 사용합니다:
```
(?<pod_name>[a-z0-9](?:[-a-z0-9]*[a-z0-9])?(?:\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*)_(?<namespace_name>[^_]+)_(?<container_name>.+)-(?<docker_id>[a-z0-9]{64})\.log$
```
이 작업이 어떻게 수행되는지 Rublar.com 웹 사이트에서 확인할 수 있으며, 다음 데모 링크를 확인하세요: https://rubular.com/r/HZz3tYAahj6JCd

#### Custom Regex
일반적인 조건이 아닌 특정 조건에서 사용자는 하드코딩된 정규식을 변경하고 싶을 수 있으며, 이를 위해 Regex_Parser 옵션을 사용할 수 있습니다(상단에 문서화되어 있음).

#### Final Comments
따라서 이 시점에서 필터는 pod_name과 네임스페이스의 값을 수집할 수 있으며, 이 정보로 로컬 캐시(내부 해시 테이블)에서 해당 키 쌍에 대한 메타데이터가 존재하는지 확인하고, 존재하는 경우 메타데이터 값으로 레코드를 보강하고, 그렇지 않은 경우 Kubernetes 마스터/API 서버에 연결하여 해당 정보를 검색합니다.

### Optional Feature: Using Kubelet to Get Metadata
클러스터가 너무 커서 너무 많은 요청이 전송될 때 kube-apiserver가 넘어져 응답하지 않는 문제가 보고되었습니다. 이 기능의 경우, 유창한 비트 쿠버네티스 필터는 요청을 kube-apiserver 대신 kubelet /pods 엔드포인트로 전송하여 파드 정보를 검색하고 이를 사용하여 로그를 보강합니다. Kubelet은 노드에서 로컬로 실행되므로 요청에 더 빠르게 응답하고 각 노드는 한 번만 하나의 요청을 받게 됩니다. 이렇게 하면 다른 요청을 처리할 수 있는 kube-apiserver의 전력을 절약할 수 있습니다. 이 기능을 활성화하면 로그에 추가되는 kubernetes 메타데이터에 차이가 없어야 하지만, 클러스터가 클 때는 Kube-apiserver 병목 현상을 피해야 합니다.

#### Configuration Setup
이 기능을 사용하려면 몇 가지 구성 설정이 필요합니다.
플루언트 비트 데몬셋의 역할 구성 예시:
```
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: fluentbitds
  namespace: fluentbit-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: fluentbit
rules:
  - apiGroups: [""]
    resources:
      - namespaces
      - pods
      - nodes
      - nodes/proxy
    verbs: 
      - get
      - list
      - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: fluentbit
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: fluentbit
subjects:
  - kind: ServiceAccount
    name: fluentbitds
    namespace: fluentbit-system
```
차이점은 리소스 노드/프록시가 HTTP 요청을 수신하려면 kubelet에 특별한 권한이 필요하다는 것입니다. 역할 또는 clusterRole을 생성할 때, 리소스에 대한 규칙에 노드/프록시를 추가해야 합니다.
플루언트 비트 구성 예제:
```
    [INPUT]
        Name              tail
        Tag               kube.*
        Path              /var/log/containers/*.log
        DB                /var/log/flb_kube.db
        Parser            docker
        Docker_Mode       On
        Mem_Buf_Limit     50MB
        Skip_Long_Lines   On
        Refresh_Interval  10

    [FILTER]
        Name                kubernetes
        Match               kube.*
        Kube_URL            https://kubernetes.default.svc.cluster.local:443
        Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token
        Merge_Log           On
        Buffer_Size         0
        Use_Kubelet         true
        Kubelet_Port        10250
```
따라서 유창한 비트 구성을 위해서는 이 기능을 활성화하려면 Use_Kubelet을 true로 설정해야 합니다.
데몬셋 구성 예제:
```
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentbit
  namespace: fluentbit-system
  labels:
    app.kubernetes.io/name: fluentbit
spec:
  selector:
    matchLabels:
      name: fluentbit
  template:
    metadata:
      labels:
        name: fluentbit
    spec:
      serviceAccountName: fluentbitds
      containers:
        - name: fluent-bit
          imagePullPolicy: Always
          image: fluent/fluent-bit:latest
          volumeMounts:
            - name: varlog
              mountPath: /var/log
            - name: varlibdockercontainers
              mountPath: /var/lib/docker/containers
              readOnly: true
            - name: fluentbit-config
              mountPath: /fluent-bit/etc/
          resources:
            limits:
              memory: 1500Mi
            requests:
              cpu: 500m
              memory: 500Mi
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
      volumes:
        - name: varlog
          hostPath:
            path: /var/log
        - name: varlibdockercontainers
          hostPath:
            path: /var/lib/docker/containers
        - name: fluentbit-config
          configMap:
            name: fluentbit-config
```
핵심은 hostNetwork를 true로 설정하고 dnsPolicy를 ClusterFirstWithHostNet으로 설정하여 유창한 비트 데몬셋이 로컬로 Kubelet을 호출할 수 있도록 하는 것입니다. 그렇지 않으면 kubelet에 대한 dns를 확인할 수 없습니다.
이제 이 새로운 기능을 사용할 수 있습니다!

#### Verify that the Use_Kubelet option is working
기본적으로 로그 파일을 쿠버네티스 메타데이터로 보강하는 경험에는 차이가 없어야 합니다.
플루언트 비트가 kubelet을 사용하고 있는지 확인하려면, 플루언트 비트 로그를 확인하면 다음과 같은 로그가 있어야 합니다:
```
[ info] [filter:kubernetes:kubernetes.0] testing connectivity with Kubelet...
```
디버그 모드에서는 더 많은 것을 볼 수 있습니다:
```
[debug] [filter:kubernetes:kubernetes.0] Send out request to Kubelet for pods information.
[debug] [filter:kubernetes:kubernetes.0] Request (ns=<namespace>, pod=node name) http_do=0, HTTP Status: 200
[ info] [filter:kubernetes:kubernetes.0] connectivity OK
[2021/02/05 10:33:35] [debug] [filter:kubernetes:kubernetes.0] Request (ns=<Namespace>, pod=<podName>) http_do=0, HTTP Status: 200
[2021/02/05 10:33:35] [debug] [filter:kubernetes:kubernetes.0] kubelet find pod: <podName> and ns: <Namespace> match
```