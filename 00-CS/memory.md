# Private Bytes, Virtual Bytes, and Working Set
- https://www.baeldung.com/cs/private-bytes-virtual-bytes-working-set

## 1. Overview
- 이 튜토리얼에서는 운영 체제의 세 가지 메모리 관련 개념인 private bytes, virtual bytes, working set에 대해 설명합니다.
- 마지막으로 이들 간의 핵심적인 차이점에 대해 알아보겠습니다.

## 2. Private Bytes
- private bytes는 애플리케이션이 실행 중 또는 실행 전에 요청하는 메모리 양에 대한 합리적인 근사치입니다. 특히 프로세스가 private 메모리를 완전히 소진할 때 private bytes는 운영 체제에서 프로세스에 할당된 RAM의 양을 나타냅니다. 그러나 private bytes set의 중요한 측면은 프로세스에서 사용하는 메모리가 아니라 항상 할당된 메모리를 나타낸다는 것입니다.

- 프로세스는 private bytes set을 사용하여 OS에 RAM을 요청합니다. 하지만 프로세스가 할당된 메모리 전체를 사용할 수도 있고 사용하지 않을 수도 있습니다. 메모리 매핑된 파일은 private bytes set에 포함되지 않습니다. 물리적 메모리와 디스크 메모리로 구성될 수 있습니다.

- private bytes set을 사용하여 private 메모리의 지속적인 증가를 모니터링하고 분석할 수 있습니다. 예를 들어, 애플리케이션의 원치 않는 무한 루프에서 할당 요청이 발생하면 시스템에서 메모리 누수가 발생할 수 있습니다. 애플리케이션의 private bytes set의 지속적인 증가를 모니터링하여 메모리 누수를 식별할 수 있습니다.

- private bytes set에서 프로세스는 요청된 메모리를 다른 프로세스와 공유하지 않습니다. 또한 프로세스는 실행 중에 요청된 메모리 전체를 사용하지 않습니다. 또한 프로세스의 private bytes에는 페이지 파일 사용량도 포함됩니다. 페이지 파일은 OS가 오랫동안 사용하지 않은 하드 디스크 메모리의 예약된 부분입니다.

- 따라서 private set의 실제 할당된 메모리는 private bytes set와 페이지파일 메모리에 사용된 메모리의 합계입니다:
- Private Byte Set(Allocated Memory) = Private Byte Set(Used Memory) + Pagefile

## 3. Working Set
- 애플리케이션을 실행하는 동안 working bytes set을 현재 물리적 메모리에 있는 프로세스의 페이지로 볼 수 있습니다. working set에는 특정 프로세스에 의해 할당된 RAM의 가장 최근 페이지가 포함됩니다.

- 그러나 프로세스가 이전에 물리적 메모리에 로드되지 않은 페이지를 요청하면 오류가 발생합니다. 이 오류는 시스템에서 페이지 오류로 이어집니다. 또한 페이지 오류 처리기를 사용하여 누락된 페이지를 탐색할 수 있습니다. 그럼에도 불구하고 누락된 페이지를 찾은 후에는 working set에 포함할 수 있습니다. 따라서 이러한 경우 working set의 총 크기는 새로 추가된 페이지 크기만큼 증가합니다. 페이지 결함을 하드 페이지 결함과 소프트 페이지 결함의 두 가지 범주로 나눌 수 있습니다.

- 하드 페이지 오류는 오류 페이지를 요청한 프로세스에서 생성한 페이징 파일 또는 메모리 매핑 파일을 읽음으로써 해결할 수 있습니다. 시스템은 백업 저장소 파일의 콘텐츠를 읽어 원하는 페이지의 콘텐츠를 검색합니다. 검색이 완료되면 해당 페이지를 working set에 추가합니다.

- 소프트 페이지 오류는 백라인 저장소 파일을 읽을 필요가 없습니다. 다양한 상황에서 발생할 수 있습니다. 몇 가지 상황을 살펴보겠습니다. 다른 프로세스의 다른 working set 내에서 페이지가 실행되고 있다고 가정해 보겠습니다. 이 경우 소프트 페이지 오류가 발생할 수 있습니다. 또한 프로세스의 working set을 떠난 후 전환 중인 페이지에서도 소프트 페이지 오류가 발생할 수 있습니다.

- 프로세스가 working set 페이지 중 하나를 사용하여 완료되면 해당 페이지는 나머지 프로세스에 영향을 주지 않고 set에서 제거됩니다. 페이지가 working set의 일부가 아닌 경우 다른 용도로 요청되거나 수정될 때까지 해당 페이지를 전환 페이지라고 합니다.

- private bytes set과 달리 working set에는 페이지가 지정되지 않은 private bytes와 메모리 매핑된 파일이 모두 포함될 수 있습니다.

## 4. Virtual Bytes
- virtual bytes set는 프로세스에 할당된 virtual 메모리 주소 공간을 의미합니다. 고유한 프로세스가 주소의 모든 공간에 액세스하는 자유로운 사용을 지원합니다. virtual 주소는 현재 물리적 메모리 위치를 나타내지 않습니다. 그러나 모든 프로세스에는 virtual 주소를 해당 물리적 주소로 변환하는 데 도움이 되는 페이지 테이블이 함께 제공됩니다. 프로세스가 주소를 요청하면 시스템은 페이지 테이블을 기반으로 물리적 주소로 응답합니다.

- 보조 스토리지와 virtual 공간을 사용하여 물리적 RAM을 확장할 수 있습니다. 이 virtual 메모리는 RAM의 용량을 초과하여 실제 실제 메모리보다 더 많은 주소 간격과 참조 주소를 확보합니다. 예를 들어 보겠습니다. 32비트 Windows 사용자 모드에서 프로세스는 최대 2GB를 사용할 수 있습니다. 그러나 Boot.ini 파일을 수정하여 할당된 메모리를 3GB로 확장할 수 있습니다.

- virtual bytes set에는 페이징되지 않은 private bytes, 메모리 매핑된 파일 및 디스크의 데이터가 포함될 수 있습니다. 마지막으로 virtual bytes set는 working set, private bytes 및 대기 목록의 조합입니다:
- Virtual Byte Set = Working Set + Private Byte Set + Standby List

## 5. Differences
- virtual bytes set을 working set과 private bytes의 합으로 정의할 수 있습니다. 또한 private bytes set은 프로세스의 할당된 메모리와 페이지 사용 메모리의 합계입니다. 따라서 private bytes set은 working set의 상위 set입니다. 또한 virtual bytes set은 private bytes set과 working set의 상위 set입니다:

- Virtual byte set > Private byte set > Working byte set

Private bytes | Working Set | Virtual Bytes
---|---|---
프로세스당 메모리 할당의 총 크기를 나타냅니다. | 총 메모리 사용량을 나타냅니다 | 주소 지정 공간의 전체 크기를 나타냅니다.
프로세스로 인한 메모리 누수 감지에 사용 | CPU 캐싱을 위한 메모리 크기를 설명하는 데 사용됩니다. | 시스템의 부하가 높은지 확인하는 데 사용됩니다.
메모리 크기가 Working byte set보다 크지만 Virtual byte set보다 작습니다 | Private byte set의 하위 세트 | Private 및 Working set를 포함합니다.
할당된 메모리는 다른 프로세스와 공유할 수 없습니다. | 허용되는 메모리에는 공유 메모리가 포함될 수 있습니다 | 공유 메모리를 포함하며 공유가 허용됩니다.