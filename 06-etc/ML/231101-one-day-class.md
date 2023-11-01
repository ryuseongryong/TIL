- AWS personalize : 추천 모델 생성
- AWS sagemaker : AI Hub LLM 모델 생성 및 사용법
- 전처리 단계 설명 예정
---
- sagemaker 시작하기(이진혁 님) -> 도메인 생성
- personalize 설명(김진아 님)
개인화 추천
대형화면에서 모바일 화면으로 전환, 추천 서비스의 중요도 증가
60% 추천서비스 제공 시 단골이 됨
10-15% 이익률 향상
추천 서비스를 처음부터 진행하는 것은 쉽지 않음
    - 대규모 = TCO증가
    - AWS personalize 시작

API 호출을 통한 편리한 사용이 가능
ML life cycle : data -> algorithm -> train test -> model -> prediction
AWS Personalize : data -> solution(model) -> campaigns(endpoint)

- 머신러닝 전문성 없이 개인화된 추천 제공 가능
일반적인 ML 산출물을 넘어서는 강력한 기능
실시간 추천
time to market을 줄이는 자동화 단계
기존 시스템과 자연스럽게 통합
프라이빗, 안전하게 암호화

User Personalization(유저 프로필과 흥미에 맞춤식 추천)
Related items(유저가 이전에 둘러본 것과 유사한 것)
Personalized ranking
user segmentation(비슷한 관심사가 있는 유저)

커스텀 | 데이터  데이터 | 도메인(커스텀)
        솔루션/레시피   레커멘더
        솔루션 버전     레커멘더
    캠페인(추천을 위한 API endpoint)

top picks for you
more like Y 등 옵션 설정 가능

사용자 그룹화를 통해 마켓팅, 프로모션 행사 제공
추천결과 명시적 제어 가능

interactions data(필수, 최소 1500) + item metadata(50) + user metadata(50) => personalize -> API

column header
data0
data1
...
+ 스키마 정보도 같이 입력해줘야 함(데이터 타입 구분)
+ 각 필요한 데이터 별로 필수 조건이 다르기 때문에 확인해서 진행해야 함

MCR, Precise 등 설정
캠페인 생성 솔루션 지정 및 배포하여 캠페인 생성

롯데마트, 코세라, 지그재그, 에이블리 등

Q. 실제 스타트업에서 사용하려면?
데이터 준비에 시간이 많이 소요됨

Q. sagemaker는 MLops 솔루션 : 데이터 전처리 수집, 깃헙 통합, 모델 트레이닝, 배포, 노트북 환경에서 개발 등 모든 작업이 통합된 서비스

Q. personalize는 이미 모델이 있어서 데이터만 넣고 결과값을 받아올 수 있는 서비스임

concat vs join

missing data 처리 방법은 여러가지가 있음

item data

s3://sagemaker-us-east-1-7***1/output_1698816827

interaction data
s3://sagemaker-us-east-1-7***1/output_1698817536

user data
s3://sagemaker-us-east-1-7***1/output_1698817749

rating => interaction data

metadata 범주형이거나 integer 타입이 있음

genAI -> jump start model -> 바로 배포 / jump start 등
personalize

세일즈에서 크레딧 사용 과정
- 실습 비용 크레딧 12월 1주, 테스트 자유롭게 사용 가능
- 연락 받으면 삭제 가능
- 11월 10일 정도에 크레딧 지급

온프레미스 GPU 사용하다가 AWS GPU로 옮길 때 비용문제가 발생(instance 점유 문제) -> sagemaker로 대체 + ECR로 비용 절감 가능

p type instance는 가격이 많이 나옴(nvidia)
gravvy dong계열을 추천함
-> sagemaker로 컴퓨팅 사용효율 극대화 + instance type 변경(비용차이가 얼마나 나는지 : pricing calc, 성능차이는? 케이스 바이 케이스) 80% 효율, 50% 가격
ml.g4dn.4xlarge = ml.p3.2xlarge

숫자 기반 학습
단어를 벡터 공간에 표시하여 유사도 등을 설정
(라이브러리들이 있음 word2vec)
| 달다(5,0)
|    쓰다(4,1)
|         읽다(3,3)
|
|________________

대충 언어모델이 이렇게 만들어져서 서비스 되는 구나

rag, commercial use case file
rag는 chat gpt의 거짓말을 보완하기 위한 모델, 중간에 검색을 함, 지식을 강제로 넣어줌, 거대 IT에서 고려중임

commercial use case는 실제 LLM, genAI를 어디서 사용하는지에 대한 내용

필터는 추가적인 부분

테스트가 필요한 시나리오
fancon 7b bf16 ml.g5.8xlarge
gpt2 ml.p3.4xlarge vs ml.p3.4xlarge
bloom 1b7 ml.p3.2xlarge, ml.g4dn.4xlarge

리소스 사용량을 7-80%로 타이트하게 가져가면 빡셀 수 있음
50% 이하로 사용하는 것을 추천함

삭제는 노트북 인스턴스, 트레이닝, 인퍼런스 등 에 대해서는 success, failed로 나오는 것은 이미 끝난 것이고, 인퍼런스, 엔드포인트는 꼭 확인이 필요함