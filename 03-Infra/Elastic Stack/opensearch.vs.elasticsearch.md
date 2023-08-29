# OpenSearch vs Elasticsearch : which one is better to use?
- https://sematext.com/blog/opensearch-vs-elasticsearch-which-one-is-better-sematext/

## Feature : 어떤 엔진이 작업을 더 잘 수행하는지?
- 두 엔진 모두 수많은 기능을 제공하므로 공통, 경쟁력 및 다양한 기능으로 분류할 수 있다.
- 공통 기능은 문서 색인 및 병합부터 유사도 및 필터 캐시에 이르기까지 모든 것이 Elasticsearch와 Opensearch 모두에 열려있다. 앞으로도 계속 제공될 가능성이 높다. 둘 다 최신 버전의 Lucene으로 업그레이드할 때 동일한 개선 사항, 버그 수정 및 장단점을 상속받게 된다.
  Lucene 외에도 Opensearch의 원래 기반이 된 Elasticsearch 7.10.2에서 제공되는 공통 기능도 있다. 그러나 이 두 엔진은 개별적으로 진화할 것이므로, 이 코드의 점점 더 많은 부분이 병렬적으로 진화하는 것으로 대체될 것이다.
- 경쟁되는 기능으로 인해 Opensearch 포크가 시작되었다. 인증 및 권한 부여, 인덱스 관리, 알림 등과 같은 기능은 전통적으로 Elasticsearch의 독점적인 것이었기 때문에 Opensearch는 오픈 소스 대안을 구현했다. 예를 들어 Elasticsearch에는 인덱스 수명 주기 관리가 있는 반면, Opensearch에는 인덱스 상태 관리가 있다. 대체로 동일한 작업을 수행하지만 세부적인 차이점이 있다. 이러한 세부 사항은 자주 변경되므로 관심 있는 특정 기능의 현재 상태를 확인하는 것이 좋다. 예를 들어 이 글을 쓰는 시점에 검색 가능한 스냅샷은 Elasticsearch에서 오랫동안 사용되어 왔지만 Opensearch에서는 약간 알파 버전처럼 보인다. 그러나 Elasticsearch의 모든 기능이 무료인 것은 아니다. 즉 기본 라이선스가 적용된다. 예를 들어, 인덱스 수명 주기 관리는 무료이지만 클러스터 간 복제는 그렇지 않다. 
- 마지막으로 Elasticsearch와 Opensearch는 모두 서로가 복제하지 않는 기능을 제공한다. 예를 들어 Elasticsearh에는 시계열 데이터 스트림이 있는 반면 OpenSearch에는 세그먼트 복제가 (재)도입되었다. 아직까지 큰 변화는 없지만, 두 프로젝트가 계속 발전함에 따라 점점 더 많은 기능을 기대할 수 있다. 일반적인 느낌은 로그(및 기타 시계열) 사용 사례에 대해 Elasticsearch가 더 강하게 밀어붙이는 경향이 있다는 것이다. 한편, OpenSearch는 여전히 그렇게 하고 있지만, Elasticsearch에 대응하는 많은 것들(머신러닝 등)이 무료가 아니기 때문에 엔터프라이즈 검색 사용 사례에 더 많은 기여를 하게 될 가능성이 높다.

## Community : 향후 버전은 어떻게 되는지?

처음에는 Elasticsearch에 더 많은 커밋과 기여자가 있는 것처럼 보입니다:

포크 전 커밋을 "상속"한 OpenSearch와 비교하면, 2021년 포크 이후 기여 수가 감소했다가 지금은 서서히 증가하는 것을 볼 수 있습니다:

그러나 Elasticsearch의 GitHub 리포지토리에는 X-Pack(SQL 또는 머신 러닝과 같은 모든 플러그인 포함)이 포함되어 있는 반면 OpenSearch의 경우 별도의 리포지토리이기 때문에 사과와 사과를 비교하는 것은 아닙니다.

마찬가지로 포럼 게시물 수도 비교하기가 어렵습니다: Elastic은 ELK와 관련된 모든 것에 대해 하나의 카테고리를 가지고 있는 반면, OpenSearch는 예를 들어 OpenSearch와 OpenSearch 대시보드(Kibana의 포크)에 대해 서로 다른 카테고리를 가지고 있습니다. 숫자를 더하면 Elastic이 약 5배 더 높습니다. 여전히 100% 정확한 비교는 아니지만 그 차이는 충분히 분명합니다.

Google 트렌드에 따르면 지난 1년 동안 Elasticsearch에 대한 관심은 서서히 감소하고 있는 반면 OpenSearch에 대한 관심은 서서히 증가하고 있는 것으로 나타났습니다. 따라서 앞으로 모든 절대적인 수치가 더 가까워질 수도 있습니다:

Elasticsearch와 OpenSearch 모두 활발한 커뮤니티가 있기 때문에 어느 한 쪽이 곧 사라지거나 지원이 제대로 이루어지지 않을 것이라고는 걱정하지 않습니다. 다만, OpenSearch 사용자라면 작동 방식을 이해하기 위해 (더 완전한) Elasticsearch 문서와 더 다양한 토론을 참조할 가능성이 높습니다. 적어도 단기적으로는요.

## License and governance : 현재와 미래에도 사용할 수 있는지?
OpenSearch는 Apache 라이선스이기 때문에 원하는 대로 거의 자유롭게 사용할 수 있습니다. 반면에 Elasticsearch는 대부분 Elastic License에 기반하고 있으며, 이는 다른 사람에게 서비스로서 그 기능의 상당 부분을 제공할 수 없음을 의미합니다.

거버넌스 측면에서 보면, 코드를 보고 OpenSearch와 Elasticsearch 모두에 거의 동일한 방식으로 기여할 수 있습니다. OpenSearch는 AWS에서 관리하며, Elasticsearch는 Elastic에서 관리합니다. 그러나 라이선스 차이로 인해 외부 기여자에게는 OpenSearch가 더 매력적으로 다가갈 수 있습니다.

전자상거래 웹사이트의 경우처럼 검색 엔진의 기능이 외부에 노출되지 않는 경우에는 아무 문제가 없습니다. 회사에서 어떤 라이선스를 사용할 수 있는지에 대한 정책을 가지고 있지 않는 한, OpenSearch의 Apache 라이선스는 승인을 받을 가능성이 높지만 Elasticsearch의 Elastic 라이선스에는 해당되지 않을 수 있습니다.

전자 상거래 사이트 검색을 위한 SaaS와 같이 중요한 방식으로 검색을 다루는 SaaS를 구축하려는 경우, OpenSearch가 더 안전한 선택입니다(물론 변호사가 더 잘 알 것입니다).

마지막으로, 개방형 거버넌스가 중요하다면 Apache Solr를 살펴보세요. 이미 Elasticsearch 대 Solr에 대한 게시물과 OpenSearch 대 Solr에 대한 게시물이 있습니다.

## Ethics and principles

지금까지 저는 두 가지 극단적인 이야기를 보았습니다. 하나는 Amazon은 악하고 Elasticsearch 상표를 남용한 반면, Elastic은 선하고 오픈 소스 커뮤니티를 옹호하여 AWS가 실제로 제공되는 소프트웨어를 유지 관리하도록 했다는 것입니다. 다른 하나는 Elastic은 사악하며 사용자와 기여자 모두의 신뢰를 악용하는 반면, AWS는 Elasticsearch를 포크하고 Elastic이 제공하지 못한 부분을 계속 제공함으로써 하루를 구했다는 것입니다.

좀 더 미묘한 관점은 두 회사 모두 커뮤니티에 기여하는 좋은 의도를 가지고 있었고 지금도 가지고 있으며, 때로는 많은 사람들의 견해와 상충되는 자체적인 이익도 가지고 있다는 것입니다. 다음은 여러분 스스로 판단할 수 있도록 간략한 타임라인입니다:

2010: Shay Banon이 작성한 Elasticsearch가 출시되고 Apache 라이선스가 부여되었습니다.
2012: 서비스(지원, 교육, 컨설팅)를 제공할 뿐만 아니라 Elasticsearch의 개발을 지속하고 관리하는 회사가 설립되었으며, 곧 Logstash와 Kibana가 합류(ELK 설립)했습니다.
2014: Elastic(당시 Elasticsearch)은 상업용 애드온(예: 모니터링용)을 출시하기 시작했고, 나중에 X-Pack이라는 패키지로 결합되었으며, Elasticsearch의 핵심은 영원히 Apache 라이선스로 유지될 것이라고 밝혔습니다.
2015: AWS가 Elasticsearch SaaS를 출시했습니다: Amazon Elasticsearch Service. 그 후 Elastic은 AWS를 상표권 침해로 고소했습니다. 2021년에 OpenSearch가 출시되면서, Amazon Elasticsearch Service는 Amazon OpenSearch Service로 이름이 변경되었습니다.
2018: Elastic은 오픈 소스는 아니지만 무료에서 플래티넘까지 다양한 라이선스를 기반으로 기능을 사용할 수 있는 X-Pack 코드를 공개했습니다. Elasticsearch의 기본 배포판은 Elastic 라이선스가 적용되었지만, X-Pack 없이도 Apache 라이선스 Elasticsearch를 계속 다운로드할 수 있었습니다.
2019: AWS는 보안과 같은 기능을 제공하는 오픈 소스 도구 모음으로, X-Pack이 제공하던 것과 거의 겹치는 Open Distro for Elasticsearch를 출시했습니다. 이제 Elasticsearch용 Open Distro는 더 이상 사용되지 않으며 OpenSearch로 대체됩니다.
2021: Elastic이 새 버전의 Elasticsearch에 대한 라이선스를 변경합니다. 이전에는 Apache 라이선스였던 코어는 이제 SSPL로 별도로 컴파일할 수 있으며, 기본 배포는 이전과 마찬가지로 Elastic License로 유지됩니다. 이로써 7.10.2는 Apache 라이선스가 부여된 마지막 Elasticsearch 버전이 됩니다.
2021: AWS에서 Elasticsearch 7.10.2의 포크인 OpenSearch를 출시합니다.
2021: AWS가 Amazon Elasticsearch Service의 이름을 Amazon OpenSearch Service로 변경하고, 이제 OpenSearch와 UltraWarm과 같은 추가적인 독점 기능을 제공합니다.
