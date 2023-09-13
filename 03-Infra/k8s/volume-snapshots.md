# Volume Snapshots
- https://kubernetes.io/ko/docs/concepts/storage/volume-snapshots/


## 소개

- API 리소스 PersistentVolume 및 PersistentVolumeClaim 가 사용자와 관리자를 위해 볼륨을 프로비전할 때 사용되는 것과 유사하게, VolumeSnapshotContent 및 VolumeSnapshot API 리소스는 사용자와 관리자를 위한 볼륨 스냅샷을 생성하기 위해 제공된다.

- VolumeSnapshotContent 는 관리자가 프로비져닝한 클러스터 내 볼륨의 스냅샷이다. 퍼시스턴트볼륨이 클러스터 리소스인 것처럼 이것 또한 클러스터 리소스이다.

- VolumeSnapshot 은 사용자가 볼륨의 스냅샷을 요청할 수 있는 방법이다. 이는 퍼시스턴트볼륨클레임과 유사하다.

- VolumeSnapshotClass 을 사용하면 VolumeSnapshot 에 속한 다른 속성을 지정할 수 있다. 이러한 속성은 스토리지 시스템에의 동일한 볼륨에서 가져온 스냅샷마다 다를 수 있으므로 PersistentVolumeClaim 의 동일한 StorageClass 를 사용하여 표현할 수는 없다.

- 볼륨 스냅샷은 쿠버네티스 사용자에게 완전히 새로운 볼륨을 생성하지 않고도 특정 시점에 볼륨의 콘텐츠를 복사하는 표준화된 방법을 제공한다. 예를 들어, 데이터베이스 관리자는 이 기능을 사용하여 수정 사항을 편집 또는 삭제하기 전에 데이터베이스를 백업할 수 있다.

- 사용자는 이 기능을 사용할 때 다음 사항을 알고 있어야 한다.

    - API 오브젝트인 VolumeSnapshot, VolumeSnapshotContent, VolumeSnapshotClass 는 핵심 API가 아닌, CRDs 이다.
    - VolumeSnapshot 은 CSI 드라이버에서만 사용할 수 있다.
    - 쿠버네티스 팀은 VolumeSnapshot 의 배포 프로세스 일부로써, 컨트롤 플레인에 배포할 스냅샷 컨트롤러와 CSI 드라이버와 함께 배포할 csi-snapshotter라는 사이드카 헬퍼(helper) 컨테이너를 제공한다. 스냅샷 컨트롤러는 VolumeSnapshot 및 VolumeSnapshotContent 오브젝트를 관찰하고 VolumeSnapshotContent 오브젝트의 생성 및 삭제에 대한 책임을 진다. 사이드카 csi-snapshotter는 VolumeSnapshotContent 오브젝트를 관찰하고 CSI 엔드포인트에 대해 CreateSnapshot 및 DeleteSnapshot 을 트리거(trigger)한다.
    - 스냅샷 오브젝트에 대한 강화된 검증을 제공하는 검증 웹훅 서버도 있다. 이는 CSI 드라이버가 아닌 스냅샷 컨트롤러 및 CRD와 함께 쿠버네티스 배포판에 의해 설치되어야 한다. 스냅샷 기능이 활성화된 모든 쿠버네티스 클러스터에 설치해야 한다.
    - CSI 드라이버에서의 볼륨 스냅샷 기능 유무는 확실하지 않다. 볼륨 스냅샷 서포트를 제공하는 CSI 드라이버는 csi-snapshotter를 사용할 가능성이 높다. 자세한 사항은 CSI 드라이버 문서를 확인하면 된다.
    - CRDs 및 스냅샷 컨트롤러는 쿠버네티스 배포 시 설치된다.
