# rclone sync
- https://rclone.org/commands/rclone_sync/
- 원본과 대상을 동일하게 만들고 대상만 수정한다.

## 설명
- 소스를 대상에 동기화하여 대상만 변경한다. 원본과 대상에서 동일한 파일은 전송하지 않고, 크기와 수정 시간 또는 MD5SUM으로 테스트한다.
- 필요한 경우 파일 삭제를 포함하여 소스와 일치하도록 대상을 업데이트한다.(중복된 개체 제외)
- 대상에서 파일을 삭제하지 않으려면 복사 명령을 대신 사용할 것.
- 데이터 손실이 발생할 수 있으므로 먼저 --dry-run 또는 --interactive/-i 플래그를 사용하여 테스트 할 것
- 대상에 오류가 있는 경우 대상에 있는 파일은 삭제되지 않는다는 점에 유의할 것.
- 중복개체(동일한 이름을 가진 파일, 이를 지원하는 제공업체에 있는 파일)도 아직 처리되지 않음.
- 동기화되는 것은 항상 디렉터리 자체가 아니라 디렉터리의 컨텐츠임. source:path가 디렉터리인 경우 복사되는 것은 디렉터리의 이름과 내용이 아니라 source:path의 내용임. 확실하지 않은 경우 복사 명령에 대한 자세한 설명을 참조할 것.
- dest:path가 존재하지 않으면 새로 만들어지고 source:path의 컨텐츠가 그곳으로 이동함.
- 겹치는 리모트는 동기화할 수 없음. 그러나 필터 규칙을 사용하거나 대상 디렉터리 내에 exclude-if-present 파일을을 넣어 대상 디렉터리를 동기화에서 제외하고 소스 디렉터리 내에 있는 대상과 동기화할 수 있음.
- 실시간 전송 통계를 보려면 -P/--progress 플래그를 사용할 것.
- "소스/대상에서 중복된 개체/디렉터리가 발견됨 - 무시" 오류를 처리하려면 rclone dedupe 명령을 사용할 것.