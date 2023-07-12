- kubectl kustomize --enable-helm으로 설치 시,
```
resource mapping not found for name: "stats-filter-1.13" namespace: "istio-system" from "STDIN": no matches for kind "EnvoyFilter" in version "networking.istio.io/v1alpha3"
ensure CRDs are installed first
```
와 같은 에러가 발생함
- 실제로는 설치되고 있지만, crd설치 시간보다 해당 crds를 사용하여 설치하는 서비스의 명령이 더 빠르기 때문에 발생함
- 이와 관련된 helm 문서
- https://helm.sh/docs/chart_best_practices/custom_resource_definitions/

# Custom Resource Definitions
- 사용자 지정 리소스 정의 개체를 만들고 사용하는 방법에 대해 다룬다.
- CRD로 작업할 때는 두 가지 다른 부분을 구분하는 것이 중요하다.
    - CRD의 선언이 있다. CustomResourceDefinition 종류가 있는 YAML 파일이다.
    - CRD를 사용하는 리소스가 있다. apiVersion과 kind가 모두 CRD를 사용하는 리소스이다.

## Install a CRD Declaration before using the Resource
- Helm은 쿠버네티스에 가능한 한 많은 리소스를 최대한 빨리 로드하도록 최적화되어 있다.
- 설계상, 쿠버네티스는 전체 매니페스트 세트를 가져와서 모두 온라인으로 가져올 수 있다.(이를 조정:reconciliation 루프라고 함)
- 하지만 CRD와는 차이가 있다.
- CRD의 경우 해당 CRD 종류의 리소스를 사용하기 전에 선언을 등록해야 한다. 그리고 등록 절차는 때때로 몇 초가 걸리기도 한다.

### Method 1. Let helm Do It for you
- helm3 출시 이후, 보다 간단한 방법으로 기존 crd 설치 hook를 제거했다. 이제 차트에 crds라는 특수 디렉토리를 생성하여 CRD를 저장할 수 있다. 이 CRD는 템플릿이 지정되어 있지 않지만 차트에 대한 헬름 설치를 실행할 때 기본적으로 설치된다. CRD가 이미 존재하는 경우 경고와 함께 건너뛴다. `--skip-crds` 플래그를 통해 CRD 설치를 건너뛸 수도 있다.

#### Some caveats (and explanations)

- 현재 헬름을 사용하여 CRD를 업그레이드하거나 삭제하는 것은 지원되지 않는다. 이는 의도하지 않은 데이터 손실의 위험 때문에 많은 커뮤니티 논의 끝에 내린 명시적인 결정이다. 또한 현재 CRD를 처리하는 방법과 수명 주기에 대한 커뮤니티 합의가 이루어지지 않았다. 이것이 발전함에 따라 헬름은 이러한 사용 사례에 대한 지원을 추가할 것이다.

- 헬름 설치 및 헬름 업그레이드의 `--dry-run` 플래그는 현재 CRD에 대해 지원되지 않는다. "Dry Run"의 목적은 차트의 출력이 서버로 전송될 때 실제로 작동하는지 검증하는 것이다. 그러나 CRD는 서버의 동작을 수정하는 것이다. 헬름은 데모 실행에서 CRD를 설치할 수 없으므로 검색 클라이언트는 해당 사용자 지정 리소스(CR)에 대해 알지 못하고 유효성 검사는 실패한다. 대신 CRD를 자체 차트로 이동하거나 헬름 템플릿을 사용할 수 있다.

- CRD 지원에 대한 논의에서 고려해야 할 또 다른 중요한 점은 템플릿 렌더링이 처리되는 방식이다. 헬름 2에서 사용된 crd 설치 방법의 뚜렷한 단점 중 하나는 API 가용성 변경으로 인해 차트의 유효성을 제대로 검사할 수 없다는 점이었다(CRD는 실제로 쿠버네티스 클러스터에 사용 가능한 다른 API를 추가하는 것임). 차트에 CRD가 설치되면 헬름은 더 이상 유효한 API 버전 집합을 사용할 수 없었다. 이것이 CRD에서 템플릿 지원을 제거한 이유이기도 하다. 새로운 CRD 설치 방법을 사용하면 이제 헬름이 클러스터의 현재 상태에 대해 완전히 유효한 정보를 갖도록 보장한다.

### Method 2: Separate Charts

- 또 다른 방법은 CRD 정의를 한 차트에 넣은 다음 해당 CRD를 사용하는 모든 리소스를 다른 차트에 넣는 것입니다.

- 이 방법에서는 각 차트를 별도로 설치해야 합니다. 그러나 이 워크플로는 클러스터에 대한 관리자 액세스 권한이 있는 클러스터 운영자에게 더 유용할 수 있습니다.

