- https://docs.ceph.com/en/latest/rados/configuration/common/

# COMMON SETTINGS
하드웨어 권장 사항 섹션에서는 Ceph 스토리지 클러스터를 구성하기 위한 몇 가지 하드웨어 가이드라인을 제공합니다. 단일 Ceph 노드에서 여러 데몬을 실행할 수 있습니다. 예를 들어, 여러 개의 드라이브가 있는 단일 노드는 일반적으로 각 드라이브에 대해 하나의 ceph-osd를 실행합니다. 이상적으로는 각 노드가 특정 유형의 프로세스에 할당됩니다. 예를 들어, 일부 노드는 ceph-osd 데몬을 실행하고, 다른 노드는 ceph-mds 데몬을 실행하고, 또 다른 노드는 ceph-mon 데몬을 실행할 수 있습니다.

각 노드에는 이름이 있습니다. 노드의 이름은 호스트 설정에서 찾을 수 있습니다. 모니터는 또한 네트워크 주소와 포트(즉, 도메인 이름 또는 IP 주소)를 지정하며, 이는 addr 설정에서 찾을 수 있습니다. 기본 구성 파일은 일반적으로 모니터 데몬의 각 인스턴스에 대해 최소한의 설정만 지정합니다. 예를 들어
```
[global]
mon_initial_members = ceph1
mon_host = 10.0.0.1

```
- 중요
호스트 설정의 값은 노드의 짧은 이름입니다. FQDN이 아닙니다. IP 주소가 아닙니다. 노드 이름을 검색하려면 명령줄에 호스트 이름 -s를 입력합니다. Ceph를 수동으로 배포하는 경우가 아니라면 초기 모니터 설정 이외의 다른 용도로 호스트 설정을 사용하지 마세요. chef 또는 cephadm과 같은 배포 도구를 사용할 때는 개별 데몬 아래에 호스트 설정을 지정하지 마세요. 이러한 도구는 클러스터 맵에 적절한 값을 입력하도록 설계되어 있습니다.

## MONITORS
Ceph 프로덕션 클러스터는 일반적으로 모니터 인스턴스 충돌 시 가용성을 보장하기 위해 최소 3개의 Ceph 모니터 데몬을 프로비저닝합니다. 최소 3개의 Ceph 모니터 데몬이 있으면 Paxos 알고리즘이 어떤 버전의 Ceph 클러스터 맵이 가장 최신 버전인지 확인할 수 있습니다. 이 결정은 쿼럼에 있는 대다수의 Ceph 모니터를 참조하여 이루어집니다.

- 참고

단일 모니터로 Ceph를 배포할 수 있지만 인스턴스에 장애가 발생하면 다른 모니터가 부족하여 데이터 서비스 가용성이 중단될 수 있습니다.

Ceph 모니터는 일반적으로 새 v2 프로토콜의 경우 포트 3300에서, 이전 v1 프로토콜의 경우 포트 6789에서 수신 대기합니다.

기본적으로 Ceph는 모니터 데이터를 다음 경로에 저장할 것으로 예상합니다:

```
/var/lib/ceph/mon/$cluster-$id

```

사용자 또는 배포 도구(예: cephadm)가 해당 디렉터리를 만들어야 합니다. 메타변수가 완전히 표현되고 클러스터 이름이 "ceph"인 경우 위 예제에서 지정된 경로는 다음과 같이 평가됩니다:

```
/var/lib/ceph/mon/ceph-a

```

## AUTHENTICATION
인증은 다음과 같이 Ceph 구성 파일의 [전역] 섹션에서 명시적으로 활성화 또는 비활성화할 수 있습니다:
```
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx
```

## OSDS
기본적으로 Ceph는 Ceph OSD 데몬의 데이터를 다음 경로에 저장할 것으로 예상합니다:

```
/var/lib/ceph/osd/$cluster-$id

```

사용자 또는 배포 도구(예: cephadm)가 해당 디렉터리를 만들어야 합니다. 메타변수가 완전히 표현되고 클러스터 이름이 "ceph"인 경우 위 예제에서 지정된 경로는 다음과 같이 평가됩니다:

```
/var/lib/ceph/osd/ceph-0
```

osd_data 설정을 사용하여 이 경로를 재정의할 수 있습니다. 기본 위치는 변경하지 않는 것이 좋습니다. OSD 호스트에 기본 디렉터리를 만들려면 다음 명령을 실행합니다:

```
ssh {osd-host}
sudo mkdir /var/lib/ceph/osd/ceph-{osd-number}
```

osd_data 경로는 운영 체제와 공유되지 않는 장치로 연결되어야 합니다. 운영 체제와 데몬이 포함된 장치 이외의 장치를 사용하려면 다음 형식의 명령을 실행하여 Ceph와 함께 사용할 수 있도록 준비하고 방금 만든 디렉터리에 마운트합니다:

```
ssh {new-osd-host}
sudo mkfs -t {fstype} /dev/{disk}
sudo mount -o user_xattr /dev/{disk} /var/lib/ceph/osd/ceph-{osd-number}
```
mkfs를 실행할 때는 xfs 파일 시스템을 사용하는 것이 좋습니다. (btrfs 및 ext4 파일 시스템은 권장되지 않으며 더 이상 테스트되지 않습니다.)

## HEARTBEATS
런타임 작업 중에 Ceph OSD 데몬은 다른 Ceph OSD 데몬을 검사하고 그 결과를 Ceph 모니터에 보고합니다. 이 프로세스에서는 사용자가 설정을 제공할 필요가 없습니다. 그러나 네트워크 지연 문제가 있는 경우 기본 설정을 수정할 수 있습니다.

## LOGS / DEBUGGING
때때로 Ceph의 로깅 및 디버깅 기능을 사용해야 하는 문제가 발생할 수 있습니다.

## EXAMPLE CEPH.CONF
```
[global]
fsid = {cluster-id}
mon_initial_members = {hostname}[, {hostname}]
mon_host = {ip-address}[, {ip-address}]

#All clusters have a front-side public network.
#If you have two network interfaces, you can configure a private / cluster 
#network for RADOS object replication, heartbeats, backfill,
#recovery, etc.
public_network = {network}[, {network}]
#cluster_network = {network}[, {network}] 

#Clusters require authentication by default.
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx

#Choose reasonable number of replicas and placement groups.
osd_journal_size = {n}
osd_pool_default_size = {n}  # Write an object n times.
osd_pool_default_min_size = {n} # Allow writing n copies in a degraded state.
osd_pool_default_pg_autoscale_mode = {mode} # on, off, or warn
# Only used if autoscaling is off or warn:
osd_pool_default_pg_num = {n}

#Choose a reasonable crush leaf type.
#0 for a 1-node cluster.
#1 for a multi node cluster in a single rack
#2 for a multi node, multi chassis cluster with multiple hosts in a chassis
#3 for a multi node cluster with hosts across racks, etc.
osd_crush_chooseleaf_type = {n}

```