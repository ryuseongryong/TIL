- 240309
# WebAssembly
- 문제
- 해결
- 웹어셈블리가 무엇인가?

## 문제
- 프론트엔드에서 빅데이터 처리하는 과정
    - CSR(react.js) : 데이터를 프론트에서 처리
    - SSR(next.js) : 데이터를 백엔드에서 처리
    - F/E:react.js <- B/E:python <- DeltaQuery:DataFusion <- S3
    - F/E <- B/E:next.js <- DeltaQuery:DataFusion <- S3
    - 보안 이슈로 SSR을 사용하는 경우도 있음

## 해결
- 데이터 전달 방식 개선
    - 자바스크립트에서 주로 이용하는 방식은 Json/CSV로 데이터 전달
    - ArrowJS를 이용하여 Arrow에서 제공하는 IPC Stream 사용 가능(InterProcessCommunication)
        - RecordBatch를 바이트 스트림으로 변환 후 HTTP로 전달
    - F/E:react.js <-(json/csv)- B/E:python <-(record batch)- DeltaQuery:DataFusion <-(parquet file)- S3
    - F/E <-(record batch)- B/E:next.js <-(record batch)- DeltaQuery:DataFusion <-(parquet file)- S3
    - Level of Detail(게임 멀리있는 캐릭터와 가까이 있는 캐릭터)와 같이 그래프를 표현할 때 적용

- 데이터 처리 방식 개선
    - 데이터베이스/백엔드에서 데이터 처리 후 프론트엔드로 전달
    - 프론트엔드에서 데이터를 직접 처리
        - DuckDB/DataFusion/.. On WebAssembly
    - F/E:react.js <-(record batch)- B/E:python <-(record batch)- DeltaQuery:DataFusion <-(parquet file)- S3 : 쿼리 결과값 자체를 전달
    - F/E:wasm(DuckDB WebAssembly) <-(presigned url)- B/E:next.js <-(presigned url)- DeltaSharing <-(presigned url)- S3, F/E <-(presigned url)- S3 : 쿼리 값에 해당하는 parquet file의 presigned url을 전달 --> client 리소스 사용
        - selection은 확실히 유리
        - group by 등 aggregation이 크면 client가 못버티니까 사용이 어려움

- DataFusion은 webassembly 버전 전환이 느림(디펜던시가 webassembly 버전이 없는 경우가 있음)
- DuckDB, Postgresql 등은 webassembly 버전 있음

## 웹 어셈블리란?
- ISA(Instruction Set Architecture) e.g. X86-ISA, ARM-ISA, X86을 바로 실행할 수 있는 코드
- WebEmbedding
- Non-WebEmbedding
    - WASI(Web Assembly System Interface)
    - WASIX => POSIX 호환
- LLVM으로 컴파일 가능한 모든 언어를 웹 어셈블리로 만들 수 있음
- 물리 CPU에서 실행되지 않는(지원되지 않는) 코드를 바이트 코드라고 함

- 웹 어셈블리 런타임 엔진(wasmer, ...)
    - C/Go/... => LLVM IR(compiler) => WASM => LLVM IR(Runtime) => X86/ARM/...
    - WA -> Runtime API -> Singlepass -> Executable code :: line by line reading 같이 동작
                        -> Cranelift -> Executable code
                        -> LLVM -> Executable code
    - JIT 같은 방식
- 웹이 필요한 경우에만 해당 프로젝트가 필요함(WebEmbedding 환경)
- 컨테이너 환경으로는 물음표(Non-WebEmbedding 환경)

# AI 모델 경량화 소개(AI Optimization)
- k8s vs AI
- AI modeling vs AI lightweight
- 3D 모델 처음 나오고 알고리즘 개발 -> 최적화 -> Nvidia 등 개발 진행
- On device CPU, GPU, Compiler 분야에 대한 소개(SaaS, cloud 기반 외 서비스)
- LLVM(Compiler)이 핵심 내용
- 학습 : tensorFlow vs pytorch
- 리소스를 줄이고 성능을 높이는 것이 일반적인 경량화
- 네트워크를 탄다는 것은 불확실성(리스크)이 높아짐
- 자율주행은 사장되어 감, TTS를 탑재하는 것으로 방향이 잡혀감
- 생성형 AI는 정확도가 떨어지더라도 사용성이 있는 부분이 있음
---
- killer service LLM
- 기술 가능성 확인 과정에 필요한 기술과 기술이 활용될 때 필요한 기술이 다름(3D modeling)
- 커널 vs 컴파일러(양대산맥)
---
- AI모델
- AI 학습
- AI 컴파일러
- AI 파이프라인

## AI 모델
- offline data -> Data extraction & analysis : AI 화 할 수 있는 데이터 인지 확인
- Data preparation(Labeling) - Model training - Model evaluation & Validation(Iteration) :: Manual Experiment steps
- Trained Model
- Model Registry -- ML Ops
- Model Serving
- 장비빨 : TPU로 1일 => Nvidia 천만원대 서버 1개월
- 핵심 기술로 갈 수록 몇 가지로 통합됨
- SOTA(State of datta?) 로 실제 회사의 실무는 통합되어 가는 추세
- An example of CNN architecture for image classification
    - input image -> convolution layer -> ReLU layer -> pooling layer -> Fully connected layer -> output classes(dog, not dog)
    - convolution layer : 입력값 5X5 -> Parameter 3X3에 대입하여 결과값 정리
      --> 최적화 Parameter를 찾아내는 것이 학습, 근데 우리 관점에서 설명할 수 없음
## AI 학습
```
        Param
          ^
          |
          v
In <-> Operator <-> Out
```
IN/OUT PUT 30만개, param 10억개, 더 많은 데이터
- 내가 원하는 결과와 현재 결과의 갭을 줄이는 과정(Loss Function)
- 경사하강법, back propagation, ... 갭을 줄이는 과정
- 학습 방법이 중요함

## AI 컴파일러
```
In              HLO(각 단계에 대응하는 IR)             NPU(Conv)
|
Conv            두 개의 Conv를 하나로 합치는 과정
|
Conv
|
ReLU                            LLVM(Conv)        X86/ARM/...(Conv)
|
MaxPool
|
Conn                                              NVIDIA(Conv)
|
Out
```
- CPU, GPU(KUDA CNN), NPU 세 가지
- Pytorch 2.0
    - 동일한 과정, 런타임 설정 조정
- 컴파일러는 3D에서 진행된 과정과 비슷한 과정을 거치는 중
- ONNXRuntime

## AI 파이프라인
- pytorch - pickle    --       pytorch - cpu/gpu
                    onnx - onnx runtime(cuDNN, Triton, ...) - cpu/gpu/npu
                         - tensorRT - cpu/gpuNvidia
- TensorFlow - HDF5

- 모델링 경량화
- 리소스 경량화
- triton

#### todos
- what is presigned url
- LLVM(GCC에서 대체)
- 리누스 토발즈(LINUX) vs 크리스 래트너(LLVM)
- triton