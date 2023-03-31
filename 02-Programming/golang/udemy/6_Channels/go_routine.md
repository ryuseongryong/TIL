# Go Routine
- Go runtime이 관리하는 가상 thread
- go 키워드를 사용하여 함수를 호출하면 런타임 시 새로운 goroutine을 실행
- goroutine은 asynchronously 함수를 실행하므로, 여러 코드를 동시에 실행하는데 사용
- OS thread보다 훨씬 가볍게 비동기 동시성 처리를 구현하기 위해 사용되며, go runtime이 자체 관리
- go runtime에서 관리되는 작업단위인 여러 goroutine들은 하나의 OS thread 1개로 실행되기도 함(goroutine들은 OS thread와 1대1 대응되지 않고, multiplexing으로 훨씬 적은 OS thread를 사용)
- 메모리 측면에서도 OS thread가 1MB의 스택을 갖는 반면, goroutine은 이보다 훨씬 적은 KB단위의 스택을 갖는다.(동적으로 증가 가능)
- go runtime은 goroutine을 관리하면서 go channel을 통해 go routine간 통신을 쉽게 함