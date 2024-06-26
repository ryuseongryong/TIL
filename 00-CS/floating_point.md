# Floating point problem in programming
- https://stackoverflow.com/questions/21872854/floating-point-math-in-different-programming-languages

(2014y)
모든 언어는 십진수가 아닌 이진수로 값을 표현하는 시스템 제공 부동소수점 형식을 사용하고 있습니다. 
0.2 및 0.4와 같은 값은 해당 형식으로 정확히 표현할 수 없으므로 대신 가장 가까운 값이 저장되므로 작은 오류가 발생합니다. 
예를 들어 숫자 리터럴 0.2는 정확한 값이 0.200000000000000011102230246251565404236316680908203125 인 부동 소수점 숫자가 됩니다. 마찬가지로 부동 소수점 숫자에 대해 주어진 산술 연산을 수행하면 정확히 표현할 수 없는 값이 나올 수 있으므로 실제 수학적 결과는 가장 가까운 표현 가능한 값으로 대체됩니다. 이것이 여러분이 보고 있는 오류의 근본적인 이유입니다.

그러나 이것은 언어 간의 차이를 설명하지 않습니다. 모든 예제에서 정확히 동일한 계산이 수행되고 정확히 동일한 결과에 도달하고 있습니다. 차이점은 다양한 언어가 결과를 표시하는 방식에 있습니다.

엄밀히 말하면 표시된 답 중 어느 것도 정답이 아닙니다. 가장 가까운 반올림 모드를 사용하는 IEEE 754 이진 64 연산의 (상당히 안전한) 가정을 하면 첫 번째 합의 정확한 값은 다음과 같습니다:

0.600000000000000088817841970012523233890533447265625
의 정확한 값은 두 번째 합계입니다:

0.59999999999999997779553950749686919152736663818359375
그러나 두 출력물 모두 특별히 사용자 친화적인 것은 아니며, 테스트한 모든 언어가 인쇄할 때 출력물을 축약하는 합리적인 결정을 내린 것은 분명합니다. 그러나 모든 언어가 출력 서식을 지정하는 데 동일한 전략을 채택하지는 않았기 때문에 차이가 있는 것입니다.

서식을 지정하는 데는 여러 가지 전략이 있지만 특히 일반적인 세 가지 전략이 있습니다:

1. 올바르게 반올림된 17개의 유효 자릿수를 계산하고 표시하며, 후행 0이 나타나는 경우 0을 제거할 수 있습니다. 17자리의 출력은 고유한 이진64 부동 소수점이 고유한 표현을 갖도록 보장하므로 부동 소수점 값을 그 표현에서 명확하게 복구할 수 있습니다(17은 이 속성을 가진 가장 작은 정수입니다). 예를 들어 파이썬 2.6에서 사용하는 전략입니다.

2. 일반적인 반올림-동일 반올림 모드에서 주어진 이진64 값으로 반올림되는 최단 십진수 문자열을 계산하여 표시합니다. 이 방법은 전략 1보다 구현하기가 다소 복잡하지만 고유한 부동 소수점이 고유한 표현을 갖는다는 특성을 유지하며 더 보기 좋은 출력을 생성하는 경향이 있습니다. 이는 테스트한 모든 언어(R 제외)에서 사용하는 전략인 것으로 보입니다.

3. 올바르게 반올림된 유효 자릿수를 15자리(또는 그 이하) 계산하여 표시합니다. 이는 십진수에서 이진수로 변환할 때 발생하는 오류를 숨기는 효과가 있어 정확한 십진수 연산을 하는 것처럼 보이게 합니다. 하지만 서로 다른 부동 소수점이 동일한 표현을 가질 수 있다는 단점이 있습니다. 이것이 바로 R이 하는 일인 것 같습니다. (댓글에서 표시할 자릿수를 제어하는 R 설정이 있다는 점을 지적해 주신 @hadley에게 감사드립니다. 기본값은 유효 자릿수 7자리입니다).