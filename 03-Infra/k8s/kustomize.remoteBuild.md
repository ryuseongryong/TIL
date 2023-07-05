# remote targets
- https://github.com/kubernetes-sigs/kustomize/blob/master/examples/remoteBuild.md

## remote directories

- kustomize build는 URL에서 실행할 수 있다. 리소스도 URL을 통해 다른 사용자 지정 디렉터리를 참조할 수 있다.
- URL 형식은 선택적 디렉터리와 일부 쿼리 문자열 매개변수가 있는 HTTPS 또는 SSH `git clone` URL이다. kustomize는 현재 URL에서 포트 지원은 되지 않는다. 디렉터리는 레포지토리 URL 뒤에 `//`를 추가하여 지정한다. 다음 쿼리 문자열 매개변수도 지정할 수 있다.
    - ref : 일반적으로 브랜치, 태그 또는 전체 커밋 해시(짧은 해시는 지원되지 않음)로 git에서 가져올 수 있는 참조이다.
    - version : ref와 동일하다. ref가 제공되면 무시된다.
    - timeout(default 27s) : 초 단위 숫자, 지속시간. 리소스를 가져오는 데 걸리는 시간 제한을 지정한다.
    - submodules(defulat true) : 서브 모듈을 복제할지 여부를 지정하는 bool값이다.
- 예를 들어, `https://github.com/kubernetes-sigs/kustomize//examples/multibases/dev/?ref=v1.0.6`은 기본적으로 HTTPS를 통해 git 리포지토리를 복제하고 v1.0.6을 체크아웃한 다음 examples/multibases/dev 디렉토리 내에서 kustomize 빌드를 실행한다.
    - `kubectl kustomize "github.com/kubernetes-sigs/gateway-api//config/crd?ref=v0.6.1"`
- SSH 클론은 `git@github.com:owner/repo` 또는 `ssh://git@github.com/owner/repo` URL을 통해서도 지원된다.

- `file:///` clone이 지원된다. 예를 들어, `file:///path/to/repo//someSubdir?ref=v1.0.6`은 리포지토리의 절대 경로인 `/path/to/repo`를 참조하고, 해당 리포지토리 내의 `someSubdir`에 있는 사용자 정의 디렉터리를 참조한다. `//` 를 사용하여 리포지토리의 루트를 구분한다. Kustomize는 리포지토리를 임시 디렉터리에 복제하고 참조를 새로 체크 아웃한다. 이 동작은 `/path/to/repo/someSubdir`와 같은 직접 경로 참조와 다르며, 이 경우 Kustomize는 Git을 전혀 사용하지 않고 경로에서 파일을 직접 처리한다.

