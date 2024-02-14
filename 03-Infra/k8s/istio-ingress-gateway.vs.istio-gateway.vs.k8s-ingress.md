
# Istio Ingress gateway vs Istio Gateway vs Kubernetes Ingress
- https://dev.to/vivekanandrapaka/istio-ingress-gateway-vs-istio-gateway-vs-kubernetes-ingress-5hgg

## Objective
네트워크 트래픽 관리는 모든 쿠버네티스 설정의 핵심 영역 중 하나이며, 들어오는 트래픽을 처리할 때 클러스터의 여러 구성 요소가 어떻게 작동하는지 이해하는 것이 중요합니다.

이 게시물의 주요 목적은 nginx 인그레스 컨트롤러와 Istio 서비스 메시의 구성 요소와 각각의 주요 차이점에 대해 다음과 함께 설명하는 것입니다:

- 쿠버네티스 클러스터에서 사용되는 다양한 서비스 유형
- 인그레스 컨트롤러란 무엇인가요?
- 인그레스 리소스란 무엇인가요?
- 이스티오 서비스 메시란 무엇인가요?
- Nginx 인그레스 컨트롤러와 Istio 서비스 메시의 트래픽 흐름.
- Istio 서비스 메시와 Nginx 인그레스 컨트롤러는 언제 사용해야 하나요?

## 쿠버네티스의 서비스 - 간략한 요약
Nginx 인그레스 컨트롤러와 Istio 서비스 메시를 알기 전에 네이티브 쿠버네티스 설정의 서비스 개념에 대해 알아두는 것이 중요합니다.

쿠버네티스에서 작업했거나 쿠버네티스의 기본을 배운 적이 있다면 "서비스"라는 객체 유형에 대해 잘 알고 있어야 합니다.

파드에서 호스팅되는 워크로드가 트래픽을 수용하려면 일종의 로드 밸런서가 필요합니다. 우리가 배포하는 모든 파드는 임시적이므로, 파드가 종료되거나 죽으면 다른 IP 주소를 가진 다른 파드로 대체되며, 파드와 직접 통신할 수 없고 대신 서비스 오브젝트라는 개념을 사용합니다.

서비스는 애플리케이션을 호스팅하는 배포된 파드를 노출하기 위한 논리적 추상화입니다. 다음은 일반적으로 사용되는 몇 가지 서비스 유형입니다.

- NodePort
- ClusterIP
- LoadBalancer
- ExternalName

선택한 서비스 유형에 따라 트래픽이 적절하게 라우팅됩니다. 각 서비스의 기능에 대해 간략히 살펴보겠습니다.

### NodePort

이러한 종류의 서비스 오브젝트를 사용하면 쿠버네티스는 각 노드에 30000-32768 범위의 임의 포트를 생성하며, 다음과 같이 노드의 IP 주소 뒤에 포트를 입력하면 백엔드 파드에 액세스할 수 있습니다:
http://192.168.126.8:32768

다음은 노드 포트 서비스용 YAML 파일입니다.
```
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: MyApp
  ports:
      # By default and for convenience, the `targetPort` is set to the same value as the `port` field.
    - port: 80
      targetPort: 80
      # Optional field
      # By default and for convenience, the Kubernetes control plane will allocate a port from a range (default: 30000-32767)
      nodePort: 30007
```

노드가 여러 개 있는 경우 각 노드에는 고유 IP가 있으며 워크로드에 액세스하려면 IP 주소와 포트 번호를 사용해야 합니다. 이는 테스트 목적과 로컬 개발에는 좋지만 실제 시나리오에는 적합하지 않습니다.

### ClusterIP

이것은 클러스터 내에서 워크로드를 생성하고 노출하는 데 사용되는 일반적인 서비스 중 하나이다. nodePort 서비스와 달리, 쿠버네티스 클러스터에 포트 번호를 할당할 포트를 선택할 수 있는 옵션이 있습니다. 클러스터IP 유형의 서비스를 생성하면 IP와 포트 번호가 지정된 서비스 오브젝트가 생성되고 클러스터 전체에서 서비스에 할당된 동일한 IP/DNS 서비스 이름을 사용하여 클러스터에 액세스할 수 있습니다. 서비스 오브젝트를 생성할 때 생성하려는 서비스 유형을 지정하지 않으면(예: clusterIP/NodePort/Loadbalancer), 기본적으로 쿠버네티스는 clusterIP 유형의 서비스를 생성한다.

아래는 clusterIp 유형의 서비스에 대한 kubernetes.io의 YAML 파일 스니펫입니다.

```
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376

```

이 유형의 서비스는 워크로드를 쿠버네티스 클러스터 외부에 노출시키지 않으며 백엔드 API 서비스, 데이터베이스, 배치 처리 워크로드 등과 같은 워크로드에 적합합니다.
일반적으로 외부에 노출할 필요가 없는 서비스는 클러스터IP로 생성됩니다.

### LoadBalancer

이것은 워크로드를 외부 세계와 클라우드에 노출하는 데 사용되는 가장 일반적으로 사용되는 서비스 중 하나입니다. 이러한 종류의 서비스를 사용하면 관리형 쿠버네티스 클러스터가 호스팅되는 클라우드 서비스 제공업체에서 로드 밸런서를 스핀업하고 클라우드에 IP 주소를 생성하여 쿠버네티스 클러스터에서 외부로 액세스할 수 있습니다. 이것은 프런트엔드 서비스를 노출하는 데 사용되는 서비스 유형 중 하나입니다. 서비스에 할당할 IP 주소를 지정할 수도 있습니다.

아래는 로드밸런서용 YAML 파일입니다.

```
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
  clusterIP: 10.0.171.239
  type: LoadBalancer
status:
  loadBalancer:
    ingress:
    - ip: 192.0.2.127
```

### ExternalName

외부 이름 유형의 서비스는 위에서 설명한 다른 유형의 서비스처럼 파드 선택기를 기반으로 파드 대신 DNS 이름을 가리킵니다.

다음은 외부 네임 서비스를 정의하는 방법을 보여주는 yaml 파일입니다.

```
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: prod
spec:
  type: ExternalName
  externalName: my.database.example.com

```

### 인그레스 컨트롤러란 무엇이며 왜 필요한가요?
이제 쿠버네티스 서비스의 기본 사항을 살펴보았으니, Nginx 인그레스 컨트롤러로 이동해 보겠습니다.

위에서 설명한 서비스 중 하나는 로드 밸런서이며, 이러한 종류의 서비스를 사용하여 워크로드를 노출할 수 있지만, 이는 몇 가지 다른 워크로드에 유용합니다. 그러나 마이크로 서비스가 커지면 외부에 노출하려면 로드 밸런서 유형의 여러 서비스를 사용해야 하며 이러한 각 서비스는 클라우드 서비스 제공업체에 추가 로드 밸런서와 공용 IP를 생성하므로 결국 모든 서비스를 관리해야 할 뿐만 아니라 로드 밸런서 서비스에서 프로비저닝한 각각의 공용 IP에 대한 비용도 지불해야 합니다.

여기서 인그레스 컨트롤러가 등장합니다.

인그레스 컨트롤러는 쿠버네티스 서비스에 대한 역방향 프록시, 구성 가능한 트래픽 라우팅 및 TLS 종료 기능을 제공하는 소프트웨어이다. 쿠버네티스 인그레스 리소스는 개별 쿠버네티스 서비스에 대한 인그레스 규칙과 경로를 구성하는 데 사용됩니다.

nginx 인그레스 컨트롤러와 같은 인그레스 컨트롤러를 사용하는 경우 워크로드를 노출하기 위해 여러 로드 밸런서 유형의 서비스를 생성할 필요가 없습니다. Nginx 인그레스 컨트롤러를 생성하면 로드 밸런서 유형의 서비스 유형이 생성되며, 이를 클러스터IP 유형의 서비스에 노출하여 모든 워크로드에 액세스하기 위한 인바운드 IP로 사용할 수 있습니다. 하지만 단일 서비스 유형을 생성하고 트래픽을 여러 백엔드 서비스로 라우팅하려면 어떻게 해야 할까요? 이는 인그레스 리소스를 사용하여 수행할 수 있습니다. 인그레스 리소스는 들어오는 트래픽을 적절한 백엔드 서비스로 전달하고 서비스로 전송된 트래픽이 파드로 전달되는 방법을 정의하는 데 사용되는 또 다른 쿠버네티스 오브젝트입니다.

AKS 클러스터에 샘플 헬로월드 애플리케이션을 배포하고, nginx 컨트롤러를 설치하고, 트래픽을 라우팅하도록 인그레스 리소스를 구성해 보겠습니다. 이 설정에 대해 모든 것을 자세히 다루지는 않겠지만, 이 링크를 따라 AKS에 인그레스 컨트롤러를 설치하는 데 사용했으며 매우 간단합니다.

AKS 클러스터를 생성하고 'ingress-namespace'라는 새 네임스페이스에 샘플 애플리케이션을 배포했습니다.

그런 다음 nginx 인그레스 컨트롤러를 설치하면 'ingress-basic' 네임스페이스에 몇 개의 쿠버네티스 오브젝트를 생성했습니다.

## 인그레스 리소스란 무엇인가요?

인그레스 리소스는 백엔드 서비스로의 라우팅을 정의하는 데 도움이 되는 리소스 유형 중 하나입니다. 인그레스에서 사용할 수 있는 라우팅 방법에는 두 가지 유형이 있습니다.

1.호스트 기반 라우팅
2.경로 기반 라우팅

인그레스 리소스를 사용하여 들어오는 요청을 각 백엔드 서비스에 매핑할 수 있습니다.

아래는 호스트 이름에 기반한 인그레스 라우팅 규칙을 보여주는 인그레스 리소스 YAML 파일입니다. 리소스에는 두 개의 호스트가 정의되어 있습니다. 들어오는 요청이 https://foo.bar.com/bar이고 호스트 이름이 "foo.bar.com"이고 접두사가 "/bar"인 경우 "service1"으로, 접두사가 "/foo"인 "*.foo.com"에 대한 요청은 "service2"로 이동합니다. 이러한 유형의 라우팅을 호스트 기반 라우팅이라고 합니다.

코드 스니펫 크레딧: Kubernetes.io

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wildcard-host
spec:
  rules:
  - host: "foo.bar.com"
    http:
      paths:
      - pathType: Prefix
        path: "/bar"
        backend:
          service:
            name: service1
            port:
              number: 80
  - host: "*.foo.com"
    http:
      paths:
      - pathType: Prefix
        path: "/foo"
        backend:
          service:
            name: service2
            port:
              number: 80

```

아래는 접두사가 '/testpath'인 애플리케이션 경로에 대한 수신 요청에 대해 라우팅이 어떻게 이루어지는지 보여주는 인그레스 리소스 YAML 파일입니다. 즉, https://myexamplesite.com/testpath 에 대한 수신 요청이 있는 경우 아래 인그레스 규칙에 따라 평가되어 포트 80의 test라는 서비스로 전송됩니다. 이 경로 기반 라우팅.

코드 스니펫 크레딧: Kubernetes.io

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx-example
  rules:
  - http:
      paths:
      - path: /testpath
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 80

```

## 인그레스 컨트롤러 및 인그레스 리소스 사용 시 트래픽 흐름

https://res.cloudinary.com/practicaldev/image/fetch/s--hXLvEi-D--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gblyktp3smny96wzpnz5.png

### 트래픽 흐름 설명:
- 클라이언트에서 시작된 요청이 인그레스 관리형 로드밸런서에 도달합니다.
- 그런 다음 라우팅 규칙에 정의된 서비스 접두사를 기반으로 인그레스 리소스에 의해 요청이 처리됩니다.
- 그런 다음 요청이 실제 서비스로 전송됩니다.
- 그런 다음 요청이 실제 백엔드 포드로 전송됩니다.
이제 인그레스 및 인그레스의 다른 옵션에 대해 살펴봤으니, Istio의 개념과 기존 인그레스 컨트롤러와 어떻게 다른지 몇 가지 살펴봅시다.

### istio란?
Istio 서비스 메시는 널리 사용되는 서비스 메시 도구 중 하나이며, 쿠버네티스 클러스터에서 호스팅되는 마이크로서비스 워크로드를 위한 통합 가시성, 트래픽 관리, 보안 등의 기능을 갖추고 있습니다. istio에 대한 자세한 내용은 https://istio.io/latest/about/service-mesh/ 참조.

### istio ingress gateway란?
Istio 인그레스 게이트웨이는 서비스 메시의 엣지에서 작동하며 트래픽 컨트롤러로 들어오는 요청을 처리하는 구성 요소 중 하나입니다. 흥미롭게도 이 역시 '서비스' 오브젝트 중 하나로 설치되며 그 뒤에 실행되는 파드가 거의 없습니다. 따라서 기본적으로 istio ingressGateway를 실행하는 파드의 트래픽을 처리하는 로직과 istio는 Envoy 프록시 이미지를 사용하여 이러한 파드를 실행합니다. 이것은 일반 Nginx 인그레스 컨트롤러와 유사하며, 인그레스 게이트웨이 파드는 게이트웨이와 가상 서비스에 의해 구성됩니다.

### istio gateway란? ingress controller와 차이점은?
Istio Gateway는 인그레스 리소스와 유사한 구성 요소입니다. 인그레스 리소스가 인그레스 컨트롤러를 구성하는 데 사용되는 방식과 마찬가지로, Istio 게이트웨이는 위 섹션에서 언급된 Istio 인그레스 게이트웨이를 구성하는 데 사용됩니다. 이 구성 요소를 사용하여 트래픽을 전송할 호스트에서 트래픽을 허용하도록 구성하고 들어오는 요청에 대한 TLS 인증서를 구성할 수 있습니다.

아래는 istio 게이트웨이 구성 요소의 yaml 스니펫입니다. 여기에서는 선택기에서 istio: ingressgateway를 레이블로 사용하여 istio ingress 게이트웨이에 바인딩하는 것을 볼 수 있으며, 이것이 istio 게이트웨이에 바인딩되는 방식입니다. 또한 포트 번호, 이 게이트웨이가 트래픽을 허용하도록 구성된 호스트를 구성하는 '서버' 섹션이 있습니다.

```
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: httpbin-gateway
spec:
  selector:
    istio: ingressgateway # use Istio default gateway implementation
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "httpbin.example.com"

```

## 가상 서비스란 무엇인가요?
가상 서비스는 백엔드 서비스에 대한 라우팅을 구성하는 데 사용됩니다. 애플리케이션과 백엔드 서비스당 하나의 가상 서비스를 구성할 수 있습니다.

아래는 가상 서비스 컴포넌트의 스니펫으로, 들어오는 호스트와 URL 접두사를 기반으로 트래픽을 백엔드 '서비스'로 라우팅하도록 구성한 방법을 보여줍니다.

```
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: reviews-route
spec:
  hosts:
  - reviews.prod.svc.cluster.local
  http:
  - name: "reviews-v2-routes"
    match:
    - uri:
        prefix: "/wpcatalog"
    - uri:
        prefix: "/consumercatalog"
    rewrite:
      uri: "/newcatalog"
    route:
    - destination:
        host: reviews.prod.svc.cluster.local
        subset: v2
  - name: "reviews-v1-route"
    route:
    - destination:
        host: reviews.prod.svc.cluster.local
        subset: v1

```

## Istio 인그레스 게이트웨이와 가상 서비스를 함께 사용할 때의 트래픽 흐름

아래 그림은 Istio에서 트래픽이 어떻게 흐르고 서비스가 어떻게 구성되는지 보여줍니다.

https://res.cloudinary.com/practicaldev/image/fetch/s--Dlns6N2n--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_800/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/r0lphd5juqwniyeh2z40.jpg

### Istio 서비스 메시와 Nginx 인그레스 컨트롤러는 언제 사용해야 하나요?
지금까지 기존 nginx 인그레스 컨트롤러와 istio 서비스 메시의 차이점을 살펴보았습니다. nginx 인그레스 컨트롤러 대신 서비스 메시를 사용하는 것은 다음과 같은 경우에만 권장됩니다:

- 서비스 간 상호 TLS 사용
- 서비스 트래픽의 관찰 가능성
- 블루/그린, 회로 차단, A/B 테스트 등과 같은 배포 기술을 구현합니다.

들어오는 트래픽을 처리하고 백엔드 서비스에 분산하려는 경우에만 기존 nginx 인그레스 컨트롤러를 사용하며, 이는 적은 수의 서비스에 적합합니다. 워크로드/서비스가 증가하면 ISTIO 서비스 메시와 같은 서비스 메시 도구를 사용하는 것이 필수적입니다.

