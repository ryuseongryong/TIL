# OLAP vs. OLTP: What’s the Difference?

- https://www.ibm.com/blog/olap-vs-oltp/

## 이러한 용어는 서로 혼동되는 경우가 많은데, 주요 차이점은 무엇이며 상황에 맞는 용어를 어떻게 선택해야 할까요?
- 우리는 데이터를 사용하여 더 현명한 의사결정을 내리고 변화하는 요구사항에 더 빠르게 대응하는 조직이 성공할 가능성이 높은 데이터 중심 시대에 살고 있습니다. 이러한 데이터는 새로운 서비스 제공(예: 차량 공유 앱)과 소매업(이커머스 및 매장 내 거래 모두)을 주도하는 강력한 시스템에서 작동하는 것을 볼 수 있습니다.
- 데이터 과학 분야에는 온라인 분석 처리(OLAP)와 온라인 트랜잭션 처리(OLTP)라는 두 가지 유형의 데이터 처리 시스템이 있습니다. 가장 큰 차이점은 하나는 데이터를 사용하여 가치 있는 인사이트를 얻고, 다른 하나는 순전히 운영 목적이라는 점입니다. 그러나 두 시스템을 모두 사용하여 데이터 문제를 해결할 수 있는 의미 있는 방법이 있습니다.
- 문제는 어떤 것을 선택하느냐가 아니라 상황에 맞게 두 가지 처리 유형을 최대한 활용하는 방법입니다.

## What is OLAP? : Column-oriented DB

- 온라인 분석 처리(OLAP)는 대량의 데이터에 대해 고속으로 다차원 분석을 수행하는 시스템입니다. 일반적으로 이 데이터는 데이터 웨어하우스, 데이터 마트 또는 기타 중앙 집중식 데이터 저장소에서 가져옵니다. OLAP은 데이터 마이닝, 비즈니스 인텔리전스 및 복잡한 분석 계산은 물론 재무 분석, 예산 책정, 판매 예측과 같은 비즈니스 보고 기능에 이상적입니다.

- 대부분의 OLAP 데이터베이스의 핵심은 다차원 데이터를 신속하게 쿼리, 보고 및 분석할 수 있는 OLAP 큐브입니다. 데이터 차원이란 무엇인가요? 데이터 차원은 단순히 특정 데이터 집합의 한 요소입니다. 예를 들어, 매출 수치에는 지역, 연도, 제품 모델 등과 관련된 여러 차원이 있을 수 있습니다.

- OLAP 큐브는 기존 관계형 데이터베이스 스키마의 행별 형식을 확장하고 다른 데이터 차원을 위한 계층을 추가합니다. 예를 들어, 큐브의 최상위 레이어는 지역별 매출을 구성할 수 있지만, 데이터 분석가는 주/도, 도시 및/또는 특정 매장별 매출에 대한 레이어로 '드릴다운'할 수도 있습니다. OLAP을 위한 이러한 과거 집계 데이터는 일반적으로 스타 스키마 또는 눈송이 스키마에 저장됩니다.

- 다음 그래픽은 지역별, 분기별, 제품별 등 여러 차원의 판매 데이터에 대한 OLAP 큐브를 보여줍니다:
    https://www.ibm.com/blog//wp-content/uploads/2021/03/ICLH_Diagram_Batch_01_09-OLAP-DataCube-WHITEBG.png

## What is OLTP? : Row-oriented DB
- 온라인 트랜잭션 처리(OLTP)는 일반적으로 인터넷을 통해 많은 사람이 대량의 데이터베이스 트랜잭션을 실시간으로 실행할 수 있게 해줍니다. OLTP 시스템은 ATM에서 매장 내 구매, 호텔 예약에 이르기까지 일상적인 많은 거래의 기반이 됩니다. OLTP는 비밀번호 변경, 문자 메시지 등 비금융 거래도 처리할 수 있습니다.

- OLTP 시스템은 다음을 수행할 수 있는 관계형 데이터베이스를 사용합니다:
    - 일반적으로 데이터 삽입, 업데이트, 삭제와 같은 비교적 간단한 트랜잭션을 대량으로 처리합니다.
    - 데이터 무결성을 보장하면서 여러 사용자가 동일한 데이터에 액세스할 수 있도록 지원합니다.
    - 밀리초 단위로 측정되는 응답 시간으로 매우 빠른 처리를 지원합니다.
    - 신속한 검색, 검색 및 쿼리를 위해 색인화된 데이터 세트를 제공합니다.
    - 지속적인 증분 백업을 통해 연중무휴 24시간 사용할 수 있어야 합니다.

- 많은 조직에서 OLTP 시스템을 사용하여 OLAP용 데이터를 제공합니다. 다시 말해, 데이터 중심 세상에서는 OLTP와 OLAP의 조합이 필수적입니다.

## The main difference between OLAP and OLTP: Processing type
- 두 시스템의 주요 차이점은 분석과 트랜잭션이라는 이름에 있습니다. 각 시스템은 해당 처리 유형에 최적화되어 있습니다.

- OLAP는 더 현명한 의사 결정을 위해 복잡한 데이터 분석을 수행하는 데 최적화되어 있습니다. OLAP 시스템은 데이터 과학자, 비즈니스 분석가 및 지식 근로자가 사용하도록 설계되었으며 비즈니스 인텔리전스(BI), 데이터 마이닝 및 기타 의사 결정 지원 애플리케이션을 지원합니다.

- 반면 OLTP는 대량의 트랜잭션을 처리하는 데 최적화되어 있습니다. OLTP 시스템은 일선 직원(예: 계산원, 은행원, 호텔 데스크 직원)이 사용하거나 고객 셀프 서비스 애플리케이션(예: 온라인 뱅킹, 전자상거래, 여행 예약)을 위해 설계되었습니다.

## Other key differences between OLAP and OLTP
- Focus: OLAP 시스템을 사용하면 복잡한 분석을 위해 데이터를 추출할 수 있습니다. 비즈니스 의사 결정을 내리기 위해 쿼리에는 대량의 레코드가 포함되는 경우가 많습니다. 반면 OLTP 시스템은 데이터베이스에서 간단한 업데이트, 삽입 및 삭제를 수행하는 데 이상적입니다. 쿼리에는 일반적으로 하나 또는 몇 개의 레코드만 포함됩니다.
- Data source: OLAP 데이터베이스에는 다차원 스키마가 있으므로 현재 및 과거 데이터에서 여러 데이터 사실에 대한 복잡한 쿼리를 지원할 수 있습니다. 다양한 OLTP 데이터베이스가 OLAP을 위한 집계 데이터의 소스가 될 수 있으며, 데이터 웨어하우스로 구성될 수 있습니다. 반면에 OLTP는 기존 DBMS를 사용하여 대량의 실시간 트랜잭션을 수용합니다.
- Processing time: OLAP의 경우 응답 시간이 OLTP보다 훨씬 느립니다. 워크로드는 읽기 집약적이며 방대한 데이터 세트를 포함합니다. OLTP 트랜잭션 및 응답의 경우, 밀리초 단위가 중요합니다. 워크로드에는 SQL(구조화된 쿼리 언어)을 통한 간단한 읽기 및 쓰기 작업이 포함되므로 시간과 저장 공간이 적게 필요합니다.
- Availability: OLAP 시스템은 현재 데이터를 수정하지 않으므로 백업 빈도를 줄일 수 있습니다. 그러나 OLTP 시스템은 트랜잭션 처리의 특성상 데이터를 자주 수정합니다. 따라서 데이터 무결성을 유지하기 위해 자주 또는 동시에 백업해야 합니다.

## OLAP vs. OLTP: Which is best for you?
- 상황에 맞는 시스템을 선택하는 것은 목표에 따라 달라집니다. 비즈니스 인사이트를 위한 단일 플랫폼이 필요하신가요? OLAP은 방대한 양의 데이터에서 가치를 창출하는 데 도움이 될 수 있습니다. 일일 트랜잭션을 관리해야 하나요? OLTP는 초당 많은 수의 트랜잭션을 빠르게 처리하도록 설계되었습니다.

- 기존 OLAP 도구는 데이터 모델링 전문 지식이 필요하고 여러 사업부 간의 협력이 필요한 경우가 많습니다. 반면, OLTP 시스템은 비즈니스에 필수적인 시스템으로, 다운타임이 발생하면 거래 중단, 매출 손실, 브랜드 평판 손상으로 이어집니다.

- 대부분의 경우 조직은 OLAP 시스템과 OLTP 시스템을 모두 사용합니다. 실제로 OLTP 시스템에서 비즈니스 프로세스 개선으로 이어지는 데이터를 분석하는 데 OLAP 시스템을 사용할 수 있습니다.

