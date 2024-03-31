- https://docs.ceph.com/en/latest/rados/configuration/ceph-conf/

# Configuring Ceph
Ceph 서비스가 시작되면 초기화 프로세스는 백그라운드에서 실행되는 일련의 데몬을 활성화합니다. Ceph 스토리지 클러스터는 최소 세 가지 유형의 데몬을 실행합니다:

Ceph Monitor (ceph-mon)

Ceph Manager (ceph-mgr)

Ceph OSD Daemon (ceph-osd)

Ceph 파일 시스템을 지원하는 모든 Ceph 스토리지 클러스터는 하나 이상의 Ceph 메타데이터 서버(ceph-mds)도 실행합니다. Ceph 오브젝트 스토리지를 지원하는 모든 클러스터는 Ceph RADOS 게이트웨이 데몬(radosgw)을 실행합니다.

각 데몬에는 여러 가지 구성 옵션이 있으며, 각 옵션에는 기본값이 있습니다. 이러한 구성 옵션을 변경하여 시스템의 동작을 조정할 수 있습니다. 기본값을 재정의하기 전에 클러스터의 성능과 안정성이 크게 저하될 수 있으므로 그 결과를 이해해야 합니다. 기본값은 릴리스 간에 변경되는 경우가 있습니다. 따라서 사용 중인 Ceph 릴리스에 적용되는 이 설명서의 버전을 검토하는 것이 가장 좋습니다.

## option names
각 Ceph 구성 옵션에는 소문자로 구성된 단어와 밑줄(_)로 연결된 고유한 이름이 있습니다.

명령줄에서 옵션 이름을 지정할 때 밑줄(_)과 대시(-) 문자를 서로 바꿔서 사용할 수 있습니다(예: `--mon-host`는 `--mon_host`와 동일).

설정 파일에 옵션 이름이 표시될 때 밑줄이나 대시 대신 공백을 사용할 수도 있습니다. 그러나 명확성과 편의성을 위해 이 문서 전체에서와 같이 밑줄을 일관되게 사용하는 것이 좋습니다.

## Config Sources
각 Ceph 데몬, 프로세스 및 라이브러리는 아래 나열된 여러 소스 중 하나 이상에서 구성을 가져옵니다. 목록에서 나중에 발생하는 소스는 목록의 앞쪽에 발생하는 소스보다 우선합니다(둘 다 존재하는 경우).

- 컴파일된 기본값
- 모니터 클러스터의 중앙 집중식 구성 데이터베이스
- 로컬 호스트에 저장된 구성 파일
- 환경 변수
- 명령줄 인수
- 관리자가 설정한 런타임 오버라이드

Ceph 프로세스가 시작 시 가장 먼저 하는 일 중 하나는 명령줄, 환경, 로컬 구성 파일을 통해 제공되는 구성 옵션을 구문 분석하는 것입니다. 그런 다음 프로세스는 모니터 클러스터에 연결하여 전체 클러스터에 대해 중앙에 저장된 구성을 검색합니다. 구성에 대한 전체 보기를 사용할 수 있게 되면 데몬 또는 프로세스의 시작이 시작됩니다.

### BOOTSTRAP OPTIONS
부트스트랩 옵션은 프로세스의 모니터 연결, 인증, 클러스터에 저장된 구성 검색 기능에 영향을 주는 구성 옵션입니다. 따라서 이러한 옵션은 노드에 로컬로 저장하고 로컬 구성 파일을 통해 설정해야 할 수 있습니다. 이러한 옵션에는 다음이 포함됩니다:

mon_host
쉼표, 공백 또는 세미콜론으로 구분된 IP 주소 또는 호스트 이름의 목록입니다. 호스트명은 DNS를 통해 확인됩니다. 모든 A 및 AAAA 레코드가 검색 목록에 포함됩니다.

mon_host_override
Ceph 프로세스가 Ceph 클러스터와 처음 통신을 설정할 때 처음 접촉하는 모니터 목록입니다. 이것은 이전 Ceph 인스턴스(예: 라이브러라도 클러스터 핸들)로 전송된 MonMap 업데이트에서 파생된 알려진 모니터 목록을 재정의합니다. 이 옵션은 주로 디버깅에 유용할 것으로 예상됩니다.

- mon_dns_srv_name
- 데몬이 데이터를 저장하는 로컬 디렉터리를 정의하는 mon_data, osd_data, mds_data, mgr_data 및 이와 유사한 옵션.
- 모니터 인증에 사용할 인증 자격 증명을 지정하는 데 사용할 수 있는 keyring, keyfile 및/또는 key. 대부분의 경우 기본 keyring 위치는 위에 지정된 데이터 디렉터리에 있습니다.

대부분의 경우 이러한 옵션의 기본값을 수정할 이유가 없습니다. 그러나 한 가지 예외가 있는데, 바로 클러스터의 모니터 주소를 식별하는 mon_host 옵션입니다. 그러나 DNS를 사용하여 모니터를 식별하는 경우 로컬 Ceph 구성 파일을 완전히 피할 수 있습니다.

### SKIPPING MONITOR CONFIG
클러스터의 모니터에서 구성 정보를 검색하는 단계를 건너뛰려면 모든 명령에 --no-mon-config 옵션을 전달할 수 있습니다. 이 검색 단계를 건너뛰면 구성이 구성 파일을 통해 전적으로 관리되는 경우 또는 유지 관리 활동을 수행해야 하지만 모니터 클러스터가 다운된 경우에 유용할 수 있습니다.

## CONFIGURATION SECTIONS
단일 프로세스 또는 데몬과 관련된 각 구성 옵션에는 단일 값이 있습니다. 그러나 구성 옵션의 값은 데몬 유형에 따라 다를 수 있으며, 같은 유형의 다른 데몬 간에도 다를 수 있습니다. 모니터 구성 데이터베이스 또는 로컬 구성 파일에 저장된 Ceph 옵션은 소위 "구성 섹션"이라고 하는 섹션으로 그룹화되어 어떤 데몬 또는 클라이언트에 적용되는지를 나타냅니다.

이러한 섹션에는 다음이 포함됩니다:

- global
글로벌 설정은 Ceph 스토리지 클러스터의 모든 데몬과 클라이언트에 영향을 줍니다.

예제
log_file = /var/log/ceph/$cluster-$type.$id.log

- mon
mon 아래의 설정은 Ceph 스토리지 클러스터의 모든 ceph-mon 데몬에 영향을 미치며, global의 동일한 설정을 재정의합니다.

예제
mon_cluster_log_to_syslog = true

- mgr
mgr 섹션의 설정은 Ceph 스토리지 클러스터의 모든 ceph-mgr 데몬에 영향을 미치며, 글로벌에서 동일한 설정을 재정의합니다.

예제
mgr_stats_period = 10

- osd
osd 섹션의 설정은 Ceph 스토리지 클러스터의 모든 ceph-osd 데몬에 영향을 미치며, 글로벌에서 동일한 설정을 재정의합니다.

예시
osd_op_queue = wpq

- mds
mds 섹션의 설정은 Ceph 스토리지 클러스터의 모든 ceph-mds 데몬에 영향을 미치며, 글로벌에서 동일한 설정을 재정의합니다.

예시
mds_cache_memory_limit = 10G

- client
클라이언트 아래의 설정은 모든 Ceph 클라이언트(예: 마운트된 Ceph 파일 시스템, 마운트된 Ceph 블록 디바이스)와 RGW(RADOS Gateway) 데몬에 영향을 줍니다.

예제
objecter_inflight_ops = 512

구성 섹션에는 개별 데몬 또는 클라이언트 이름을 지정할 수도 있습니다. 예를 들어, mon.foo, osd.123, client.smith는 모두 유효한 섹션 이름입니다.

지정된 데몬은 전역 섹션, 데몬 또는 클라이언트 유형 섹션, 그리고 그 이름을 공유하는 섹션에서 설정을 가져옵니다. 가장 구체적인 섹션의 설정이 우선하므로, 예를 들어 동일한 옵션이 동일한 소스(즉, 동일한 구성 파일)의 global, mon, mon.foo에 모두 지정되어 있는 경우 mon.foo 설정이 사용됩니다.

동일한 섹션에 동일한 구성 옵션의 값이 여러 개 지정되어 있는 경우 마지막으로 지정된 값이 우선 적용됩니다.

로컬 설정 파일의 값은 표시되는 섹션에 관계없이 항상 모니터 설정 데이터베이스의 값보다 우선한다는 점에 유의하세요.

## METAVARIABLES

메타변수는 Ceph 스토리지 클러스터 구성을 획기적으로 간소화합니다. 메타변수가 구성 값에 설정되면 Ceph는 구성 값이 사용되는 시점에 메타변수를 확장합니다. 이러한 방식으로 Ceph 메타변수는 Bash 셸에서 변수 확장이 작동하는 방식과 유사하게 작동합니다.

Ceph는 다음과 같은 메타변수를 지원합니다:

- $cluster
Ceph 스토리지 클러스터 이름으로 확장합니다. 동일한 하드웨어에서 여러 Ceph 스토리지 클러스터를 실행할 때 유용합니다.

예제
/etc/ceph/$cluster.keyring
기본값
ceph

- $type
데몬 또는 프로세스 유형으로 확장합니다(예: mds, osd 또는 mon).

예제
/var/lib/ceph/$type

- $id
데몬 또는 클라이언트 식별자로 확장합니다. osd.0의 경우 0이 되고, mds.a의 경우 a가 됩니다.

예제
/var/lib/ceph/$type/$cluster-$id

- $host
프로세스가 실행 중인 호스트 이름으로 확장합니다.

- $name
type.$id로 확장합니다.

예제
/var/run/ceph/$cluster-$name.asok

- $pid
데몬 pid로 확장합니다.

예제
/var/run/ceph/$cluster-$name-$pid.asok

## CEPH CONFIGURATION FILE
Ceph 프로세스는 시작 시 다음 위치에서 구성 파일을 검색합니다:

1. $CEPH_CONF(즉, $CEPH_CONF 환경 변수 뒤의 경로)
2. -c path/path(즉, -c 명령줄 인수)
3. /etc/ceph/$cluster.conf
4. ~/.ceph/$cluster.conf
5. ./$cluster.conf(즉, 현재 작업 디렉터리)
6. FreeBSD 시스템에서만, /usr/local/etc/ceph/$cluster.conf

여기서 $cluster는 클러스터의 이름입니다(기본값: ceph).

Ceph 구성 파일은 ini 스타일 구문을 사용합니다. 파운드 기호(#) 또는 세미콜론 세미콜론(;) 뒤에 "주석 텍스트"를 추가할 수 있습니다. 예시

```
# <--댓글 앞에 숫자 기호(#)를 붙입니다.
; 댓글은 무엇이든 입력할 수 있습니다.
# 댓글은 항상 각 줄에 세미콜론 세미콜론(;) 또는 파운드 기호(#)가 뒤에 와야 합니다.
# 줄의 끝은 댓글을 종료합니다.
# 구성 파일에 코멘트를 제공하는 것이 좋습니다.
```

### CONFIG FILE SECTION NAMES

구성 파일은 섹션으로 나뉩니다. 각 섹션은 대괄호로 묶인 유효한 구성 섹션 이름(위의 구성 섹션 참조)으로 시작해야 합니다. 예를 들어

```
[global]
debug_ms = 0

[osd]
debug_ms = 1

[osd.1]
debug_ms = 10

[osd.2]
debug_ms = 10

```

### CONFIG FILE OPTION VALUES
구성 옵션의 값은 문자열입니다. 문자열이 너무 길어서 한 줄에 넣을 수 없는 경우에는 줄 끝에 백슬래시(\)를 넣으면 백슬래시가 줄 계속 마커로 작동합니다. 이 경우 옵션의 값은 현재 줄의 = 뒤에 오는 문자열과 다음 줄의 문자열이 결합된 문자열이 됩니다. 다음은 예시입니다:

```
[global]
foo = long long ago\
long ago

```

이 예에서 "foo" 옵션의 값은 "long long ago long ago"입니다.

옵션 값은 일반적으로 개행 또는 주석으로 끝납니다. 예를 들어

```
[global]
obscure_one = difficult to explain # I will try harder in next release
simpler_one = nothing to explain

```

이 예에서 'obscure one' 옵션의 값은 'difficult to explain'이고 'simpler one' 옵션의 값은 'nothing to explain'입니다.

옵션 값에 공백이 포함된 경우 범위를 명확히 하고 값의 첫 번째 공백이 값의 끝으로 해석되지 않도록 하기 위해 작은따옴표 또는 큰따옴표로 묶을 수 있습니다. 예를 들어

```
[global]
line = "to be, or not to be"

```

옵션 값에서 이스케이프 문자로 취급되는 문자는 =, #, ;, [ 등 네 가지입니다. 옵션 값 바로 앞에 백슬래시 문자(\)가 오는 경우에만 옵션 값에 포함될 수 있습니다. 예를 들어

```
[global]
secret = "i love \# and \["

```

각 구성 옵션은 다음 유형 중 하나에 속합니다:

- int
64비트 부호 있는 정수. "K", "M", "G", "T", "P", "E"(각각 103, 106, 109 등을 의미)와 같은 일부 SI 접미사가 지원됩니다. "B"는 유일하게 지원되는 단위 문자열입니다. 따라서 "1K", "1M", "128B" 및 "-1"이 모두 유효한 옵션 값입니다. 임계값 옵션에 음수 값이 지정되면 해당 옵션이 "무제한", 즉 임계값이나 제한이 적용되지 않음을 나타낼 수 있습니다.

예시
42, -1

- uint
음수 값이 허용되지 않는다는 점만 정수와 다릅니다.

예시
256, 0

- str
UTF-8로 인코딩된 문자열입니다. 특정 문자는 허용되지 않습니다. 자세한 내용은 위의 참고 사항을 참조하세요.

예시
"hello world", "I LOVE \#", yet-another-name

- boolean
일반적으로 참 또는 거짓 두 값 중 하나입니다. 그러나 모든 정수가 허용됩니다. "0"은 거짓을 의미하고 0이 아닌 값은 참을 의미합니다.

예시
true, false, 1, 0

- addr
단일 주소로, 선택적으로 메신저 프로토콜에 따라 v1, v2 또는 임의의 접두사를 붙일 수 있습니다. 접두사를 지정하지 않으면 v2 프로토콜이 사용됩니다. 자세한 내용은 주소 형식을 참조하세요.

예시
v1:1.2.3.4:567, v2:1.2.3.4:567, 1.2.3.4:567, 2409:8A1E:8FB6:AA20:1260:4BFF:FE92:18F5::567, [::1]:6789

- addrvec
","로 구분된 주소 집합입니다. 주소는 선택적으로 [ 및 ]로 따옴표로 묶을 수 있습니다.

예시
[v1:1.2.3.4:567,v2:1.2.3.4:568], v1:1.2.3.4:567,v1:1.2.3.14:567 [2409:8a1e:8fb6:aa20:1260:4bff:fe92:18f5::567], [2409:8a1e:8fb6:aa20:1260:4bff:fe92:18f5::568]

- uuid
RFC4122에 정의된 uuid의 문자열 형식입니다. 특정 변형도 지원됩니다. 자세한 내용은 Boost 문서를 참조하세요.

예시
f81d4fae-7dec-11d0-a765-00a0c91e6bf6

- size
64비트 부호 없는 정수. SI 접두사와 IEC 접두사가 모두 지원됩니다. "B"만 지원되는 단위 문자열입니다. 음수 값은 허용되지 않습니다.

예시
1Ki, 1K, 1KiB 및 1B.

- secs
기간을 나타냅니다. 기본 시간 단위는 초입니다. 지원되는 시간 단위는 다음과 같습니다:

second: s, sec, second, seconds

minute: m, min, minute, minutes

hour: hs, hr, hour, hours

day: d, day, days

week: w, wk, week, weeks

month: mo, month, months

year: y, yr, year, years

예시
1 m, 1m, 1 week

## MONITOR CONFIGURATION DATABASE
모니터 클러스터는 전체 클러스터에서 사용할 수 있는 구성 옵션의 데이터베이스를 관리합니다. 이를 통해 전체 시스템의 중앙 구성 관리를 간소화할 수 있습니다. 관리의 용이성과 투명성을 위해 대부분의 구성 옵션은 이 데이터베이스에 저장할 수 있으며 저장해야 합니다.

일부 설정은 프로세스의 모니터 연결, 인증, 구성 정보 가져오기 기능에 영향을 미치기 때문에 로컬 구성 파일에 저장해야 할 수도 있습니다. 대부분의 경우 이는 mon_host 옵션에만 적용됩니다. DNS SRV 레코드를 사용하면 이 문제를 피할 수 있습니다.

### SECTIONS AND MASKS
모니터에 저장된 구성 옵션은 전역 섹션, 데몬 유형 섹션 또는 특정 데몬 섹션에 저장할 수 있습니다. 이 경우 구성 파일의 옵션과 다르지 않습니다.

또한 옵션에는 옵션이 적용되는 데몬 또는 클라이언트를 추가로 제한하기 위해 옵션에 마스크를 연결할 수 있습니다. 마스크는 두 가지 형태가 있습니다:

type:location 여기서 type은 rack 또는 host와 같은 CRUSH 속성이고 location는 해당 속성에 대한 값입니다. 예를 들어 host:foo는 특정 호스트에서 실행 중인 데몬 또는 클라이언트로만 옵션을 제한합니다.

class:device-class 여기서 device-class는 CRUSH 장치 클래스의 이름입니다(예: hdd 또는 ssd). 예를 들어 class:ssd는 SSD로 지원되는 OSD로만 옵션을 제한합니다. (이 마스크는 SSD가 아닌 데몬이나 클라이언트에는 영향을 미치지 않습니다.)

구성 옵션을 지정하는 명령에서 옵션의 인수(다음 예제에서는 "who" 문자열)는 섹션 이름, 마스크 또는 슬래시 문자(/)로 구분된 두 가지의 조합일 수 있습니다. 예를 들어 osd/rack:foo는 foo 랙에 있는 모든 OSD 데몬을 참조합니다.

구성 옵션이 표시될 때 섹션 이름과 마스크는 가독성을 높이기 위해 별도의 필드나 열에 표시됩니다.

### COMMANDS

다음 CLI 명령은 클러스터를 구성하는 데 사용됩니다:

`ceph config dump`는 클러스터의 전체 모니터 구성 데이터베이스를 덤프합니다.

`ceph config get <who>`는 특정 데몬 또는 클라이언트에 대한 모니터 구성 데이터베이스에 저장된 구성 옵션을 덤프합니다(예: mds.a).

`ceph config get <who> <option>`은 특정 데몬 또는 클라이언트에 대해 모니터 구성 데이터베이스에 저장된 구성 값(예: mds.a)을 표시하거나 해당 값이 모니터 구성 데이터베이스에 없는 경우 컴파일된 기본값을 표시합니다.

`ceph config set <who> <option> <value>`은 모니터 구성 데이터베이스의 구성 옵션을 지정합니다.

`ceph config show <who>`는 실행 중인 데몬의 구성을 표시합니다. 로컬 구성 파일이 사용 중이거나 명령줄 또는 런타임에 옵션이 재정의된 경우 이러한 설정은 모니터에 저장된 설정과 다를 수 있습니다. 옵션 값의 소스는 출력에 표시됩니다.

`ceph config assimilate-conf -i <input file> -o <output file>` 입력 파일에서 구성 파일을 수집하고 유효한 옵션이 있으면 모니터 구성 데이터베이스로 이동합니다. 인식할 수 없거나 유효하지 않거나 모니터에서 제어할 수 없는 설정은 모두 출력 파일에 저장된 축약된 구성 파일로 반환됩니다. 이 명령은 레거시 구성 파일에서 중앙 집중식 모니터 기반 구성으로 전환하는 데 유용합니다.

`ceph config set <who> <option> <value>`과 `ceph config get <who> <option>`이 반드시 동일한 값을 반환하지는 않습니다. 후자의 명령은 컴파일된 기본값을 표시합니다. 모니터 구성 데이터베이스에 구성 옵션이 있는지 확인하려면 `ceph config dump`를 실행합니다.

## Help
특정 옵션에 대한 도움말을 받으려면 다음 명령을 실행하세요:

```
$ ceph config help <option>

$ ceph config help log_file

log_file - path to log file
 (std::string, basic)
 Default (non-daemon):
 Default (daemon): /var/log/ceph/$cluster-$name.log
 Can update at runtime: false
 See also: [log_to_stderr,err_to_stderr,log_to_syslog,err_to_syslog]

$ ceph config help log_file -f json-pretty
{
    "name": "log_file",
    "type": "std::string",
    "level": "basic",
    "desc": "path to log file",
    "long_desc": "",
    "default": "",
    "daemon_default": "/var/log/ceph/$cluster-$name.log",
    "tags": [],
    "services": [],
    "see_also": [
        "log_to_stderr",
        "err_to_stderr",
        "log_to_syslog",
        "err_to_syslog"
    ],
    "enum_values": [],
    "min": "",
    "max": "",
    "can_update_at_runtime": false
}

```

level 속성은 basic, advanced 또는 dev일 수 있습니다. 개발 옵션은 개발자가 일반적으로 테스트 목적으로 사용하기 위한 것으로 운영자가 사용하는 것은 권장하지 않습니다.

참고

이 명령은 실행 중인 모니터에 컴파일된 구성 스키마를 사용합니다. 혼합 버전 클러스터가 있는 경우(예: 업그레이드 중에 있을 수 있음) 다음 형식의 명령을 실행하여 실행 중인 특정 데몬에서 옵션 스키마를 쿼리할 수 있습니다:

```
$ ceph daemon <name> config help [option]

```

## RUNTIME CHANGES
대부분의 경우 Ceph는 런타임에 데몬의 구성을 변경할 수 있도록 허용합니다. 이는 로깅 출력량을 늘리거나 줄이고, 디버그 설정을 활성화 또는 비활성화하고, 런타임 최적화를 위해 사용할 수 있습니다.

`ceph config set` 명령을 사용하여 구성 옵션을 업데이트합니다. 예를 들어 특정 OSD에서 가장 자세한 디버그 로그 수준을 활성화하려면 다음 형식의 명령을 실행합니다:

```
$ ceph config set osd.123 debug_ms 20

```

참고

로컬 구성 파일에서 옵션을 사용자 지정한 경우에는 로컬 구성 파일보다 우선 순위가 낮으므로 중앙 구성 설정이 무시됩니다.

참고

로그 수준 범위는 0에서 20까지입니다.

### OVERRIDE VALUES
옵션은 Ceph CLI의 Ceph CLI tell 또는 데몬 인터페이스를 사용하여 일시적으로 설정할 수 있습니다. 이러한 재정의 값은 임시적이므로 현재 데몬 인스턴스에만 영향을 미치며 데몬이 다시 시작되면 영구적으로 구성된 값으로 되돌아갑니다.

오버라이드 값은 두 가지 방법으로 설정할 수 있습니다:

모든 호스트에서 다음 형식의 명령어를 사용하여 데몬에 메시지를 보냅니다:

```
$ ceph tell <name> config set <option> <value>
$ ceph tell osd.123 config set debug_osd 20

```

1. tell 명령은 와일드카드를 데몬 식별자로 사용할 수도 있습니다. 예를 들어 모든 OSD 데몬의 디버그 수준을 조정하려면 다음 형식의 명령을 실행합니다:

```
$ ceph tell osd.* config set debug_osd 20

```

2. 데몬이 실행 중인 호스트에서 다음 형식의 명령을 실행하여 /var/run/ceph의 소켓을 통해 데몬에 연결합니다:

```
$ ceph daemon <name> config set <option> <value>
$ ceph daemon osd.4 config set debug_osd 20

```

참고

`ceph config show` 명령의 출력에서 이러한 임시 값은 override의 소스가 있는 것으로 표시됩니다.

## VIEWING RUNTIME SETTINGS

실행 중인 데몬에 지정된 현재 설정은 ceph config show 명령으로 확인할 수 있습니다. 예를 들어, 데몬 osd.0의 (기본값이 아닌) 설정을 확인하려면 다음 명령을 실행합니다:

```
$ ceph config show osd.0

특정 설정을 확인하려면 다음 명령을 실행하세요:
$ ceph config show osd.0 debug_osd

기본값을 포함한 모든 설정을 확인하려면 다음 명령을 실행하세요:
$ ceph config show-with-defaults osd.0

로컬 호스트에서 관리자 소켓을 통해 연결하면 현재 실행 중인 데몬의 모든 설정을 볼 수 있습니다. 예를 들어 현재 모든 설정을 덤프하려면 다음 명령을 실행합니다:
$ ceph daemon osd.0 config show

기본값이 아닌 설정을 보고 각 값의 출처(예: 구성 파일, 모니터 또는 재정의)를 확인하려면 다음 명령을 실행하세요:
$ ceph daemon osd.0 config diff

단일 설정의 값을 확인하려면 다음 명령을 실행하세요:
$ ceph daemon osd.0 config get debug_osd

```