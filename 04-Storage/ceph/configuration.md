- https://docs.ceph.com/en/latest/rados/configuration/

# Configutation

각 Ceph 프로세스, 데몬 또는 유틸리티는 시작할 때 여러 소스에서 구성을 가져옵니다. 이러한 소스에는 (1) 로컬 구성, (2) 모니터, (3) 명령줄, (4) 환경 변수가 포함될 수 있습니다.

구성 옵션은 전역적으로 설정하여 (1) 모든 데몬, (2) 특정 유형의 모든 데몬 또는 서비스 또는 (3) 특정 데몬, 프로세스 또는 클라이언트에만 적용하도록 할 수 있습니다.

(1) global
(2) mon, mgr, osd, mds, client
