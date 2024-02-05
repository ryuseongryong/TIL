- vacuum을 실행할 때, with_retention_period로 주어지는 변수는 실제 vacuum을 실행할 때, 해당 기간이 초과한 remove 로그에 대해서 동작하도록 되어 있다.
- 즉 Remove 로그가 10일치 데이터에 대해서 남겨져 있을 때, 실제로 데이터는 존재하지만 델타 테이블에서는 아무런 데이터가 없다고 판단하는 상황을 예로 들면, 
  vacuum이 실행될 때, vacuum_retention_period가 1d이면, 실행시간 기준 1일이전 데이터 중 Remove가 있는 로그에 대해서만 데이터를 삭제한다.