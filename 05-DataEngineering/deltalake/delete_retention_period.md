- delete_retention_period를 초과하는 로그에 대해서만 Remove를 생성하여 보존 기간을 설정한다.
- 해당 보존 기간 설정은 Remove 로그를 추가하는 것이고, 실제 데이터 삭제는 vacuum에 의해 이루어진다.