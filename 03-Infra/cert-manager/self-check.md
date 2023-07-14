- https://cert-manager.io/docs/configuration/acme/dns01/#setting-nameservers-for-dns01-self-check

# Setting Nameservers for DNS01 Self Check
- cert-manager는 DNS01 challenge를 시도하기 전에 올바른 DNS 레코드가 있는지 확인한다. 기본적으로 cert-manager는 /etc/resolv.conf에서 가져온 재귀 이름 서버를 사용하여 권한이 있는 서버를 쿼리한 다음 직접 쿼리하여 DNS 레코드가 있는지 확인한다.
- 이 동작을 원하지 않는 경우(여러 권한 있는 nameservers 또는 split-horizon DNS), cert-manager controller는 이 동작을 변경할 수 있는 두 개의 플래그를 노출한다.
- `--dns01-recursive-nameservers` : cert-manager가 쿼리해야 하는 재귀 이름 서버의 호스트 및 포트가 쉼표로 구분된 문자열
- `--dns01-recursive-nameservers-only` : cert-manager가 확인을 위해 재귀 이름 서버만 사용하도록 함. 이 옵션을 사용하면 재귀 이름 서버에서 수행하는 캐싱으로 인해 DNS01 자체 확인이 더 오래 걸릴 수 있음

## Q. cert-manager를 통해 생성하려는 인증서가 waiting not yet propagated 상태에서 pending되어 있었는데, 그럼 원인은 AWS에 DNS레코드 확인이 되지 않아서인지?