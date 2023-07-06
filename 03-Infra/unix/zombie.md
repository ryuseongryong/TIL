`=> There is 1 zombie process.`
- To Check the zombie process run below command
`ps axo stat,ppid,pid,comm | grep -w defunct` / `$ ps -ef | grep defunct | grep -v grep` / `ps aux | egrep "Z|defunct"`
 / `top -b -n 1 | grep zombie`
- and Then kill the parent process
`sudo kill -9 <parent_process_number>`

---
# Zombie process

- 유닉스 운영체제에서 좀비 프로세스 또는 사라진 프로세스(defunct process)는 실행이 완료되었지만 프로세스 테이블에 여전히 항목이 존재하고 있어서 시작한 프로세스가 종료 상태를 읽을 수 있는 프로세스이다. 자식 프로세스는 죽었지만 아직 수확하지 못한 상태이다.
- 프로세스가 종료되면 프로세스와 관련된 모든 메모리와 리소스가 다른 프로세스에서 사요할 수 있도록 할당 해제된다. 그러나 프로세스 테이블의 프로세스 항목은 그대로 유지된다.
- 부모에게는 자식이 죽었음을 나타내는 SIGCHLD 신호가 전송되며, 이 신호의 핸들러는 일반적으로 종료 상태를 읽고 좀비를 제거하는 대기 시스템 호출을 실행한다. 그러면 좀비의 프로세스 ID와 프로세스 테이블의 항목을 재사용할 수 있다.
- 그러나 부모가 SIGCHLD를 무시하면 좀비가 프로세스 테이블에 남게 된다. 부모가 다른 자식 프로세스를 생성하는 경우 동일한 프로세스 ID가 할당되지 않도록 하는 등 일부 상황에서는 이것이 바람직할 수 있다.

- 프로세스가 종료되고 리소스는 모두 회수되었지만, 시스템 프로세스 테이블에 남아있는 defunct 상태의 프로세스를 '좀비 프로세스'
- 실행이 종료되었지만 아직 삭제되지 않은 프로세스

