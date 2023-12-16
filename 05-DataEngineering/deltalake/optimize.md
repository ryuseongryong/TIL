- https://docs.databricks.com/en/delta/tune-file-size.html
# Configure Delta Lake to control data file size

델타 레이크는 write 및 optimize 작업을 위한 대상 파일 크기를 수동 또는 자동으로 구성할 수 있는 옵션을 제공합니다. 데이터브릭스는 이러한 설정 중 상당수를 자동으로 조정하고, 파일 크기를 적절히 조정하여 테이블 성능을 자동으로 개선하는 기능을 지원합니다.
---
note
Databricks 런타임 13.3 이상에서는 델타 테이블 레이아웃에 클러스터링을 사용할 것을 권장합니다. 델타 테이블에 리퀴드 클러스터링 사용을 참조하십시오.

예측 최적화를 사용하여 델타 테이블에 대한 최적화 및 비우기를 자동으로 실행할 것을 권장합니다. 델타 레이크에 대한 예측 최적화를 참조하세요.

Databricks 런타임 10.4 LTS 이상에서는 자동 압축 및 최적화된 쓰기가 MERGE, UPDATE 및 DELETE 작업에 대해 항상 활성화됩니다. 이 기능은 비활성화할 수 없습니다.

달리 명시되지 않는 한, 이 문서의 모든 권장 사항은 최신 런타임을 실행하는 Unity 카탈로그 관리 테이블에는 적용되지 않습니다.
---
Unity 카탈로그 관리 테이블의 경우 SQL 웨어하우스 또는 Databricks Runtime 11.3 LTS 이상을 사용하는 경우 Databricks가 대부분의 구성을 자동으로 조정합니다.

Databricks Runtime 11.0 이하에서 워크로드를 업그레이드하는 경우 백그라운드 자동 압축으로 업그레이드를 참조하세요.

## When to run OPTIMIZE
자동 압축과 최적화된 쓰기는 각각 작은 파일 문제를 줄여주지만, OPTIMIZE를 완전히 대체하지는 못합니다. 
특히 1TB보다 큰 테이블의 경우, Databricks는 파일을 더욱 통합하기 위해 일정에 따라 OPTIMIZE를 실행할 것을 권장합니다. 
Databricks는 테이블에서 ZORDER를 자동으로 실행하지 않으므로 향상된 데이터 건너뛰기 기능을 사용하려면 ZORDER와 함께 OPTIMIZE를 실행해야 합니다. 
델타 레이크의 경우 Z 순서 인덱스를 사용한 데이터 건너뛰기를 참조하십시오.

## What is auto optimize on Databricks?
자동 최적화라는 용어는 delta.autoOptimize.autoCompact 및 delta.autoOptimize.optimizeWrite 설정에 의해 제어되는 기능을 설명할 때 사용되기도 합니다. 
각 설정을 개별적으로 설명하기 위해 이 용어는 폐기되었습니다. 
데이터브릭의 델타 레이크에 대한 자동 압축 및 데이터브릭의 델타 레이크에 대한 최적화된 쓰기를 참조하세요.

## Auto compaction for Delta Lake on Databricks
자동 압축은 델타 테이블 파티션 내의 작은 파일을 결합하여 작은 파일 문제를 자동으로 줄여줍니다. 
자동 압축은 테이블에 대한 쓰기가 성공한 후에 발생하며 쓰기를 수행한 클러스터에서 동기적으로 실행됩니다. 
자동 압축은 이전에 압축되지 않은 파일만 압축합니다.

Spark 구성 spark.databricks.delta.autoCompact.maxFileSize를 설정하여 출력 파일 크기를 제어할 수 있습니다. 
데이터브릭스는 워크로드 또는 테이블 크기에 따라 자동 조정을 사용할 것을 권장합니다. 
워크로드에 따라 파일 크기 자동 조정 및 테이블 크기에 따라 파일 크기 자동 조정을 참조하세요.

자동 압축은 특정 개수 이상의 작은 파일이 있는 파티션 또는 테이블에 대해서만 트리거됩니다. 
선택적으로 spark.databricks.delta.autoCompact.minNumFiles를 설정하여 자동 압축을 트리거하는 데 필요한 최소 파일 수를 변경할 수 있습니다.

다음 설정을 사용하여 테이블 또는 세션 수준에서 자동 압축을 활성화할 수 있습니다:
- Table property: delta.autoOptimize.autoCompact
- SparkSession setting: spark.databricks.delta.autoCompact.enabled

auto (recommended): 다른 자동 튜닝 기능을 존중하면서 목표 파일 크기를 조정합니다. 데이터브릭스 런타임 10.1 이상이 필요합니다.
legacy: true의 별칭입니다. 데이터브릭스 런타임 10.1 이상이 필요합니다.
true: 대상 파일 크기로 128MB를 사용합니다. 동적 크기 조정은 사용하지 않습니다.
false: 자동 압축을 끕니다. 세션 수준에서 설정하여 워크로드에서 수정된 모든 델타 테이블에 대한 자동 압축을 재정의할 수 있습니다.

---
Important!
Databricks Runtime 10.3 이하에서는 다른 작성자가 DELETE, MERGE, UPDATE 또는 OPTIMIZE와 같은 작업을 동시에 수행할 때 자동 압축으로 인해 트랜잭션 충돌로 인해 다른 작업이 실패할 수 있습니다. 
이는 데이터브릭스 런타임 10.4 이상에서는 문제가 되지 않습니다.
---

# Optimized writes for Delta Lake on Databricks
최적화된 쓰기는 데이터가 기록될 때 파일 크기를 개선하고 테이블의 후속 읽기 작업에도 도움이 됩니다.

최적화된 쓰기는 각 파티션에 쓰여지는 작은 파일 수를 줄이므로 파티션이 분할된 테이블에 가장 효과적입니다. 
큰 파일을 적게 쓰는 것이 작은 파일을 많이 쓰는 것보다 더 효율적이지만, 쓰기 전에 데이터가 섞이기 때문에 쓰기 지연 시간이 늘어날 수 있습니다.

다음 이미지는 최적화된 쓰기가 어떻게 작동하는지 보여줍니다: https://docs.databricks.com/en/_images/optimized-writes.png
---
note
데이터를 쓰기 직전에 coalesce(n) 또는 repartition(n)을 실행하여 작성되는 파일 수를 제어하는 코드가 있을 수 있습니다. 
최적화된 쓰기를 사용하면 이 패턴을 사용할 필요가 없습니다.
---

데이터브릭스 런타임 9.1 LTS 이상에서는 다음 작업에 대해 최적화된 쓰기가 기본적으로 활성화되어 있습니다:
- MERGE
- UPDATE with subqueries
- DELETE with subqueries

SQL 웨어하우스를 사용할 때 CTAS 문과 INSERT 연산에 대해서도 최적화된 쓰기가 활성화됩니다. 
데이터브릭스 런타임 13.1 이상에서는 Unity 카탈로그에 등록된 모든 델타 테이블에 대해 파티셔닝된 테이블에 대한 CTAS 문과 INSERT 작업에 대해 최적화된 쓰기가 활성화됩니다.

테이블 또는 세션 수준에서 다음 설정을 사용하여 최적화된 쓰기를 활성화할 수 있습니다:
- Table setting: delta.autoOptimize.optimizeWrite
- SparkSession setting: spark.databricks.delta.optimizeWrite.enabled

이 설정에서는 다음 옵션을 사용할 수 있습니다:
- true: 대상 파일 크기로 128MB를 사용합니다.
- false: 최적화된 쓰기를 끕니다. 세션 수준에서 설정하여 워크로드에서 수정된 모든 델타 테이블에 대한 자동 압축을 재정의할 수 있습니다.

## Set a target file size
델타 테이블의 파일 크기를 조정하려면 테이블 속성 delta.targetFileSize를 원하는 크기로 설정하세요. 
이 속성을 설정하면 모든 데이터 레이아웃 최적화 작업에서 지정된 크기의 파일을 생성하기 위해 최선을 다합니다. 
여기에는 최적화 또는 Z 정렬, 자동 압축, 최적화된 쓰기 등의 예가 있습니다.

기존 테이블의 경우 SQL 명령 ALTER TABLE SET TBL PROPERTIES를 사용하여 속성을 설정하거나 설정 해제할 수 있습니다. 
Spark 세션 구성을 사용하여 새 테이블을 만들 때 이러한 속성을 자동으로 설정할 수도 있습니다. 
자세한 내용은 델타 테이블 속성 참조를 참조하세요.

