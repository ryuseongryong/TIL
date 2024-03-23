- https://ko.wikipedia.org/wiki/MIME

MIME(영어: Multipurpose Internet Mail Extensions)는 전자 우편을 위한 인터넷 표준 포맷이다. 전자 우편은 7비트 ASCII 문자를 사용하여 전송되기 때문에 8비트 이상의 코드를 사용하는 문자나 이진 파일들은 MIME 포맷으로 변환되어 SMTP로 전송된다. 실질적으로 SMTP로 전송되는 대부분의 전자 우편은 MIME 형식이다. MIME 표준에 정의된 content types은 HTTP와 같은 통신 프로토콜에서 사용되며, 점차 그 중요성이 커지고 있다.

## 개요
기본적으로 인터넷 전자 우편 전송 프로토콜인 SMTP는 7비트 ASCII 문자만을 지원한다. 이것은 7비트 ASCII 문자로 표현할 수 없는 영어 이외의 언어로 쓰인 전자 우편은 제대로 전송될 수 없다는 것을 의미한다. MIME은 ASCII가 아닌 문자 인코딩을 이용해 영어가 아닌 다른 언어로 된 전자 우편을 보낼 수 있는 방식을 정의한다. 또한 그림, 음악, 영화, 컴퓨터 프로그램과 같은 8비트짜리 이진 파일을 전자 우편으로 보낼 수 있도록 한다. MIME은 또한 전자 우편과 비슷한 형식의 메시지를 사용하는 HTTP와 같은 통신 프로토콜의 기본 구성 요소이다. 메시지를 MIME 형식으로 변환하는 것은 전자 우편 프로그램이나 서버 상에서 자동으로 이루어진다.

전자 우편의 기본적인 형식은 RFC 2821에서 정의하고 있다. 이 문서는 RFC 822를 대체한다. 이 문서는 텍스트 전자 우편의 헤더와 본문의 형식을 명시하고 있으며, 그중에는 우리에게 익숙한 "To:", "Subject:", "From:", "Date:" 등의 헤더가 포함되어 있다. MIME은 메시지의 종류를 나타내는 content-type, 메시지 인코딩 방식을 나타내는 content-transfer-encoding과 같은 추가적인 전자 우편 헤더를 정의하고 있다. MIME은 또한 ASCII가 아닌 문자를 전자 우편 헤더로 사용할 수 있도록 규정하고 있다.

MIME은 확장 가능하다. MIME 표준은 새로운 content-type과 또 다른 MIME 속성 값을 등록할 수 있는 방법을 정의하고 있다.

MIME의 명시적인 목표 중 하나는 기존 전자 우편 시스템과의 호환성이다. MIME을 지원하는 클라이언트에서 비 MIME가 제대로 표시될 수 있고, 반대로 MIME을 지원하지 않는 클라이언트에서 간단한 MIME 메시지가 표시될 수 있다.

## MIME 헤더
### MIME-Version
이 헤더는 해당 메시지가 MIME 형식임을 나타낸다. 현재 사용되는 값은 "1.0"이므로 아래와 같이 사용할 수 있다.

MIME-Version: 1.0

### Content-Type
이 헤더는 메시지의 타입과 서브타입을 나타낸다. 예를 들면

Content-Type: text/plain

타입과 서브타입을 합쳐 MIME 타입이라 부른다. Internet media type 이라고도 부른다. 다양한 파일 포맷이 MIME 타입으로 등록되어 있다. text 타입은 charset 인자를 가질 수 있으며 이 인자는 문자 인코딩을 지정한다.

content-type 헤더와 MIME 타입은 전자 우편을 위해 정의된 것이지만, 이제는 HTTP, SIP와 같은 인터넷 프로토콜에서 함께 사용하고 있다. MIME 타입 등록은 IANA에서 관리하고 있다.

multipart 메시지 타입을 통해 MIME은 트리 구조의 메시지 형식을 정의할 수 있다. 이 방식은 다음을 지원한다.

- text/plain을 통한 단순 텍스트 메시지 ("Content-type:"의 기본값")
- 첨부가 포함된 텍스트 (text/plain 파트와 텍스트가 아닌 파트로 구성된 multipart/mixed). 파일을 첨부한 MIME 메시지는 "Content-disposition:" 헤더를 통해 파일의 본래 이름을 지정한다. 파일의 종류는 MIME의 content-type 헤더와 파일 확장자를 통해 알 수 있다.
- 원본 메시지가 첨부된 답장 메시지 (text/plain 파트와 원본 메시지를 나타내는 message/rfc822 파트로 구성된 multipart/mixed)
- 평문 텍스트와 HTML과 같이 다른 포맷을 함께 보낸 메시지 (multipart/alternative)
- 그 외 다양한 메시지 구조들

### Content-Transfer-Encoding
MIME (RFC 2045)는 바이너리 데이터를 ASCII 텍스트 형식으로 변환하기 위한 몇가지 방법을 정의하고 있다. content-transfer-encoding MIME 헤더를 통해 변환 방식을 지정한다. RFC 문서와 전송 인코딩에 대한 IANA 목록은 다음을 정의하고 있다.

- 일반 SMTP에 사용 가능
    - 7bit - [1..127]의 ASCII 코드로 이루어진 데이터로 줄 단위로 표현하며 각 줄을 CR, LF로 끝난다. 한 줄의 최대 길이는 CR (ASCII 코드 13), LF (ASCII 코드 10)를 제외하고 998자이다.
    - quoted-printable - 약간의 바이너리 데이터가 포함된 US-ASCII로 이루어진 텍스트 데이터를 표현할 때 효과적이다. US-ASCII는 특별한 변환을 거치지 않고 그대로 표시되기에 효율적이며 인코딩한 데이터를 사람이 이해할 수 있다.
    - base64 - 임의의 바이너리 데이터를 7비트 데이터로 변환한다. 고정된 오버헤드가 발생하고 비 텍스트 데이터의 변환 시 사용한다.
- 8BITMIME 지원하는 SMTP 서버에 사용 가능
    - 8bit - 8비트로 표현된 데이터로 한 줄 당 998자로 표현하며 CR, LF로 끝난다.
    - binary - 일련의 octets. SMTP에서는 사용할 수 없다.

## Encoded-Word
RFC 2822의 정의에 따르면 메시지 헤더와 그 값은 항상 ASCII 문자를 사용해야 한다. ASCII가 아닌 헤더 값은 MIME의 encoded-word 문법(RFC 2047)에 따라 인코딩해야 한다. 이 문법은 원본 문자 인코딩("문자셋")과 원본 데이터를 ASCII 문자로 변환하는 데 사용한 인코딩 방식을 포함한다.

encoded-word의 형식: "=?문자셋?인코딩 방식?인코드된 데이터?=".

- 문자셋은 보통 utf-8을 사용한다. 하지만 IANA에 등록된 어떤 문자셋도 사용 가능하다.
- 인코딩 방식은 quoted-printable 인코딩 방식과 비슷한 Q-encoding 방식을 나타내는 "Q"나 base64 인코딩을 나타내는 "B" 중 하나를 사용할 수 있다.
- 인코드된 데이터는 인코딩 방식에 의해 변환된 데이터이다.
Q-encoding과 quoted-printable의 차이

RFC 2047에 따르면, encoded-word는 공백 문자(white space)를 포함해서는 안 된다. 따라서 ASCII 코드로 20h(iso-8859-1에서의 스페이스)인 문자는 인코딩을 거쳐야 한다. ASCII 20h(20h가 공백이 아닐지라도)인 문자는 보통 "_" 문자(ASCII 5Fh)로 변환한다. 공백을 "=20"으로 인코딩한 것보다 이 방식이 인코드된 데이터의 가독성을 높여준다.

예를 들어,

Subject: =?utf-8?Q?=C2=A1Hola,_se=C3=B1or!?=

위 문장은 "Subject: ¡Hola, señor!"를 인코딩한 데이터이다.

encoded-word 형식은 헤더 이름에는 사용할 수 없다. 헤더 이름은 항상 US-ASCII로 표현해야 한다.
