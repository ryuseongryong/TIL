# Kustomize
- https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/

## 요약
- Kustomize는 템플릿 없이 구성 파일을 사용자 지정하는 데 도움이 됩니다.
- 사용자 지정은 생성기와 같은 여러 가지 편리한 방법을 제공하여 사용자 지정을 더 쉽게 할 수 있습니다.
- Kustomize는 패치를 사용하여 이미 존재하는 표준 구성 파일을 방해하지 않고 환경별 변경 사항을 도입합니다.

- Kustomize는 템플릿과 DSL 없이도 Kubernetes 리소스 구성을 사용자 정의할 수 있는 솔루션을 제공합니다.
- Kustomize를 사용하면 템플릿이 없는 원시 YAML 파일을 여러 용도에 맞게 사용자 정의할 수 있으며, 원본 YAML은 그대로 사용할 수 있습니다.
- Kustomize는 Kubernetes를 대상으로 하며, Kubernetes 스타일 API 객체를 이해하고 패치할 수 있습니다. 파일에 선언된다는 점에서 make와 비슷하고, 편집된 텍스트를 출력한다는 점에서 sed와 비슷합니다.

## 사용법
1) Make a kustomization file
- yaml resource files가 포함된 directory에 kustomization file을 생성한다.
- 이 파일에는 해당 리소스와 리소스에 적용할 사용자 지정(예: 공통 레이블 추가)이 선언되어 있어야 합니다.
- File structure:
    ```
    ~/someApp
    ├── deployment.yaml
    ├── kustomization.yaml
    └── service.yaml
    ```
- 이 디렉터리의 리소스는 다른 사람의 구성의 포크일 수 있습니다. 이 경우 리소스를 직접 수정하지 않으므로 소스 자료에서 쉽게 리베이스하여 개선 사항을 캡처할 수 있습니다.

- Generate customized YAML with:
`kustomize build ~/someApp`
- The YAML can be directly applied to a cluster:
`kustomize build ~/someApp | kubectl apply -f -`

2) Create variants using overlays
- 공통 기반을 수정하는 오버레이를 사용하여 개발, 스테이징 및 프로덕션과 같은 기존 구성의 변형을 관리하세요.
- File structure:
    ```
    ~/someApp
    ├── base
    │   ├── deployment.yaml
    │   ├── kustomization.yaml
    │   └── service.yaml
    └── overlays
        ├── development
        │   ├── cpu_count.yaml
        │   ├── kustomization.yaml
        │   └── replica_count.yaml
        └── production
            ├── cpu_count.yaml
            ├── kustomization.yaml
            └── replica_count.yaml
    ```
- 위 (1)의 작업을 일부App 하위 디렉터리인 base로 이동한 다음 형제 디렉터리에 오버레이를 배치합니다.
- 오버레이는 베이스를 참조하고 해당 베이스에 적용할 패치를 참조하는 또 다른 커스터마이징입니다.
- 이 배열을 사용하면 git으로 구성을 쉽게 관리할 수 있습니다. 베이스에는 다른 사람이 관리하는 업스트림 리포지토리의 파일이 있을 수 있습니다. 오버레이는 사용자가 소유한 리포지토리에 있을 수 있습니다. 리포지토리 클론을 디스크에 형제자매로 배열하면 git 서브모듈이 필요하지 않습니다(서브모듈을 좋아하는 분이라면 이 방법도 괜찮지만).

다음을 사용하여 YAML을 생성합니다.
```
kustomize build ~/someApp/overlays/production

```

YAML은 클러스터에 직접 적용할 수 있습니다:
```
kustomize build ~/someApp/overlays/production | kubectl apply -f -

```