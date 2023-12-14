- https://medium.com/@squarecog/logging-101-d74ff92f8c91

로깅은 처음에는 사소해 보이지만 금방 복잡해지고 미묘한 차이가 생기는 주제 중 하나입니다. 사람들은 로깅 프레임워크를 만들고, 모범 사례에 대해 논쟁하고, 로깅 규칙을 문서화합니다... 여기에는 신입 소프트웨어 엔지니어에게 놀랄 만한 것들이 많이 있습니다. 이 글에서는 주요 개념에 대한 기본적인 이해와 모범 사례로 간주되는 내용을 통해 시작하기 위한 기초를 다질 수 있습니다.

이 글은 크리스 리코미니와 공동 집필한 '누락된 README(https://themissingreadme.com/)'라는 책에서 발췌한 것입니다: 새내기 소프트웨어 엔지니어를 위한 가이드입니다. Amazon에서 구입할 수 있습니다.

터미널에 "Hello, World!"를 처음 썼을 때, 로깅을 하고 있었습니다. 로그 메시지를 인쇄하는 것은 코드를 이해하거나 작은 프로그램을 디버깅할 때 간단하고 편리합니다. 복잡한 애플리케이션의 경우, 언어에는 정교한 로깅 라이브러리가 있어 운영자가 로깅 대상과 시기를 더 잘 제어할 수 있습니다. 운영자는 로깅 수준을 통해 로그 양을 조절하고 로그 형식을 제어할 수 있습니다. 프레임워크는 디버깅할 때 사용할 수 있는 스레드 이름, 호스트 이름, ID와 같은 컨텍스트 정보도 삽입합니다. 로깅 프레임워크는 운영자가 로그 메시지를 집계하여 필터링하고 검색할 수 있도록 하는 로그 관리 시스템과 잘 작동합니다.

로깅 프레임워크를 사용하면 코드를 더 쉽게 작동하고 디버깅할 수 있습니다. 운영자가 애플리케이션의 로그 볼륨을 제어할 수 있도록 로그 수준을 설정하세요. 로그를 원자적이고, 빠르고, 안전하게 유지하세요.

## Use Log Levels
로깅 프레임워크에는 운영자가 중요도에 따라 메시지를 필터링할 수 있는 로그 수준이 있습니다. 운영자가 로그 수준을 설정하면 해당 수준 이상의 모든 로그가 방출되고, 그보다 낮은 수준의 메시지는 무음 처리됩니다. 수준은 일반적으로 전역 설정과 패키지 또는 클래스 수준 오버라이드를 통해 제어됩니다. 운영자는 로그 수준을 통해 매우 상세한 디버깅 로그부터 일반 작업의 일정한 백그라운드 윙윙거리는 소리까지 주어진 상황에 맞게 로그 볼륨을 조정할 수 있습니다.

예를 들어, 다음은 오류 수준의 루트 상세도를 정의하는 Java log4j.properties 스니펫과 com.foo.bar 패키지 공간에서 발생하는 로그에 대한 패키지별 INFO 수준의 상세도를 정의하는 스니펫을 예로 들 수 있습니다:

```
# set root logger to ERROR level for fout FileAppender
log4j.rootLogger=ERROR,fout
# set com.foo.bar to INFO level
log4j.logger.com.foo.bar=INFO
```

로그 수준을 유용하게 사용하려면 각 로그 메시지에 대해 적절한 중요도를 사용해야 합니다. 로그 수준이 완전히 표준화된 것은 아니지만 다음과 같은 수준이 일반적입니다:

### TRACE
이는 특정 패키지나 클래스에 대해서만 켜지는 매우 세밀한 수준의 디테일입니다. 개발 외에는 거의 사용되지 않습니다. 라인별 로그나 데이터 구조 덤프가 필요한 경우 이 수준이 적합합니다. TRACE를 자주 사용한다면 디버거를 사용하여 코드를 단계별로 살펴보는 것이 좋습니다.

### DEBUG
이는 프로덕션 문제 발생 시에는 메시지가 유용하지만 정상 운영 시에는 유용하지 않을 때 사용합니다. 디버깅할 때 출력을 사용할 수 없을 정도로 디버그 수준 로깅을 많이 사용하지 마시고, TRACE를 위해 저장하세요.

### INFO
이는 애플리케이션 상태에 대한 유용한 정보이지만 문제가 있음을 나타내는 것은 아닙니다. "서비스 시작" 및 "포트 5050에서 수신 대기 중"과 같은 애플리케이션 상태 메시지는 여기로 이동합니다. INFO가 기본 로그 수준입니다. "만일의 경우를 대비한" 로깅은 TRACE 또는 DEBUG로 이동하므로 INFO로 무분별하게 로그를 내보내지 마세요. INFO 로깅은 정상적인 작업 중에 유용한 정보를 알려주어야 합니다.

### WARN
잠재적으로 문제가 될 수 있는 상황에 대한 메시지입니다. 리소스가 용량에 가까워지면 경고가 필요합니다. 경고를 기록할 때마다 메시지를 받는 사람이 취해야 할 구체적인 조치가 있어야 합니다. 경고가 실행 가능한 것이 아니라면 정보에 기록하세요.

### ERROR
주의가 필요한 오류가 발생하고 있습니다. 쓰기 불가능한 데이터베이스에는 오류 로그가 필요합니다. 오류 로그는 문제를 진단할 수 있을 만큼 상세해야 합니다. 관련 stack tarces 및 소프트웨어가 수행한 결과 작업을 포함하여 명시적인 세부 사항을 기록하세요.

### FATAL
이것이 바로 '마지막 헐떡임' 로그 메시지입니다. 프로그램이 즉시 종료되어야 할 정도로 심각한 상태가 발생하면 문제의 원인에 대한 메시지를 치명적인 수준으로 기록할 수 있습니다. 프로그램 상태에 대한 관련 컨텍스트를 포함하며, 복구 또는 진단 관련 데이터의 위치가 기록되어야 합니다.

다음은 Rust에서 생성된 INFO-level log입니다:
info!("Failed request: {}, retrying", e);

로그 줄에는 요청 실패의 원인이 되는 오류가 포함됩니다. INFO 수준은 애플리케이션이 자동으로 재시도하기 때문에 사용되며 운영자의 조치가 필요하지 않습니다.

## Keep Logs Atomic
정보가 다른 데이터와 결합되었을 때만 유용하다면 하나의 메시지에 모든 정보를 원자 단위로 기록하세요. 모든 관련 정보가 한 줄에 들어 있는 원자 로그는 로그 수집기와 함께 사용하면 더 효과적입니다. 로그가 특정 순서로 표시될 것이라고 가정하지 마세요. 많은 운영 도구가 메시지 순서를 바꾸거나 삭제하기도 합니다. 시스템 시계 타임스탬프에 의존하여 순서를 정하지 마세요. 시스템 시계는 재설정되거나 호스트 간에 변동될 수 있습니다. 로그 메시지에서 줄 바꿈은 피하세요. 많은 로그 수집기는 각각의 새 줄을 별도의 메시지로 취급합니다. stack tarces은 인쇄할 때 종종 줄 바꿈이 포함되므로 단일 메시지에 기록되도록 하세요.

다음은 비원자 로그 메시지의 예입니다:

```
2020–03–19 12:18:32,320 - appLog - WARNING - Request failed with:
2020–03–19 12:18:32,348 - appLog - INFO - User login: 986
Unable to read from pipe.
2020–03–19 12:18:32,485 - appLog - INFO - User logout: 986
```

WARNING 로그 메시지에 줄 바꿈이 있어 읽기 어렵습니다. WARNING의 후속 줄에는 타임스탬프가 없으며 다른 스레드에서 오는 다른 INFO 메시지와 섞여 있습니다. WARNING는 한 줄로 원자 단위로 작성되어야 합니다.

원자 단위로 출력할 수 없는 로그 메시지의 경우 나중에 서로 연결할 수 있도록 메시지에 고유 ID를 포함하세요.

## Keep Logs Fast
과도한 로깅은 성능을 저하시킵니다. 로그는 디스크, 콘솔 또는 원격 시스템 등 어딘가에 기록해야 합니다. 문자열은 기록하기 전에 연결하고 형식을 지정해야 합니다. 빠른 로깅을 유지하려면 매개변수화된 로깅과 비동기식 appenders를 사용하세요.

문자열 연결은 속도가 느리고 성능에 민감한 루프에서 치명적일 수 있습니다. 연결된 문자열이 로그 메서드에 전달되면 인수가 메서드에 전달되기 전에 평가되기 때문에 상세도 수준에 관계없이 연결이 이루어집니다. 로그 프레임워크는 실제로 필요할 때까지 문자열 연결을 지연시키는 메커니즘을 제공합니다. 일부 프레임워크는 로그 줄을 호출하지 않으면 평가되지 않는 클로저에 로그 메시지를 강제로 넣는 반면, 다른 프레임워크는 매개변수화된 메시지를 지원합니다.

예를 들어 Python에는 로그 호출에서 문자열을 연결하는 세 가지 방법이 있으며, 그 중 두 가지 방법은 추적 메서드를 호출하기 전에 문자열 매개 변수를 연결합니다.

```
while(messages.size() > 0) {
  Message m = message.poll()
  
  // This string is concatenated even when trace is disabled!
  log.trace("got message: " + m);
  // This string is also concatenated when trace is disabled.
  log.trace("got message: {}".format(m));
  // This string is only concatenated when trace is enabled. It’s faster.
  log.trace("got message: {}", m);
}
```

최종 호출은 로그 행이 실제로 기록된 경우에만 평가되는 매개변수화된 문자열을 사용합니다.

추가 기능을 사용하여 성능에 미치는 영향을 관리할 수도 있습니다. appenders는 로그를 콘솔, 파일 또는 원격 로그 애그리게이터 등 다양한 위치로 라우팅합니다. 기본 로그 appenders는 일반적으로 인쇄 호출과 같은 방식으로 호출자의 스레드에서 작동합니다. 비동기 appenders는 실행 스레드를 차단하지 않고 로그 메시지를 작성합니다. 애플리케이션 코드가 로그가 작성될 때까지 기다릴 필요가 없으므로 성능이 향상됩니다. 일괄 추가기는 디스크에 쓰기 전에 로그 메시지를 인메모리에 버퍼링하므로 쓰기 처리량이 향상됩니다. 운영 체제의 페이지 캐시도 버퍼 역할을 함으로써 로그 처리량을 지원합니다. 비동기 및 일괄 쓰기는 성능을 향상시키지만, 모든 로그가 디스크에 플러시되는 것은 아니므로 애플리케이션이 충돌할 경우 로그 메시지가 손실될 수 있습니다.

로그 상세도 및 구성을 변경하면 애플리케이션 속도가 느려지므로 경쟁 조건 및 버그가 제거될 수 있습니다. 문제를 디버깅하기 위해 자세한 로깅을 사용하도록 설정했는데 버그를 발견하지 못하면 로깅 변경 자체가 원인일 수 있습니다.

### Don’t Log Sensitive Data
민감한 데이터를 다룰 때는 주의하세요. 로그 메시지에는 비밀번호, 보안 토큰, 신용카드 번호, 이메일 등의 개인 데이터가 포함되어서는 안 됩니다. 이는 당연한 것처럼 보이지만 잘못 생각하기 쉬운데, 단순히 URL이나 HTTP 응답을 로깅하는 것만으로도 로그 수집기가 보호하도록 설정되지 않은 정보가 노출될 수 있습니다. 대부분의 프레임워크는 규칙 기반 문자열 교체 및 삭제 기능을 지원하므로 이를 구성하되, 이를 유일한 방어 수단으로 사용해서는 안 됩니다. 민감한 데이터를 로깅하면 보안 위험이 발생하고 개인정보 보호 규정을 위반할 수 있습니다.

### There is more to learn!
이 글의 제목이 "로깅 101"인 이유도 바로 이 때문입니다. 미디엄 독자를 위한 보너스로, "로깅 201"을 다루기 위해 로깅 게임의 레벨을 높이고자 하는 경우 조사해야 할 주제 목록이 있습니다:

- Structured logging. What it is, why it’s useful, and how to structure it. Maybe watch https://www.youtube.com/watch?v=Y5eyEgyHLLo or https://www.youtube.com/watch?v=FyJI4Z6jD4w (thanks to HackerNews users @m_ke and @jeffreygoesto for posting these!)
- Log processing systems: ELK, Splunk, and their ilk. What happens to your logs once you print them out? How do you best make use of them?
- Learn about automated web app monitoring via tools like sentry.io
- Logging is often mixed together with collecting data about application usage. Learn about tools like iterative.ly and segment.com. While you are there, learn about Segment’s approach to ensuring data quality via tracking plans.
- Logging and tracing share a number of concerns; for example, both benefit from having a unique id for each request being processed, to tie related messages together. Learn more about tracing via https://opentelemetry.io/ ; for ID generation, research how to do that for your particular stack — answers vary.