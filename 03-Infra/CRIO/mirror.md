- https://github.com/containers/image/blob/main/docs/containers-registries.conf.5.md

- 오해하고 있던 부분이 있었다. mirrored registry로 등록된 경우에 기존 location은 무시하고 mirrored registry로 바로 연결해주는 것으로 이해하고 있었다. 만약에 mirrored registry에 이미지가 없다면 바로 에러를 발생하는 것으로 이해했었다.(기존에는 network가 끊어진 환경에서 mirrored registry를 적용했기 때문에 기존 public 환경의 location에 접근이 불가능했다.) 하지만 문서를 다시 읽어보니 우선순위에 따라 registry에 접근하는 것으로 확인했다.


EXAMPLE
```
unqualified-search-registries = ["example.com"]

[[registry]]
prefix = "example.com/foo"
insecure = false
blocked = false
location = "internal-registry-for-example.com/bar"

[[registry.mirror]]
location = "example-mirror-0.local/mirror-for-foo"

[[registry.mirror]]
location = "example-mirror-1.local/mirrors/foo"
insecure = true

[[registry]]
location = "registry.com"

[[registry.mirror]]
location = "mirror.registry.com"
```
Given the above, a pull of `example.com/foo/image:latest` will try:

1. `example-mirror-0.local/mirror-for-foo/image:latest`
2. `example-mirror-1.local/mirrors/foo/image:latest`
3. `internal-registry-for-example.net/bar/image:latest`

in order, and use the first one that exists.

Note that a mirror is associated only with the current `[[registry]]` TOML table. If using the example above, pulling the image `registry.com/image:latest` will hence only reach out to `mirror.registry.com`, and the mirrors associated with `example.com/foo` will not be considered.