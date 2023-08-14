23.3. Template Databases
- https://www.postgresql.org/docs/current/manage-ag-templatedbs.html

- `CREATE DATABASE`는 실제로 기존 데이터베이스를 복사하는 방식으로 작동한다.
  기본적으로 template1이라는 표준 시스템 데이터베이스를 복사한다. 
  따라서 이 데이터베이스는 새 데이터베이스를 만드는 '템플릿'이 된다.
  template1에 개체를 추가하면 이러한 개체는 이후에 생성되는 사용자 데이터베이스에 복사된다.
  이 동작을 통해 데이터베이스의 표준 개체 집합을 site-local에서 수정할 수 있다.
  예를 들어, template1에 절차적 언어 PL/Perl을 설치하면 해당 데이터베이스가 생성될 때 별도의 작업을 수행하지 않고도 사용자 데이터베이스에서 자동으로 사용할 수 있다.
- template0이라는 두 번째 표준 시스템 데이터베이스가 있다. 
  이 데이터베이스에는 template1의 초기 내용과 동일한 데이터, 즉 사용중인 PostgreSQL 버전에 의해 사전 정의된 표준 개체만 포함되어 있다. 
  데이터베이스 클러스터가 초기화된 후에는 template0을 절대 변경해서는 안된다.
  template1 대신 template0을 복사하도록 `CREATE DATABASE`에 지시하면 template1에 site-local 추가 사항이 없는 꺠긋한 사용자 데이터베이스(사용자 정의 개체가 존재하지 않고 시스템 개체가 변경되지 않은 데이터베이스)를 생성할 수 있다.
  이 기능은 pg_dump 덤프를 복원할 때 특히 유용하다.
  덤프 스크립트를 깨끗한 데이터베이스에서 복원해야 나중에 template1에 추가되었을 수 있는 개체와 충돌하지 않고 덤프된 데이터베이스의 올바른 내용을 다시 생성할 수 있다.

- template1 대신 template0을 복사하는 또 다른 이유는 template0을 복사할 때 새로운 인코딩 및 locale 설정을 지정할 수 있는 반면, template1의 복사본은 동일한 설정을 사용해야 하기 때문이다. 
  template1에는 인코딩별 또는 locale별 데이터가 포함될 수 있지만 template0에는 포함되지 않을 수 있기 때문이다.

- 설정 방법
  - `CREATE DATABASE dbname TEMPLATE template0;`
  - `createdb -T template0 dbname`

- 템플릿 데이터베이스를 추가로 생성할 수 있고, 실제로 클러스터의 모든 데이터베이스를 CREATE DATABASE의 템플릿으로 지정하여 복사할 수 있다.
  그러나 이것은 아직 범용 데이터베이스 복사 기능이 아니다.
  주요 제한 사항은 복사하는 동안 다른 세션은 소스 데이터베이스에 연결할 수 없다는 것이다.
  `CREATE DATABASE`가 시작될 때 다른 연결이 있으면 실패하며, 복사 작업 중에는 소스 데이터베이스에 대한 연결이 차단된다.

- 각 데이터베이스에 대해 두 가지 유용한 플래그가 pg_database에 존재한다.
  `datistemplate` 및 `datallowconn` 열 이다.
  `datistemplate`는 데이터베이스가 `CREATE DATABASE`의 템플릿으로 사용되도록 설정할 수 있다. 이 플래그가 설정되어 있으면 CREATEDB 권한이 있는 모든 사용자가 데이터베이스를 복제할 수 있으며, 설정되어 있지 않으면 수퍼유저와 데이터베이스 소유자만 데이터베이스를 복제할 수 있다.
  `datallowconn`이 false이면 해당 데이터베이스에 대한 새 연결이 허용되지 않는다.(false 설정 이후 기존 세션 종료는 되지 않음) template0 데이터베이스는 수정되지 않도록 일반적으로 datallowconn = false로 표시된다. 
  template0와 template1은 모두 항상 datistemplate = true여야 한다.

- template1과 template0은 template1이라는 이름이 CREATE DATABASE의 기본 소스 데이터베이스 이름이라는 사실 외에는 특별한 상태가 없다. 
  예를 들어 template1을 삭제하고 template0에서 다시 생성해도 아무런 문제 없이 사용할 수 있다. 
  이 작업은 template1에 부주의하게 많은 정크를 추가한 경우 권장할 수 있다. (template1을 삭제하려면 pg_database.datistemplate = false여야 한다.)

- 데이터베이스 클러스터가 초기화될 때 포스트그레스 데이터베이스도 생성된다. 
  이 데이터베이스는 사용자 및 애플리케이션이 연결할 기본 데이터베이스로 사용된다. template1의 복사본일 뿐이며 필요한 경우 삭제하고 다시 만들 수 있습니다.
