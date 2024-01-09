- https://minikube.sigs.k8s.io/docs/handbook/persistent_volumes/

# Persistent Volumes
퍼시스턴트 볼륨(호스트 경로) 정보
미니큐브는 기본적으로 호스트패스 타입의 퍼시스턴트볼륨을 지원합니다. 이러한 퍼시스턴트볼륨은 실행 중인 미니큐브 인스턴스 내부의 디렉터리(보통 VM)에 매핑됩니다(`--driver=none`, `--driver=docker` 또는 `--driver=podman`을 사용하지 않는 한). 작동 방식에 대한 자세한 내용은 아래의 동적 프로비저닝 섹션을 참조하세요.

## A note on mounts, persistence, and minikube hosts

미니큐브는 다음 디렉터리에 저장된 파일을 유지하도록 구성되며, 이 디렉터리는 미니큐브 가상 머신(또는 베어메탈에서 실행하는 경우 로컬 호스트)에 만들어집니다. 재부팅 시 다른 디렉터리의 데이터가 손실될 수 있습니다.

- `/data*`
- `/var/lib/minikube`
- `/var/lib/docker`
- `/var/lib/containerd`
- `/var/lib/buildkit`
- `/var/lib/containers`
- `/tmp/hostpath_pv*`
- `/tmp/hostpath-provisioner*`

`/var` 또는 별도의 데이터 디스크에 저장된 다른 디렉터리에 대한 * 마운트 지점

다음은 '/data' 디렉터리에 데이터를 영구 보존하기 위한 PersistentVolume 구성 예시입니다:

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0001
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 5Gi
  hostPath:
    path: /data/pv0001/

```

마운트된 호스트 폴더에 PV를 생성하여 지속성을 확보할 수도 있습니다.

## Dynamic provisioning and CSI 

또한 미니큐브는 배포와 함께 실행되는 동적 스토리지 컨트롤러의 매우 간단하고 표준적인 구현을 구현합니다. 이는 (이전의 인트리 호스트경로 공급자를 통하지 않고) 호스트경로 볼륨의 프로비저닝을 관리합니다.

기본 스토리지 프로비저너 컨트롤러는 미니큐브 코드베이스에서 내부적으로 관리되며, 사용자 정의 스토리지 컨트롤러를 시스템의 스토리지 구성 요소로 쿠버네티스에 연결하는 것이 얼마나 쉬운지 보여주고, 퍼시스턴트 스토리지가 매핑될 때 파드의 동작을 테스트하기 위해 동적으로 파드에 제공한다.

이것은 CSI 기반 스토리지 프로바이더가 아니라, 컨트롤러가 미결 스토리지 요청이 있음을 확인할 때 호스트경로 유형의 퍼시스턴트볼륨 오브젝트를 동적으로 선언한다는 점에 유의하세요.

동적 프로비저닝을 활성화하고 스냅샷뿐만 아니라 멀티노드 클러스터를 지원하는 CSI 호스트경로 드라이버 애드온도 있습니다.

