- 240427
# AI pipeline
- AI 처음 나왔을 때, AI 자체에 관심 -> 이후로 실제 실행환경이나 운영에 대한 관심
- AI 상업화를 위한 기술적인 전략
    - 온디바이스 기술
    - 파이프라인 기술(MLOps)
- OpenAI ChatGPT의 등장으로 AI 산업이 기술적인 가능성 뿐만 아니라 상업적인 가능성까지 인정
- 기존의 AI 연구/개발자보다 클라우드/시스템 개발자의 역할이 더욱 커질 것으로 기대

AI 모델
- https://cointelegraph.com/explained/what-are-convolutional-neural-networks
- 좋은 모델들은 쏟아져 나오고 있음 Llama3
- parameter의 수를 조정하는 연구, 규모의 경제로 운영됨
- 그래프형태 디자인 -> 가장 좋은 결과 -> 반복 실험(연구) : brute force -> HW성능이 좋으면 이김
- 학습 : 모델의 parameter를 채우는 것
- convolution layer
    - 3X3, 5X5, 7X7을 조정해 feature를 수정
- 모델의 역할 : 비정형 데이터에서 정보를 뽑아내는 것
    - 128byte의 정형화된 데이터로 변환해서 정보를 찾아가는 것
    - embedding feature을 뽑아가기 위해서 동작하는 것
    - back profiling
- input image - convolution layer - ReLU layer - Pooling layer - Fully connected layer
- 단순한 연산들의 집합으로 만든 것이 AI라고 할 수 있음, 데이터의 힘
- 온디바이스 : 빠르고 효율적으로 각각의 레이어들을 실행
- c.f.) VectorDB?
    - AI는 입력된 값과 가장 유사한 것을 찾는 것
    - 학습 - 모델 - embedding vector를 뽑아주는 것 - vector값 -> vectorDB에 저장 -> embedding vector와 비슷한 값으로 검색했을 때, 나중에 원본값을 알려주는 것
    - 최신 데이터를 사용할 수 없는 문제점을 해결하기 위해서 나온 것이 vectorDB, 질문내용과 유사한 검색의 최신데이터를 같이 넣어서 돌려주는 것
    - NNStreamer : GStreamer + Pipeline
    - NNTrainer

# AI 학습
          param
- in -> operater -> out

           X
- in -> Multiply -> out
  
X 값을 찾는 것이 학습
입력과 출력 값 정답을 만들어 놓은 것이 학습 데이터
heuristic한 연산자를 찾는 것
이미지 연산 -> 눈 부위의 이미지의 데이터를 계산하여 값을 찾는 것

- convolution - ReLU - convolution - ReLU의 레이어 배치는 다양할 수 있음
- 현재는 어느정도 디팩토가 나왔고, 더 이상 향상이 필요없는 수준에 도달한 것으로 보임
- 완전한 무작위를 자동화하기는 어려움(코드 작성과 비슷)

# AI 미래
- 구글 알파고 등장(2016)
    - AI 기술적인 가능성 확인
- OpenAI ChatGPT 등장(2022)
    - AI 상업적 가능성 확인 : 100%가 아니어도 사용할 수 있는 영역에 적용
    - AI 상품화를 위해 기술 패러다임 변경
        - 학습을 위한 클러스터 -> 추론을 위한 온디바이스
            - GPU/NPU, 컴파일러, sLLM/sLM, ... -> sLLM, sLM : 기존 AI 연구원들이 원하는 모델의 레이어/파라미터 개수를 수정해서 적정 수준의 리소스로 구현하는 것
        - 학습을 위한 파이프라인 -> 추론을 위한 파이프라인

# AI 프로세서
각각의 레이어를 하나의 instruction set으로 가정하고 진행

<in>                  <HLO(High Level)>         <NPU>

conv                   Conv    Conv             Conv
conv                   Conv                    <LLVM>     <X86/ARM/...>
ReLU                  ReLU    ReLU              Conv        Conv
MaxPool               MaxPool MaxPool                     <NVIDIA>
Conn                  Conn    Conn                          Conv

<out>

- CPU
    - Complex control flow
        - Branch prediction
    - SIMD(Data)
    - Single Instruction Multiple
    - L1 cache, ALU, Control
    - L2, L3 Cache
- GPU
    - SIMT(Thread)
        - IP register : 1 IP register -> many ALUs 공유(디코딩 한 번, 연산 10번)
    - SIMD(Data)
    
    - L1 cache, Control, Many ALUs
    - L2 Cache
- NVIDIA GPU Warp Synchronization
    - if (threadIdx.x < 4) {
        A;
        B;
    } else {
        X;
        Y;
    }
    - masking(결과를 반영하지 않는 것, 전류 소모 리스크가 있음)
        - 페르미 이후 if/else를 사용하면 안됨
        - m : masking
        - m X; m    Y; m    Z;
        - A; m  B; m    Z; ...
    - 효율성이 극대화된 ISA

- CUDA Programming
    - GPU로 사용할 것을 미리 할당
    - 4개 블록, 8개 스레드가 동시에 실행(32개 스레드)
    - 각각이 어떤 스레드인지를 인지하기 위해 각각의 인덱스를 가져야 함
    - 행렬 연산이 중요함

- CPU vs GPU vs NPU
    - scalar(1value) vs Vector vs Tensor(2D이상의 데이터 구조)

- NVIDIA GPU vs ???
    - CUDA 생태계 -> 높은 진입 장벽(SW까지 완성도가 높고, 검증이 잘 되어 있음)
        - CUDA vs SYCL(OpenCL):AMD에서 주력함
    - x86 vs ARM
        - ISA 호환 문제 -> 컴파일러 발전
        - CPU 독립적인 언어 -> 자바, 파이썬
        - QEMU, Binary Translation
cf.) ARM, MIPS ISA 호환 문제(기존 x86기반) -> 임베디드 개발자의 주요 업무가 컴파일링 -> 컴파일러 발전으로 해결됨 + CPU 독립적인 언어 발전(e.g. JAVA)

- PyTorch/TensorFlow 백엔드 구현
    - 상당한 시간과 노력 필요(커뮤니티의 승인이 빡셈)
    - PyTorch Mobile
        - ARM, Metal/Vulkan, NPU
- ONNX 런타임 구현(가장 현실적인 방법)
    - ONNX에 정의된, 널리 사용되는 오퍼레이터만 지원 가능
    - 일반적인 스타트업에서 사용하는 방식(FuriosaAI)
- OpenAI Triton 백엔드 구현(OpenAI가 진행하기 때문에 관심이 높고 미래가 밝음)
    - 특정 아키텍처에 종속적이지 않은 프레임워크
    - OpenAI LLM이 시장을 선도하면서 관심 집중
    - LLVM 기반 최적화 파이프라인 제공
        - Quantization, Vectorization

# AI 런타임(PyTorch Mobile)
- TorchScript 기반 최적화 제공
    - ARM(Android, iOS 지원)
    - Metal/Vulkan 하드웨어 가속 지원
    - 다양한 NPU 지원
- PyTorch 2.0 등장
    - OpenAI Triton에 영감을 받아서 등장
    - TorchDynamo, TorchInductor

c.f) PyTorch 개선점
    1. GPU, NPU활용 -> triton 관심사
    2. Python Script 개선
    - LLVM MLIR(Multi-Level Intermediate Representation)

# AI 런타임(ONNXRuntime)
- https://onnxruntime.ai/docs/execution-providers/

# AI 컴파일러
- OpenAI Triton
    - 일반적인 AI 개발자들이 CUDA에 대한 전문적인 지식없이 새로운 오퍼레이터를 개발할 수 있도록 지원
        - 기존에 널리 사용되는 오퍼레이터는 이미 CUDA 구현체가 있음(Conv, ReLU)
    - CUDA에 종속성 문제를 해결할 수 있는 가능성
        - Python -> TTIR/TTGIR -> LLVM(IR) -> PTX(NVIDIA ISA)/SPIR-V/...

- Triton with PyTorch -> TTIR/TTGIR -> CUDA/PTX -> CPU/NVIDIA
-                                   -> SYCL/SPIR-V -> CPU/GPU/NPU

- LLVM의 역할이 점점 커져감
// 여기까지 온디바이스 기술에 대한 설명들
// 특정 모델을 빠르게 실행할 수 있을까

# AI 파이프라인
- DataOps + AI/ML
- SQL 기반 AI 파이프라인 구축
    - Arrow In-Memory format
    - Arrow Datafusion
    - SQL/DataFrameAPIs
    - Parquet, CSV/JSON, Avro, ...
    - Network Traffic Monitoring
- 모델은 이미 만들어져 있고, 이를 어떻게 배포하고 사용할 수 있도록 만드는 방법
- 생성형 AI는 영상, 음성, 텍스트 정도에 한정, 기타 금융데이터, 시계열 데이터 등에 대해서는 AI를 적용하기 어려움
- 너무 구체적인 분야에 대해서는 AI를 적용하기 어려움
