# CRIO container creation error
- https://access.redhat.com/solutions/5972661
- https://bugzilla.redhat.com/show_bug.cgi?id=1950536

- 서비스 설치 중 crio version이 업데이트 되어 있지 않아서 crio daemon을 restart함
- local-path pod에 다음과 같은 에러 발생
- k8s pod에서는 에러가 발생하면서 컨테이너 생성이 되지 않음
```
  Warning  Failed     10s                kubelet            Error: container create failed: time="2023-06-22T05:47:35Z" level=error msg="container_linux.go:380: starting container process caused: exec: \"local-path-provisioner\": executable file not found in $PATH"
```

- 이 문제는 하나 이상의 이미지에 영향을 줄 수 있음
- 일반적으로 오류는 특정 노드에 영향을 미친다.
- 이미지를 삭제하고 다시 다운로드해도 문제가 해결되지 않음
- 노드에서 crio나 podman, docker로 이미지를 직접 실행하려고 하면 다른 오류가 발생할 수 있음
```
$ podman run 2810ace6e1fe
readlink /var/lib/containers/storage/overlay: invalid argument"
```

## 해결책
- 해결 방법은 `/var/lib/containers/storage` 디렉터리에서 모든 이미지를 삭제하고 재부팅하는 것이다. 이를 수행하는 단계는 다음과 같다.
1. 문제가 있는 이미지가 있는 노드를 비움
2. 노드에 SSH로 접속하여 크리오 및 kubelet 서비스를 비활성화하고 재부팅
3. 노드에서 ssh를 다시 시작하고 노드에서 스토리지 오버레이 디렉터리를 삭제한 후, 크리오 및 kubelet 서비스를 활성화하고 시작, 루트 사용자로 실행
4. 몇 분간 기다렸다가 컨테이너가 다시 실행 중인지 확인.