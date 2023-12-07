- https://opensearch.org/docs/latest/tools/index/

이 섹션에서는 다음과 같은 OpenSearch 지원 도구에 대한 설명서를 제공합니다:

- 에이전트 및 수집 도구
- OpenSearch CLI
- OpenSearch Kubernetes 운영자
- OpenSearch 업그레이드, 마이그레이션 및 비교 도구
다운스트림 분석 및 시각화를 위해 데이터를 필터링, 보강, 변환, 정규화 및 집계하기 위한 서버 측 데이터 수집기인 Data Prepper에 대한 자세한 내용은 Data Prepper를 참조하세요.

역사적으로, 많은 인기 있는 여러 에이전트와 수집 도구들이 Beats, Logstash, Fluentd, FluentBit, OpenTelemetry와 같은 Elasticsearch OSS와 함께 작동해 왔습니다. OpenSearch는 광범위한 에이전트와 수집 도구 세트를 계속 지원하는 것을 목표로 하고 있지만, 모든 에이전트와 수집 도구가 테스트를 거쳤거나 OpenSearch 호환성을 명시적으로 추가한 것은 아닙니다.

중간 단계의 호환성 솔루션으로, 클러스터가 실제 버전이 아닌 버전 7.10.2를 반환하도록 지시하는 설정이 OpenSearch에 있습니다.

버전 확인 기능이 포함된 클라이언트를 사용하는 경우(예: 7.x - 7.12.x 사이의 Logstash OSS 또는 Filebeat OSS 버전), 이 설정을 활성화하세요:

```
PUT _cluster/settings
{
  "persistent": {
    "compatibility": {
      "override_main_response_version": true
    }
  }
}

# in opensearch.yml
compatibility.override_main_response_version: true
```

Logstash OSS 8.0은 모든 플러그인이 기본적으로 ECS 호환성 모드에서 실행되는 획기적인 변화를 도입했습니다. 호환되는 OSS 클라이언트를 사용하는 경우, 기존 동작을 유지하려면 기본값을 재정의해야 합니다:
```
ecs_compatibility => disabled
```

OpenSearch 다운로드에서 Logstash용 OpenSearch 출력 플러그인을 다운로드할 수 있습니다. Logstash 출력 플러그인은 OpenSearch 및 Elasticsearch OSS(7.10.2 이하)와 호환됩니다.

이 버전들은 OpenSearch 호환성을 갖춘 최신 버전의 Beats OSS입니다. 자세한 내용은 아래의 호환성 매트릭스 섹션을 참조하세요.

7.12.x보다 최신 버전의 Beats는 OpenSearch에서 지원되지 않습니다. 사용 중인 환경의 Beats 에이전트를 최신 버전으로 업데이트해야 하는 경우, Beats에서 Logstash로 트래픽을 리디렉션하고 Logstash 출력 플러그인을 사용해 데이터를 OpenSearch로 수집함으로써 비호환성을 해결할 수 있습니다.

OpenSearch CLI
OpenSearch CLI 명령줄 인터페이스(opensearch-cli)를 사용하면 명령줄에서 OpenSearch 클러스터를 관리하고 작업을 자동화할 수 있습니다. OpenSearch CLI에 대한 자세한 내용은 OpenSearch CLI를 참조하세요.

오픈서치 쿠버네티스 운영자
OpenSearch Kubernetes Operator는 컨테이너화된 환경에서 OpenSearch 및 OpenSearch 대시보드의 배포 및 프로비저닝을 자동화하는 데 도움이 되는 오픈 소스 Kubernetes 운영자입니다. 오퍼레이터 사용 방법에 대한 자세한 내용은 OpenSearch Kubernetes 오퍼레이터를 참조하세요.

OpenSearch 업그레이드, 마이그레이션 및 비교 도구
OpenSearch 마이그레이션 도구는 OpenSearch로의 마이그레이션과 최신 버전의 OpenSearch로의 업그레이드를 용이하게 해줍니다. 이러한 도구를 사용하면 Docker 컨테이너를 사용해 로컬에서 개념 증명 환경을 설정하거나 원클릭 배포 스크립트를 사용해 AWS에 배포할 수 있습니다. 이를 통해 마이그레이션 전에 클러스터 구성을 미세 조정하고 워크로드를 보다 효과적으로 관리할 수 있습니다.

OpenSearch 마이그레이션 도구에 대한 자세한 내용은 OpenSearch 마이그레이션 GitHub 리포지토리에 있는 설명서를 참조하세요.

