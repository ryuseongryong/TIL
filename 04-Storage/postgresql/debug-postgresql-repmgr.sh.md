# bitnami postgresql-repmgr:16.1.0-debian-11* 에 대한 동작 구성에 대한 분석글
- https://github.com/bitnami/containers/tree/main/bitnami/postgresql-repmgr/16/debian-11
- 배경 : postgresql-ha helm chart로 설정한 DB에 에러가 발생하여 디버깅 중 확인이 필요하여 분석함
- 발생한 에러는 마스터 노드 정상 동작, pgpool, repmgr를 통한 스탠바이 노드 비정상 동작(실행되지 않음)
    - 실행되지 않는 원인으로는 Cloning data로그 이후에 실행되는 과정에서 마스터 노드에 대해 timeout이 발생함
    - 임의로 해당 timeout을 늘려 접근 가능하도록 설정하면, `/tmp/.s.PGSQL.5432` 소켓이 없어서 통신이 불가능하다는 에러가 발생함
    - 정상 동작하는 스탠바이 노드에서는 로컬 postgresql 소켓에 대해 요청하는 것이 아니라, 마스터 노드에 대해 요청해야 하고, 해당 요청의 명령어는 다음과 같다. : `PGPASSWORD="$REPMGR_PASSWORD" repmgr -h "postgresql-ha-postgresql-0.postgresql-ha-postgresql-headless.postgresql-ha.svc.cluster.local" -p 5432 -U repmgr -d "dbname=repmgr connect_timeout=30" -D /bitnami/postgresql/data --fast-checkpoint --force standby clone`
    - 위 명령어(`repmgr standby clone`)로 `pg_basebackup`이 시작되고 : `pg_basebackup -l "repmgr base backup"  -D /bitnami/postgresql/data -h postgresql-ha-postgresql-0.postgresql-ha-postgresql-headless.postgresql-ha.svc.cluster.local -p 5432 -U repmgr -c fast -X stream -S repmgr_slot_1001` 마스터 노드의 데이터를 백업해온다. 하지만 문제가 발생한 노드에서는 애초 타임아웃 문제를 해결하더라도 pg_basebackup에 대한 host설정이 localhost로 설정되어 있고, replication slot 또한 존재하지 않는다고 나타난다. 이 부분이 핵심적인 문제로 보이는데(host 설정이 localhost인 것과 replication slot이 없다고 나타내는 문제) 정확한 원인이 어디인지 확인이 필요하다.

- 문제 해결 : Readiness에서 에러가 발생하는 것과 연관이 있는 것으로 보이나 정확한 원인은 확인하지 못함
    - https://github.com/bitnami/charts/issues/15390#issuecomment-1831941719
    - Readiness에서 `exec [bash -ec PGPASSWORD=$POSTGRES_PASSWORD psql -w -U "postgres" -d "postgres" -h 127.0.0.1 -p 5432 -c "SELECT 1"]` 를 실행하도록 되어있다. 그러나 어떤 이유에서인지 해당 readiness가 실행되지 않고, main scripts는 위에서 말한 것과 같이 timeout이 발생한다.
    - 이상한 점은 Readiness는 kubernetes에서 컨테이너의 준비상태를 확인하기 위한 것인데, 이 기능을 false로 설정하여 사용하지 않으면 main scripts가 정상동작하며 postgresql이 잘 실행되고 standby모드로 잘 동작한다는 것이다.
    - pgpool의 rollout을 headlessWithNotReadyAddresses인 상태에서도 유지하기 위한 변수가 있어서 이를 사용하면 bitnami에서 별도로 만들어놓은 readiness-probe.sh 스크립트를 실행하도록 되어 있다.
    - readiness-probe.sh는 pgpool의 liveness timeout과 period의 값을 합친 만큼을 기다려주는 것이다. 해당 스크립트를 readiness로 설정하면 정상동작한다.
    - pod restart는 liveness에서 확인해주기 때문에 일단은 위 설정으로 사용할 수 있으나, 정확한 원인은 계속 확인이 필요하다.

- readiness-probe.sh
    - chart에서 별도로 hooks-scripts-configmap으로 생성하도록 설정되어 있다.
```
  readiness-probe.sh: |-
    #!/bin/bash
    set -o errexit
    set -o pipefail
    set -o nounset

    # Debug section
    exec 3>&1
    exec 4>&2

    # Load Libraries
    . /opt/bitnami/scripts/liblog.sh
    . /opt/bitnami/scripts/libpostgresql.sh

    # Load PostgreSQL & repmgr environment variables
    . /opt/bitnami/scripts/postgresql-env.sh

    # Process input parameters
    MIN_DELAY_AFTER_POD_READY_FIRST_TIME=$1
    TMP_FIRST_READY_FILE_TS="/tmp/ts-first-ready.mark"
    TMP_DELAY_APPLIED_FILE="/tmp/delay-applied.mark"

    DB_CHECK_RESULT=$(echo "SELECT 1" | postgresql_execute_print_output "$POSTGRESQL_DATABASE" "$POSTGRESQL_USERNAME" "$POSTGRESQL_PASSWORD" "-h 127.0.0.1 -tA" || echo "command failed")
    if [[ "$DB_CHECK_RESULT" == "1" ]]; then
      if [[ ! -f "$TMP_DELAY_APPLIED_FILE" ]]; then
        # DB up, but initial readiness delay not applied
        if [[ -f "$TMP_FIRST_READY_FILE_TS" ]]; then
          # calculate delay from the first readiness success
          FIRST_READY_TS=$(cat $TMP_FIRST_READY_FILE_TS)
          CURRENT_DELAY_SECONDS=$(($EPOCHSECONDS - $FIRST_READY_TS))
          if (( $CURRENT_DELAY_SECONDS > $MIN_DELAY_AFTER_POD_READY_FIRST_TIME )); then
            # minimal delay of the first readiness state passed - report success and mark delay as applied
            touch "$TMP_DELAY_APPLIED_FILE"
          else
            # minimal delay of the first readiness state not reached yet - report failure
            exit 1
          fi
        else
          # first ever readiness test success - store timestamp and report failure
          echo $EPOCHSECONDS > $TMP_FIRST_READY_FILE_TS
          exit 1
        fi
      fi
    else
      # DB test failed - report failure
      exit 1
    fi
```