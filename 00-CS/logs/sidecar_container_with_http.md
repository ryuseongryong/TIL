- https://kodekloud.com/blog/kubernetes-sidecar-container/

# Sidecar Container: What is it and How to use it(examples)

코드나 이미지를 수정하지 않고 기본 컨테이너에 추가 기능을 추가하고 싶었던 적이 있나요? 아니면 성능에 영향을 주지 않고 컨테이너화된 애플리케이션을 모니터링, 로깅 또는 보호하고 싶으신가요? 그렇다면 쿠버네티스의 사이드카 컨테이너에 대해 배워야 합니다.

이 글에서는 사이드카 컨테이너가 무엇인지 살펴보고 이를 사용하는 방법에 대한 몇 가지 예를 살펴보겠습니다. 쿠버네티스 개념과 명령어에 대한 기본적인 이해가 있다고 가정합니다. 그렇지 않다면 완전 초보자를 위한 Kubernetes 과정을 확인하실 수 있습니다.

## Key Takeaways
사이드카 컨테이너를 사용하면 동일한 포드에서 메인 컨테이너와 함께 추가 컨테이너를 실행하여 메인 컨테이너를 강화하는 작업을 수행할 수 있습니다.
사이드카 컨테이너의 일반적인 사용 사례 중 하나는 구성 파일, 시크릿 또는 인증서와 같이 원격 소스의 데이터를 메인 컨테이너에서 공유하는 로컬 볼륨으로 동기화하는 것이다.
쿠버네티스에서 사이드카 컨테이너를 사용하려면, 동일한 라이프사이클, 리소스 및 네트워크 네임스페이스를 공유하지만 자체 파일 시스템과 프로세스 공간을 가진 두 개의 컨테이너로 파드를 정의해야 한다.

## What is a Sidecar Container?
사이드카 컨테이너는 동일한 포드에서 메인 컨테이너와 함께 추가 컨테이너를 실행할 수 있는 디자인 패턴입니다. 사이드카 컨테이너는 원격 소스에서 데이터 동기화, 로그 수집 및 전송, 상태 확인 및 메트릭 제공, 네트워크 트래픽 프록시, 데이터 암호화 또는 복호화, 테스트를 위한 결함 주입 등 메인 컨테이너를 보완하는 작업을 수행할 수 있습니다.

사이드카 컨테이너는 메인 컨테이너와 동일한 수명 주기, 리소스 및 네트워크 네임스페이스를 공유하지만 자체 파일 시스템 및 프로세스 공간을 갖습니다. 즉, 사이드카 컨테이너는 메인 컨테이너와 동일한 포트, 볼륨, 환경 변수에 액세스할 수 있지만 실행을 간섭할 수는 없습니다.

예제를 통해 서로 다른 두 가지 사이드카 사용 사례를 살펴보겠습니다.

## Prerequisites
이 도움말을 따라 하려면 다음이 필요합니다:

- 하나 이상의 워커 노드가 있는 쿠버네티스 클러스터. 미니큐브를 사용하여 생성할 수 있습니다.
- 클러스터에 액세스하도록 설치 및 구성된 kubectl 명령줄 도구.
- 코드 에디터. 이 예제에서는 VS-Code를 사용했다.
- 쿠버네티스 개념과 명령어에 대한 기본적인 이해.

## Example 1: Access logs from logfile in main container using sidecar
사이드카 컨테이너의 기본적인 사용 사례 중 하나는 사이드카 컨테이너를 사용하여 메인 컨테이너의 로그 파일에서 로그에 액세스하는 것입니다. 예를 들어, 메인 컨테이너의 로그를 추적하여 표준 출력으로 인쇄하고 싶을 수 있습니다.

이를 보여주기 위해 매초마다 파일에 로그를 기록하는 간단한 애플리케이션을 만들어 보겠습니다. 메인 컨테이너는 로그를 생성하는 셸 스크립트를 실행하는 바쁘다 상자 이미지를 실행합니다. 사이드카 컨테이너는 파일에서 로그를 읽기 위해 꼬리를 실행하는 또 다른 바쁜 상자 이미지를 실행합니다.

먼저, 두 개의 컨테이너로 파드를 정의하는 Kubernetes 배포를 생성해야 합니다:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: log-app # Name of the deployment
spec:
  replicas: 1 # Number of replicas
  selector:
    matchLabels:
      app: log-app # Label selector for the pod
  template:
    metadata:
      labels:
        app: log-app # Label for the pod
    spec:
      volumes:
        - name: log-volume # Define a volume to store the logs
          emptyDir: {} # Use an emptyDir volume type
      containers:
        - name: log-generator # Main container
          image: busybox # Use the busybox image
          command: ["/bin/sh"] # Override the default command
          args: ["-c", "while true; do date >> /var/log/app.log; sleep 1; done"] # Run a shell script that generates logs every second
          volumeMounts:
            - name: log-volume # Mount the volume to the container
              mountPath: /var/log # Mount it to the log directory
        - name: log-reader # Sidecar container
          image: busybox # Use another busybox image
          command: ["/bin/sh"] # Override the default command
          args: ["-c", "tail -f /var/log/app.log"] # Run a shell script that tails the log file
          volumeMounts:
            - name: log-volume # Mount the same volume as the main container
              mountPath: /var/log # Mount it to the same directory in the sidecar container

```

파드에는 로그 생성기와 로그 리더라는 두 개의 컨테이너가 있음을 알 수 있습니다. 로그 생성기는 로그-볼륨이라는 볼륨에 로그를 저장합니다. 로그-리더를 사용하여 로그-볼륨에 저장된 로그를 읽고 싶습니다.

(이 부분은 volume이 공유되기 때문에 가능한 방법)

## Example 2: Access logs from the main container using HTTP in the sidecar
사이드카 컨테이너의 또 다른 기본 사용 사례는 사이드카 컨테이너에서 HTTP를 사용하여 메인 컨테이너의 로그에 액세스하는 것입니다. 예를 들어, 메인 컨테이너의 로그를 반환하는 HTTP 엔드포인트를 노출하고 싶을 수 있습니다.

이를 보여주기 위해 매초마다 표준 출력에 로그를 기록하는 간단한 웹 서버를 만들어 보겠습니다. 메인 컨테이너는 포트 80을 노출하는 nginx 이미지를 실행합니다. 사이드카 컨테이너는 포트 8080에서 수신 대기하고 메인 컨테이너의 로그를 반환하기 위해 socat을 실행하는 알파인 이미지를 실행합니다.

먼저, 두 개의 컨테이너로 파드를 정의하는 Kubernetes 배포를 생성해야 합니다:
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server # Name of the deployment
spec:
  replicas: 1 # Number of replicas
  selector:
    matchLabels:
      app: web-server # Label selector for the pod
  template:
    metadata:
      labels:
        app: web-server # Label for the pod
    spec:
      containers:
        - name: nginx # Main container
          image: nginx # Use the nginx image
          ports:
            - containerPort: 80 # Expose port 80
          command: ["/bin/sh"] # Override the default command
          args: ["-c", "while true; do echo \"$(date) Hello from nginx\"; sleep 1; done | tee /var/log/nginx/access.log"] # Run a shell script that generates logs every second and writes them to a file and standard output 
        - name: socat # Sidecar container
          image: alpine/socat # Use the alpine/socat image
          ports:
            - containerPort: 8080 # Expose port 8080
          command: ["socat"] # Override the default command
          args: ["-v", "TCP-LISTEN:8080,fork,reuseaddr", "EXEC:\"kubectl logs web-server-7f9f8c4b9-6xq8w -c nginx\""] # Run socat to listen on port 8080 and execute kubectl logs to return the logs from the main container
```
다음으로, 사이드카 컨테이너의 포트를 외부에 노출하는 Kubernetes 서비스를 생성해야 합니다:
```
apiVersion: v1
kind: Service
metadata:
  name: web-server-service # Name of the service
spec:
  type: LoadBalancer # Use a load balancer service type
  selector:
    app: web-server # Select pods with this label
  ports:
    - protocol: TCP # Use TCP protocol
      port: 80 # Expose port 80 on the service
      targetPort: 8080 # Map it to port 8080 on the pod

```
배포에는 두 개의 컨테이너가 실행 중인 하나의 파드가 있으며, 이 서비스에는 클라우드 제공자가 할당한 외부 IP 주소가 있음을 알 수 있습니다. 이 IP 주소를 사용하여 브라우저에서 사이드카 컨테이너의 로그에 액세스할 수 있습니다:

브라우저에서 사이드카 컨테이너의 로그에 액세스하려면 획득한 서비스의 외부 IP 주소를 사용할 수 있습니다. 이 경우 외부 IP 주소는 35.238.123.123입니다.

웹 브라우저를 열고 다음 URL을 입력합니다:

`http://35.238.123.123:8080`

그러면 사이드카 컨테이너로 HTTP 요청이 전송되고, 사이드카 컨테이너는 요청을 메인 컨테이너로 프록시하여 메인 컨테이너의 표준 출력에서 로그를 반환합니다.

또한 사이드카 컨테이너가 메인 컨테이너의 표준 출력에서 로그를 반환하는 것을 볼 수 있습니다. 요청은 사이드카 컨테이너에 의해 메인 컨테이너로 프록시됩니다.

요청이 사이드카 컨테이너에 의해 메인 컨테이너로 프록시되는지 확인하려면 다음 명령을 사용하면 됩니다:

`kubectl logs web-server-7f9f8c4b9-6xq8w -c socat`

socat이 포트 8080에서 수신 대기 중이며 브라우저로부터의 연결을 수락하고 있음을 알 수 있습니다. 그런 다음, 자식 프로세스를 포크하고 kubectl 로그를 실행하여 web-server-7f9f8c4b9-6xq8w라는 파드의 nginx라는 메인 컨테이너에서 로그를 가져옵니다. 이렇게 하면 사이드카 컨테이너가 메인 컨테이너의 로그를 반환하는 HTTP 엔드포인트를 노출합니다.

## Why use Kubernetes sidecar container
사이드카 컨테이너는 파일 동기화, 로깅, 감시자 기능 등 메인 컨테이너에 헬퍼 기능을 제공합니다.

사이드카는 기본 애플리케이션의 메인 트래픽이나 API의 일부가 아닙니다. 일반적으로 비동기적으로 작동하며 공용 API에 관여하지 않습니다. 따라서 코드나 이미지를 수정하지 않고도 메인 컨테이너를 향상시킬 수 있습니다.

일반적인 예는 중앙 로깅 에이전트입니다. 메인 컨테이너는 그냥 stdout에 로깅할 수 있지만 사이드카 컨테이너는 모든 로그를 중앙 로깅 서비스로 보내 전체 시스템의 로그와 함께 집계합니다.

다음은 쿠버네티스에서 사이드카 컨테이너를 사용할 때 얻을 수 있는 몇 가지 이점이다:
- 모듈화: 서로 다른 기능에 대한 우려를 분리하고 메인 컨테이너의 코드나 이미지를 수정하지 않아도 됩니다. 따라서 애플리케이션을 더욱 모듈화할 수 있고 유지 관리 및 업데이트가 더 쉬워집니다.
- 재사용성: 동일한 사이드카 컨테이너를 동일한 기능이 필요한 다른 메인 컨테이너에 재사용할 수 있습니다. 이렇게 하면 중복을 줄이고 일관성과 효율성을 개선할 수 있습니다.
- 확장성: 사이드카 컨테이너의 리소스 요구 사항이나 성능 특성이 다른 경우 메인 컨테이너와 독립적으로 사이드카 컨테이너를 확장할 수 있습니다. 이를 통해 애플리케이션의 리소스 사용률과 성능을 최적화할 수 있습니다.
- 보안: 다른 보안 정책이나 네트워크 규칙을 사용하여 사이드카 컨테이너를 메인 컨테이너에서 격리할 수 있습니다. 이를 통해 애플리케이션에 대한 무단 액세스 또는 악의적인 공격을 방지할 수 있습니다.





