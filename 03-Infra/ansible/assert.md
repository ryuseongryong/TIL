# Ansible variable validation with ansible.utils.assert

## Ansible variable validation을 하는 이유
- 아래의 변수들로부터 야기되는 플레이북 오류와 디벙깅 하기 어려운 런타임 오류, 부작용을 방지하기 위해
    - 정의되지 않은 변수
    - 유효하지 않은 변수

## Ansible variable validation
- ansible에는 기본 제공 데이터 유형이 별도로 없음
- assertions을 수동으로 구성해야 함
- ansible variable validation에 사용할 수 있는도 주요 도구는 Jinja2 테스트 및 필터 위에 빌드되는 `ansible.builtin.assert` 모듈이다.

## Fail as early as possible
- 가능한 한 빨리 실패하면 잘못된 구성을 최소화 할 수 있다.
- 일반적으로 잘못된 구성은 누락되거나 잘못된 시간 변수 유효성 검사로 인해 발생하며 다음 두 가지 범주에 속한다.
    - 부분 구성 : ansible이 이미 일부 작업을 실행한 후에 실패가 발생한다. 이 경우 때떄로 실행한 것에 대한 정리가 필요할 수 있다. 예를 들어 작업이 비활성 상태가 아닌 경우 부작용 없이 작업을 두 번 연속으로 실행하지 못할 수 있다.
    - 숨겨진 잘못된 구성 : ansible은 모든 것이 정상이라고 생각하지만 구성 파일에 잘못된(또는 누락된) 변수 값이 있을 때 발생한다. 이는 나중에 디버깅 하기 매우 까다로울 수 있다.
- 따라서 유효하지 않은 변수에 대해 실패할 뿐만 아니라 가능한 한 빨리 실패해야 한다. ansible 변수 유효성 검사를 위한 올바른 위치는 사용 사례에 따라 다르다.
    - Roles : top of <role>/tasks/main.yml
    - (Orchestration) playbooks : top of the playbook
- 그렇기 때문에 대부분의 경우 작업 실행 시 수행되는 변수 유효성 검사에 의존해서는 안 된다.
- 또한 includes 보다 imports를 사용하면 늦은 실패를 피할 수 있다. 역할이나 작업을 import하면 코드에 정적으로 추가된다. 즉 import는 가져온 역할이나 작업을 복사하여 자신의 코드에 붙여넣는 것과 거의 동일합니다. import의 긍정적인 측면은 ansible 실행이 시작되기 전에 변수의 유효성 검사를 할 수 있다는 것이다. 반면 includes는 플레이북이 이미 실행 중일 때 런타임에 평가되므로 누락되거나 유효하지 않은 변수는 오류를 일으킬 때까지 눈에 띄지 않을 수 있다.

## Minimal Ansible variable validation: 변수가 정의되어 있는지 확인하기
- 모든 변수에 대해 수행해야 하는 최소한의 점검은 변수가 존재하는지 확인하는 것이다. 
- tasks를 수행하기 전에 assert를 수행하면 최소로 필요한 모든 변수를 설정했는지 확인할 수 있다.
- 변수를 전달하지 않았다면 ansible은 오류 메시지와 함께 즉시 오류를 발생시킨다. 하지 않은 것보다는 낫지만 최적화는 아니다. 

## 변수가 특정 type인지 확인하기
- 변수가 특정 type인지 확인하는 것은 변수가 정의되었는지를 확인하는 것보다 한 단계 더 높은 단계이다.
```
- name: validate parameters
  ansible.builtin.assert:
    that:
      - my_string is string
      - my_integer is number
      - my_float is float
      - my_boolean is boolean
```

## 변수가 미리 정의된 집합에 속하는지 검증하기
- 정규표현식을 사용하여 제한된 값 집합을 취하는 문자열 변수의 경우 일치 항목이 매우 유용하다.
```
- name: validate parameters
  ansible.builtin.assert:
    that:
      - myrole_state is match ('^(present|absent)$')
```

## 변수의 값과 일치하는지 검증하기
- 일반적으로 변수가 하드코딩된 값과 일치하는지 확인하는 것은 거의 의미가 없다. 하지만 bool 연산자를 함께 사용하면 유용할 수 있다. 예를 들어 변수가 도메인 이름과 일치하는지 또는 특수 값인 none이 있는지 확인해야할 수 있다.
```
- name: Validate DNS domain name
  ansible.builtin.assert:
    that: domain_name is match ('^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)[A-Za-z]{2,6}') or domain_Name == 'none'

```
- 위 함수는 빈 문자열을 전달할 수 없을 때 특히 유용하다. 한 가지 예로 빈 값이 포함된 목록을 만들려고 할 때 막히는 set_fact를 들 수 있다.

## 복잡한 문자열 유효성 검사를 위한 정규식
- 정규식은 다음과 같이 DNS 이름이 유효성을 검사하는 데도 도움이 된다.
```
- name: validate parameters
  ansible.builtin.assert:
    that:
      - myrole_dnsname is match ('^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)[A-Za-z]{2,6}')
```
- 정규 표현식이 복잡해지면 오류가 발생할 확률도 크다.

## 숫자 값 검증
- 포트 번호 같은 숫자를 쉽게 확인할 수 있다.
```
- name: validate parameters
  ansible.builtin.assert:
    that:
      - myrole_port >= 1 and myrole_port <= 65535
```

## loop에서 여러 변수에 대한 유효성 검사
- 때로는 동일하게 복잡한 유효성 검사 규칙 집합이 필요한 변수가 많을 수 있다. 이 경우 loop를 사용하면 코드를 절약하고 코드 반복을 줄일 수 있다. 다음은 정규표현식을 이용한 도메인 이름 목록의 유효성 검사이다.
```
- name: Create list of DNS domain parameters for validation
  ansible.builtin.set_fact:
    dns_domains:
      - foo.example.org
      - bar.example.org
      - baz.example.org
- name: Validate DNS domains
  ansible.builtin.assert:
    that: dns_domain is match ('^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)[A-Za-z]{2,6}')
  loop: "{{ dns_domains }}"
  loop_control:
    loop_var: dns_domain

```

## list 길이 검증하기
- list 변수의 길이가 특정한 것으로 정해져야 한다고 예상되는 경우에 사용할 수 있다.
```
- name: Assert that list length is 1
  assert:
    that:
      - mylist|length == 1

```

## Validating task results
- 위에서 설명한 유효성 검사 전략은 입력 유효성 검사에 중점을 두고 있다. 
- Ansible 모듈을 개발할 때는 통합 테스트를 수행해야 하며, 이러한 맥락에서 tasks출력도 테스트하는 것이 매우 중요하다. 
- Ansible 모듈이 실행을 완료하면 변수로 등록할 수 있는 dictionary를 반환하고 `ansible.builtin.assert`로 검사할 수 있다.
- dictionary의 정확한 형식은 모듈마다 다르지만, 특별한 의미를 갖는 몇 가지 일반적인 사전 키(일종의 예약어)가 있다.
- 다음은 작업 반환 값을 사용하여 작업 결과의 유효성을 검사하기 위해 assert를 사용하는 방법에 대한 Ansible 모듈 중 하나인 keycloak_authz_permission의 예제이다.
```
- name: Create scope permission
  community.general.keycloak_authz_permission:
    auth_keycloak_url: "{{ url }}"
    auth_realm: "{{ admin_realm }}"
    auth_username: "{{ admin_user }}"
    auth_password: "{{ admin_password }}"
    state: present
    name: "ScopePermission"
    description: "Scope permission"
    permission_type: scope
    scopes:
      - "file:delete"
    policies:
      - "Default Policy"
    client_id: "{{ client_id }}"
    realm: "{{ realm }}"
  register: result
```
- 이 작업은 다음과 같은 사전을 반환한다.
```
TASK [keycloak_authz_permission : Create scope permission] *********************                                                                                                                                    changed: [testhost] =>
{
    "changed": true,
    "end_state": {
        "decisionStrategy": "UNANIMOUS",
        "description": "Scope permission",
        "logic": "POSITIVE",
        "name": "ScopePermission",
        "policies": ["570d477f-ac97-4c7b-8b9f-ae91454cc22d"],
        "resources": [],
        "scopes": ["ebbc7ca8-8f62-4822-87a6-6a05b5efb5d2"],
        "type": "scope"
    },
    "msg": "Permission created",
}   

```
- 결과를 확인하기 위해 반환된 사전을 변수에 등록하고 다음과 같이 그 내용을 확인할 수 있다.
```
- name: Assert that scope permission was created
  assert:
    that:
      - result is changed
      - result.end_state != {}
      - result.end_state.name == "ScopePermission"
      - result.end_state.description == "Scope permission"
      - result.end_state.type == "scope"
      - result.end_state.resources == []
      - len(result.end_state.policies) == 1
      - len(result.end_state.scopes) == 1
```
- 작업 정의와 실제 결과 객체 사이에 불일치가 있는 경우 어설션은 실패합니다. 이 방법은 테스트를 작성할 때 가장 유용하지만, 일반적인 플레이북에서도 사용할 수 있다.






- https://www.puppeteers.net/blog/ansible-quality-assurance-part-1-ansible-variable-validation-with-assert/