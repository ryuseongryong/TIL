- https://logging.apache.org/log4j/2.x/manual/json-template-layout.html

# JSON Template Layout
- JsonTemplateLayout은 사용자 정의가 가능하고 효율적이며 가비지 없는 JSON 생성 레이아웃입니다. 이 레이아웃은 제공된 JSON 템플릿에 설명된 구조에 따라 LogEvents를 인코딩합니다. 간단히 말해, 이 레이아웃의 장점은
    - 사용자 정의 가능한 JSON 구조(eventTemplate[Uri] 및 stackTraceElementTemplate[Uri] 레이아웃 구성 매개변수 참조).
    - 사용자 정의 가능한 타임스탬프 형식(타임스탬프 이벤트 템플릿 리졸버 참조)
    - 다양한 예외 서식 지정 기능(예외 및 예외RootCause 이벤트 템플릿 리졸버 참조)
    - 확장 가능한 플러그인 지원
    - 사용자 정의 가능한 객체 재활용 전략

# Usage
- 종속성 목록에 log4j-layout-template-json 아티팩트를 추가하는 것만으로도 Log4j 구성에서 JsonTemplateLayout에 액세스할 수 있습니다:
```
<dependency>
    <groupId>org.apache.logging.log4j</groupId>
    <artifactId>log4j-layout-template-json</artifactId>
    <version>2.22.0</version>
</dependency>
```
- 예를 들어, Elastic Common Schema(ECS) 사양을 모델링하는 다음 JSON 템플릿이 있다고 가정해 보겠습니다(클래스 경로: EcsLayout.json을 통해 액세스 가능).
```
{
  "@timestamp": {
    "$resolver": "timestamp",
    "pattern": {
      "format": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'",
      "timeZone": "UTC"
    }
  },
  "ecs.version": "1.2.0",
  "log.level": {
    "$resolver": "level",
    "field": "name"
  },
  "message": {
    "$resolver": "message",
    "stringified": true
  },
  "process.thread.name": {
    "$resolver": "thread",
    "field": "name"
  },
  "log.logger": {
    "$resolver": "logger",
    "field": "name"
  },
  "labels": {
    "$resolver": "mdc",
    "flatten": true,
    "stringified": true
  },
  "tags": {
    "$resolver": "ndc"
  },
  "error.type": {
    "$resolver": "exception",
    "field": "className"
  },
  "error.message": {
    "$resolver": "exception",
    "field": "message"
  },
  "error.stack_trace": {
    "$resolver": "exception",
    "field": "stackTrace",
    "stackTrace": {
      "stringified": true
    }
  }
}
```
- 아래 log4j2.xml 구성과 함께 사용합니다:
```
<JsonTemplateLayout eventTemplateUri="classpath:EcsLayout.json"/>
```
- 또는 아래 log4j2.properties 구성을 사용합니다:
```
appender.console.layout.type = JsonTemplateLayout
appender.console.layout.eventTemplateUri = classpath:EcsLayout.json
```
- JsonTemplateLayout은 다음과 같이 JSON을 생성합니다:
```
{
  "@timestamp": "2017-05-25T19:56:23.370Z",
  "ecs.version": "1.2.0",
  "log.level": "ERROR",
  "message": "Hello, error!",
  "process.thread.name": "main",
  "log.logger": "org.apache.logging.log4j.JsonTemplateLayoutDemo",
  "error.type": "java.lang.RuntimeException",
  "error.message": "test",
  "error.stack_trace": "java.lang.RuntimeException: test\n\tat org.apache.logging.log4j.JsonTemplateLayoutDemo.main(JsonTemplateLayoutDemo.java:11)\n"
}
```
# Layout Configuration
- JsonTemplateLayout은 다음 파라미터로 구성됩니다:
- JsonTemplateLayout 매개변수
    - charset(charset) : 문자열 인코딩에 사용되는 문자셋
    - locationInfoEnabled(boolean) : 로그 이벤트 소스(파일 이름, 줄 번호 등)에 대한 액세스를 토글합니다(기본값은 log4j.layout.jsonTemplate.locationInfoEabled 속성에 의해 설정된 false).
    - stackTraceEnabled(boolean) : 스택 추적에 대한 액세스를 토글합니다(기본값은 log4j.layout.jsonTemplate.stackTraceEnabled 속성에 의해 설정된 true).
    - eventTemplate(string) : 로그 이벤트를 렌더링하기 위한 인라인 JSON 템플릿(eventTemplateUri보다 우선 순위가 있으며, 기본값은 log4j.layout.jsonTemplate.eventTemplate 속성에 의해 설정된 null입니다).
    - eventTemplateUri(String) : LogEvents를 렌더링하기 위한 JSON 템플릿을 가리키는 URI(기본값은 log4j.layout.jsonTemplate.eventTemplateUri 속성에 의해 설정된 classpath:EcsLayout.json입니다).
    - eventTemplateRootObjectKey(String) : 있는 경우, 이벤트 템플릿은 제공된 키가 있는 단일 멤버로 구성된 JSON 객체에 넣습니다(기본값은 log4j.layout.jsonTemplate.eventTemplateRootObjectKey 속성에 의해 설정된 null).
    - eventTemplateAdditionalField(EventTemplateAdditionalFeld[]) : 이벤트 템플릿의 루트에 추가 키-값 쌍을 추가합니다.
    - stackTraceElementTemplate(String) : 스택트레이스 엘리먼트를 렌더링하기 위한 인라인 JSON 템플릿(스택트레이스 엘리먼트 템플릿유리보다 우선권을 가짐, 기본값은 로그4j.layout.jsonTemplate.stackTraceElementTemplate 속성에 의해 설정된 null임).
    - stackTraceElementTemplateUri(String) : 스택트레이스 엘리먼트를 렌더링하기 위한 JSON 템플릿을 가리키는 URI(기본값은 log4j.layout.jsonTemplate.stackTraceElementTemplateUri 속성에 의해 설정된 classpath:StackTraceElementLayout.json입니다).
    - eventDelimiter(String) : 렌더링된 로그 이벤트를 구분하는 데 사용되는 구분 기호(기본값은 log4j.layout.jsonTemplate.eventDelimiter 속성에 의해 설정된 System.lineSeparator()입니다).
    - nullEventDelimiterEnabled(boolean) : 렌더링된 LogEvents를 구분하는 모든 eventDelimiter 끝에 \0(null) 문자를 추가합니다(기본값은 log4j.layout.jsonTemplate.nullEventDelimiterEnabled 속성에 의해 설정된 false로 설정됨).
    - maxStringLength(int) : 지정된 제한보다 긴 문자열 값을 잘라냅니다(기본값은 log4j.layout.jsonTemplate.maxStringLength 속성에 의해 설정된 16384입니다).
    - truncatedStringSuffix(String) : 최대 문자열 길이를 초과하여 잘린 문자열에 추가할 접미사(기본값은 ... log4j.layout.jsonTemplate.truncatedStringSuffix 속성에 의해 설정됨)입니다.
    - recyclerFactory(RecyclerFactory) : 더미, 스레드 로컬 또는 대기열이 될 수 있는 재활용 전략(log4j.layout.jsonTemplate.recyclerFactory 속성으로 설정).

