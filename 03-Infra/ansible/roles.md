# Roles
- roles을 사용하면 알려진 파일 구조를 기반으로 관련 vars, files, tasks, handlers, 기타 Ansible 요소들을 자동으로 로드할 수 있다. 콘텐츠를 역할로 그룹화하면 쉽게 재사용하고 다른 사용자와 공유할 수 있다.

## Role directory structure
- Ansible 역할에는 8개의 주요 표준 디렉터리가 있는 정의된 디렉터리 구조가 있다. 각 역할에 이런 디렉터리 중 하나 이상을 포함해야 한다. 역할에서 사용하지 않는 디렉터리는 생략할 수 있다.

```
roles/
    common/               # 이 계층 구조는 roles을 나타냄
        tasks/            #
            main.yml      #  <-- 필요한 경우 작업 파일에 더 작은 파일을 포함할 수 있음.
        handlers/         #
            main.yml      #  <-- handlers file
        templates/        #  <-- 템플릿 리소스와 함께 사용할 파일
            ntp.conf.j2   #  <------- templates end in .j2
        files/            #
            bar.txt       #  <-- copy resource와 함께 사용할 파일
            foo.sh        #  <-- 스크립트 리소스와 함께 사용할 스크립트 파일
        vars/             #
            main.yml      #  <-- variables associated with this role
        defaults/         #
            main.yml      #  <-- roles의 기본 우선 순위가 낮은 변수
        meta/             #
            main.yml      #  <-- role dependencies
        library/          # roles can also include custom modules
        module_utils/     # roles can also include custom module_utils
        lookup_plugins/   # or other types of plugins, like lookup in this case

    webtier/              # same kind of structure as "common" was above, done for the webtier role
    monitoring/           # ""
    fooapp/               # ""

```

- 기본적으로 Ansible은 역할 내의 각 디렉터리에서 관련 콘텐츠가 있는 main.yaml(또는 main) 파일을 찾는다.
    - task/main.yml : roles이 실행하는 작업의 기본 목록
    - handlers/main.yml : roles 내부 또는 외부에서 사용할 수 있는 핸들러
    - library/my_module.py : roles 내에서 사용할 수 있는 모듈
    - default/main.yml : roles의 기본 변수. 사용 가능한 변수 중 우선순위가 가장 낮고, 인벤토리 변수를 비롯한 다른 변수로 쉽게 재정의 할 수 있음
    - vars/main.yml : roles에 대한 기타 변수
    - files/main.yml : roles이 배포하는 파일
    - templates/main.yml : roles이 배포하는 템플릿
    - meta/main.yml : roles 종속성 및 지원되는 플랫폼과 같은 선택적 Galaxy 메타데이터를 포함한 역할의 메타데이터


- https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-directory-structure

