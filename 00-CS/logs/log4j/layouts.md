- https://logging.apache.org/log4j/2.x/manual/layouts.html

# Layouts
애펜더는 레이아웃을 사용하여 로그 이벤트를 소비하는 모든 것의 요구 사항을 충족하는 형식으로 로그 이벤트의 형식을 지정합니다. Log4j 1.x와 Logback에서 레이아웃은 이벤트를 문자열로 변환할 것으로 예상되었습니다. Log4j 2에서 레이아웃은 바이트 배열을 반환합니다. 따라서 레이아웃의 결과가 더 많은 유형의 애펜더에서 유용하게 사용될 수 있습니다. 그러나 이는 바이트 배열에 올바른 값이 포함되도록 대부분의 레이아웃을 문자셋으로 구성해야 함을 의미합니다.

문자셋을 사용하는 레이아웃의 루트 클래스는 org.apache.logging.log4j.core.layout.AbstractStringLayout이며 기본값은 UTF-8입니다. 추상 문자열 레이아웃을 확장하는 각 레이아웃은 자체 기본값을 제공할 수 있습니다. 아래의 각 레이아웃을 참조하세요.

Log4j 2.4.1에 ISO-8859-1 및 US-ASCII 문자 집합을 위한 사용자 정의 문자 인코더가 추가되어 Java 8에 내장된 일부 성능 개선 사항을 Java 7에서 사용할 수 있도록 Log4j로 가져왔습니다. ISO-8859-1 문자만 기록하는 애플리케이션의 경우 이 문자셋을 지정하면 성능이 크게 향상됩니다.

## JSON Layout
참고: JsonTemplate은 더 이상 사용되지 않는 것으로 간주됩니다. 더 많은 기능을 제공하는 JsonTemplateLayout을 대신 사용해야 합니다.

일련의 JSON 이벤트를 바이트 단위로 직렬화된 문자열로 추가합니다.

### Complete well-formed JSON vs. fragment JSON
complete="true"를 설정하면 애펜더가 올바른 형식의 JSON 문서를 출력합니다. 기본적으로 complete="false"를 사용하면 출력을 별도의 파일에 외부 파일로 포함시켜 올바른 형식의 JSON 문서를 만들어야 합니다.

complete="false"인 경우, 어펜더는 문서의 시작 부분 "[", 끝 부분 "]", 레코드 사이에 쉼표 ","와 같은 JSON 오픈 배열 문자를 쓰지 않습니다.

### Pretty vs. compact JSON
압축 속성은 출력이 "예쁘게" 출력될지 여부를 결정합니다. 기본값은 "false"이며, 이는 애펜더가 줄 바꿈 문자를 사용하고 줄을 들여쓰기하여 텍스트 서식을 지정한다는 의미입니다. compact="true"인 경우 줄 바꿈이나 들여쓰기가 사용되지 않으므로 출력의 공간이 줄어듭니다. 물론 메시지 내용에는 이스케이프 처리된 줄 끝 문자가 포함될 수 있습니다.

매개변수 이름 유형 설명
- charset(String): 바이트 배열로 변환할 때 사용할 문자셋입니다. 값은 유효한 문자셋이어야 합니다. 지정하지 않으면 UTF-8이 사용됩니다.
- compact(boolean): 참이면 어펜더는 줄 바꿈과 들여쓰기를 사용하지 않습니다. 기본값은 false입니다.
- eventEol(boolean): true이면 어펜더가 각 레코드 뒤에 줄 끝을 추가합니다. 기본값은 false입니다. 한 줄당 하나의 레코드를 가져오려면 eventEol=true 및 compact=true와 함께 사용합니다.
- endOfLien(String): 설정하면 기본 줄 끝 문자열을 재정의합니다. 예를 들어, "\n"으로 설정하고 eventEol=true 및 compact=true와 함께 사용하면 한 줄당 하나의 레코드가 "\r\n" 대신 "\n"으로 구분됩니다. 기본값은 null입니다(즉, 설정되지 않음).
- complete(boolean): 참이면 애펜더에 JSON 머리글과 바닥글, 레코드 사이의 쉼표가 포함됩니다. 기본값은 false입니다.
- properties(boolean): true이면 어펜더가 생성된 JSON에 스레드 컨텍스트 맵을 포함합니다. 기본값은 false입니다.
- propertiesAsList(boolean): true이면 스레드 컨텍스트 맵이 맵 항목 개체의 목록으로 포함되며, 각 항목은 "키" 속성(값이 키)과 "값" 속성(값이 값)을 가집니다. 기본값은 false이며, 이 경우 스레드 컨텍스트 맵은 키-값 쌍의 단순한 맵으로 포함됩니다.
- locationInfo(boolean): true이면 어펜더가 생성된 JSON에 위치 정보를 포함합니다. 기본값은 false입니다. 위치 정보 생성은 비용이 많이 드는 작업이며 성능에 영향을 줄 수 있습니다. 주의해서 사용하세요.
- includeStacktrace(boolean): true이면 로깅된 모든 Throwable의 전체 스택트레이스를 포함합니다(선택 사항, 기본값은 true).
- includeTimeMillis(boolean): true인 경우, timeMillis 속성이 인스턴트 대신 Json 페이로드에 포함됩니다. timeMillis에는 1970년 1월 1일 자정(UTC) 이후의 밀리초 수가 포함됩니다.
- stacktraceAsString(boolean): 스택트레이스의 형식을 중첩된 객체가 아닌 문자열로 지정할지 여부(선택 사항, 기본값은 false).
- includeNullDelimiter(boolean): 각 이벤트 뒤에 NULL 바이트를 구분 기호로 포함할지 여부(선택 사항, 기본값은 false).
- objectMessageAsJsonObject(boolean): true이면 ObjectMessage가 출력 로그의 "message" 필드에 JSON 객체로 직렬화됩니다. 기본값은 false입니다.