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

- 일부 디렉터리에 다른 YAML 파일을 추가할 수 있음. e.g. 플랫폼별 작업을 별도의 파일에 배치하고 tasks/main.yml 파일에서 참조할 수 있다.(`import_tasks`)
- roles에는 library라는 디렉터리에 모듈, 기타 플러그인 types도 포함될 수 있음.

## Storing and finding roles
- 기본적으로 ansible은 다음의 위치에서 roles를 찾아서 실행한다.
    - collections을 사용하는 경우, collections에서 찾음
    - playbook file 기준으로 roles/ 디렉터리에서 찾음
    - 기본 검색 경로 : `~/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles`
    - playbook file이 있는 디렉터리에서 찾음

- roles를 다른 위치에 저장하는 경우 ansible에서 roles를 찾을 수 있도록 roles_path 구성 옵션을 설정할 수 있다. shared roles을 단일 위치로 확인하면 여러 playbooks에서 더 쉽게 사용할 수 있음.

- 또는 정규화된 경로를 사용하여 roles를 호출할 수 있음.

## Using roles
- roles는 3가지 방법으로 사용할 수 있다.
    - roles option을 사용하여 play 수준에서 사용(play에서 사용되는 고전적인 roles 사용 방법)
    - include_role을 사용하여 tasks 수준에서 사용(include_role을 사용하여 play의 tasks 섹션에서 roles를 동적으로 재사용 가능)
    - import_role을 tasks 수준에서 사용(import_role을 사용하여 play의 tasks 섹션에서 roles를 정적으로 재사용)

### Using roles at the play level
- roles를 사용하는 고전적인 방법은 주어진 플레이에 대한 roles 옵션을 사용하는 것
```
---
- hosts: webservers
  roles:
    - common
    - webservers
```
- play 수준에서 roles 옵션을 사용하는 경우 각 roles에 대해 X로 표시됨
    - `roles/x/tasks/main.yml`이 존재하면, ansible은 해당 파일에 있는 tasks를 play에 추가함
    - `roles/x/handlers/main.yml`이 존재하면, ansible은 해당 파일에 있는 handlers를 play에 추가함
    - `roles/x/vars/main.yml` / `roles/x/defaults/main.yml`이 존재하면, ansible은 해당 파일에 있는 변수를 play에 추가함
    - `roles/x/meta/main.yml`이 존재하면, ansible은 해당 파일에 있는 role dependency를 roles list에 추가함
    - 모든 복사본, 스크립트, 템플릿, include tasks(in the role)은 상대적 또는 절대적 경로를 지정하지 않고도 roles/x/{files,templates,tasks}/dir에 있는 파일을 참조할 수 있음.

## References
- https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-directory-structure
- https://www.digitalocean.com/community/tutorials/how-to-use-ansible-roles-to-abstract-your-infrastructure-environment

