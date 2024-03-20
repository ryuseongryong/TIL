- https://www.akadia.com/services/ora_bind_variables.html

# 변수 바인딩 - 애플리케이션 성능의 열쇠

한동안 오라클에서 애플리케이션을 개발해 왔다면 다음과 같은 개념을 접해 보셨을 것입니다. "변수 바인딩". 바인드 변수는 전문가들이 애플리케이션 성능의 핵심으로 자주 언급하는 오라클 개념 중 하나이지만, 변수가 정확히 무엇이고 이를 사용하기 위해 프로그래밍 스타일을 어떻게 변경해야 하는지 정확히 파악하기가 쉽지 않은 경우가 많습니다.

바인드 변수를 이해하려면 테이블에 대해 수천 개의 SELECT 문을 생성하는 애플리케이션을 예로 들어 보겠습니다:

```sql
SELECT fname, lname, pcode FROM cust WHERE id = 674;
SELECT fname, lname, pcode FROM cust WHERE id = 234;
SELECT fname, lname, pcode FROM cust WHERE id = 332;
```

쿼리가 제출될 때마다 Oracle은 먼저 공유 풀에서 이 문이 이전에 제출된 적이 있는지 확인합니다. 이전에 제출된 적이 있는 경우 이 문이 이전에 사용한 실행 계획을 검색하고 SQL을 실행합니다. 공유 풀에서 해당 문을 찾을 수 없는 경우, 오라클은 해당 문을 구문 분석하고 다양한 실행 경로를 파악하여 최적의 액세스 계획을 수립하는 과정을 거쳐야만 실행할 수 있습니다. 이 프로세스를 '하드 파싱'이라고 하며, OLTP 애플리케이션의 경우 실제로 DML 명령어 자체를 수행하는 데 더 오랜 시간이 걸릴 수 있습니다.

공유 풀에서 일치하는 문을 찾을 때는 문 텍스트와 정확히 일치하는 문만 고려되므로, 제출하는 모든 SQL 문이 고유한 경우(id = 674에서 id=234 등으로 매번 술어가 바뀌는 경우) 일치하는 문이 없을 것이며, 제출하는 모든 문을 하드 파싱해야 할 것입니다. 하드 구문 분석은 CPU를 많이 사용하며 주요 공유 메모리 영역에 대한 래치를 확보해야 하므로 작은 데이터 집합에 대해 실행되는 단일 프로그램에는 영향을 미치지 않지만, 수백 개의 프로그램 복사본이 동시에 문을 하드 구문 분석하려고 하면 다중 사용자 시스템이 무릎을 꿇을 수 있습니다. 이 문제의 추가 보너스는 하드 구문 분석으로 인한 경합이 사용 가능한 메모리, 프로세서 수 증가 등의 조치에 거의 영향을 받지 않는다는 점입니다. 하드 구문 분석은 Oracle이 다른 많은 작업과 동시에 수행할 수 없기 때문에 개발 시스템을 레코드 하위 집합을 작업하는 단일 사용자에서 전체 데이터 집합을 작업하는 수백 명의 사용자로 확장하려고 할 때만 종종 드러나는 문제이기 때문이죠.

오라클이 이러한 문에 대한 실행 계획을 재사용하도록 하는 방법은 바인드 변수를 사용하는 것입니다. 바인드 변수는 리터럴 (예: 674, 234, 332) 대신 사용되는" 치환" 변수로, 쿼리가 실행될 때마다 정확히 동일한 SQL을 Oracle에 전송하는 효과가 있습니다. 예를 들어, 저희 애플리케이션에서는 다음과 같이 제출합니다.

```sql
SELECT fname, lname, pcode FROM cust WHERE id = :cust_no;
```

이번에는 실행 계획을 매번 재사용할 수 있게 되어 SGA의 래치 활동이 줄어들어 총 CPU 활동이 줄어들고, 이는 애플리케이션이 대규모 데이터 세트에서 많은 사용자로 확장할 수 있는 효과를 가져옵니다.

## SQL*Plus에서 변수 바인딩

SQL*Plus에서는 다음과 같이 바인드 변수를 사용할 수 있습니다:

```sql
변수 부서 번호
exec :부서 번호 := 10
select * from emp where deptno = :부서 번호;

```

이제 SELECT 문에서 리터럴 값을 가져와서 자리 표시자(바인드 변수)로 바꾸고, 문이 처리될 때 SQL*Plus가 바인드 변수 값을 Oracle에 전달합니다. 이 부분은 매우 간단합니다(SQL*Plus에서 바인드 변수를 선언한 다음 SELECT 문에서 바인드 변수를 참조하면 됩니다).

## PL/SQL에서 변수 바인딩

PL/SQL을 먼저 살펴보면, 좋은 소식은 PL/SQL 자체가 바인드 변수와 관련된 대부분의 문제를 처리한다는 점이며, 사용자가 작성하는 대부분의 코드가 사용자도 모르게 이미 바인드 변수를 사용하고 있을 정도입니다. 예를 들어 다음 PL/SQL을 살펴봅시다:

```sql
create or replace procedure dsal(p_empno in number)
as
  begin
    update emp
    set sal=sal*2
    where empno = p_empno;
    commit;
  end;
/

```
이제 p_empno를 바인드 변수로 대체해야 한다고 생각할 수 있습니다. 하지만 좋은 소식은 PL/SQL 변수에 대한 모든 참조가 실제로는 바인드 변수라는 것입니다.

## 동적 SQL
사실 PL/SQL로 작업할 때 바인드 변수를 사용하기로 의식적으로 결정해야 하는 경우는 동적 SQL을 사용할 때뿐입니다.

동적 SQL을 사용하면 실행 즉시 명령을 사용하여 SQL이 포함된 문자열을 실행할 수 있습니다. 다음 예제는 제출될 때 항상 하드 파싱이 필요합니다:
```sql
create or replace procedure dsal(p_empno in number)
as
  begin
    execute immediate
     'update emp set sal = sal*2 where empno = '||p_empno;
  commit;
  end;
/


```
대신 바인드 변수를 사용하는 방법은 다음과 같이 EXECUTE IMMEDIATE 명령을 변경하는 것입니다:
```sql
create or replace procedure dsal(p_empno in number)
as
  begin
    execute immediate
     'update emp set
     sal = sal*2 where empno = :x' using p_empno;
  commit;
  end;
/


```
여기까지가 전부입니다. 하지만 한 가지 명심해야 할 점은 실제 개체 이름(테이블, 뷰, 열 등)을 바인드 변수로 대체할 수 없고 리터럴만 대체할 수 있다는 것입니다. 객체 이름이 런타임에 생성되는 경우에도 이러한 부분을 문자열로 연결해야 하며, 동일한 객체 이름이 나올 때만 공유 풀에 이미 있는 객체 이름과 일치하는 SQL이 실행됩니다. 그러나 동적 SQL을 사용하여 문에서 술어 부분을 구성할 때마다 바인드 변수를 사용하면 래치 경합이 발생하는 양을 크게 줄일 수 있습니다.

## 성능 킬러

성능 측면에서 얼마나 큰 차이를 가져올 수 있는지 아주 작은 테스트만 실행해도 알 수 있습니다:

성능 킬러는 다음과 같습니다 ....
```sql
SQL> alter system flush shared_pool;
SQL> set serveroutput on;

declare
      type rc is ref cursor;
      l_rc rc;
      l_dummy all_objects.object_name%type;
      l_start number default dbms_utility.get_time;
  begin
      for i in 1 .. 1000
      loop
          open l_rc for
          'select object_name
             from all_objects
            where object_id = ' || i;
          fetch l_rc into l_dummy;
          close l_rc;
          -- dbms_output.put_line(l_dummy);
      end loop;
      dbms_output.put_line
       (round((dbms_utility.get_time-l_start)/100, 2) ||
        ' Seconds...' );
  end;
/
101.71 Seconds...


```
... 그리고 여기 퍼포먼스 수상자가 있습니다:
```sql
declare
      type rc is ref cursor;
      l_rc rc;
      l_dummy all_objects.object_name%type;
      l_start number default dbms_utility.get_time;
  begin
      for i in 1 .. 1000
      loop
          open l_rc for
          'select object_name
             from all_objects
            where object_id = :x'
          using i;
          fetch l_rc into l_dummy;
          close l_rc;
          -- dbms_output.put_line(l_dummy);
      end loop;
      dbms_output.put_line
       (round((dbms_utility.get_time-l_start)/100, 2) ||
        ' Seconds...' );
end;
/

1.9초...
```
사실 이렇게 하면 실행 속도가 훨씬 빨라질 뿐만 아니라(쿼리를 파싱하고 실제로 실행하는 데 더 많은 시간을 할애했습니다!) 더 많은 사용자가 동시에 시스템을 사용할 수 있습니다.

## VB, Java 및 기타 애플리케이션의 변수 바인딩

다음 질문은 오라클 데이터베이스에 대해 SQL 쿼리를 실행하는 VB, Java 및 기타 애플리케이션은 어떨까요? 이들은 바인드 변수를 어떻게 사용할까요? 실제로 SQL을 바인드 변수를 설정하는 문과 문 자체를 위한 두 개의 문으로 분할해야 할까요?

사실 이에 대한 답은 아주 간단합니다. Java나 VB 등을 사용하여 SQL 문을 작성할 때는 일반적으로데이터베이스에 액세스하기 위한 API(VB의 경우 ADO, Java의 경우 JDBC)를 사용합니다. 이러한 모든 API에는 바인드 변수에 대한 기본 지원이 내장되어 있으며, 문자열을 직접 연결하여 데이터베이스에 제출하는 대신 이 지원을 사용하기만 하면 됩니다.

예를 들어 Java에는 바인드 변수를 사용할 수 있는 PreparedStatement와 문자열 연결 방식을 사용하는 Statement가 있습니다. 바인드 변수를 지원하는 메서드를 사용하는 경우 API 자체가 런타임에 바인드 변수 값을 Oracle에 전달하며, 사용자는 평소처럼 SQL 문을 제출하기만 하면 됩니다. 바인드 변수 값을 오라클에 별도로 전달할 필요가 없으며, 실제로 개발자의 추가 작업도 필요하지 않습니다. 바인드 변수에 대한 지원은 Oracle에만 국한된 것이 아니라 Microsoft SQL Server와 같은 다른 RDBMS 플랫폼에서도 공통적으로 지원되므로, Oracle 전용 기능이라고 해서 사용하지 않을 이유가 없습니다.

## 결론

마지막으로, 바인드 변수가 적절하지 않을 수 있는 몇 가지 경우를 염두에 둘 필요가 있습니다. 일반적으로 쿼리가 1초에 여러 번 실행되는 대신(OLTP 시스템처럼) 실제로 쿼리를 실행하는 데 몇 초, 몇 분 또는 몇 시간이 걸리는 경우, 즉 의사 결정 지원 및 데이터 웨어하우징에서 이러한 상황이 발생할 수 있다는 점을 유념할 필요가 있습니다. 이 경우 쿼리를 하드 파싱하는 데 걸리는 시간은 전체 쿼리 실행 시간의 일부에 불과하며, 하드 파싱을 피함으로써 얻을 수 있는 이점은 쿼리 최적화 프로그램에 제공되는 중요한 정보의 감소보다 더 클 수 있습니다. 실제 술어를 바인드 변수로 대체하면 최적화 프로그램이 열의 데이터 분포와 값을 비교할 수 있는 기능이 제거되므로 전체 테이블 스캔이나 인덱스가 적절하지 않은 경우 인덱스를 선택하게 될 수 있기 때문입니다. Oracle 9i는 바인드 변수 피킹이라는 기능을 사용하여 이 문제를 해결하는데, 이 기능을 통해 Oracle은 바인드 변수 뒤에 있는 값을 확인하여 최상의 실행 계획을 선택할 수 있습니다.

바인드 변수 및 데이터 웨어하우징 쿼리의 또 다른 잠재적 단점은 바인드 변수를 사용하면 스타 변환이 허용되지 않아 스타 스키마에서 팩트 및 차원 테이블을 효율적으로 조인하는 이 강력한 옵션이 사라진다는 점입니다.