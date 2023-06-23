# 의존성 주입
- RDBMS를 사용하고자 하는 것은 정해졌으나, MySQL, PostgresQL 등 어떤 것을 쓸 지가 정해지지 않았거나, 각각 필요에 따라 사용할 상황이 있을 때, RDBMS의 형태로 spring 코드를 작성하면 JAVA spring에서 런타임을 읽어들여 어떤 DB를 사용할지 정해주는 것
- 즉 의존성을 JAVA가 주입시켜준다는 뜻