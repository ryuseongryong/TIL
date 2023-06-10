- https://docs.docker.com/engine/reference/builder/

# Dockerfile reference
- Docker는 Docker 파일의 지침을 읽어 이미지를 자동으로 빌드할 수 있음.
- Docker파일은 사용자가 명령줄에서 호출하여 이미지를 어셈블할 수 있는 모든 명령이 포함된 텍스트 문서이다.

## Format
```
INSTRUCTION arguments
```
- 명령어는 대소문자 구분을 하지 않지만 argument와 구분을 위해 대문자로 사용하는 것이 컨벤션
- 도커는 도커파일의 명령어를 순서대로 실행한다. 
- 도커파일을 FROM 명령어로 시작해야 한다.
- 이는 구문 분석기 지시어, 주석 및 전역 범위의 ARG 뒤에 올 수 있다.
- FROM 명령은 빌드할 부모 이미지를 지정한다. FROM 앞에 하나 이상의 ARG 명령어만 올 수 있고, 이 명령어는 도커파일의 FROM 줄에 사용되는 인수를 선언한다.
- 줄이 유요한 구문 분석기 지시어가 아닌 한, `#`으로 시작하는 줄은 주석으로 취급한다. 줄의 다른 위치에 있는 `#` 마커는 인수로 취급된다.
- 주석 줄은 도커파일 명령이 실행되기 전에 제거된다.
- 댓글에서는 Line continuation 문자가 지원되지 않는다.

### whitespace
- 이전 버전과의 호환성을 위해 주석(`#`) 및 명령어 앞의 선행 공백은 무시되지만 권장되지 않는다.
- 그러나 명령 인수의 공백은 유지된다.

## Parser directives
- 구문 분석기 지시어는 선택사항이며 도커파일의 후속 줄이 처리되는 방식에 영향을 준다.
- 파서 지시어는 빌드에 레이어를 추가하지 않으며 빌드 단계로 표시되지 않는다.
- 파서 지시어는 `# directive=value` 형식의 특수한 유형의 주석으로 작성된다. 하나의 지시어는 한 번만 사용 가능하다.
- 주석, 빈 줄 또는 빌더 명령어가 처리되면 도커는 더 이상 파서 지시어를 찾지 않는다. 대신 파서 지시어로 형식이 지정된 모든 것을 주석으로 취급하고 파서 지시어인지 여부를 확인하려고 시도하지 않는다. 따라서 모든 파서 지시어는 도커파일의 맨 위에 있어야 한다.
- 파서 지시어는 대소문자를 구분하지 않는다. 그러나 소문자를 사용하는 것이 일반적이다. 또한 파서 지시어 뒤에는 빈 줄을 포함하는 것이 일반적이다. 파서 지시어에서는 줄 연속 문자가 지원되지 않는다.
- 파서 지시어에는 줄을 나누지 않는 공백이 허용된다.
- syntax와 escape 지시어가 있다.
### syntax
- BuildKit 백엔드를 사용할 때만 사용가능
- 클래식 빌더 백엔드를 사용할 때는 무시됨
### escape
- 이스케이프 지시어는 도커파일에서 문자를 이스케이프하는 데 사용되는 문자를 설정한다.
- 지정하지 않으면 기본 이스케이프 문자는 `\`이다.
- 이스케이프 문자는 한 줄의 문자를 이스케이프하고 새 줄을 이스케이프하는 데 모두 사용된다. 따라서 Dockerfile 명령이 여러 줄에 걸쳐 있을 수 있다. 
- 이스케이프 파서 지시어가 도커파일에 포함되어 있는지 여부에 관계없이, 한 줄 끝을 제외하고는 RUN 명령에서 이스케이프가 수행되지 않는다는 점에 유의해야 한다.
- 이스케이프 문자를 `(Backtik)으로 설정하는 것은 Windows에서 특히 유용하고, 여기서 `\`는 디렉터리 경로 구분 기호이다. Backtikdms Windows PowerShell과 일치한다.
- Windows에서 명확하지 않은 방식으로 실패할 수 있는 다음 예제가 있을 수 있다. 두 번째 줄 끝에 있는 두 번째 `\`는 첫 번째 `\`의 이스케이프 대상이 아니라 새 줄의 이스케이프로 해석된다. 마찬가지로 세 번째 줄 끝에 있는 `\`는 실제로 명령으로 처리되었다고 가정하면 줄 연속으로 처리된다. 이 도커 파일의 결과는 두 번째 줄과 세 번째 줄이 하나의 명령어로 간주된다는 것이다.
    - example code
        ```
        FROM microsoft/nanoserver
        COPY testfile.txt c:\\
        RUN dir c:\
        ```
    - result in
        ```
        PS E:\myproject> docker build -t cmd .

        Sending build context to Docker daemon 3.072 kB
        Step 1/2 : FROM microsoft/nanoserver
        ---> 22738ff49c6d
        Step 2/2 : COPY testfile.txt c:\RUN dir c:
        GetFileAttributesEx c:RUN: The system cannot find the file specified.
        PS E:\myproject>
        ```
- 위의 문제에 대한 한 가지 해결책은 `/`를 COPY 명령과 dir의 대상으로 모두 사용하는 것이다. 그러나 이 구문은 Windows의 경로에 자연스럽지 않기 때문에 기껏해야 혼란스럽고, 최악의 경우 Windows의 모든 명령이 `/`를 경로 구분 기호로 지원하지 않기 때문에 오류가 발생하기 쉽다.
- 이스케이프 파서 지시문을 추가하면 다음 도커파일은 Windows의 파일 경로에 대한 자연스러운 플랫폼 시맨틱을 사용하여 예상대로 성공한다.
    ```
    # escape=`

    FROM microsoft/nanoserver
    COPY testfile.txt c:\
    RUN dir c:\
    ```
## Environment replacement
- 환경 변수(ENV문으로 선언)는 특정 명령어에서 도커파일에서 해석할 변수로 사용할 수 있다. 이스케이프는 변수와 유사한 구문을 문자 그대로 포함할 때도 처리된다.
- 환경 변수는 도커파일에서 `$변수_이름` 또는 `$(변수_이름)`으로 표기된다. 이 둘은 동등하게 취급되며 중괄호 구문은 일반적으로 `${foo}_bar`와 같이 공백이 없는 변수 이름에 대한 문제를 해결하는 데 사용된다.
- `${variable_name}` 구문은 아래에 명시된 몇 가지 표준 bash 수정자를 지원한다.
    - `${variable:-word}`는 변수가 설정되어 있으면 결과가 해당 값임을 나타낸다. 변수가 설정되어 있지 않으면 단어가 결과가 된다.
    - `${variable:+word}`는 변수가 설정되어 있으면 단어가 결과가 되고, 설정되어 있지 않으면 빈 문자열이 결과임을 나타낸다.
- 모든 경우에 단어는 추가 환경 변수를 포함한 모든 문자열이 될 수 있다.
- 변수 앞에 `\`를 추가하면 이스케이프가 가능하다. 예를 들어 `\$foo` 또는 `\${foo}`는 각각 `$foo` 및 `${foo}` 리터럴로 변환된다.
    ```
    FROM busybox
    ENV FOO=/bar
    WORKDIR ${FOO}   # WORKDIR /bar
    ADD . $FOO       # ADD . /bar
    COPY \$FOO /quux # COPY $FOO /quux
    ```
- 환경변수는 도커파일의 다음 목록들이 지원된다.
    - ADD
    - COPY
    - ENV
    - EXPOSE
    - FROM
    - LABEL
    - STOPSIGNAL
    - USER
    - VOLUME
    - WORKDIR
    - ONBUILD (when combined with one of the supported instructions above)

- 환경 변수 치환은 전체 명령어에 걸쳐 각 변수에 동일한 값을 사용한다.
    ```
    ENV abc=hello
    ENV abc=bye def=$abc # def=hello
    ENV ghi=$abc # ghi=bye
    ```

## .dockerignore file
- 도커 CLI는 컨텍스트를 도커 데몬으로 보내기 전에 컨텍스트의 루트 디렉터리에서 .dockerignore라는 파일을 찾는다. 
- 이 파일이 있으면 CLI는 컨텍스트의 패턴과 일치하는 파일 및 디렉터리를 제외하도록 컨텍스트를 수정한다. 
- 이렇게 하면 용량이 크거나 민감한 파일 및 디렉터리를 불필요하게 데몬으로 보내거나 ADD 또는 COPY를 사용하여 이미지에 추가하는 것을 방지할 수 있다.

- CLI는 `.dockerignore` 파일을 유닉스 셸의 파일 글로브와 유사한 패턴의 개행으로 구분된 목록으로 해석한다. 
- 매칭을 위해 컨텍스트의 루트는 작업 디렉터리와 루트 디렉터리 모두로 간주된다. 예를 들어 `/foo/bar` 및 `foo/bar` 패턴은 모두 PATH의 foo 하위 디렉터리 또는 URL에 위치한 git 리포지토리의 루트에서 bar라는 이름의 파일 또는 디렉터리를 제외한다. 둘 다 다른 것은 제외하지 않는다.
- `.dockerignore` 파일의 줄이 #으로 시작하면 이 줄은 주석으로 간주되어 CLI에서 해석하기 전에 무시된다.

| Rule     |      Behavior       |
| -------- | ------------------- |
|# comment | 주석으로 간주하고 무시됨. |
| */temp*  | 루트의 바로 하위 디렉터리에서 이름이 temp로 시작하는 파일과 디렉터리를 제외한다. 예를 들어 일반 파일 `/somedir/temporary.txt`는 제외되며 `/somedir/temp` 디렉터리도 제외된다. |
| */*/temp* | 루트보다 두 단계 아래에 있는 하위 디렉터리에서 temp로 시작하는 파일과 디렉터리를 제외한다. 예를 들어 `/somedir/subdir/temporary.txt`는 제외된다. |
| temp? | 루트 디렉터리에 있는 파일 및 디렉터리 중 이름이 한 글자 확장자 temp인 파일과 디렉터리는 제외한다. 예를 들어 `/tempa` 및 `/tempb` 는 제외된다. |

- 매칭은 Go의 filepath.Match 규칙을 사용하여 수행된다. 
- 전처리 단계는 선행 및 후행 공백을 제거하고 Go의 `filepath.Clean`을 사용하여 `.`및 `..`요소를 제거한다. 
- 전처리 후 비어 있는 줄은 무시된다.
- Go의 `filepath.Match` 규칙 외에도 Docker는 디렉터리 수에 관계없이(0포함) 일치하는 특수 와일드카드 문자열 `**`도 지원한다. 예를 들어 `**/*.go`는 빌드 컨텍스트의 루트를 포함하여 모든 디렉터리에서 발견되는 `.go`로 끝나는 모든 파일을 제외한다.
- `!`로 시작하는 줄은 제외에 대한 예외를 만드는 것으로 사용할 수 있다.
    ```
    *.md
    !README.md # README.md를 제외한 모든 마크다운 파일은 컨텍스트에서 제외됨.
    ```
- 예외 규칙의 배치에 따라 동작에 영향을 미치고, 특정 파일과 일치하는 `.dockerignore`의 마지막 줄에 따라 포함 또는 제외 여부가 결정된다.
    ```
    *.md
    !README*.md
    README-secret.md # 컨텍스트에 포함된 마크다운 파일은 README-secret.md 이외의 README 파일을 제외하면 없다.
    ```
    ```
    *.md
    README-secret.md
    !README*.md # 모든 README 파일이 포함된다. !README*.md가 마지막 줄에 오기 때문에 영향을 미치지 않는다.
    ```

- `.dockerignore`파일을 사용하여 도커파일 및 `.dockerignore` 파일을 제외할 수도 있다. 
- 이러한 파일은 작업을 수행하는 데 필요하기 때문에 여전히 데몬으로 전송된다. 
- 그러나 ADD 및 COPY 명령은 이미지에 복사하지 않는다.
- 컨텍스트에서 제외할 파일 대신 포함할 파일을 지정하려면, 첫 번째 패턴으로 `*`를 지정하고, 그 뒤에 하나 이상의 `!`예외 패턴을 지정한다.
- `.`패턴은 과거 있었던 이력 때문에 무시된다.

## WORKDIR
- WORKDIR 명령은 도커파일에서 그 뒤에 오는 모든 RUN, CMD, ENTRYPOINT, COPY, ADD 명령에 대한 작업 디렉터리를 설정한다. WORKDIR이 존재하지 않는 경우, 후속 도커파일 명령어에서 사용되지 않더라도 생성된다.