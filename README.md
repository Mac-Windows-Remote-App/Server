# 🚀 Remote Control Project (Mac-Windows)

Mac과 Windows 간의 상호 입력(Mouse, Keyboard, Trackpad) 및 제스처 연동을 위한 크로스 플랫폼 원격 제어 시스템입니다.

## 📁 Project Structure

Plaintext

```
/Remote-Control-Project
├── 📁 Server       # FastAPI (Python): 데이터 중계 및 세션 관리
├── 📁 Client       # Unity (C#): 입력 수집 및 시스템 제어 실행
└── README.md       # 프로젝트 통합 가이드
```

---

## 📑 Protocol Specification

모든 통신은 **WebSocket**을 기반으로 하며, 메시지 분류 효율을 위해 `event` 기반의 **Base Wrapper** 구조를 사용합니다.

### 1. Common Message Wrapper

|**Field**|**Type**|**Description**|
|---|---|---|
|`event`|String|메시지의 목적을 식별하는 고유 이벤트명|
|`payload`|Object|이벤트에 따른 세부 데이터 컨테이너|

JSON

```
{
  "event": "EVENT_NAME",
  "payload": { "data_field": "value" }
}
```

---

### 2. Connection & Handshake

서버 접속 시 기기의 역할(Role)을 정의하고 해상도 정보를 동기화합니다.

|**Event**|**Direction**|**Description**|
|---|---|---|
|`CONN_REQ`|Client → Server|초기 접속 요청 및 기기 정보(OS, Resolution) 전달|
|`CONN_ACK`|Server → Client|접속 승인 및 세션 ID 부여|
|`CONN_REJ`|Server → Client|인증 실패 또는 중복 ID 접속 거절|

**Request Example (`CONN_REQ`):**

JSON

```
{
  "event": "CONN_REQ",
  "payload": {
    "device_name": "My_Macbook",
    "os": "macOS",
    "role": "CONTROLLER", // 제어 주체(Controller) vs 대상(Target)
    "resolution": { "width": 2560, "height": 1600 },
    "auth_token": "secure_token_here"
  }
}
```

- **Why `os`?**: OS별 키 매핑(Cmd ↔ Ctrl) 및 제스처 변환 기준점으로 활용.
    
- **Why `resolution`?**: 이기종 간 마우스 좌표 보정을 위해 사용.
    

---

### 3. Input & Gesture Synchronization

실시간 입력 데이터를 전송합니다. 좌표는 해상도에 구애받지 않도록 **정규화(0.0 ~ 1.0)**하여 처리합니다.

#### A. Mouse Movement

JSON

```
{
  "event": "MOUSE_MOVE",
  "payload": {
    "pos_x": 0.5234, // 전체 너비 대비 비율 (0~1)
    "pos_y": 0.7681, // 전체 높이 대비 비율 (0~1)
    "is_relative": false // true일 경우 상대 이동 거리로 처리
  }
}
```

#### B. Trackpad Gestures

JSON

```
{
  "event": "TRACKPAD_GESTURE",
  "payload": {
    "type": "PINCH", // SCROLL, PINCH, SWIPE, TAP
    "fingers": 2,    // 인식된 손가락 개수
    "delta": { "x": 0, "y": 1.5, "z": 1.1 },
    "velocity": 0.8  // 관성 스크롤 재현을 위한 가속도 데이터
  }
}
```

#### C. Keyboard Action

JSON

```
{
  "event": "INPUT_ACTION",
  "payload": {
    "type": "KEY_DOWN", // KEY_DOWN, KEY_UP
    "key_code": "C",
    "modifiers": ["CMD"] // CTRL, ALT, SHIFT, CMD 조합
  }
}
```

---

## 🛑 Error Codes

시스템 안정성을 위해 정의된 공통 에러 코드입니다.

|**Code**|**Name**|**Description**|
|---|---|---|
|**1001**|`AUTH_FAILED`|인증 토큰 불일치|
|**2002**|`TARGET_OFFLINE`|제어 대상 기기가 연결되어 있지 않음|
|**3001**|`INVALID_PAYLOAD`|데이터 규격 오류 또는 필수 필드 누락|
|**3003**|`OUT_OF_RANGE`|정규화 좌표값 범위를 초과함|
