# background
- https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-secret-by-providing-credentials-on-the-command-line
```
kubectl create secret docker-registry regcred -o yaml --dry-run=cilent --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
```
- 위의 커맨드로 보면 토큰 값이 하나 주어진다. 해당 토큰을 base64 decode하면 json 구조의 docker registry secret이 나온다. 
- 이 중 auth key에 해당하는 value를 base64로 decode 해보면 padding이 추가된 값이 나오고, 해당 값을 써야 kubernetes에서 인식한다.
```
// padding이 추가된 결과값
YWJjZGVmZw==
```
- 이 부분은 base64에서 자동으로 padding을 계산하는 것 때문에 발생한다.
- https://stackoverflow.com/questions/4080988/why-does-base64-encoding-require-padding-if-the-input-length-is-not-divisible-by
- 해당 설명에 따르면 3Byte를 기준으로 이보다 작은 경우에는 각각 모자라는 Byte 수만큼 `=`로 대체한다고 되어 있다.
- 이것이 의미하는 것은 각 단어에 전체 길이를 나타내도록 하는 것인데, 인코딩할 전체 데이터의 길이를 알 수 있도록 하는 것이다.
- 각 청크의 길이를 미리 알 수 있도록 하는 것이고, 일부 상황에서는 필요한 기능이다.
- `echo "aasdf" | base64` 로 인코딩 했을 때 `YXNkZgo=` 이렇게 인코딩된다. 이것을 다시 디코딩해보면 한 줄이 더 생기게 된다. 
```
$ echo "YXNkZgo=" | base64 -d
asdf

```
- 문제가 발생한 부분이 이 부분이고, `echo`를 사용하여 인코딩을 하려고 한다면 trailing newline을 제거하는 `-n` 옵션을 사용하면 된다.