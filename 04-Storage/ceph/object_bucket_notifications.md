- https://rook.io/docs/rook/latest-release/Storage-Configuration/Object-Storage-RGW/ceph-object-bucket-notifications/
# Object Bucket Notifications

- CephBucketNotification은 버킷 알림의 주제, 이벤트 및 필터를 정의하는 사용자 지정 리소스이며, 아래에 표시된 사용자 지정 리소스 정의(CRD)로 설명됩니다. 버킷 알림은 오브젝트 버킷 클레임(OBC)에 레이블을 설정하여 버킷과 연결됩니다.
- CephBucketTopic은 버킷 알림 토픽을 나타내는 사용자 지정 리소스이며 아래에 표시된 CRD로 설명됩니다. 버킷 알림 주제는 버킷 알림을 보낼 수 있는 엔드포인트(또는 이 엔드포인트 내부의 "주제")를 나타냅니다.

## Notifications
Ceph버킷 알림은 알림을 트리거하는 버킷 작업과 알림을 전송할 주제를 정의합니다. 또한, 개체의 이름 및 기타 개체 속성을 기반으로 필터를 정의할 수도 있습니다. 알림은 다음과 같은 형식으로 ObjectBucketClaim에 레이블을 추가하여 ObjectBucketClaim을 통해 만든 버킷과 연결할 수 있습니다:
```
bucket-notification-<notification name>: <notification name>

```
CephBucketTopic, CephBucketNotification 및 ObjectBucketClaim은 모두 동일한 네임스페이스에 속해야 합니다. 버킷을 수동으로 만든 경우(ObjectBucketClaim을 통하지 않고), 이 버킷에 대한 알림도 수동으로 만들어야 합니다. 그러나 이러한 알림의 토픽은 CephBucketTopic 리소스를 통해 생성된 토픽을 참조할 수 있습니다.

## Topics
Ceph 버킷 토픽은 엔드포인트(유형: Kafka, AMQP0.9.1 또는 HTTP) 또는 이 엔드포인트 내부의 특정 리소스(예: Kafka 또는 AMQP 토픽 또는 HTTP 서버의 특정 URI)를 나타냅니다. Ceph버킷토픽은 또한 CephObjectStore의 RGW(RADOS 게이트웨이)가 엔드포인트에 연결하는 데 필요한 모든 추가 정보를 보유합니다. 토픽은 특정 버킷이나 알림에 속하지 않습니다. 여러 버킷의 알림이 동일한 토픽으로 전송될 수 있으며, 하나의 버킷(여러 CephBucketNotifications를 통해)이 여러 토픽에 알림을 전송할 수도 있습니다.

## Notification Reliability and Delivery
알림은 알림을 트리거한 작업의 일부로 동기식으로 전송될 수 있습니다. 이 모드에서는 토픽의 구성된 엔드포인트로 알림이 전송된 후에만 작업이 승인되므로 알림의 왕복 시간이 작업 자체의 대기 시간에 추가됩니다. 원래 트리거 작업은 알림이 오류로 실패하거나 전달할 수 없거나 시간이 초과되더라도 여전히 성공한 것으로 간주됩니다.

알림은 비동기적으로 전송될 수도 있습니다. 알림은 영구 저장소에 커밋된 다음 토픽의 구성된 엔드포인트로 비동기적으로 전송됩니다. 이 경우 원래 작업에 추가되는 유일한 지연 시간은 영구 저장소에 알림을 커밋하는 것입니다. 알림이 오류로 실패하거나 전달할 수 없거나 시간이 초과되면 성공적으로 확인될 때까지 다시 시도됩니다.
