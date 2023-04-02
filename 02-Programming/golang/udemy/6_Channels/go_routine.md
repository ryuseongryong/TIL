# Intro
```
go checkLink(link)
go : Create a new thread go routine
function : run this function with it
```

# Go Scheduler
```
            One CPU Core

            Go Scheduler

Go Routine0 Go Routine1 Go Routine2
```
- Scheduler runs one routine until it finishes or makes a blocking call(like an HTTP request)

```
One CPU Core0 One CPU Core1 One CPU Core2 

            Go Scheduler

Go Routine0 Go Routine1 Go Routine2
```
- by default, Go tries to use one core
- Scheduler runs one thread on each logical core

### Concurrency
- we can have multiple threads executing code. If one thread blocks, another one is picked up and worked on

### Parallelism
- Multiple threads executed at the executed at the exact same time. Requires multiple CPU's

## Bug
- Main Routine : main routine created when we launched our program
- Child go routine : child routines created by the go keyword
- these are crash?

# Go Routine
- Go runtime이 관리하는 가상 thread
- go 키워드를 사용하여 함수를 호출하면 런타임 시 새로운 goroutine을 실행
- goroutine은 asynchronously 함수를 실행하므로, 여러 코드를 동시에 실행하는데 사용
- OS thread보다 훨씬 가볍게 비동기 동시성 처리를 구현하기 위해 사용되며, go runtime이 자체 관리
- go runtime에서 관리되는 작업단위인 여러 goroutine들은 하나의 OS thread 1개로 실행되기도 함(goroutine들은 OS thread와 1대1 대응되지 않고, multiplexing으로 훨씬 적은 OS thread를 사용)
- 메모리 측면에서도 OS thread가 1MB의 스택을 갖는 반면, goroutine은 이보다 훨씬 적은 KB단위의 스택을 갖는다.(동적으로 증가 가능)
- go runtime은 goroutine을 관리하면서 go channel을 통해 go routine간 통신을 쉽게 함

# 익명함수 Go Routine
- 익명함수에 대해서도 사용할 수 있음
- go 키워드 뒤에 익명함수를 정의하여 익명함수를 비동기로 실행하게 함

# 다중 CPU 처리
- 디폴트로 1개의 CPU 사용
- 여러 개의 Go Routine을 만들더라도 1개의 CPU에서 작업을 시분할하여 처리함
- 머신이 여러 개의 CPU를 가진 경우, Go 프로그램을 다중 CPU에서 병렬 처리할 수 있는데, 병렬 처리를 위해서는 runtime.GOMAXPROCS(<CPU 수>)함수를 호출해야 함