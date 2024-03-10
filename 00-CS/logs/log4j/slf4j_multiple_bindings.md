- https://www.slf4j.org/codes.html#multiple_bindings

# Multiple bindings were found on the class path
SLF4J API는 한 번에 하나의 기본 로깅 프레임워크와만 바인딩하도록 설계되었습니다. 클래스 경로에 바인딩이 두 개 이상 있는 경우 SLF4J는 해당 바인딩의 위치를 나열하는 경고를 표시합니다.

클래스 경로에서 여러 바인딩을 사용할 수 있는 경우 사용하려는 바인딩을 하나만 선택하고 다른 바인딩은 제거합니다. 예를 들어 클래스 경로에 slf4j-simple-2.0.7.jar와 slf4j-nop-2.0.7.jar가 모두 있고 nop(동작 없음) 바인딩을 사용하려는 경우 클래스 경로에서 slf4j-simple-2.0.7.jar를 제거합니다.

이 경고에서 SLF4J가 제공하는 위치 목록은 일반적으로 원치 않는 SLF4J 바인딩을 프로젝트에 일시적으로 끌어오는 종속성을 식별하는 데 충분한 정보를 제공합니다. 프로젝트의 pom.xml 파일에서 부도덕한 종속성을 선언할 때 이 SLF4J 바인딩을 제외하세요. 예를 들어, cassandra-all 버전 0.8.1은 log4j와 slf4j-log4j12를 모두 컴파일 타임 종속 요소로 선언합니다. 따라서 프로젝트에 cassandra-all을 종속 요소로 포함하면, cassandra-all 선언으로 인해 slf4j-log4j12.jar와 log4j.jar가 모두 종속 요소로 가져올 수 있습니다. log4j를 SLF4J 백엔드로 사용하지 않으려면 다음과 같이 Maven에 이 두 아티팩트를 제외하도록 지시할 수 있습니다:

```
<dependencies>
  <dependency>
    <groupId> org.apache.cassandra</groupId>
    <artifactId>cassandra-all</artifactId>
    <version>0.8.1</version>

    <exclusions>
      <exclusion> 
        <groupId>org.slf4j</groupId>
        <artifactId>slf4j-log4j12</artifactId>
      </exclusion>
      <exclusion> 
        <groupId>log4j</groupId>
        <artifactId>log4j</artifactId>
      </exclusion>
    </exclusions> 

  </dependency>
</dependencies>
```

참고 
SLF4J가 내보내는 경고는 단지 경고일 뿐입니다. 바인딩이 여러 개 있는 경우에도 SLF4J는 하나의 로깅 프레임워크/구현을 선택해 바인딩합니다. SLF4J가 바인딩을 선택하는 방식은 JVM에 의해 결정되며 모든 실용적인 목적에서는 무작위로 간주되어야 합니다. 버전 1.6.6부터 SLF4J는 실제로 바인딩되는 프레임워크/구현 클래스의 이름을 지정합니다.

라이브러리나 프레임워크와 같은 임베디드 컴포넌트는 SLF4J 바인딩에 대한 종속성을 선언해서는 안 되며, slf4j-api에만 종속성을 선언해야 합니다. 라이브러리가 SLF4J 바인딩에 대한 컴파일 타임 종속성을 선언하면 최종 사용자에게 해당 바인딩이 부과되므로 SLF4J의 목적이 무효화됩니다. SLF4J 바인딩에 대한 컴파일 타임 종속성을 선언하는 임베디드 컴포넌트를 발견하면 시간을 내어 해당 컴포넌트/라이브러리의 작성자에게 연락하여 수정을 요청해 주시기 바랍니다.

