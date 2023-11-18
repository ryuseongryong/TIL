- https://lms.kmooc.kr/course/view.php?id=10039#section-2

# 데이터베이스의 등장 배경과 개념
- 데이터 처리 및 저장
- 데이터를 다루는 전통적인 방법
    1. 저장(정형화됨, 파일 시스템)
    2. 처리(개별 프로그램을 작성하여 처리)
- 파일시스템의 문제점
    1. 데이터 종속성(data dependency) : 데이터를 이용하는 응용 프로그램이 데이터의 구조(파일구조)의 변화에 영향을 받는 현상
    2. 데이터 무결성(data integrity)의 침해 : 데이터가 오류가 없는 정확한 값을 저장하고 있어야 함을 의미
    3. 데이터 중복성(data redundancy)과 데이터 불일치(data inconsistency) : 동일한 데이터가 여러 곳에 저장, 관리됨 = 저장공간 낭비, 보안 어려움 / 여러 곳에 저장된 동일 데이터의 내용이 다른 문제
    4. 데이터 보안성(data security)의 결여
- 대안으로 등장한 것이 데이터베이스 시스템
    - 데이터베이스와 DBMS, 두 가지로 구성됨
    - 데이터베이스 : 모아둔 데이터의 집합
    - DBMS : 데이터베이스를 관리하는 소프트웨어(Database Management System)
    - 파일 시스템에서는 파일에 직접 접근, 데이터베이스 시스템에서는 DBMS를 통해서만 접근
    1. 데이터 중복성 제거
    2. 보안성 강화
    3. 데이터 무결성 강화
    4. 데이터 종속성 완화
    - 과거 파일시스템의 문제점이 해결되었기 때문에 많이 사용됨
- 여러 종류의 데이터베이스 중 관계형 데이터베이스가 대부분 차지함.
    - 1970. IBM E.F.Codd 박사에 의해 관계형 데이터베이스 이론 제안
            Oracle 발표
    - 1983. IBM DB2 발표
    
# 실습환경 구축
- mysql community server download

---

# 데이터베이스 맛보기
- show databases;
- world database, sakila database 추가
    - download, source ~/filepath로 추가
- use world;
- show tables;
- desc country;
- select name, population from country where continent = 'Asia';
- select name, population from country where name = 'South Korea';

# 데이터베이스 시스템의 개념
- sql이라는 언어를 통해서 데이터베이스를 이용
- 데이터베이스 시스템은 DBMS <-> Database[File0, File1, File2] 구조
    - DBMS : 관리 SW
    - 데이터베이스 : 데이터의 집합체
    - 데이터의 저장 단위인 파일 = Table
- 데이터베이스 : 데이터를 한 곳에 체계적으로 모아 놓은 데이터 저장소 = 데이터 뱅크
    - 데이터베이스는 보통 물리 저장장치인 하드디스크에 구현함
    - 특정 폴더 아래 테이블을 파일 형태로 저장하는 형태가 있고,
    - 하나의 커다란 파일 안에 테이블을 저장하는 형태가 있다.
    - e.g. mysql : world database[city, country, country language, ...(tables)]
    - 데이터베이스에는 데이터와 데이터베이스를 관리하기 위한 정보(메타정보)도 함께 저장됨 : 사용자가 필요로 하는 테이블 + 시스템이 사용하는 테이블
        - 데이터베이스를 관리하는 정보를 시스템 카탈로그, 데이터 사전이라고 부르기도 함. : 사용자 계정정보, 권한정보, 테이블 목록 및 구조, 저장공간 정보, 사용 로그 등
        => 데이터에 대한 데이터 = 메타데이터
- DBMS : 데이터베이스를 관리하는 소프트웨어
    - e.g. mysqld.exe의 형태라고 window에서는 볼 수 있음
    - 백그라운드 프로세스로 상시 실행 가능
    - 데이터베이스의 성능 = DBMS의 성능
    - 기능
        - 데이터 정의 기능 : 사용자가 데이터베이스를 생성하거나
        데이터베이스 내 원하는 구조의 파일(테이블)을 생성/변경할 수 있도록 지원
        - 데이터 조작 기능 : 사용자가 데이터베이스 내의 파일(테이블)에 대해 조회하거나 데이터를 삽입, 수정, 변경, 삭제하는 기능을 지원
        - 데이터 제어 기능 : 다수의 사용자가 이요하는 데이터베이스 내의 데이터를 정확하고 안전하게 유지하는 기능 - 보안관리(접근제어), 병행수행 제어, 데이터베이스의 백업 및 복구
- 데이터베이스 : 데이터의 집합체

# 데이터베이스 사용자, 언어
- 최종 사용자(end user), 개발자, 관리자(DBA)
    - 최종 사용자(end user) : 이미 구축된 데이터베이스를 이용하는데 주된 관심
        - 캐주얼 사용자 : SQL을 이용하여 매번 다른 정보를 검색, 개발자, 기업 내부 사용자
        - 초보 사용자 : 이미 구축된 데이터베이스를 이용하는데 주된 관심, 데이터베이스의 존재를 알지 못하고 사용, REST API를 통해 구축된 시스템을 이용해 간접적으로 데이터베이스를 사용하는 의미인듯(e.g. 신용카드, 교통카드 이용, 인터넷 우편번호 조회 등)
    - 응용 프로그래머(Application Developer) : 데이터베이스를 이용하는 앱 개발자(초보 사용자가 사용하는 SW)
        - 대규모 정보시스템, 동영상 플랫폼, 일정 관리 프로그램 등
        - 개발언어 + SQL(ORM 이용) : 내장 SQL / 임베디드 SQL
    - 데이터베이스 관리자(DBA) : 일반관리자 ~ 최고관리자(DBA)
        - 데이터베이스 시스템의 운영, 관리에 대한  책임을 지고 있는 사용자
        - 현장 업무와 기술적인 지식 필요
        - SQL(Structured Query Language) : 관계형 데이터베이스 표준 언어
            - DMBS와 커뮤니케이션 하기 위한 언어
            - 한국의 인구와 GNP는 얼마인가? = SELECT name, population, GNP FROM country WHERE name='South Korea';
            - 아시아에 속한 국가들의 이름과 인구수는? = SELECT name, population FROM country WHERE continent='Asia';
            - 아시아에 속한 국가들의 GNP의 합계는? = SELECT SUM(GNP) FROM country WHERE continent='Asia';
            - 한국인의 기대수명을 80으로 바꾸시오 = UPDATE country SET LifeExpectancy = 80 WHERE name='South Korea';
            - New Stan이라는 신생국의 정보를 추가하시오 = INSERT INTO country (code, name, continent) values ('NST', 'New Stan', 'Asia');
            - NEW Stan에 대한 자료를 삭제하시오 = DELETE FROM country WHERE name='New Stan';
---
# 관계형 데이터베이스
# 데이터 모델의 개념
- 데이터를 어떤 형태로 저장할 것인가? 
    - 데이터 모델
        - 현실 세계에 존재하는 데이터(정보)를 컴퓨터 안에 어떻게 표현할 것인가를 나타내는 것
        - 데이터 요소와 이들 간의 관계를 시각적으로 표현
        - 논리적 모델 : 사용자의 눈으로 봤을 때 데이터가 어떤 모양으로 보이는가?(어떤 형태로 표현되고 관리되는가?)
            - DBMS가 어떤 논리적인 데이터 모델을 제공하는지에 따라서 : 계층형 DBMS -> 네트워크형 DBMS -> 관계형 DBMS
        - 물리적 모델 : 데이터를 저장장치에 저장할 때 어떤 모양으로 저장할 것인가?
        - 계층형 DBMS
            - 데이터들이 계층적 구조로 연결되어 있다고 보는 관점
            - 초기 DBMS 제품에서 많이 채택해서 사용되던 모델
            - 장점 : 구조가 간단, 데이터 수정이나 검색이 빠름
            - 단점 : 검색 경로가 한정적, 삽입과 삭제 연산이 매우 복잡
        - 네트워크형 DBMS
            - 계층형 모델의 단점을 보완한 모델
            - 네트워크 모델에서는 하나의 하위정보가 여러 개의 상위 정보와 연결
        - 관계형 DBMS
            - 정보 또는 데이터간 상하 개념이 존재하지 않음
            - 장점 : 유연한 정보 검색 가능
            - 단점 : 검색 속도가 계층형이나 네트워크 모델에 비해 떨어짐
            - 검색 속도는 다른 방법으로 극복 가능함
            - 오늘날 우리가 알고 있는 대부분의 DBMS제품들(오라클, MSSQL, MySQL 등)은 관계형 모델
        - 1960s : 일반적인 파일 시스템, 데이터베이스 이전 시대
        - 1970s : 계층형과 네트워크형, 계층형 메인, 70s후반 관계형 모델 제안
        - 1980s : 관계형 모델 활성화
        - 1990s : 객체 지향형(Object-oriented), 객체 관계형(Object-relational) 모델 등장, 데이터를 보는 관점이 달라짐
        - 2000s : 비정형데이터를 다루기 위한 데이터베이스 등장
- 저장된 데이터를 사용자들이 어떤 방법을 통해서 이용할 수 있게 할 것인가?
- 저장되는 데이터들이 오류가 없도록 어떻게 관리할 것인가?
# 관계형 모델
- 1970s E.F Codd에 의해서 제안됨(논문)
- 데이터간 물리적 링크가 존재하지 않음
- 사용자에게 데이터가 테이블의 형태로 보임
- 릴레이션(relation, 오늘날 테이블)
    - 데이터를 저장하는 기본 단위
    - 릴레이션과 릴레이션 구분을 위해 이름을 갖음(테이블 이름) 
    - 릴레이션들이 모여서 데이터베이스를 구성함
    - 데이터베이스 : 서로 다른 이름을 갖는 여러 릴레이션들의 집합
- 속성(attribute)
    - 릴레이션의 열(column)을 가리키는 용어
    - 릴레이션에 저장되는 정보 항목의 이름
    - 동일한 릴레이션 내에서는 중복된 속성이름이 존재할 수 없음
    - 차수(degree) : 한 릴레이션에 포함된 속성의 개수
        - 변동성이 적음
- 튜플(tupple)
    - 하나의 릴레이션에서 행(row)를 가리킴
    - STUDENT 릴레이션에서 하나의 튜플은 한 명의 학생에 대한 정보를 담고 있음
    - 카디널리티(cardinality) : 하나의 릴레이션에 포함된 튜플의 수
        - 변동성이 많음
- 도메인(domain)
    - 릴레이션에서 각 속성이 속성에 저장될 수 있는 값들의 집합
    - 릴레이션에 올바르지 않은 데이터가 입력되는 것을 방지할 목적으로 고안됨
    - 속성에 들어올 수 있는 값의 집합을 미리 정의함 / 도메인에 있는 값만 속성에 넣을 수 있음
    - E.F.Codd가 도메인 개념을 제안한 이유 : 릴레이션에 올바르지 않은 데이터가 입력되는 것을 막기 위해서
    - 실제 구현에서 현실적인 문제가 발생
        - 모든 경우의 수를 갖기 어려움
        - 오늘날 도메인의 취지를 살려서 일부 구현이 되어 있음
    - 도메인 : 올바른 데이터가 들어오는 것을 실현하기 위한 개념
- 기본키(primary key)
    - 릴레이션에서 각 튜플을 식별할 수 있는 어떤 속성(또는 속성의 집합)
    - 튜플을 구분하는데 기준이 되는 속성(column)
- 외래키(foreign key)
    - 두 릴레이션을 참조 관계로 맺어주는 속성(또는 속성의 집합)
- 파일시스템 - 관계형 모델 - 현실 사용
    - 파일 = 릴레이션 = 테이블
    - 필드 = 속성 = 열(컬럼)
    - 레코드 = 튜플 = 행(로우)
- 릴레이션의 특징
    - 속성의 원자성
        - 릴레이션의 각 튜플의 특정 속성은 원자 값(Atomic value)을 가져야 함
        - 원자 값 : 더 이상 쪼개면 의미를 상실하는 입력 값
    - 튜플의 유일성
        - 릴레이션에는 중복되는 튜플이 저장되는 안 된다는 특성
    - 튜플(과 속성)의 무순서 성질
        - 릴레이션에 저장되는 속성에도 순서라는 개념이 없음
    - 속성 이름의 유일성
        - 동일한 릴레이션 내에 같은 이름을 가진 속성이 중복해서 존재할 수 없음
        - 다른 릴레이션에는 동일한 이름을 가진 속성이 있을 수 있음(구분 가능)
    - 이런 속성이 지켜져야
        - 데이터 관리에 용이함
        - 잘못된 데이터가 들어오는 것을 막을 수 있음
        - 원하는 데이터를 조회할 수 있음
- 관계형 모델에서 제시된 모든 이론들이 구현된 것은 아님
- 대부분의 개념은 제품화하면서 적용됨

# 데이터 무결성 규칙
- 데이터베이스에 포함된 오류는 다양한 문제를 야기함
- 저장되는 데이터가 정확하고 유효한 상태로 유지되는 성질
- 데이터의 무결성 침해 사례
    - 몸무게가 5600KG으로 저장되는 경우
    - 이름이 홍길동56으로 저장되는 경우
    - 유통기한이 지난 재고 수량이 데이터에 포함된 경우
- DBMS 역할
    - 데이터 무결성을 최대한 지킬 수 있어야 함
    - DBMS가 쉽게 확인할 수 있는 무결성 침해 사례도 있지만, 그렇지 않은 경우도 있음
- 관계형 데이터 모델에서 요구하는 기본 무결성 규칙(DBMS에게 유지 책임이 있음)
    - 개체 무결성 규칙 : 릴레이션의 기본키 속성에는 널(null)값이 입력될 수 없음
        - 학번이 없는 학생
            - 학생을 구분할 수 없음
            - 학생에 대한 정보를 저장할 수 없음
        - 정보의 관리 대상은 모두 고유한 식별 번호가 붙어 있음 : 주민등록번호, 학번, 도서번호, 주문번호, 전화번호 등 -> 고유 식별번호 속성
        - DBMS 역할 : 튜플들이 입력될 때 학번에 어떤 값이 들어오는지 감시하고 학번이 없는 학생의 등록을 막음(개체 무결성 규칙 준수)
    - 참조 무결성 규칙
        - 참조하는 속성과 참조되는 속성사이에는 일관성이 있어야 함
        - DBMS 역할 : 외래키를 통해서 참조 관계를 맺어주면 참조 무결성 규칙을 지켜줄 수 있음
- 널(null) 값
    - 릴레이션에 저장될 수 있는 특별한 값
    - 사용자가 아무 값도 입력하지 않을 때 자동으로 저장
    - 없음을 나타내는 값이기 때문에 공백이나 0과는 다름
    - 릴레이션을 설계할 때 어떤 속성에 널 값이 입력되는 것을 허용할지 말지를 정해야 함
        - 학번, 주민등록번호, 학생 이름, 성별 등 반드시 있어야 하는 것에는 null이 허용되면 안 됨
        - 취미, 추가 연락처, 희망진로 등 필수가 아닌 것에는 허용 가능
- 요약
    - 개체 무결성 규칙 : 기본키 컬럼에는 널이 들어갈 수 없음
    - 참조 무결성 규칙 : 외래키로 연결되어 있을 때, 무결성 규칙을 사용자가 지정함
    - 기타 무결성 규칙 : DBMS마다 지원되는 어떤 기능의 범위가 다름(강하게 지원하는 경우 비용이 큼)

# MySQL 워크벤치의 기본 사용
- 오라클에서 제공하는 오픈소스 유틸리티 소프트웨어 GUI지원
- [워크벤치 / 콘솔] -> DBMS -> Database

---
# 관계 대수
- DBMS와 소통하기 위해 SQL을 사용해야 함

# 관계대수 개요
- E.F.Codd는 관계형 모델을 제안하면서 원하는 데이터를 추출할 수 있는 방법을 제시함
    - 관계 대수(relational algebra)
    - 관계 해석(relational calculus)
    - 위 두 가지는 데이터를 추출하는 능력은 동일함(표현력은 동등함)
    - 관계 대수란 테이블 형태의 데이터에서 원하는 정보를 어떻게 추출할 것인가라고 요약할 수 있음
- 수학연산과 유사하게 관계 대수의 연산도 표현할 수 있음
    - 연산의 대상, 연산의 결과 : 테이블
- 관계대수 연산의 특징
    - 관계 대수의 연산 대상(피연산자) : 릴레이션
    - 관계 대수의 연산 결과 : 릴레이션
    - 관계 대수 연산의 닫힘 성질(close property)라고 부름
- 관계 대수 연산자
    - 일반 집합 연산자
        - 합집합, 교집합, 차집합, 카디션 프로덕트
    - 순수 관계 연산자
        - 셀렉트, 프로젝트, 조인, 디비전
    - 주로 셀렉트, 프로젝트, 조인 세 가지를 사용함

# 일반 집합연산
- 합집합(∪) : 릴레이션 A와 릴레이션 B의 튜플들을 하나로 모은다.
    - 두 릴레이션의 속성의 개수(차수)가 같아야 한다.
    - 두 릴레이션에서 대응하는 속성의 도메인이 같아야 한다.(속성 이름은 달라도 된다.)
        = 합쳐지는 값의 성질이 같아야 한다.
- 교집합(∩) : 릴레이션 A와 릴레이션 B의 튜플들 중 중복되는 것들을 모은다.
    - 두 릴레이션의 속성의 개수와 대응하는 속성의 도메인이 같아야 연산 가능(합집합과 동일)
- 차집합(-) : 릴레이션 A에는 존재하지만 릴레이션 B에는 존재하지 않는 튜플들을 추출한다.
- 카티션 프로덕트(×) : 릴레이션 A의 모든 튜플에 대해 릴레이션 B의 모든 튜플들을 연결한다.

# 순수 관게연산
- 셀렉트(σ, σ조건식(A)) : 릴레이션 A에서 조건식을 만족하는 튜플들을 추출(cf. 테이블에서 행을 추출하는 연산)
    - 조건에 맞는 튜플들만 선택해서 새로운 릴레이션을 구성하는 것
    - 회원등급이 A이고 취미가 등산인 회원들의 정보를 보이시오
    - σ조건1(σ조건2(A)), σ조건1∧조건2(A) 형태로 사용 가능
- 프로젝트(π, π속성리스트(A)) : 릴레이션 A에서 리스트에 있는 속성들로만 구성된 튜플들을 추출(cf. 테이블에서 열을 추출하는 연산)
- 조인(▷◁) : 릴레이션 A와 B의 공통 속성을 이용하여 A와 B의 튜플들을 연결하여 새로운 릴레이션을 구성
- 디비전(÷) : 릴레이션 B의 모든 튜플과 관련이 있는 릴레이션 A의 튜플들을 추출
- 비교 연산자
    - >, >=, <, <=, =, <>(같지 않다, 다른 기호를 쓰는 경우도 있음 e.g. !=)
- 논리 연산자
    - ∧(and), ∨(or), ¬(not)
# 관계 대수의 응용
- 관계 대수 연산자를 적절히 활용하면 원하는 정보를 추출할 수 있다.
- 셀렉트, 프로젝트, 조인 연산자를 이해하자.
    - 프로젝트 회원이름, 취미(셀렉트 대전) : 회원과 대출 릴레이션 조인 -> 회원이름, 취미 속성 추출(프로젝션)
    - 홍길동 회원이 대출한 도서의 목록 : 회원과 대출 릴레이션 조인 -> 홍길동이 포함된 튜플 추출(셀렉션) -> 대출도서 속성 추출(프로젝션)

# SQL 언어 개요
- SQL : structured query language의 약자
    - 관계형 데이터베이스가 인기를 얻게 된 비결은 쉬운 SQL문법에 있음
    - 관계 대수 이론을 실제 사용할 수 있도록 언어 형태로 구현한 것
    - 표준화되어 모든 DBMS 제품에서 동일하게 사용 가능
- SQL의 명령어
    - DDL(Data Definition Language) : 데이터 정의어
        - CREATE : 데이터베이스 및 데이터베이스 내의 개체(테이블, 뷰, 인덱스 등)를 정의
        - ALTER : 데이터베이스 및 데이터베이스 내의 개체의 구조를 변경
        - DROP : 데이터베이스 및 데이터베이스 내의 개체를 삭제
    - DML(Data Mnipulation Language) : 데이터 조작어
        - INSERT : 테이블에 새로운 데이터(튜플)를 추가
        - UPDATE : 테이블에 저장된 데이터를 수정
        - DELETE : 테이블에 저장된 데이터(튜플)를 삭제
        - SELECT : 테이블에 저장된 데이터를 조건에 맞게 조회
    - DCL(Data Control Language) : 데이터 제어어
        - GRANT : 접근/사용 권한을 부여
        - REVOKE : 접근/사용 권한을 회수
- SQL 언어학습 : 가장 실용성이 높은 학습 주제
    - SQL 명령어나 테이블 이름, 컬럼 이름 등은 대소문자를 구분하지 않는다.
    - SQL 명령문은 한줄에 작성해도 되고, 여러줄에 걸쳐서 작성해도 된다.
    - SQL 문 뒤에는 세미콜론(;)을 붙인다. 세미콜론은 하나의 명령문의 끝을 의미한다. 그리고 명령문과 명령문을 구분하는 역할을 한다.
# 실습용 데이터베이스 설치
# SELECT문 개요
- 어떤 정보를 추출할 때 사용하는 명령문
- 데이터베이스의 목적은? 필요한 정보를 모아놓고 공유하는 시스템
    - 따라서 들어있는 데이터를 검색하는 일이 가장 많음 -> SELECT문을 많이 사용
- 기본 구조 : 
    SELECT 컬럼명 -> 필수
    FROM 테이블명  -> 필수
    WHERE 검색조건; -> 생략 가능
- 담당업무가 SALESMAN인 사원의 이름과 연봉
    - SELECT ename, sal FROM emp WHERE job='SALESMAN'; 
    - π이름,연봉(σ담당업무='SALESMAN'(사원))
- SELECT문의 실행 과정
    - SELECT ename, sal => 프로젝트(π)
    - FROM emp => 대상 테이블
    - WHERE job='SALESMAN'; => 셀렉트(σ)
- SELECT문 작성 팁
    - 기본 문법을 적는다.
    - 질의를 해결하기 위해서 어떤 테이블을 검색해야 하는가 = FROM 테이블명
    - 질의에서 요구되는 정보는 어떤 컬럼에 있는가 = SELECT 컬럼명
    - 데이터를 검색하기 위한 조건은 무엇인가 = WHERE 검색조건
- WHERE절에서 조건의 지정
    - WHERE절이 없으면 모든 튜플을 반환
    - 비교연산자들 : =, <>, >, >=, <, <=
    - 논리연산자
        - AND : 연결된 조건들을 모두 만족하는 튜플 검색
        - OR : 연결된 조건들 중 하나라도 만족하는 튜플 검색
        - NOT : 지정된 조건들을 만족하지 않는 튜플 검색
- WHERE절에서 값의 비교
    - 숫자, 문자, 날짜, null값(is 사용)
- 사원의 담당 업무 목록을 보이시오
    - SELECT job FROM emp; => 모든 job을 보여줌
    - SELECT DISTINCT job FROM emp => 모든 job 중 중복된 것을 제거하고 보여줌
- 와일드 문자(*) : 테이블에서 모든 컬럼을 의미

# SELECT문 추가사항
# 내장함수의 사용
- WHERE절에서 문자 컬럼의 부분 비교
    - LIKE : 문자 속성의 컬럼에 대해 지정한 문자열을 포함하는지 비교
    - % : LIKE와 함께 사용되며 임의의 개수인 문자를 표현
    - _ : LIKE와 함꼐 사용되며 하나의 문자를 표현
- WHERE절에서 값의 범위 지정
    - BETWEEN AND : 포함되는 값( >= AND <=)
    - NOT BETWEEN AND : 제외되는 값 (< OR >)
- WHERE절에서 비교할 값들의 집합을 지정
    - IN : 어느 하나라도 매칭이 되면 선택 (= OR = OR =)
    - NOT IN : 조건 값이 아닌 나머지 (<> AND <> AND <>)

# 정렬과 그룹
- 정렬 : 결과를 주어진 기준에 따라 튜플을 정렬하여 보여주는 기능
    - 담당업무가 SALESMAN인 사원에 대해 입사일자가 빠른 순으로 사원의 이름, 입사일자를 보이시오.
        - SELECT ename, hiredate 
        - FROM emp 
        - WHERE job = 'SALESMAN' 
        - ORDER BY hiredate ; -> 정렬을 위한 키워드
    - 정렬 기준
        - 오름차순(기본) : A - Z, ㄱ - ㅎ, 1 - 100
        - 내림차순 : Z - A, ㅎ - ㄱ, 100 - 1
    - 담당업무가 SALESMAN인 사원에 대해 연봉이 많은 순으로 사원의 이름과 연봉을 보이시오.
        - SELECT ename, sal
        - FROM emp
        - WHERE job = 'SALESMAN'
        - ORDER BY sal DESC ; -> 내림차순 정렬
    - 모든 사원의 부서번호, 이름, 담당업무를 보이되 8부서번호 순으로 정렬하여 보이시오. 같은 부서안에서는 이름 알파벳 순으로 정렬하시오.
        - SELECT deptno, ename, job
        - FROM emp
        - ORDER BY deptno, ename -> 두 기준으로 정렬
    - SQL 정렬 기준은 여러 개 지정 가능
- 그룹(GROUP) : 테이블에 대해서 어떤 질의를 했을 때 그 결과를 그룹으로 묶어서 봄
    - 각 부서번호별 사원의 수를 구하시오
        - SELECT deptno, COUNT(*) AS 사원수
        - FROM emp
        - GROUP BY deptno ; -> 그룹핑 후, COUNT(*) 튜플의 개수를 센다.
    - 각 부서번호별 평균 연봉을 구하시오
        - SELECT deptno, AVG(sal) AS 평균연봉
        - FROM emp
        - GROUP BY deptno ; -> deptno으로 그룹핑된 튜플의 평균값(sal)을 산출함
    - GROUP BY를 사용 시 SELECT 다음에 올 수 있는 컬럼들
        - GROUP BY에 사용한 컬럼
        - COUNT(), MAX(), MIN() 집계함수를 적용한 컬럼
        - 기타 컬럼은 에러가 나지는 않지만, 의미 없는 값이 온다.
- HAVING : GROUP BY를 적용한 결과에서 추가로 적용할 때 사용
    - 각 부서번호별 사원의 수를 구하시오. 단, 사원의 수가 5명 이상인 부서만 보이시오.
        - SELECT deptno, COUNT(*) AS 사원수
        - FROM emp
        - GROUP BY deptno
        - HAVING COUNT(*) >= 5 ;
    => 튜플에 대한 조건 = WHERE
    => GROUPING 결과에 대한 조건 = HAVING
- 각 부서번호별 사원의 수를 구하시오. 단, 사원의 수가 5명 이상인 부서만 보이되, 사원수가 많은 순으로 보이시오.
    - SELECT deptno, COUNT(*) AS 사원수
    - FROM emp
    - GROUP BY deptno -> 그룹핑
    - HAVING 사원수 >= 5 -> 조건지정
    - ORDER BY 사원수 DESC ; -> 정렬
- 각 부서번호별 급여합계를 구하시오. 단, 급여합계가 2500이상인 부서만 보이되 급여합계가 많은 순으로 하고 급여가 500 미만인 사원은 대상에서 제외하시오.
    - SELECT deptno, SUM(sal) AS 급여합계
    - FROM emp
    - WHERE sal >= 500
    - GROUP BY deptno
    - HAVING 급여합계 >= 2500
    - ORDER BY 급여합계 DESC ;

- LIMIT : 출력되는 데이터 제한 가능(비표준 문법이라 DBMS마다 조금씩 다를 수 있음)

# 기본키와 외래키
- 기본키(primary key)
    - 튜플을 식별하는 기준이 되는 컬럼
    - 개체 무결성 규칙을 구현하는 수단
        - 기본키 컬럼에는 null이 저장될 수 없음
        - 즉 테이블에 저장되는 튜플들은 중복된 것이 존재하면 안됨
    - 중복여부 검토를 위해 기본키 컬럼을 비교
    - 관련 용어
        - 후보키(candidate key) : 기본키가 될 수 있는 키, 식별자 역할이 가능한 키
        - 기본키(primary key)
        - 대체키(alternate key) : 기본키가 되지 않은 식별자 역할이 가능한 키
    - 역할
        - 튜플의 식별 기준이 되는 컬럼들
        - 튜플의 중복성 여부를 검토하는 기준
        - 검색을 빠르게 하기 위해 기본키 컬럼에는 인덱스가 설정됨(검색의 기준)
    - 데이터 조회나 검색에 주로 사용됨
- 외래키(참조 무결성 규칙 구현 수단)
    - 부모테이블과 자식테이블을 이어줄 때, 자식테이블에서 참조되는 키
    - 외래키는 항상 부모테이블의 기본키를 참조함
- 일반적으로 기본키와 외래키는 테이블이 생성될 때 설정됨
- 외래키에는 null값이 허용됨