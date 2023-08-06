# Rsync vs Rclone
- https://www.clusterednetworks.com/blog/post/rsync-vs-rclone-what-are-differences
- Rsync는 컴퓨터와 서버 간 또는 서버와 서버 간에 데이터를 동기화하는 데 탁월한 도구이다.
  반면에 Rclone은 매우 유용한 유틸리티로 사용할 수 있는 몇 가지 고유한 기능이 있다.

## Rsync
- Rsync는 빠르고 매우 다재다능한 파일 복사 도구이다. 로컬로 복사하거나, 원격 셸을 통해 다른 호스트에 복사하거나 원격 rsync 데몬에 복사할 수 있다. 동작의 모든 측면을 제어하고 복사할 파일 집합을 매우 유연하게 지정할 수 있는 다양한 옵션을 제공한다. 소스 파일과 대상 파일의 기존 파일 간의 차이점만 전송하여 네트워크를 통해 전송되는 데이터의 양을 줄이는 델타 전송 알고리즘으로 유명하다. Rsync는 백업 및 미러링에 널리 사용되며 일상적인 사용을 위한 향상된 복사 명령으로 사용된다.

## Rclone
- Rclone은 클라우드 스토리지의 파일을 관리할 수 있는 명령줄 프로그램이다. 클라우드 공급업체의 웹 스토리지 인터페이스에 대한 풍부한 기능의 대안이다. 40개 이상의 클라우드 스토리지 제품이 S3 오브젝트 스토어, 비즈니스 및 소비자 파일 스토리지 서비스, 표준 전송 프로토콜을 포함하여 rclone을 지원한다.
- Rclone은 유닉스 명령 rsync, cp, mv, mount, ls, ncdu, tree, rm, cat에 상응하는 강력한 클라우드 명령을 제공한다. 셸 파이프라인 지원과 --dry-run 보호 기능이 포함된 친숙한 구문도 Rclone의 특징이다. 명령줄, 스크립트 또는 API를 통해 사용할 수 있다.
- Rclone은 클라우드 스토리지의 "스위스 군용 칼"이라고 불린다.

Rsync | Rclone
--- | ---
두 대의 Linux/Unix 컴퓨터/서버 간의 동기화에 사용됨 | Google Drive 또는 BackBlaze와 같은 클라우드 스토리지 백업에 사용됨
양방향 동기화 | 단방향 동기화
링크, 장치, 소유자, 그룹, 권한 복사 지원 | 전송하는 각 파일을 원격 클라우드 스토리지 시스템에 기본 개체로 저장
익명 또는 인증된 rsync 데몬 지원(미러링에 이상적) | 복사 또는 동기화 명령 지원

## Conclusion
- 백업의 3-2-1 규칙
- 데이터 사본 3개, 로컬 네트워크의 다른 두 가지 미디어 유형에 2개, 오프사이트 위치(원격 사무실 또는 클라우드)에 1개 복사하는 것이 중요함.