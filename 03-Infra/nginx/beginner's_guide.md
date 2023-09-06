- https://nginx.org/en/docs/beginners_guide.html

- 이 가이드는 nginx에 대한 기본적인 소개와 함께 이를 통해 수행할 수 있는 몇 가지 간단한 작업을 설명한다. 이 가이드에서는 nginx를 시작 및 중지하고 구성을 다시 로드하는 방법을 설명하고, 구성 파일의 구조를 설명하며, 정적 콘텐츠를 제공하도록 nginx를 설정하는 방법, nginx를 프록시 서버로 구성하는 방법, FastCGI 애플리케이션과 연결하는 방법에 대해 설명한다.

- nginx에는 하나의 마스터 프로세스와 여러 개의 작업자 프로세스가 있다. 마스터 프로세스의 주요 목적은 구성을 읽고 평가하며 작업자 프로세스를 유지 관리하는 것이다. 작업자 프로세스는 요청의 실제 처리를 수행한다. nginx는 이벤트 기반 모델과 OS 종속 메커니즘을 사용하여 작업자 프로세스 간에 요청을 효율적으로 배포한다. 워커 프로세스의 수는 구성 파일에 정의되어 있으며 주어진 구성에 맞게 고정되거나 사용 가능한 CPU 코어 수에 따라 자동으로 조정될 수 있다(worker_processes 참조).

- nginx와 해당 모듈의 작동 방식은 설정 파일에서 결정된다. 기본적으로 구성 파일의 이름은 `nginx.conf`이며 `/usr/local/nginx/conf`, `/etc/nginx` 또는 `/usr/local/etc/nginx` 디렉터리에 배치된다.

## Starting, Stopping, and Reloading Configuration
- nginx를 시작하려면 실행 파일을 실행한다. nginx가 시작되면 -s 파라미터로 실행 파일을 호출하여 제어할 수 있다.

## Configuration File's Structure
- nginx는 설정 파일에 지정된 지시어로 제어되는 모듈로 구성된다. 지시어는 단순 지시어와 블록 지시어로 나뉜다. 단순 지시어는 공백으로 구분된 이름과 매개변수로 구성되며 세미콜론(;)으로 끝난다. 블록 지시어는 단순 지시어와 구조는 같지만 세미콜론 대신 중괄호({ 및 })로 둘러싸인 추가 지시어 집합으로 끝난다. 블록 지시어가 중괄호 안에 다른 지시어를 포함할 수 있는 경우 이를 컨텍스트라고 한다(예: 이벤트, http, 서버, 위치).

- 컨텍스트 외부의 구성 파일에 있는 지시어는 기본 컨텍스트에 있는 것으로 간주된다. `events` 및 `http` 지시문은 `main` 컨텍스트에, `server`는 `http`에, `location`는 `server`에 있다.

- 기호 뒤의 나머지 줄은 주석으로 간주된다.

## Serving static content
- 중요한 웹 서버 작업은 파일(예: 이미지 또는 정적 HTML 페이지)을 제공하는 것이다. 요청에 따라 서로 다른 로컬 디렉터리에서 파일을 제공하는 예제를 구현해 보겠다: `/data/www`(HTML 파일을 포함할 수 있음) 및 `/data/images`(이미지 포함). 이를 위해서는 구성 파일을 편집하고 두 개의 위치 블록이 있는 http 블록 내부에 서버 블록을 설정해야 한다.

- 먼저 `/data/www` 디렉터리를 생성하고 텍스트 콘텐츠가 포함된 `index.html` 파일을 넣고 `/data/images` 디렉터리를 생성하여 이미지를 몇 개 넣는다.

- 다음으로 구성 파일이다. 기본 구성 파일에는 이미 서버 블록의 몇 가지 예가 포함되어 있으며 대부분 주석 처리되어 있다. 지금은 이러한 블록을 모두 주석 처리하고 새 서버 블록을 시작한다.
    - ```
        http {
            server {
            }
        }

      ```
- 일반적으로 구성 파일에는 수신하는 포트와 서버 이름으로 구분되는 여러 서버 블록이 포함될 수 있다. nginx가 요청을 처리할 서버를 결정하면 요청 헤더에 지정된 URI를 서버 블록 내부에 정의된 위치 지시어의 매개변수와 비교하여 테스트한다. 서버 블록에 다음 location 블록을 추가한다.
    - ```
        location / {
            root /data/www;
        }

      ```
    - 이 위치 블록은 요청의 URI와 비교하여 "/" 접두사를 지정한다. 일치하는 요청의 경우 URI는 루트 지시어에 지정된 경로, 즉 `/data/www`에 추가되어 로컬 파일 시스템에서 요청된 파일의 경로를 형성한다. 일치하는 위치 블록이 여러 개 있는 경우 nginx는 접두사가 가장 긴 위치 블록을 선택한다. 위의 위치 블록은 길이가 1로 가장 짧은 접두사를 제공하므로 다른 모든 위치 블록이 일치하는 것을 제공하지 못하는 경우에만 이 블록이 사용된다.

- 다음으로 두 번째 위치 블록을 추가한다.
    - ```
        location /images/ {
            root /data;
        }
        
      ```
- /images/로 시작하는 요청과 일치한다(location /도 이러한 요청과 일치하지만 접두사가 더 짧다).

- 서버 블록의 결과 구성은 다음과 같아야 한다.
    - ```
        server {
            location / {
                root /data/www;
            }
        
            location /images/ {
                root /data;
            }
        }
      ```
    - 이것은 이미 표준 포트 80에서 수신 대기하고 로컬 컴퓨터에서 http://localhost/ 에 액세스할 수 있는 서버의 작동 구성이다. images/로 시작하는 URI를 가진 요청에 대한 응답으로 서버는 /data/images 디렉토리에서 파일을 보낸다. 예를 들어 http://localhost/images/example.png 요청에 대한 응답으로 nginx는 /data/images/example.png 파일을 전송한다. 해당 파일이 존재하지 않으면 nginx는 404 오류를 나타내는 응답을 보낸다. images/로 시작하지 않는 URI를 가진 요청은 /data /www 디렉터리에 매핑됩니다. 예를 들어 http://localhost/some/example.html 요청에 대한 응답으로 nginx는 /data/www/some/example.html 파일을 전송한다.

- 새 구성을 적용하려면 nginx가 아직 시작되지 않은 경우 시작하거나 실행하여 nginx의 마스터 프로세스에 다시 로드 신호를 보내면 된다. nginx -s reload

- 예상대로 작동하지 않는 경우 /usr/local/nginx/logs 또는 /var/log/nginx 디렉터리에 있는 access.log 및 error.log 파일에서 원인을 찾아볼 수 있습니다.

## Setting up a simple proxy server

- nginx를 자주 사용하는 방법 중 하나는 프록시 서버로 설정하는 것인데, 프록시 서버란 요청을 수신하여 프록시 서버에 전달하고 서버에서 응답을 검색하여 클라이언트로 전송하는 서버를 의미한다.

- 로컬 디렉터리의 파일로 이미지 요청을 처리하고 다른 모든 요청을 프록시 서버로 보내는 기본 프록시 서버를 구성하겠다. 이 예제에서는 두 서버가 모두 단일 nginx 인스턴스에 정의된다.

- 먼저 nginx의 구성 파일에 다음 내용으로 서버 블록을 하나 더 추가하여 프록시 서버를 정의한다.
    - ```
        server {
            listen 8080;
            root /data/up1;
        
            location / {
            }
        }
        
      ```

- 이 서버는 포트 8080(이전에는 표준 포트 80이 사용되었기 때문에 listen 지시어가 지정되지 않음)에서 수신 대기하고 모든 요청을 로컬 파일 시스템의 /data/up1 디렉토리에 매핑하는 간단한 서버이다. 이 디렉터리를 생성하고 index.html 파일을 넣는다. 루트 지시어는 서버 컨텍스트에 배치된다는 점에 유의해야 한다. 이러한 루트 지시어는 요청을 제공하기 위해 선택한 위치 블록에 자체 루트 지시어가 포함되어 있지 않을 때 사용된다.

- 그런 다음 이전 섹션의 서버 구성을 사용하여 프록시 서버 구성이 되도록 수정한다. 첫 번째 위치 블록에 매개변수에 지정된 프록시 서버의 프로토콜, 이름 및 포트(이 경우 http://localhost:8080)와 함께 proxy_pass 지시어를 넣는다:
- ```
        server {
            location / {
                proxy_pass http://localhost:8080;
            }
        
            location /images/ {
                root /data;
            }
        }
  ```

- 현재 /images/ 접두사가 있는 요청을 /data/images 디렉터리 아래의 파일에 매핑하는 두 번째 위치 블록을 수정하여 일반적인 파일 확장자를 가진 이미지 요청과 일치하도록 한다. 수정된 위치 블록은 다음과 같다:

- ```
        location ~ \.(gif|jpg|png)$ {
            root /data/images;
        }
        
  ```
- 매개 변수는 .gif, .jpg 또는 .png로 끝나는 모든 URI와 일치하는 정규식이다. 정규식 앞에는 ~가 와야 한다. 해당 요청은 /data/images 디렉터리에 매핑된다.

- nginx는 요청을 처리할 위치 블록을 선택할 때 먼저 접두사를 지정하는 위치 지시어를 확인하여 접두사가 가장 긴 위치를 기억한 다음 정규 표현식을 확인한다. 정규 표현식과 일치하는 것이 있으면 nginx는 이 위치를 선택하거나 그렇지 않으면 이전에 기억된 위치를 선택한다.

- 프록시 서버의 결과 구성은 다음과 같다:

- ```
        server {
            location / {
                proxy_pass http://localhost:8080/;
            }
        
            location ~ \.(gif|jpg|png)$ {
                root /data/images;
            }
        }

  ```
- 이 서버는 .gif, .jpg 또는 .png로 끝나는 요청을 필터링하여 (루트 지시문의 매개변수에 URI를 추가하여) /data/images 디렉터리에 매핑하고 다른 모든 요청은 위에 구성된 프록시 서버로 전달한다.

- 새 구성을 적용하려면 이전 섹션에서 설명한 대로 nginx에 재로드 신호를 보낸다.

- 프록시 연결을 추가로 구성하는 데 사용할 수 있는 더 많은 지시어가 있다.

## Setting up fastCGI Proxying

- nginx는 PHP와 같은 다양한 프레임워크와 프로그래밍 언어로 구축된 애플리케이션을 실행하는 FastCGI 서버로 요청을 라우팅하는 데 사용할 수 있다.

- FastCGI 서버와 함께 작동하기 위한 가장 기본적인 nginx 구성에는 proxy_pass 지시문 대신 fastcgi_pass 지시문을 사용하고 FastCGI 서버에 전달되는 매개 변수를 설정하는 fastcgi_param 지시문을 사용하는 것이 포함된다. 
  - localhost:9000에서 FastCGI 서버에 액세스할 수 있다고 가정한다. 
    이전 섹션의 프록시 구성을 기준으로 proxy_pass 지시문을 fastcgi_pass 지시문으로 바꾸고 매개 변수를 localhost:9000으로 변경한다. 
    PHP에서 SCRIPT_FILENAME 매개변수는 스크립트 이름을 결정하는 데 사용되며 QUERY_STRING 매개변수는 요청 매개변수를 전달하는 데 사용된다. 
    결과 구성은 다음과 같다:

    - ```
            server {
                location / {
                    fastcgi_pass  localhost:9000;
                    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                    fastcgi_param QUERY_STRING    $query_string;
                }
            
                location ~ \.(gif|jpg|png)$ {
                    root /data/images;
                }
            }
            
      ```

- 이렇게 하면 정적 이미지에 대한 요청을 제외한 모든 요청을 FastCGI 프로토콜을 통해 localhost:9000에서 작동하는 프록시 서버로 라우팅하는 서버가 설정된다.