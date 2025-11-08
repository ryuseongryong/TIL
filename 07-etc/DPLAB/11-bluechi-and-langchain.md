- 240601

k8s -> 임베디드에 적용? -> k3s

k3s - kine etcd compatable 분산저장용

docker oci 표준 X -> docker CE -> 유지보수 이슈로 containerd, CRIO

embeded에서는 실시간성, 동작 완성 보장이 필요하기 때문에 멀티노드 컨트롤하는 방법
- bluechictl : d-bus(local IPC) + TCP/IP
- hird, eclipse bluechi
- ansible로 배포

- podman : rootless(docker는 root server와 연결되어 있는 구조라 systemd가 host systemd와 연관)
- bluechi-selinux
- bluechictl unix domain에서 동작하기 때문에 master에서만 동작
- master HA? - SPF상태, leader node - follower node로 동작하게 left algorithm? 확인 필요

- statemanager에서 직접 구현해야 함(scheduler 역할)
    - cross node dependency 기능 - bluechi의 기능

- 사용할 서비스는 미리 설치, 실행 순서만 컨트롤 : systemd wants, after bluechi-proxy@agent03.service
- https://hirte.readthedocs.io/en/latest/architecture/
---
Lang Chain - chatgpt
- triton 등 가볍지 않은 이야기 위주로 진행했어서
- chatbot이 유행했던 시기가 있었음 javis 같은 느낌
- openAI 회의론자 - 기술력이 아닌, 비용문제로 회의적
- chatGPT API를 적용하는 관점에서 LangChain을 알면 도움이 됨

LLM Large Language Model
- 학습될 때 기준 데이터까지만 모델에 반영되기 때문에, 최신정보를 반영한 모델을 위하여 탄생한 것이 Prompt, Rag

Embedding Vector
- 데이터를 숫자(부동 소수점)의 배열로 표현
- 데이터의 길이와 관계없이 배열의 크기는 동일(OpenAI Embedding 1536, 3072 배열로 구성됨)
- 배열의 공간상 위치는 의미를 가짐
    - cat - dog < cat - car (embedding vector의 거리)
    - 치와와 - 진돗개 < 치와와 - 고양이
    - 이렇게 만들어야 하는 게 OpenAI Embedding vector
    - 문장에 대한 벡터도 동일하게 적용
- 벡터DB
    - embedding vector 저장
    - 유사도 기준 검색

Prompt Engineering
- 토큰 사이즈(한 번에 입력할 수 있는 단어의 개수)가 중요함
- 컨텍스트

RAG(Retrieval-Augmented Generation)
- User -Q-> LangChain -Q->          Embedding model
                      <-Qvector-

                      -Q vectore->    Qdrant
                      <-Top K facts-

                      -Prompt + Top K facts-> LLM
                      <-Answer-

- 환상을 깨주는 알고리즘
- 사전에 계속해서 split - embedding - vectorizing - store

LangChain
- Document Loading(URLs, PDFs, Database -> Documents)
- Splitting(Splits)
- Storage(vector Store)
- Retrieval(Retrieval splits, query)
- Output

Text-To-SQL
- https://github.com/r0mymendez/text-to-sql
- 약어를 자신만 알게 쓰는 것에 대한 문제가 여기서도 문제가 됨
- LLM의 성능이 아닌 데이터 퀄리티 문제로 쉽지 않아 보임
- 현실적인 방법으로 LangChain을 갖고 이를 만드는 것을 시도함