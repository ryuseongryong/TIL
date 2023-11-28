# bitnami postgresql-repmgr:16.1.0-debian-11* 에 대한 동작 구성에 대한 분석글
- https://github.com/bitnami/containers/tree/main/bitnami/postgresql-repmgr/16/debian-11
- 배경 : postgresql-ha helm chart로 설정한 DB에 에러가 발생하여 디버깅 중 확인이 필요하여 분석함
- 발생한 에러는 마스터 노드 정상 동작, pgpool, repmgr를 통한 스탠바이 노드 비정상 동작(실행되지 않음)
    - 실행되지 않는 원인으로는 Cloning data로그 이후에 실행되는 과정에서 마스터 노드에 대해 timeout이 발생함
    - 임의로 해당 timeout을 늘려 접근 가능하도록 설정하면, `/tmp/.s.PGSQL.5432` 소켓이 없어서 통신이 불가능하다는 에러가 발생함
    - 정상 동작하는 스탠바이 노드에서는 로컬 postgresql 소켓에 대해 요청하는 것이 아니라, 마스터 노드에 대해 요청해야 하고, 해당 요청의 명령어는 다음과 같다. : `PGPASSWORD="$REPMGR_PASSWORD" repmgr -h "postgresql-ha-postgresql-0.postgresql-ha-postgresql-headless.postgresql-ha.svc.cluster.local" -p 5432 -U repmgr -d "dbname=repmgr connect_timeout=30" -D /bitnami/postgresql/data --fast-checkpoint --force standby clone`
    - 위 명령어(`repmgr standby clone`)로 `pg_basebackup`이 시작되고 : `pg_basebackup -l "repmgr base backup"  -D /bitnami/postgresql/data -h postgresql-ha-postgresql-0.postgresql-ha-postgresql-headless.postgresql-ha.svc.cluster.local -p 5432 -U repmgr -c fast -X stream -S repmgr_slot_1001` 마스터 노드의 데이터를 백업해온다. 하지만 문제가 발생한 노드에서는 애초 타임아웃 문제를 해결하더라도 pg_basebackup에 대한 host설정이 localhost로 설정되어 있고, replication slot 또한 존재하지 않는다고 나타난다. 이 부분이 핵심적인 문제로 보이는데(host 설정이 localhost인 것과 replication slot이 없다고 나타내는 문제) 정확한 원인이 어디인지 확인이 필요하다.