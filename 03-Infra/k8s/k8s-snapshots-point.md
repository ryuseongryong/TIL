# Point in time Snapshot of Persistent Volume Data with Kubernetes' Volume Snapshots
- https://medium.com/linux-shots/point-in-time-snapshot-of-persistent-volume-data-with-kubernetes-volume-snapshots-abfafc210802

애플리케이션에서 업그레이드를 수행하거나 구성을 변경할 때 애플리케이션이 예기치 않은 동작을 할 수 있는 위험은 항상 존재합니다. 애플리케이션의 업그레이드/업데이트 버전은 영구 볼륨에 있는 많은 파일을 변경할 수 있으며, 예기치 않은 결과가 발생할 경우 나중에 되돌리기가 어려워질 수 있습니다.

쿠버네티스에는 기존 PVC에서 스냅샷을 생성하거나 PVC를 복제하는 데 사용할 수 있는 기능이 있습니다. 이는 스냅샷 기능이 있는 CSI 드라이버 기반 퍼시스턴트 볼륨에서 지원된다. 이는 업그레이드 또는 애플리케이션 변경을 수행하기 전에 퍼시스턴트 볼륨의 백업을 생성하는 데 사용할 수 있습니다.

이 기능은 CSI 드라이버를 제공하는 대부분의 클라우드 제공업체 및 타사 솔루션에서 지원됩니다. 몇 가지를 나열하면 다음과 같습니다:

- GCE persistent disk CSI driver(pd.csi.storage.gke.io)
- AWS EBS CSI driver (ebs.csi.aws.com)
- Azure Disk CSI driver (disk.csi.azure.com)
- Portworx CSI driver (pxd.portworx.com)
- NetApp Trident CSI driver (csi.trident.netapp.io)
- Host path CSI driver (hostpath.csi.k8s.io)

## Enable support for volume snapshots

- 이 기능을 사용하려면 클러스터에 볼륨 스냅샷 CRD와 스냅샷 컨트롤러가 배포되어 있어야 합니다.
```
$ kubectl get crds | grep snapshot.storage.k8s.io
volumesnapshotclasses.snapshot.storage.k8s.io
volumesnapshotcontents.snapshot.storage.k8s.io
volumesnapshots.snapshot.storage.k8s.io
```

1. 목록에 없는 경우 아래 명령을 실행하여 해당 CRD를 생성하세요.(https://github.com/kubernetes-csi/external-snapshotter)
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/release-6.1/client/config/crd/snapshot.storage.k8s.io_volumesnapshotclasses.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/release-6.1/client/config/crd/snapshot.storage.k8s.io_volumesnapshotcontents.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/release-6.1/client/config/crd/snapshot.storage.k8s.io_volumesnapshots.yaml
```

- VolumeSnapshotClass는 K8의 스토리지 클래스와 동일합니다. 프로비저너와 volumesnapshot 생성에 사용할 수 있는 다양한 어트리뷰트를 정의하는 데 사용됩니다. volumesnapshot을 통해 요청이 수신되면 VolumeSnapshotContent를 생성합니다.

- VolumeSnapshotContent는 PV에 해당한다. 이것은 클러스터 관리자가 프로비저닝하거나 VolumeSnapshotClass에 의해 동적으로 프로비저닝되어 소스 볼륨의 데이터를 저장하는 스토리지의 일부입니다.

- volumesnapshot은 PVC와 동일하다. 사용자가 스토리지 스냅샷을 요청하는 것입니다.

2. Install Snapshot controller
```
$ kubectl -n kube-system get po --selector app=snapshot-controller

# ---

$ kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/release-6.1/deploy/kubernetes/snapshot-controller/rbac-snapshot-controller.yaml
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/release-6.1/deploy/kubernetes/snapshot-controller/setup-snapshot-controller.yaml


```

3. 컴퓨터에서 CSI 드라이버가 실행 중이어야 합니다. 클라우드 네이티브 K8s 클러스터(예: EKS, GKE 또는 AKS)를 사용하는 경우, 클러스터에서 사용할 수 있어야 합니다.

데모에서는 hostpath-csi driver를 사용하여 노드의 경로를 볼륨으로 사용하고 있습니다. 이 데모를 테스트하기 위해 이 드라이버를 사용하려면 아래 명령어를 사용하여 설치할 수 있습니다. 호스트 경로는 라이브/프로덕션 클러스터에서는 사용하지 않는 것이 좋습니다.

```
git clone https://github.com/kubernetes-csi/csi-driver-host-path.git
cd csi-driver-host-path
deploy/kubernetes-latest/deploy.sh

# Deploy storage class using below command

cat <<EOF | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: csi-hostpath-sc
provisioner: hostpath.csi.k8s.io
reclaimPolicy: Delete
volumeBindingMode: Immediate
EOF

# To remove it after demo
cd csi-driver-host-path
deploy/kubernetes-latest/destroy.sh
kubectl delete sc csi-hostpath-sc
```

## Deploy a sample application with a PVC
1. Deploy PVC
```
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: csi-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: csi-hostpath-sc
EOF
```

2. Deploy application which uses this volume claim
```
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-csi-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-csi-app
  template:
    metadata:
      labels:
        app: my-csi-app
    spec:
      containers:
        - name: my-frontend
          image: busybox
          volumeMounts:
          - mountPath: "/data"
            name: my-csi-volume
          command: [ "sleep", "1000000" ]
      volumes:
        - name: my-csi-volume
          persistentVolumeClaim:
            claimName: csi-pvc
EOF

```

3. Create a file inside pod volume
```
kubectl exec -it <pod-name-of-app> -- sh
echo "This is version 1" > /data/version.txt

```

## Create snapshot from PVC
- PVC를 생성하기 전에 볼륨 스냅샷을 위해 StorageClass와 유사한 볼륨 스냅샷 클래스를 생성해야 합니다.

```
cat <<EOF | kubectl apply -f -
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-hostpath-sc
driver: hostpath.csi.k8s.io
deletionPolicy: Delete
EOF

```

위의 매니페스트 YAML에서 스토리지 클래스의 프로비저너 대신 드라이버가 있고, 여기에는 reclaimPolicy 대신 삭제Policy가 있다는 점을 눈치채셨을 것입니다.

PVC에서 스냅샷 생성
```
cat <<EOF | kubectl apply -f -
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: new-snapshot-demo
spec:
  volumeSnapshotClassName: csi-hostpath-sc
  source:
    persistentVolumeClaimName: csi-pvc
EOF
```

위의 매니페스트에는 이 볼륨 스냅샷의 소스를 정의하는 spec.source 필드가 있습니다. 또한, 클러스터가 사용할 각각의 볼륨 스냅샷 클래스를 알 수 있도록 spec.volumeSnapshotClassName을 정의합니다. 이 값을 정의하지 않으면, 퍼시스턴트볼륨클레임의 프로비저너를 사용하여 볼륨 스냅샷을 생성합니다.

Check for snapshot

```
$ kubectl get VolumeSnapshot new-snapshot-demo
$ kubectl get VolumeSnapshotContent
# READYTOUSE 열이 참이 될 때까지 기다립니다.
```

## Restore from snapshot
애플리케이션의 PV에 있는 파일을 변경해 보겠습니다. 그런 다음 스냅샷에서 다시 복원합니다.

```
kubectl exec -it <pod-name-of-app> -- sh
echo "This is version 2" > /data/version.txt

```

이제 스냅샷에서 이전 버전으로 복원해 보겠습니다. 복원된 PVC의 이름을 csi-pvc-restored로 지정합니다. 볼륨 스냅샷에서 PVC를 복원하려면 일반 PVC 매니페스트를 사용합니다. spec.dataSource에 스냅샷 세부 정보를 추가하여 볼륨 스냅샷에서 PVC를 생성합니다.

```
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: csi-pvc-restored
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: csi-hostpath-sc
  dataSource:
    name: new-snapshot-demo
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
EOF
```

여기서는 새 PVC를 생성할 때 복원된 새 PVC를 생성하는 데 사용할 소스 볼륨 스냅샷을 정의하는 spec.dataSource를 사용하고 있습니다. 이렇게 하면 PVC가 생성되고 스냅샷에서 데이터가 복원됩니다.

목록에서 복원된 PVC를 볼 수 있어야 한다. kubectl get pvc

이제 복원된 PVC를 사용하도록 애플리케이션 배포 파일을 업데이트하고 적용할 수 있습니다.

```
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-csi-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-csi-app
  template:
    metadata:
      labels:
        app: my-csi-app
    spec:
      containers:
        - name: my-frontend
          image: busybox
          volumeMounts:
          - mountPath: "/data"
            name: my-csi-volume
          command: [ "sleep", "1000000" ]
      volumes:
        - name: my-csi-volume
          persistentVolumeClaim:
            claimName: csi-pvc-restored
EOF
```

이제 영구 볼륨에 들어가서 파일을 확인하면 이전 버전이어야 합니다.

```
$ kubectl exec -it <pod-name> -- cat /data/version.txt
```

## Create clone of a PVC
PVC의 복제본을 생성하기 위해 csi-pvc-clone이라는 이름의 다른 PVC를 생성합니다. PVC 매니페스트의 spec.dataSource에 소스 PVC 세부 정보를 추가합니다.

```
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: csi-pvc-clone
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: csi-hostpath-sc
  dataSource:
    name: csi-pvc
    kind: PersistentVolumeClaim
EOF
```

여기서는 볼륨스냅샷을 데이터 소스로 사용하는 대신, 퍼시스턴트볼륨클레임을 사용하여 이를 복제할 새 PVC를 생성합니다.

이렇게 하면 기존 PVC가 복제되고 새 PVC가 생성됩니다.