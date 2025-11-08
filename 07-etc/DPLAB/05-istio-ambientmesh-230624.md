# delta sync, rust(김인혁 이사님)
- istio ambientmesh에서 eBPF 코드가 빠졌음.(license 문제로 추정됨)
- rust의 결과 리뷰
- Delta Sync : 효율적인 데이터 수집/변환/저장
    - spark는 배치 목적
    30s 1번씩, batch에는 유리
    - JAVA, Scala로 개발된 프로그램은 GC에 영향을 받음(minor GC도 주기적으로 발생)
    - 같은 양의 데이터를 처리해도 100ms이상 차이가 남(minor GC 때문, batch duration에 영향)
    - rust로 개발된 스트리밍 처리에서는 안정적으로 동작함(batch duration)
    - 사용되는 resources의 차이
        - RES : 실제 사용하는 물리 메모리 양
        - VIRT : 요청된 메모리 양
        - 동일한 일을 하는데 spark는 3.4G(drive 1.2G, excuter 2G), rust deltasync는 50M정도 사용함
    - 기존에 micro services architecture를 monolitic service로 변경하면서 성능 향상을 하는 부분도 있음(cloud 비용 증가)
    - Rust에서 AWS SDK등 패키지를 구축되어 있어서 사용성도 괜찮음.
    - 필요한 부분만 Rust로 개발할 수 있는데, RPC 등이 필요해서 불필요하다고 생각됨.
    - delta sync도 consuming 검증(병렬 처리 가능) deployment - consumer group - departitioning
    - spark : managed, rust : native로 저장, delta log의 데이터 양이 증가하면 spark이 훨씬 더 많이 증가함.
    - memory call option -> GC -> rust

# eBPF(박성제 님)
- extended Berkeley Packet Filter
- cilium 창업자, youtube 채널로 자료를 많이 제공
- Kernel Architecture
    - Process -> syscall -> resources -> H/W
    -                (configuration)
    - Process -> syscall -> eBPF -> scheduler
- eBPF runtime
    - code -> kernel로 어떻게 넣을 것인지
    - user space : Controller -> syscall -> Linux Kernel : verifier -> JIT Compiler(byte code) -> eBPF
    - user space program에서 할 수 없는 것들을 eBPF를 통해서 할 수 있음
    - kernel module, kernel code를 사용할 필요가 없음(성능이슈, context switching없이 가능)
- eBPF Hook
    - syscall, VFS, Block Device, user Process, Sockets, TCP/IP, Network Device, Network HW(TCP Offload)
- eBPF Helpers
- eBPF Tail and Function Calls
    - A program eBPF -> B program eBPF (call stack frame 변경)
- Tail-call
    trainsition to the other program
- C코드 -> BPF target, byte code kernel, JIT compiler, byte code 실행, op code, assembly -> binary code -> kernel
- syscall 에서 호출할 때 이름이  byte code로 들어감(exec syscall에 hooked 되어 있음, loading이 목적임)
- live bpf -> ELF Object file(https://en.wikipedia.org/wiki/Executable_and_Linkable_Format) -> Section 이름으로 어디에 삽입될 지 정해서, bpf syscall로 등록할 때 그 section이름으로 동작
- ISS(Instruction Set Spec) : assembly code(https://docs.kernel.org/bpf/instruction-set.html)
- ISS로 처리되기 떄문에 더 안전할 수 있음
- Flexibility도 가능(kernel live patch)
- 성능적인 측면 : Packet Capture, Socket syscall -> low IP -> Packet | network stack | user space | operates -> Kernel 제어하게 되면 성능이 떨어질 수 있음, 이 과정이전에 eBPF에서 처리 가능.
- 기존 kernel patch, module 시는 반영에 많은 시간이 소요됨. runtime에도 update시에 재부팅이 필요한 경우도 있음. eBPF는 kernel module을 바꾸는 것은 아니고, (실제 짤 수 있는 것은 다름), API break이 발생하지 않을 수 밖에 없는 환경
- tail call이 왜 쓰이냐, 이벤트를 기능하는 함수를 짤 때 하나로 짜는 게 젤 좋은데, 나누어서 각 함수들이 다음 함수로 호출하는 경우에 대해 사용됨(eBPF에서 함수 하나는 프로그램으로 보는 것. 내부 함수는 같은 함수로 보고, tail call로 만들어야 할 이유가 있는 경우에 그렇게 사용함.)
- call option, stack over flow 등은 verifier에서 잡아주는 개념.(초기에는 loop가 없었음)
- tail call은 재귀함수가 아니고, loop임
- https://blog.cloudflare.com/assembly-within-bpf-tail-calls-on-x86-and-arm/
- tail recursion

# rust 문법(김기오 님)
- https://fluoridated-wholesaler-418.notion.site/60e0315e6d3e4f7099b775273e5cd721
- 소유권 ~ 
- primitive type은 stack rewind되면서 해제됨
