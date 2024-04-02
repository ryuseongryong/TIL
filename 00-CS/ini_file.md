- https://en.wikipedia.org/wiki/INI_file

# INI file
INI 파일은 속성에 대한 키-값 쌍으로 구성된 구조와 구문을 가진 텍스트 기반 콘텐츠와 속성을 구성하는 섹션으로 구성된 컴퓨터 소프트웨어용 구성 파일입니다.[1] 이러한 구성 파일의 이름은 이 소프트웨어 구성 방법을 대중화한 MS-DOS 운영 체제에서 사용되는 초기화를 위한 파일 이름 확장자 INI에서 유래했습니다. 이 형식은 많은 구성 상황에서 비공식적인 표준이 되었지만 다른 운영 체제의 많은 애플리케이션에서는 conf 및 cfg와 같은 다른 파일 이름 확장자를 사용합니다.[2]

## History
Windows에서 소프트웨어 구성의 기본 메커니즘은 원래 한 줄에 하나의 키-값 쌍이 있는 텍스트 줄로 구성된 텍스트 파일 형식으로, 섹션으로 구성되었습니다. 이 형식은 장치 드라이버, 글꼴 및 시작 실행기와 같은 운영 체제 구성 요소에 사용되었습니다. INI 파일은 일반적으로 애플리케이션에서 개별 설정을 저장하는 데도 사용되었습니다.[3]

이 형식은 Windows 3.1x까지 16비트 Microsoft Windows 플랫폼에서 유지되었습니다. Windows 95부터 Microsoft는 Windows 레지스트리 사용을 선호했고 개발자가 구성에 INI 파일을 사용하지 않도록 유도하기 시작했습니다. 이후 모든 버전의 Windows에서는 시스템 구성에 Windows 레지스트리를 사용했지만, .NET Framework를 기반으로 빌드된 애플리케이션은 특수 XML .config 파일을 사용합니다. 초기화 파일 기능은 여전히 Windows에서 사용할 수 있으며 개발자는 여전히 이를 사용할 수 있습니다.

Windows 소프트웨어 외에도 플랫폼에 구애받지 않는 소프트웨어에서도 이 파일 형식을 구성에 사용할 수 있습니다. 일부 유닉스 계열 구성 파일도 비슷한 형식을 사용합니다. INI는 사람이 읽을 수 있고 구문 분석이 간단하므로 그다지 복잡하지 않은 구성 파일에 사용할 수 있는 형식입니다.

## Prevalence
다음은 .INI 파일이 나타나는 위치의 전체 목록이 아닙니다.
- Desktop.ini 파일은 여전히 Windows에서 폴더의 아이콘 지정과 같은 디렉터리의 속성을 구성하는 데 사용됩니다. [4][5]
- PHP의 php.ini 파일은 .INI 형식을 사용합니다.[6][7].
- Git의 .git/config 파일은 .INI 형식으로 작성됩니다.[8].
- freedesktop.org *.desktop 데스크톱 항목은 .INI 플레이버로 작성됩니다.[9][10]
- systemd *.service 단위 구성 파일은 .INI로 작성됩니다.[10].
- Netatalk의 afp.conf 파일은 .INI 스타일의 구성 언어로 작성됩니다.[11]
- 팩맨의 pacman.conf 파일은 .INI로 작성됩니다[12].

## Example
다음 예제 파일에는 소프트웨어 소유자를 위한 섹션과 급여 데이터베이스 연결을 위한 섹션이 두 개 있습니다. 댓글에는 파일을 마지막으로 수정한 사람과 수정 사유가 기록됩니다.

```
; last modified 1 April 2001 by John Doe
[owner]
name = John Doe
organization = Acme Widgets Inc.

[database]
; use IP address in case network name resolution is not working
server = 192.0.2.62     
port = 143
file = "payroll.dat"

```

## Format
넓은 의미에서 .INI는 사람이 구성할 수 있으면서도 임시 구현에 적합한 비공식적인 형식입니다. 따라서 .INI 방언이라고 불리는 다양한 사양(때로는 파서 구현이 유일한 사양인 경우도 있음)이 존재합니다.

.INI 해석은 개인의 취향과 컴퓨팅 환경(예: 공백이 정확한 데이터의 필요성, 필드 유형 정보의 필요성, 대소문자 접기를 선호하는 Windows, 대소문자 감지를 선호하는 Unix, # 구분 주석은 Unix 스크립팅에서 차용)에 따라 많이 달라지기 때문에 .INI가 확산되기 쉽지만, 하드 코어가 존재하여 .INI 맛은 일반적으로 텍스트 기반 및 줄 기반, 공백 제거, 빈 줄 및 주석 줄(예: ; 시스템 전체 메일캡에 대한 레지스터, # d5cb328의 해결 방법) 무시, 섹션을 나타내는 대괄호(예: [단위], [분기 "마스터"]), 키-값 쌍으로 된 데이터를 종종 등호(ASCII 0x3D)로 구분(예: 아이콘 파일=Folder.ico, 타임머신 = yes) 등과 연관되어 있습니다.

가능한 한 많은 방언을 지원할 수 있는 파서를 만들려는 시도가 존재하며[13], 가장 복잡하게 해석하면 .INI 형식은 임의의 S-표현식을 표현할 수 있어 XML이나 JSON과 같은 표준화된 형식과 동일하지만 구문이 정해진 것은 아니며 어떤 사람들에게는 더 편안하게 느껴질 수 있습니다.

.INI 파일 형식은 엄격하게 정의되어 있지 않기 때문에 많은 구문 분석기가 공통 핵심을 구성하는 기능 이외의 기능을 지원합니다. 구현된 지원은 매우 변동성이 큽니다.

## Key-value pairs
.INI의 데이터는 키 또는 속성이라고 하는 키-값 쌍으로 보관됩니다. 따라서 키는 전체 키-값 쌍을 참조하거나 해당 키만 참조할 수 있습니다. 값을 속성 이름이라고도 합니다. 텍스트 표현에서 키-값 쌍은 한 줄 또는 여러 줄로 표시되며, 값의 시작은 구분 기호(대부분 등호(=, ASCII 0x3D))로 표시되지만 콜론(:, ASCII 0x3A) 또는 공백(GNU 세계에서 가끔 사용[13])으로 표시되기도 합니다. 키의 키는 구분 기호 왼쪽에 나타나며, 비어 있지 않은 경우가 많으며 구분 기호를 포함하지 않아야 합니다. 일부 버전에서는 값에 이스케이프 시퀀스를 허용합니다.

Windows 구현에서 등호 기호와 세미콜론은 예약 문자이므로 키에 표시될 수 없습니다. 키를 둘러싼 모든 공백은 구문 분석기에 의해 제거됩니다. 값에는 어떤 문자가든 포함될 수 있습니다(Windows 스타일에서는 구분 기호 주위에 공백이 없습니다. 예: IconFile=Folder.ico).

키-값 쌍은 다음과 같이 보일 수 있습니다:
```
key=key=v
  name =value
sem=;
semver=v5822.433.2

```

## Sections
키-값 쌍은 섹션 아래에 그룹화할 수 있습니다. 일부 .INI 방언은 모든 키-값 쌍이 섹션에 있어야 하며, 일부는 소위 전역 속성을 허용합니다.[14] 키-값 쌍이 그룹화되면 섹션 이름은 대괄호([, ASCII 0x5B 및 ], ASCII 0x5D)로 묶여 한 줄에 단독으로 나타나며 다른 섹션이 선언될 때까지 후속 줄의 모든 키-값 쌍에 적용됩니다. 명시적인 "섹션 끝" 구분자(예: XML의 </tag>)는 없습니다. 따라서 구문론적으로 섹션을 임의로 중첩할 수 없습니다. 필요한 경우 계층 구조를 평평하게 하고 섹션 이름 안에 사용자 정의 구분 기호 문자(주로 ., ASCII 0x2E)를 연결하여 중첩을 구현할 수 있습니다. 하위 섹션이라고 하는 한 수준의 중첩이 지원되는 경우가 많습니다.

중첩된 섹션을 사용하는 예시적인 .INI 문서:
```
[project]
name = orchard rental service (with app)
target region = "Bay Area"
; TODO: advertise vacant positions
legal team = (vacant)

[fruit "Apple"]
trademark issues = foreseeable
taste = known

[fruit.Date]
taste = novel
Trademark Issues="truly unlikely"

[fruit "Raspberry"]
anticipated problems  ="logistics (fragile fruit)"
Trademark Issues=\
 possible

[fruit.raspberry.proponents.fred]
date = 2021-11-23, 08:54 +0900
comment = "I like red fruit."
[fruit "Date/proponents/alfred"]
comment: Why,  \
 \
 \
 I would buy dates.
# folding: Is "\\\\\nn" interpreted as "\\n" or "\n"?
#   Or does "\\\\" prevent folding?
editor  =My name may contain a \\
newline.
```

#### Hierarchy(섹션 중첩)
일부 구문 분석기는 점을 경로 구분 기호로 사용하여 섹션 중첩을 허용합니다:
```
[section]
domain = example.com

[section.subsection]
foo = bar
```

경우에 따라 상대 중첩도 지원되며, 앞의 점은 이전 섹션으로의 중첩을 나타냅니다.
```
[section]
domain = example.com

[.subsection]
foo = bar
```

역사적으로 점 대신 중첩을 표현하는 방법도 존재해 왔습니다(예: 백슬래시가 [A\B\C]의 형태로 중첩 구분 기호로 사용된 IBM의 Microsoft Windows용 devlist.ini 드라이버 파일 또는 [A] 및 B,C,P = V의 형태로 완전히 다른 구문을 사용한 Microsoft Visual Studio의 AEMANAGR.INI 파일). 일부 구문 분석기는 중첩을 전혀 지원하지 않고 계층을 인식하지 못하지만, [A.B.C]가 고유 식별자를 구성한다는 사실을 악용하여 중첩을 부분적으로 에뮬레이션할 수 있습니다.

### Case sensitivity
Windows의 섹션 및 속성 이름은 대소문자를 구분하지 않습니다.[15] 대부분의 유닉스 스타일 .INI 해석은 대소문자 접기를 완전히 금지하지만, 섹션 이름[16] 또는 키[17]의 대소문자 접기는 허용되는 경우가 있습니다.

### Comments
연속된 후행 공백 뒤에 세미콜론(;, ASCII 0x3E)이 있는 줄은 주석을 나타냅니다. 또한 일부 .INI 방언에서는 숫자 기호(#, ASCII 0x23)를 사용하여 주석을 표시할 수 있으며, 이는 유닉스 셸 주석과 유사합니다. 키-값 쌍 줄 또는 섹션 줄(인라인 주석이라고 함)에 주석을 허용하는 .INI 방언도 있지만, 일부는 주석과 값 또는 섹션 닫는 괄호를 공백으로 구분해야 합니다. 그럼에도 불구하고 일부 방언에서는 숫자 기호가 키 이름에 포함되어 무시될 수 있습니다. 주석 줄은 구문 분석기가 무시하도록 설계되었습니다.
```
#! /bin/convert-ini-to-perl | perl | ssh wikipedia.org upload --sanitise=no
; Ambiguous without further knowledge of the .INI dialect:
; is the value "live" or "live # dangerously"?
I like to = live # dangerously

#var = a

var = a       ; This is an inline comment
foo = bar     # This is another inline comment
```
WinAPI의 GetPrivateProfileString의 방언에서는 주석이 줄 자체에서 발생해야 합니다.

### Order of sections and properties
섹션 내 속성의 순서와 파일 내 섹션의 순서는 무관합니다.

### Duplicate names
대부분의 구현은 섹션에 지정된 이름을 가진 프로퍼티를 하나만 지원합니다. 속성 이름이 두 번째 발생하면 중단되거나 무시되거나(값이 삭제됨) 첫 번째 발생을 재정의할 수 있습니다(첫 번째 값은 삭제됨). 일부 프로그램은 중복된 프로퍼티 이름을 사용하여 다중 값 프로퍼티를 구현합니다.

같은 이름을 가진 여러 섹션 선언에 대한 해석도 다양합니다. 일부 구현에서는 중복된 섹션을 마치 연속적으로 발생한 것처럼 단순히 프로퍼티를 병합합니다. 다른 구현에서는 INI 파일의 일부를 중단하거나 무시할 수도 있습니다.

### Quoted values
일부 구현에서는 일반적으로 큰따옴표 및/또는 아포스트로피를 사용하여 값을 따옴표로 묶을 수 있습니다. 이를 통해 공백을 명시적으로 선언하거나 특수 문자(등호, 세미콜론 등)를 인용할 수 있습니다. 표준 Windows 함수인 GetPrivateProfileString은 이를 지원하며 값을 둘러싸고 있는 따옴표를 제거합니다.

### Line continuation
C 구문을 모방하여 일부 방언에서는 줄의 마지막 문자로 백슬래시(\, ASCII 0x5C)로 줄을 접을 수 있습니다.[18] 이러한 줄 연속에서 백슬래시 바로 뒤에 EOL(줄 끝)이 오면 백슬래시와 줄 바꿈이 삭제되어 문서의 줄이 논리적 줄로 바뀝니다.

### Escape characters
일부 방언은 문자 이스케이프를 다양하게 지원하며, 일반적으로 백슬래시 문자(\, ASCII 0x5C)를 메타문자로 사용하고 C 구문을 에뮬레이트합니다[19].

일부 사양에서는 일반적인 이스케이프 시퀀스에 대해 메타문자를 명시적으로 음소거하므로[20][21] 이스케이프 시퀀스를 맹목적으로 해석하는 것은 현명하지 않습니다.
Sequence	Meaning
\\	\ (a single backslash, escaping the escape character)
\'	Apostrophe
\"	Double quotes
\0	Null character
\a	Bell/Alert/Audible
\b	Backspace, Bell character for some applications
\t	Tab character
\r	Carriage return
\n	Line feed
\;	Semicolon
\#	Number sign
\=	Equals sign
\:	Colon
\xhhhh	Unicode character with code point 0xhhhh, encoded either in UTF-8 or local encoding


## Accessing INI files
Windows에서 프로필 API는 기존 Windows .ini 파일에서 설정을 읽고 쓰는 데 사용되는 프로그래밍 인터페이스입니다. 예를 들어, GetPrivateProfileString 함수는 초기화 파일의 지정된 섹션에서 문자열을 검색합니다. ("개인" 프로필은 WIN.INI에서 가져오는 GetProfileString과 대조됩니다.)

다음 샘플 C 프로그램은 위의 샘플 INI 파일에서 속성 값을 읽는 방법을 보여줍니다(구성 파일 이름은 dbsettings.ini로 함):

```
#include <windows.h>

int main(int argc, _TCHAR *argv[])
{
  _TCHAR dbserver[1000];
  int dbport;
  GetPrivateProfileString("database", "server", "127.0.0.1", dbserver, sizeof(dbserver) / sizeof(dbserver[0]), ".\\dbsettings.ini");
  dbport = GetPrivateProfileInt("database", "port", 143, ".\\dbsettings.ini");
  // N.B. WritePrivateProfileInt() does not exist, only WritePrivateProfileString()
  return 0;
}
```
위의 두 함수 호출에서 각각 "127.0.0.1"과 143이 기본값인 GetPrivateProfileString 함수의 세 번째 매개변수입니다. 이 매개변수에 제공된 인수가 NULL인 경우 기본값은 빈 문자열인 ""입니다.

Unix에서는 INI 파일에 액세스하기 위한 다양한 구성 라이브러리가 존재합니다. 이러한 라이브러리는 프레임워크와 툴킷에 이미 포함되어 있는 경우가 많습니다. Unix용 INI 구문 분석기의 예로는 GLib, iniparser 및 libconfini가 있습니다.

## File mapping
초기화 파일 매핑은 INI 파일과 Windows 레지스트리 간에 매핑을 만듭니다.[57][58] 이 기능은 기존 .ini 파일에 설정을 저장하는 것에서 새 레지스트리로 마이그레이션하는 방법으로 Windows NT 및 Windows 95에 도입되었습니다. 파일 매핑은 프로필 API 호출을 트래핑하고, IniFileMapping 레지스트리 섹션의 설정을 사용하여 레지스트리의 적절한 위치로 읽기 및 쓰기를 지시합니다.

아래 예시를 사용하면 문자열 호출을 통해 소유자 섹션의 이름 키를 dbsettings.ini라는 설정 파일에서 가져올 수 있습니다. 반환되는 값은 "John Doe"라는 문자열이어야 합니다:

```
GetPrivateProfileString("owner", "name", ... , "c:\\programs\\oldprogram\\dbsettings.ini");
```

INI 매핑은 이 프로필 API 호출을 받아 지정된 파일 이름의 경로를 무시하고 디렉터리 아래에 파일 이름과 일치하는 레지스트리 키가 있는지 확인합니다:
- HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\IniFileMapping

이것이 존재하면 요청된 섹션과 일치하는 항목 이름을 찾습니다. 항목이 발견되면 INI 매핑은 해당 값을 레지스트리의 다른 부분에 대한 포인터로 사용합니다. 그런 다음 레지스트리의 해당 부분에서 요청된 INI 설정을 찾습니다.

일치하는 항목 이름을 찾을 수 없고 (기본) 항목 이름 아래에 항목이 있는 경우 INI 매핑은 그 항목을 대신 사용합니다. 따라서 각 섹션 이름에는 자체 항목이 필요하지 않습니다.

```
HKEY_LOCAL_MACHINE\Software\...\IniFileMapping\dbsettings.ini
(Default)	@USR:Software\oldprogs\inisettings\all
database	USR:Software\oldprogs\inisettings\db

```

따라서 이 경우 [소유자] 섹션에 대한 프로필 호출은 다음 주소로 매핑됩니다:
```
HKEY_CURRENT_USER\Software\oldprogs\inisettings\all
name	John Doe
organization	Acme Products
```

여기서 "이름" 레지스트리 항목 이름이 요청된 INI 키와 일치하는 것으로 확인됩니다. 그러면 프로필 호출에 "John Doe" 값이 반환됩니다. 이 경우 기본값의 @ 접두사는 디스크의 dbsettings.ini 파일에 대한 모든 읽기를 방지합니다. 그 결과 레지스트리에서 찾을 수 없는 설정은 INI 파일에서 찾지 않습니다.

"데이터베이스" 레지스트리 항목에는 값에 @ 접두사가 없으므로 [데이터베이스] 섹션에 대해서만 레지스트리의 설정을 먼저 가져온 다음 디스크의 dbsettings.ini 파일에 있는 설정을 가져옵니다.

## Alternatives
Windows 95부터 Microsoft는 INI 파일보다 Windows 레지스트리 사용을 강력하게 장려하기 시작했습니다.[59] INI 파일은 일반적으로 두 가지 수준(섹션 및 속성)으로 제한되며 이진 데이터를 잘 처리하지 못합니다. 그러나 이 결정은 레지스트리가 모놀리식이고 불투명하며 이진이고 파일 시스템과 동기화되어야 하며 운영 체제의 단일 장애 지점을 나타낸다는 사실로 인해 비판에서 자유롭지 못했습니다[60].

나중에 XML 기반 구성 파일은 텍스트 파일의 구성을 인코딩하는 데 널리 사용되었습니다.[인용 필요] XML은 임의로 복잡한 레벨과 중첩을 허용하고 이진 데이터 인코딩을위한 표준 메커니즘을 가지고 있습니다.

최근에는 JSON, TOML, YAML과 같은 데이터 직렬화 형식이 구성 형식으로 사용될 수 있습니다. 이 세 가지 대체 형식은 임의로 중첩할 수 있지만 INI 파일과는 다른 구문을 사용합니다. 그 중 TOML은 INI와 가장 유사하지만, TOML을 INI의 대규모 하위 집합과 의도적으로 호환되게 만들려는 아이디어는 거부되었습니다.[61]

그러나 최신 INI 구문 분석기는 동일한 수준의 임의적인 XML, JSON, TOML 및 YAML 중첩을 허용하고, 동일한 것을 표현하는 여러 구문을 허용하여 INI 파일의 "비공식적 상태"를 유지하지만 유형 값과 유니코드에 대한 동등한 지원을 제공합니다[62].

