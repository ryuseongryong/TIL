- https://kubernetes.io/ko/docs/tasks/administer-cluster/kubeadm/kubeadm-certs

- k8s의 서비스에 대한 certs는 기본적으로 1년이다.
- 인증서 기간 확인(`kubeadm certs check-expiration`)
    - certificate는 1년 기간
    - certificate authority는 10년 기간

- 자동 인증서 갱신은 kubeadm control plane을 업데이트 하는 경우에 업데이트 되는 것으로 안내한다.
- 수동 인증서 갱신은 `kubeadm certs renew all`
