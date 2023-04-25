
## commands
```
apt update
apt-cache madison kubeadm
apt-mark unhold kubeadm && apt-get update && apt-get install -y kubeadm=1.27.1-00 && apt-mark hold kubeadm
kubeadm upgrade apply v1.27.1

kubectl drain node2 --ignore-daemonsets --delete-emptydir-data --force
apt-mark unhold kubelet kubectl && apt-get update && apt-get install -y kubelet=1.27.1-00 kubectl=1.27.1-00 && apt-mark hold kubelet kubectl

[crio 새로운 버전으로 upgrade with ansible playbook]

sudo systemctl daemon-reload
sudo systemctl restart kubelet [crio]
```

## Reference
- https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/