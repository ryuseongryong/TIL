# Organizing host and group variables

- 변수를 기본 인벤토리 파일에 저장할 수 있지만 호스트 및 그룹 변수 파일을 별도로 저장하면 변수 값을 더 쉽게 정리할 수 있다. 또한 호스트 및 그룹 변수 파일에서 목록과 해시 데이터를 사용할 수 있지만 기본 인벤토리 파일에서는 사용할 수 없다.

- 호스트 및 그룹 변수 파일은 YAML 구문을 사용해야 한다. 유효한 파일 확장자에는 `.yml`, `.yaml`, `.json`, 파일 확장자가 없는 경우가 포함된다. 

# Ansible Best practice layout#2

```
inventories/
   production/
      hosts               # inventory file for production servers
      group_vars/
         group1.yml       # here we assign variables to particular groups
         group2.yml
      host_vars/
         hostname1.yml    # here we assign variables to particular systems
         hostname2.yml

   staging/
      hosts               # inventory file for staging environment
      group_vars/
         group1.yml       # here we assign variables to particular groups
         group2.yml
      host_vars/
         stagehost1.yml   # here we assign variables to particular systems
         stagehost2.yml

library/
module_utils/
filter_plugins/

site.yml
webservers.yml
dbservers.yml

roles/
    common/
    webtier/
    monitoring/
    fooapp/

```


### References
- https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#organizing-host-and-group-variables
- https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#alternative-directory-layout