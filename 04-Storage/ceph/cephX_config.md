- https://docs.ceph.com/en/latest/rados/configuration/auth-config-ref/

# CephX Config
- CephX 프로토콜은 기본적으로 활성화되어 있습니다. CephX가 제공하는 암호화 인증에는 약간의 계산 비용이 들지만 일반적으로 매우 낮습니다. 클라이언트와 서버 호스트를 연결하는 네트워크 환경이 매우 안전하여 인증 비용을 감당할 수 없는 경우인증을 비활성화할 수 있습니다.일반적으로 인증을 비활성화하는 것은 권장하지 않습니다.

참고

인증을 비활성화하면 클라이언트/서버 메시지를 변경하는 중간자 공격의 위험에 노출되어 보안에 치명적인 영향을 미칠 수 있습니다.

## DEPLOYMENT SCENARIOS
CephX를 처음 구성하는 방법은 시나리오에 따라 다릅니다. Ceph 클러스터를 배포하는 데는 두 가지 일반적인 전략이 있습니다. Ceph를 처음 사용하는 경우, 가장 쉬운 방법인 cephadm을 사용하여 클러스터를 배포하는 것이 좋습니다. 그러나 클러스터에서 다른 배포 도구(예: Ansible, Chef, Juju 또는 Puppet)를 사용하는 경우 수동 배포 절차를 사용하거나 배포 도구가 모니터를 부트스트랩하도록 구성해야 합니다.

### MANUAL DEPLOYMENT
클러스터를 수동으로 배포하는 경우 모니터를 수동으로 부트스트랩하고 client.admin 사용자 및 키링을 만들어야 합니다. 모니터를 부트스트랩하려면 모니터 부트스트랩의 단계를 따르세요. 타사 배포 도구(예: Chef, Puppet, Juju)를 사용하는 경우에는 다음 단계를 따르세요.

## ENABLING/DISABLING CEPHX
모니터, OSD 및 메타데이터 서버의 키가 이미 배포된 경우에만 CephX를 활성화할 수 있습니다. 단순히 CephX를 켜거나 끄는 경우에는 부트스트랩 절차를 반복할 필요가 없습니다.

### ENABLING CEPHX
CephX가 활성화되면 Ceph는 기본 검색 경로에서 키링을 찾습니다. 이 경로에는 /etc/ceph/$cluster.$name.keyring이 포함됩니다. Ceph 구성 파일의[전역] 섹션에 키링 옵션을 추가하여 이 검색 경로 위치를 재정의할 수 있지만 권장하지는 않습니다.

인증이 비활성화된 클러스터에서 CephX를 사용하려면 다음 절차를 수행하세요. 사용자(또는 배포 유틸리티)가 이미 키를 생성한 경우 키 생성과 관련된 단계를 건너뛸 수 있습니다.

client.admin 키를 생성하고 클라이언트 호스트용 키 사본을 저장합니다:

```ceph auth get-or-create client.admin mon 'allow *' mds 'allow *' mgr 'allow *' osd 'allow *' -o /etc/ceph/ceph.client.admin.keyring```
경고: 이 단계를 수행하면 기존의/etc/ceph/client.admin.keyring 파일이 모두 삭제됩니다. 배포 도구에서 이미 키링 파일을 생성한 경우에는 이 단계를 수행하지 마세요. 주의하세요!

모니터 키링을 만들고 모니터 비밀 키를 생성합니다:

```ceph-authtool --create-keyring /tmp/ceph.mon.keyring --gen-key -n mon. --cap mon 'allow *'```
각 모니터에 대해 모니터 키링을 모니터의 mon 데이터 디렉터리에 있는 ceph.mon.keyring 파일에 복사합니다. 예를 들어 모니터 키링을 ceph라는 클러스터의 mon.a에 복사하려면 다음 명령을 실행합니다:

```cp /tmp/ceph.mon.keyring /var/lib/ceph/mon/ceph-a/keyring```
모든 MGR에 대해 비밀 키를 생성합니다. 여기서 {$id}는 MGR 문자입니다:

```ceph auth get-or-create mgr.{$id} mon 'allow profile mgr' mds 'allow *' osd 'allow *' -o /var/lib/ceph/mgr/ceph-{$id}/keyring```
모든 OSD에 대해 비밀 키를 생성합니다. 여기서 {$id}는 OSD 번호입니다:

```ceph auth get-or-create osd.{$id} mon 'allow rwx' osd 'allow *' -o /var/lib/ceph/osd/ceph-{$id}/keyring```
모든 MDS에 대한 비밀 키를 생성합니다. 여기서 {$id}는 MDS 문자입니다:

```ceph auth get-or-create mds.{$id} mon 'allow rwx' osd 'allow *' mds 'allow *' mgr 'allow profile mds' -o /var/lib/ceph/mds/ceph-{$id}/keyring```
Ceph 구성 파일의[전역] 섹션에서 다음 옵션을 설정하여 CephX 인증을 사용하도록 설정합니다:

```
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx
```
Ceph 클러스터를 시작하거나 다시 시작합니다. 자세한 내용은 클러스터 운영하기를 참조하세요.

모니터를 수동으로 부트스트랩하는 방법에 대한 자세한 내용은 수동 배포를 참조하세요.

### DISABLING CEPHX
다음 절차에서는 CephX를 비활성화하는 방법을 설명합니다. 클러스터 환경이 안전한 경우 인증 실행에 따른 컴퓨팅 비용을 상쇄하기 위해 CephX를 비활성화할 수 있습니다. 그렇게 하는 것은 권장하지 않습니다. 그러나 인증을 일시적으로 비활성화했다가 나중에 다시 활성화하면 설정 및 문제 해결이 더 쉬워질 수 있습니다.

Ceph 구성 파일의[전역] 섹션에서 다음 옵션을 설정하여 CephX 인증을 비활성화합니다:
```
auth_cluster_required = none
auth_service_required = none
auth_client_required = none
```
Ceph 클러스터를 시작하거나 다시 시작합니다. 자세한 내용은 클러스터 운영하기를 참조하세요.

## CONFIGURATION SETTINGS
### ENABLEMENT
- auth_cluster_required : 이 구성 설정을 사용하면 Ceph 스토리지 클러스터 데몬(즉, ceph-mon, ceph-osd,ceph-mds 및 ceph-mgr)이 서로를 인증해야 합니다. 유효한 설정은 cephx 또는 none입니다.

- auth_service_required : 이 구성 설정을 활성화하면 Ceph 클라이언트는 해당 클라이언트가 Ceph 스토리지 클러스터로 인증하는 경우에만 Ceph 서비스에 액세스할 수 있습니다. 유효한 설정은 cephx 또는 none입니다.

- auth_client_required : 이 구성 설정을 사용하면 Ceph 스토리지 클러스터가 Ceph 클라이언트에 대해 인증하는 경우에만 Ceph 클라이언트와 Ceph 스토리지 클러스터 간의 통신을 설정할 수 있습니다. 유효한 설정은 cephx 또는none입니다.


### KEYS
인증이 활성화된 상태에서 Ceph를 실행하면, ceph 관리 명령과 Ceph 클라이언트는 인증 키를 사용하는 경우에만 Ceph 스토리지 클러스터에 액세스할 수 있습니다.

ceph 관리 명령과 Ceph 클라이언트에서 이러한 키를 사용할 수 있도록 하는 가장 일반적인 방법은 /etc/ceph디렉토리에 Ceph 키링을 포함하는 것입니다. cephadm을 사용하는 Octopus 이상 릴리스의 경우 파일 이름은 일반적으로 ceph.client.admin.keyring입니다. 키링이/etc/ceph 디렉터리에 포함되어 있으면 Ceph 구성 파일에 키링 항목을 지정할 필요가 없습니다.

Ceph 스토리지 클러스터의 키링 파일에는 client.admin키가 포함되어 있으므로, 관리 명령을 실행하는 노드에 키링 파일을 복사하는 것이 좋습니다.

이 단계를 수동으로 수행하려면 다음 명령을 실행합니다:

```sudo scp {user}@{ceph-cluster-host}:/etc/ceph/ceph.client.admin.keyring /etc/ceph/ceph.client.admin.keyring```
팁

클라이언트 컴퓨터에서 ceph.keyring 파일에 적절한 권한(예: chmod 644)이 설정되어 있는지 확인하세요.

Ceph 구성 파일의 키 설정을 사용하여 키 자체를 지정하거나(이 방법은 권장하지 않음), 대신 Ceph 구성 파일의 키 파일 설정을 사용하여 키 파일의 경로를 지정할 수 있습니다.

- keyring : 키링 파일의 경로입니다.
- keyfile : 키 파일(즉, 키만 포함된 파일)의 경로입니다.
- key : 키(즉, 키 자체의 텍스트 문자열)입니다. 이 설정은 사용법을 잘 모르는 경우 사용하지 않는 것이 좋습니다.

### Daemon Keyrings
관리 사용자 또는 배포 도구(예: cephadm)는 사용자 키링을 생성하는 것과 동일한 방식으로 데몬 키링을 생성합니다. 기본적으로 Ceph는 데몬의 키링을 해당 데몬의 데이터 디렉터리 내에 저장합니다. 기본 키링 위치 및 데몬이 작동하는 데 필요한 기능은 다음과 같습니다.

- ceph-mon

- ceph-osd

- ceph-mds

- ceph-mgr

- radosgw

Note

모니터 키링(즉, mon.)에는 키는 있지만 기능은 없으며 이 키링은 클러스터 인증 데이터베이스의 일부가 아닙니다.

데몬의 데이터 디렉터리 위치는 기본적으로 다음과 같은 형식의 디렉터리를 사용합니다:

/var/lib/ceph/$type/$cluster-$id
예를 들어 osd.12의 데이터 디렉토리는 다음과 같습니다:

/var/lib/ceph/osd/ceph-12
이러한 위치를 재정의할 수는 있지만 권장하지는 않습니다.

## SIGNATURES
Ceph는 서명 검사를 수행하여 전송 중 메시지 변조(예: '중간자 공격')에 대해 어느 정도 제한적인 보호 기능을 제공합니다.

Ceph 인증의 다른 부분과 마찬가지로, 서명은 세분화된 제어를 허용합니다. 클라이언트와 Ceph 간의 서비스 메시지 및 Ceph 데몬 간의 메시지에 대해 서명을 사용하거나 사용하지 않도록 설정할 수 있습니다.

서명이 활성화되어 있어도 데이터는 전송 중에 암호화되지 않습니다.

- cephx_require_signatures : 이 구성 설정을 true로 설정하면 Ceph 클라이언트와 Ceph 스토리지 클러스터 간의 모든 메시지 트래픽과 Ceph 스토리지 클러스터 내의 데몬 간의 모든 메시지 트래픽에 서명이 필요합니다.

- cephx_cluster_require_signatures : 이 구성 설정을 true로 설정하면 Ceph는 Ceph 스토리지 클러스터 내의 Ceph 데몬 간의 모든 메시지 트래픽에 대해 서명을 요구합니다.

- cephx_service_require_signatures : 이 구성 설정을 true로 설정하면 Ceph 클라이언트와 Ceph 스토리지 클러스터 간의 모든 메시지 트래픽에 서명을 요구합니다.

- CEPX_SIGN_MESSAGES : 이 구성 설정이 true로 설정되어 있고 Ceph 버전이 메시지 서명을 지원하는 경우 Ceph는 모든 메시지에 서명하여 스푸핑을 더욱 어렵게 만듭니다.

### Time to live
- auth_service_ticket_ttl : Ceph 스토리지 클러스터가 인증 티켓을 Ceph 클라이언트에 전송하면, Ceph 스토리지 클러스터는 해당 티켓에 TTL(Time To Live)을 할당합니다.

