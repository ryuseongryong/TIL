# whitespace control

- 후행 줄 바꿈이 하나 있는 경우 줄 바꿈이 제거됨
- 다른 공백(공백, 탭, 개행 등)은 변경되지 않고 반환됨

- 애플리케이션에서 jinja를 trim_blocks로 구성하면 템플릿 태그 뒤의 첫 번째 개행이 자동으로 제거됨
- lstrip_blocks 옵션은 줄의 시작부터 블록의 시작까지 탭과 공백을 제거하도록 설정할 수 있음(블록 시작 전에 다른 문자가 있는 경우 아무것도 제거되지 않음)
- trim_blocks, lstrip_blocks를 모두 활성화하면 블록 태그 자체 줄에 넣을 수 있고, 렌더링 시 전체 블록 줄이 제거되어 콘텐츠의 공백이 유지됨


```
# trim_blocks, lstrip_blocks 옵션이 모두 없는 경우
<div>
    {% if True %}
        yay
    {% endif %}
</div>
---
<div>

        yay

</div>

# trim_blocks, lstrip_blocks 옵션을 모두 활성화한 경우, 템플릿 블록 라인이 제거되고 다른 공백은 유지됨
<div>
        yay
</div>

# 블록의 시작 부분에 `+`를 넣어 lstrip_blocks 동작을 수동으로 비활성화할 수 있음
<div>
        {%+ if something %}yay{% endif %}
</div>

# 마찬가지로 블록 끝에 `+`를 넣어 trim_blocks 동작을 수동으로 비활성화할 수 있음
<div>
    {% if something +%}
        yay
    {% endif %}
</div>

# 템플릿에서 직접 공백을 제거할 수 있음 : 블록, 주석, 변수 표현식의 시작 또는 끝에 `-`를 추가하여 해당 블록 앞 또는 뒤의 공백을 제거할 수 있음
{% for item in seq -%}
    {{ item }}
{%- endfor %}
이렇게 하면 요소 사이에 공백이 없는 모든 요소가 산출됨.
seq가 1부터 9까지의 숫자 목록인 경우 출력은 123456789가 됨.
줄 문을 활성화하면 줄의 시작 부분까지 선행 공백을 자동으로 제거함.
기본적으로 Jinja는 후행 개행도 제거함. 단일 후행 개행을 유지하려면 Jinja를 keep_trailing_newline으로 구성.
```

## 실제 사용법
- 템플릿에 정의된 것과 동일한 공백으로 적용하려면 단순히 `lstrip_blocks`와 `trim_blocks` 옵션을 사용하면 된다. 
ansible에서는 해당하는 것과 동일한 명칭의 parameter가 주어지기 때문에 둘 다 켜게 되면 템플릿과 동일하게 공백을 적용할 수 있다.
(default는 `trim_blocks=true`, `lstrip_blocks=false`)
- 블록의 시작 또는 끝에 마이너스 기호를 추가하여 수동으로 공백을 제거한다.
- jinja2 블록 내부에 들여쓰기를 적용한다.
    - ansible의 기본값이 lstrip_blocks=false이기 때문에 Jinja template에서 들여쓰기를 하면 안정성이 높아짐
    - 유일한 부작용은 템플릿이 시각적으로 어떻게 표시되는지인데, 많은 블록 템플릿이 "바쁘게" 보일 수 있다는 것. 이렇게 하면 의도와 일치하는 들여쓰기가 있어야 하므로 블록 사이의 텍스트 줄을 보기 어려울 수 있음.


- https://jinja.palletsprojects.com/en/3.1.x/templates/#whitespace-control
- https://ttl255.com/jinja2-tutorial-part-3-whitespace-control/
