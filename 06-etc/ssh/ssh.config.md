# reverse-ssh로 연결하는데, 옵션을 사용하여 연결의 안정성을 보장하는 방법

- 관리가 필요한 PC를 reverse-ssh를 특정 서버와 연결하여 관리하는 환경
- PC의 reverse-ssh는 system daemon의 서비스로 script를 통해 실행한다.
- 이 때 실행되는 ssh 명령어 script를 통해 연결되는 ssh에 문제가 있는 것을 확인함

## 문제점
- 문제는 reverse-ssh를 연결하는 system daemon의 연결 확인에 있었다.
- system daemon은 정상적으로 연결된 시점을 기준으로 잘 연결되고 있다고 daemon에서 표시하고 있지만, 실제로 network가 끊기는 등의 이유로 인해 reverse-ssh를 수신하는 sshd에서는 연결이 끊겨져 있는 상황이 있었다.