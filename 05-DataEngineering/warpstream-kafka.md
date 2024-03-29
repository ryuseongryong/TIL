# kafka is dead, long live kafka

- https://www.warpstream.com/blog/kafka-is-dead-long-live-kafka

## TL;DR
- warpstream은 S3 위에 직접 구축된 Apache Kafka 프로토콜 호환 데이터 스트리밍 플랫폼이다. stateless 단일 Go binary로 제공되므로 관리해야 할 로컬 디스크, 재조정해야 할 브로커, 운영해야 할 ZooKeeper가 없다. warpstream은 영역 간 네트워킹을 사용하는 대신 S3와 직접 데이터를 주고받기 때문에 클라우드의 카프카보다 5-10배 저렴하고, 이는 대규모 카프카 배포에 드는 인프라 비용의 80% 이상에 해당할 수 있다.

## Kafka is Dead, Long Live Kafka
- 이 글의 제목에 대해 강한 반응을 보였을 가능성이 높습니다. 경험상 카프카는 데이터 분야에서 가장 양극화된 기술 중 하나입니다. 어떤 사람들은 싫어하고 어떤 사람들은 맹세하지만 거의 모든 기술 회사에서 사용하고 있습니다.

- 2011년에 처음 오픈소스화된 Apache Kafka®는 스트리밍 아키텍처 구축을 위한 기본 인프라로 빠르게 자리 잡았습니다. 지금은 잘 알려진 Jay Kreps의 The Log 블로그 게시물은 카프카가 제공하는 분산 로그 추상화가 왜 그렇게 강력한지 설명하는 글이기 때문에 여전히 제가 가장 좋아하는 블로그 게시물 중 하나입니다.

- 하지만 지금은 더 이상 2011년이 아닙니다. 최신 소프트웨어를 구축하는 방법에는 많은 변화가 있었고, 주로 클라우드 환경으로의 대대적인 전환이 이루어졌지만 Kafka는 거의 그대로 유지되고 있습니다. 많은 조직이 Kafka를 클라우드 환경으로 '이동'하는 데 성공했지만, 솔직히 말해서 그 결과에 만족하는 사람은 아무도 없습니다. Kafka는 비싸고, 까다롭고, 실행하기 어렵기 때문에 이를 사용하는 대부분의 조직에서 사용하기가 어렵습니다.

- 카프카 자체는 문제가 아닙니다. 카프카는 개발 환경에 매우 적합한 훌륭한 소프트웨어입니다: 2011년 LinkedIn의 데이터 센터입니다. 하지만 두 가지 이유로 현대 워크로드에는 적합하지 않습니다:

    1. 클라우드 경제성 - 설계상 Kafka의 복제 전략은 막대한 AZ 간 대역폭 비용을 발생시킵니다.
    2. 운영 오버헤드 - 자체 Kafka 클러스터를 운영하려면 말 그대로 전담 팀과 정교한 사용자 정의 도구가 필요합니다.

- 이 글의 나머지 부분에서는 카프카에 대해 다루겠지만, 카프카에 대해 설명하는 모든 내용은 구현된 프로그래밍 언어에 관계없이 로컬 디스크에 데이터를 저장하는 유사한 모든 시스템에 동일하게 적용된다는 점을 명심하세요.

## Kafka-nomics
- 아래 다이어그램은 일반적인 3개의 가용성 영역 Kafka 클러스터를 보여줍니다: https://global-uploads.webflow.com/64baaecd9c5c9b1b6c38aa0e/64c00427b989db231aac3e45_kafka_arch.png

- 생성되는 모든 GiB의 데이터는 내구성과 가용성을 위해 2/3의 시간1에 걸쳐 영역 간에 쓰여져야 하며, 이후 파티션 리더가 다른 두 영역의 팔로워에게 복제해야 합니다. 영역 간에 1기가바이트의 데이터가 전송될 때마다 소스 영역에서의 송신은 0.022달러, 대상 영역에서의 송신은 0.01달러, 대상 영역에서의 수신은 0.01달러의 비용이 듭니다.

- 0.01*⅔ + $0.02 *2 == $0.053은 최상의 시나리오3에서 Kafka 클러스터를 통해 스트리밍하는 데이터 1기가바이트당 $0.053입니다. 한 달 동안 S3에 1기가바이트의 데이터를 저장하는 데 드는 비용은 0.0214달러에 불과하므로, Kafka를 통해 생산자에서 소비자로 데이터를 복사하는 것과 같은 비용으로 두 달 이상 S3에 데이터를 저장할 수 있습니다. 실제로 처리량이 상당한 Kafka 클러스터의 경우, 워크로드 비용의 70~90%가 영역 간 대역폭 요금에 불과하기 때문에 하드웨어 비용은 무시할 수 있는 수준입니다. 이 문제에 대한 좋은 글도 Confluent에 있습니다.

- 이 AZ 간 대역폭 문제는 Kafka 작동 방식의 근본적인 문제라는 점을 강조하는 것이 중요합니다. 카프카는 LinkedIn의 데이터 센터에서 실행되도록 설계되었으며, 네트워크 엔지니어는 애플리케이션 개발자에게 데이터 이동에 대한 비용을 청구하지 않았습니다. 하지만 오늘날 대부분의 Kafka 사용자는 완전히 다른 제약 조건과 비용 모델을 가진 환경인 퍼블릭 클라우드에서 실행하고 있습니다. 안타깝게도 조직이 연간 수천만 달러 또는 수억 달러의 클라우드 지출을 감당할 수 있는 경우가 아니라면, 이 문제의 물리적인 문제를 피할 수는 없습니다.

- 처리량 문제뿐만 아니라, 보존 기간이 긴 저처리량 Kafka 클러스터도 대용량 스토리지 요구 사항을 가질 수 있습니다. 이 경우, 고가의 로컬 SSD에 데이터를 세 번 복제하는 Kafka의 접근 방식은 디스크 사용률 100%라는 최상의 시나리오를 가정할 때 S3와 같은 오브젝트 스토리지를 사용하는 것보다 GiB당 약 10~20배5의 비용이 더 듭니다.

## Accidental SRE

- 대부분의 개발자는 해결하고자 하는 실제 문제가 있기 때문에 아파치 카프카®를 처음 접합니다. 하지만 문제 해결을 시작하기 전에 먼저 알아야 할 것이 있습니다:

    1. Kafka (brokers, coordinators, watermarks, etc)
    2. ZooKeeper (or KRaft)
    3. Leader elections
    4. Partitions (how many partitions do I need? Unclear, but better get it right because you can never change it!)
    5. Consumer groups
    6. Rebalancing
    7. Broker tuning
    8. Client tuning
    9. etc

- Kafka의 "데이터 플레인"(브로커)과 합의 기반 "제어 플레인"(컨트롤러, ZooKeeper 등)은 모두 전문성과 주의를 기울여 관리해야 하는 로컬 SSD에서 직접 실행됩니다. 실제로, 자체 호스팅 Kafka 클러스터는 노드 교체 및 클러스터 확장과 같은 기본적인 작업조차도 안전하고 안정적으로 수행하기 전에 전담 전문가 팀과 상당한 양의 사용자 정의 도구가 필요합니다. 예를 들어, 아파치 카프카에 내장된 파티션 재할당 도구는 불가피하게 하드웨어 장애가 발생했을 때 브로커를 폐기하기 위한 계획조차 생성할 수 없습니다:

    - 파티션 재할당 도구에는 아직 사용 중지하는 브로커에 대한 재할당 계획을 자동으로 생성하는 기능이 없습니다. 따라서 관리자가 직접 할당 해제할 브로커에서 호스팅되는 모든 파티션의 복제본을 나머지 브로커로 이동하기 위한 할당 계획을 세워야 합니다. 재할당 시 모든 복제본이 사용 중지된 브로커에서 다른 브로커로 이동하지 않도록 해야 하므로 비교적 지루한 작업이 될 수 있습니다.

- 많은 경우, 클러스터 관리를 AWS MSK와 같은 호스팅 제공업체로 오프로드해도 운영 부담 문제가 해결되지 않습니다. 예를 들어, 클러스터의 밸런스를 재조정하는 방법(매우 일상적인 작업)에 대한 MSK 문서에는 어떤 파티션을 어떤 브로커로 마이그레이션해야 하는지 지정하기 위해 JSON을 직접 편집해야 하고 다음과 같은 유용한 설명이 포함된 Apache Kafka 문서로 연결되는 링크만 있습니다:

    - 많은 경우, 클러스터 관리를 AWS MSK와 같은 호스팅 제공업체로 오프로드해도 운영 부담 문제가 해결되지 않습니다. 예를 들어, 클러스터의 밸런스를 재조정하는 방법(매우 일상적인 작업)에 대한 MSK 문서에는 어떤 파티션을 어떤 브로커로 마이그레이션해야 하는지 지정하기 위해 JSON을 직접 편집해야 하고 다음과 같은 유용한 설명이 포함된 Apache Kafka 문서로 연결되는 링크만 있습니다:

- 이러한 부담을 덜어줄 수 있는 크루즈 컨트롤과 같은 오픈 소스 솔루션이 있지만, 이 역시 학습해야 할 개념과 배포 및 모니터링해야 할 서비스, 그리고 해결해야 할 난관이 많습니다. 크루즈 컨트롤 자체는 아파치 카프카와 ZooKeeper 모두에 의존하는 JVM 애플리케이션입니다. 결코 가벼운 솔루션이 아닙니다.

- 안타깝게도 많은 경우 개발자가 비즈니스 문제를 해결하기 위해 시작했지만 결국 Kafka SRE가 되어버리는 경우가 많습니다.

## S3 Is All You Need

- Apache Kafka®를 사용하는 데 드는 높은 비용(달러와 엔지니어링 시간 모두)으로 인해 오늘날 기업들은 사기 탐지 및 CDC와 같이 가장 가치가 높은 사용 사례에만 이를 사용할 수 있습니다. 다른 용도로 사용하기에는 진입 비용이 너무 높습니다.

- Datadog에 있을 때, 우리는 통합 가시성 데이터를 위해 특별히 설계된 열 형식 데이터베이스인 Husky를 구축했으며, 이 데이터베이스는 S3 위에서 바로 실행되었습니다. 이 작업을 완료했을 때, 우리는 매우 비용 효율적이고 디스크 공간이 부족하지 않으며 운영이 간단한 상태 비저장 자동 확장 데이터 레이크를 갖게 되었습니다. 거의 하룻밤 사이에 우리의 Kafka 클러스터는 갑자기 구식처럼 보였습니다.

- 데이터독의 카프카 대역폭 볼륨은 두 자릿수 GiB/s로 측정되었고, 브로커 스토리지는 PiB 단위의 NVME6로 측정되었습니다. 오픈 소스 카프카, 맞춤형 툴링, 베어 가상 머신을 사용하여 이러한 수준의 인프라를 유지하는 것은 결코 쉬운 일이 아니었습니다. 다행히도 데이터독의 책임 있는 엔지니어링 팀은 뛰어난 역량을 갖추고 있었기 때문에 이를 실현할 수 있었지만, 수년간의 투자에도 불구하고 자동화는 S3와 같은 시스템을 매우 견고하고 확장 가능하며 비용 효율적이고 탄력적으로 만드는 데 투입된 수백만 시간의 엔지니어링 시간을 따라올 수 없었습니다.

- 일반적으로 클라우드 환경에서 실행되는 대규모 스토리지 워크로드는 오브젝트 스토리지의 경제성, 안정성, 확장성, 탄력성을 따라잡을 수 없습니다. 이것이 바로 스노우플레이크나 데이터브릭스 같은 '빅데이터' 기술이 시도조차 하지 않는 이유입니다. 대신, 이들은 처음부터 상용 오브젝트 스토리지를 중심으로 시스템을 설계하여 클라우드 경제성에 의존합니다.

- Uber, Datadog, 그리고 그 밖의 많은 회사들이 이러한 결함에도 불구하고 카프카를 도입했습니다. 하지만 기존의 Kafka 구현이 진입 장벽으로 남아 있다면 결코 해결되지 않을 흥미로운 문제들이 너무 많습니다. 이것이 바로 우리가 이 분야에 관심을 기울이는 이유이며, 데이터 스트리밍 인프라를 S3만큼 접근하기 쉽게 만드는 무언가를 구축하기 시작한 이유입니다.

- S3를 기반으로 Kafka와 유사한 시스템을 직접 구축할 수 있다면, 비용이 크게 절감되고 기존의 Kafka 운영상의 골칫거리 대부분이 하룻밤 사이에 사라지는 등 Kafka의 두 가지 주요 문제를 단번에 해결할 수 있을 것입니다. 주요 클라우드 제공업체는 VM과 오브젝트 스토리지 간의 네트워킹 비용을 청구하지 않으며, AWS는 말 그대로 수백 명의 엔지니어를 고용하여 S3가 안정적으로 실행되고 무한대로 확장되도록 하는 일만 담당하고 있으므로 고객은 그럴 필요가 없습니다.

- 물론 말처럼 쉬운 일은 아니며, 아직 아무도 해내지 못한 데에는 그만한 이유가 있습니다. 로컬 디스크를 도입하지 않고도 Kafka 프로토콜의 모든 의미를 제공하면서 S3와 같이 지연 시간이 긴 스토리지 매체 위에 저지연 스트리밍 인프라를 구축하는 방법을 알아내는 것은 매우 까다로운 문제입니다!

- 그래서 저희는 스스로에게 물었습니다: "만약 오늘날 카프카가 로컬 디스크를 관리할 필요 없이 오브젝트 스토리지 바로 위에서 최신 클라우드 환경에서 실행되도록 처음부터 다시 설계되었지만 기존 카프카 프로토콜을 여전히 지원해야 한다면 어떤 모습일까요?"

워프스트림은 바로 이 질문에 대한 우리의 대답입니다.

## Introducing WarpStream

- 워프스트림은 모든 상용 개체 저장소(AWS S3, GCP GCS, Azure Blob Storage 등) 위에서 직접 실행되는 Apache Kafka® 프로토콜 호환 데이터 스트리밍 플랫폼입니다. Az 간 대역폭 비용이 전혀 들지 않으며, 관리해야 할 로컬 디스크가 없고, VPC 내에서 완전히 실행할 수 있습니다.

- 워프스트림의 아키텍처와 카프카의 아키텍처를 비교하면서 설명할 내용이 많으니 간단히 정리해 보겠습니다: https://global-uploads.webflow.com/64baaecd9c5c9b1b6c38aa0e/64cea23a28ed31049a11cfbf_with1%20(1).png

- 워프스트림에는 카프카 브로커 대신 "에이전트"가 있습니다. 에이전트는 Kafka 프로토콜을 사용하는 상태 비저장 Go 바이너리(JVM 없음!)이지만, 기존 Kafka 브로커와 달리 모든 WarpStream 에이전트는 모든 토픽의 "리더" 역할을 하거나, 모든 소비자 그룹에 대한 커밋 오프셋을 수행하거나, 클러스터의 코디네이터 역할을 할 수 있습니다. 어떤 에이전트도 특별하지 않으므로 CPU 사용량이나 네트워크 대역폭에 따라 에이전트를 자동 확장하는 것은 간단합니다.

- Apache Kafka를 사용하려면 로컬 SSD와 복제가 있는 Apache ZooKeeper(또는 KRaft)와 여러 개의 상태 저장 브로커를 실행해야 하는데 어떻게 이를 달성할 수 있었을까요?
    1. 스토리지와 컴퓨팅을 분리했습니다(데이터를 S3로 오프로드하여).
    2. 메타데이터와 데이터 분리(메타데이터를 사용자 정의 메타데이터 저장소로 오프로드하여)

- 모든 스토리지를 S3와 같은 오브젝트 스토리지로 오프로드하면 사용자는 데이터 리밸런싱 없이도 부하 변화에 따라 워프스트림 에이전트 수를 손쉽게 확장할 수 있습니다. 또한 모든 요청을 다른 에이전트에서 즉시 재시도할 수 있으므로 장애로부터 더 빠르게 복구할 수 있습니다. 또한 각 파티션의 데이터 양이 고르지 않아 일부 카프카 브로커의 부하가 다른 브로커보다 크게 높아지는 핫스팟을 대부분 제거합니다. 즉, 수동으로 파티션을 재조정할 필요가 없으며 크루즈 컨트롤과 같은 복잡한 솔루션에 대해 배울 필요가 없습니다.

- 워프스트림 설계의 다른 한 축은 최신 데이터 레이크처럼 데이터와 메타데이터를 분리하는 것입니다. 모든 워프스트림 "가상 클러스터"의 메타데이터는 처음부터 이 문제를 가장 성능과 비용 효율적인 방식으로 해결하기 위해 작성된 맞춤형 메타데이터 데이터베이스에 저장됩니다. 실제로 메타데이터 저장소의 효율성에 대한 확신을 바탕으로 워프스트림 가상 클러스터를 무료로 호스팅해 드립니다.

- 워프스트림의 아키텍처에 대한 자세한 내용은 문서에서 확인할 수 있지만, 요약하자면 다음과 같습니다: 워프스트림은 데이터 복제, 내구성, 가용성과 같은 어려운 문제를 모두 오브젝트 스토리지 버킷으로 오프로드하므로 사용자는 이에 대해 고민할 필요가 없으며, 모든 데이터는 클라우드 계정 내에 유지됩니다. 워프스트림에서 클라우드 계정을 떠나는 유일한 데이터는 파티션의 배치 순서와 같이 합의에 필요한 워크로드 메타데이터뿐입니다.

- 오늘날 인프라에 대규모 데이터 스트리밍 파이프라인을 도입하고자 하는 실무자에게는 좋은 선택지가 많지 않습니다. 많은 비용을 들여 Kafka 운영만을 담당하는 전담 엔지니어 팀을 구성하거나, 호스팅 솔루션 공급업체에 비용을 지불하고 더 많은 비용을 지출해야 하므로 많은 스트리밍 사용 사례를 경제적으로 실현할 수 없게 됩니다.

- 워프스트림은 클라우드를 약점이 아닌 강점으로 활용하는 더 나은 옵션을 제공할 수 있으며, 데이터 스트리밍 분야에서 완전히 새로운 가능성을 열어줄 수 있다고 생각합니다.

- 하지만 저희의 말만 믿으실 필요는 없습니다. 저희가 영수증을 가져왔습니다! 아래 이미지는 테스트 환경에서 실행한 연속 스트리밍 워크로드를 포함하여 전체 클라우드 계정의 영역 간 네트워킹 비용(우수한 vantage.sh를 사용하여 측정)을 보여줍니다. 이 워크로드는 140MiB/s의 데이터를 지속적으로 생성하고 3개의 전용 소비자와 함께 소비하여 총 560MiB/s의 연속 데이터 전송을 수행합니다.

- https://global-uploads.webflow.com/64baaecd9c5c9b1b6c38aa0e/64c035b364da3c257915926f_Screenshot%202023-07-25%20at%203.49.10%20PM.png

- 영역 간 네트워킹 요금이 하루 평균 $15 미만인 반면, Kafka 클러스터를 사용하여 동일한 워크로드를 실행하면 0.14GiB * $0.053/GiB * 60 * 60 * 24 == 영역 간 네트워킹 요금으로만 하루 $641이 든다는 것을 알 수 있습니다.

- 이러한 영역 간 네트워킹 비용을 하드웨어나 S3 API 비용으로만 대체한 것이 아닙니다. 동일한 워크로드에 대한 S3 API 운영 비용은 하루 40달러 미만입니다: https://global-uploads.webflow.com/64baaecd9c5c9b1b6c38aa0e/64c035bcfda4aa35de9d76ef_Screenshot%202023-07-25%20at%203.50.11%20PM.png

- 또한 에이전트 하드웨어/가상머신에 27개의 vCPU만 필요합니다.

- 총 소유 비용 측면에서 보면, 워프스트림은 대부분의 카프카 워크로드 비용을 5~10배까지 절감할 수 있습니다. 예를 들어, 다음은 1GiB/s의 지속적인 카프카 워크로드 실행 비용과 워프스트림 사용 시 동등한 워크로드 실행 비용을 비교한 것입니다: https://global-uploads.webflow.com/64baaecd9c5c9b1b6c38aa0e/64d060d06b645b27d6a23140_Screenshot%202023-08-06%20at%2010.10.56%20PM.png

    - 각주 7은 자체 호스팅된 Kafka 하드웨어 비용, 각주 8은 자체 호스팅된 Kafka 네트워크 비용입니다. 이 표는 소비자의 영역 간 네트워킹 비용을 줄이기 위해 팔로워 가져오기 기능을 사용하도록 Kafka 클러스터가 올바르게 구성된 최상의 시나리오를 가정한 것입니다. 그렇지 않은 경우, 카프카 비용은 훨씬 더 높아질 것입니다. 또한 자체 호스팅 Kafka 설정에 대한 엔지니어링 급여 비용도 생략됩니다.

- 위의 표는 대용량 Kafka 워크로드의 경우 워크로드 비용이 영역 간 네트워킹 비용에 의해 지배되기 때문에 하드웨어 비용이 무시할 수 있는 수준임을 명확하게 보여줍니다. 워프스트림은 이러한 네트워킹 비용을 완전히 제거합니다.

- 물론 모든 것이 햇살과 무지개만 있는 것은 아닙니다. 엔지니어링은 장단점을 고려해야 하는데, 워프스트림은 지연 시간이라는 중요한 문제를 해결했습니다. 현재 구현에서는 데이터가 S3에서 내구성 있게 유지되고 클라우드 컨트롤 플레인에 커밋되기 전까지는 데이터를 인식하지 않기 때문에 Produce 요청에 대해 약 400ms의 P99를 제공합니다. 또한, 현재 생산자에서 소비자에 이르는 엔드투엔드 데이터의 P99 지연 시간은 약 1초입니다: https://global-uploads.webflow.com/64baaecd9c5c9b1b6c38aa0e/64bff6c3e52acac923301fa7_CaSz12FWNfCOGHT2snOa6q1erJeqvhESfRx_X6ZHt-Fe81JVVgRlXk9wvSamfMnzG5Epjwl5VARA176g8k-kmAGiTancoQOoBT1iDZJgjKXceXv-XFKsnEn2ncDGM4rjeCja_JriSlDDn7LQ9B8vh5o.png

- 워크로드가 ~1초의 생산자-소비자 간 지연 시간을 견딜 수 있다면, 워프스트림은 운영 오버헤드가 거의 없는 상태에서 총 데이터 스트리밍 비용을 GiB당 5~10배까지 절감할 수 있습니다. 또한 독점적인 인터페이스가 아니라 Kafka만을 사용하므로 공급업체에 종속되지 않습니다. 마지막으로, 워프스트림은 오브젝트 저장소가 구현된 모든 환경에서 실행되므로 AWS의 S3, GCP의 GCS, Azure의 Azure Blob Storage 등 어느 환경에서든 사용하실 수 있습니다.

- 여기까지 읽어보셨다면, 워프스트림이 주로 클라우드 경제성과 운영 오버헤드라는 카프카의 두 가지 주요 문제를 해결한다는 것을 눈치채셨을 것입니다. 저희는 카프카의 세 번째 주요 문제인 개발자 UX가 있다고 생각합니다. 우리가 보기에 파티션은 사소하지 않은 스트림 처리 애플리케이션을 작성하기에는 너무 낮은 수준의 추상화이며, 워프스트림의 아키텍처는 개발자가 기존 애플리케이션을 작성하는 데 익숙한 방식에 훨씬 더 가까운 새로운 방식으로 스트림 처리 애플리케이션을 작성할 수 있도록 지원하는 독보적인 위치에 있다고 생각합니다.

- 이에 대해서는 향후 블로그 게시물에서 자세히 설명할 예정이지만, 우선은 개발자들이 있는 곳에서 개발자들을 만나 그들이 이미 익숙한 도구의 개선된 버전을 제공하는 것이 우선이었습니다.


