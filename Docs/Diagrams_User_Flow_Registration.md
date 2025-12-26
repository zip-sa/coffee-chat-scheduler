# User Flow Diagrams - Account Registration

## 1. Successful Registration Flow (Happy Path)

```mermaid
flowchart TD
    Start([사용자가 회원가입 페이지 방문]) --> Input[정보 입력<br/>username, email, password, display_name]
    Input --> Validate{입력값<br/>유효성 검사}

    Validate -->|유효하지 않음| ErrorType{오류 타입}
    ErrorType -->|Username 오류| UsernameError[사용자명이 유효하지 않습니다<br/>4-40자, 영문/숫자/.-만 허용]
    ErrorType -->|Email 오류| EmailError[이메일이 유효하지 않습니다<br/>유효한 이메일 형식 필요]
    ErrorType -->|Password 오류| PasswordError[비밀번호가 유효하지 않습니다<br/>8-128자 필요]
    ErrorType -->|Display Name 오류| DisplayError[표시명이 유효하지 않습니다<br/>2-40자 필요]

    UsernameError --> ShowError[오류 메시지 표시]
    EmailError --> ShowError
    PasswordError --> ShowError
    DisplayError --> ShowError
    ShowError --> Input

    Validate -->|모두 유효함| CheckDisplay{display_name<br/>입력 여부}
    CheckDisplay -->|입력 안함| AutoGen[무작위 8글자 문자열 생성]
    CheckDisplay -->|입력함| CheckDupe
    AutoGen --> CheckDupe{중복 확인}

    CheckDupe -->|Username 중복| DupeUsername[사용자명이 이미 존재합니다]
    CheckDupe -->|Email 중복| DupeEmail[이메일이 이미 존재합니다]
    DupeUsername --> ShowError
    DupeEmail --> ShowError

    CheckDupe -->|중복 없음| HashPassword[비밀번호 해시 처리]
    HashPassword --> CreateDB[(데이터베이스에<br/>계정 생성)]
    CreateDB --> Response[응답 반환<br/>username, display_name, is_host]
    Response --> Redirect([로그인 페이지/<br/>대시보드로 리디렉션])

    style Start fill:#e1f5e1
    style Redirect fill:#e1f5e1
    style ShowError fill:#ffe1e1
    style DupeUsername fill:#ffe1e1
    style DupeEmail fill:#ffe1e1
    style UsernameError fill:#ffe1e1
    style EmailError fill:#ffe1e1
    style PasswordError fill:#ffe1e1
    style DisplayError fill:#ffe1e1
    style CreateDB fill:#e1e5ff
```

---

## 2. Simplified Happy Path Only

```mermaid
flowchart LR
    A([회원가입 시작]) --> B[정보 입력]
    B --> C{유효성 검사}
    C -->|통과| D{중복 확인}
    D -->|없음| E[비밀번호 해시]
    E --> F[(계정 생성)]
    F --> G[응답 반환]
    G --> H([완료])

    style A fill:#e1f5e1
    style H fill:#e1f5e1
    style F fill:#e1e5ff
```

---

## 3. User Journey - Registration Process

```mermaid
journey
    title 신규 사용자 회원가입 여정
    section 계정 생성 시작
      회원가입 페이지 방문: 5: 사용자
      회원가입 폼 확인: 4: 사용자
    section 정보 입력
      사용자명 입력: 3: 사용자
      이메일 입력: 3: 사용자
      표시명 입력: 3: 사용자
      비밀번호 입력: 2: 사용자
    section 제출 및 검증
      폼 제출: 4: 사용자
      입력값 검증: 5: 시스템
      중복 확인: 5: 시스템
      계정 생성: 5: 시스템
    section 완료
      성공 메시지 확인: 5: 사용자
      로그인 또는 대시보드 이동: 5: 사용자
```

---

## 4. Error Handling Flow

```mermaid
flowchart TD
    Submit[회원가입 폼 제출] --> ValidateUsername{Username<br/>검증}

    ValidateUsername -->|길이 < 4 또는 > 40| E1[Username 오류]
    ValidateUsername -->|특수문자 포함| E1
    ValidateUsername -->|통과| ValidateEmail{Email<br/>검증}

    ValidateEmail -->|형식 오류| E2[Email 오류]
    ValidateEmail -->|길이 > 128| E2
    ValidateEmail -->|통과| ValidatePassword{Password<br/>검증}

    ValidatePassword -->|길이 < 8 또는 > 128| E3[Password 오류]
    ValidatePassword -->|통과| ValidateDisplay{Display Name<br/>검증}

    ValidateDisplay -->|길이 < 2 또는 > 40| E4[Display Name 오류]
    ValidateDisplay -->|통과| CheckUnique{중복 확인}

    CheckUnique -->|Username 중복| E5[Username 중복 오류]
    CheckUnique -->|Email 중복| E6[Email 중복 오류]
    CheckUnique -->|중복 없음| Success[계정 생성 성공]

    E1 --> Return[오류 응답 반환]
    E2 --> Return
    E3 --> Return
    E4 --> Return
    E5 --> Return
    E6 --> Return

    style Success fill:#e1f5e1
    style E1 fill:#ffe1e1
    style E2 fill:#ffe1e1
    style E3 fill:#ffe1e1
    style E4 fill:#ffe1e1
    style E5 fill:#ffe1e1
    style E6 fill:#ffe1e1
    style Return fill:#fff4e1
```

---

## 5. Sequence Diagram - User Registration

```mermaid
sequenceDiagram
    actor User as 사용자
    participant UI as 회원가입 UI
    participant API as Backend API
    participant Validator as Validation Service
    participant DB as Database

    User->>UI: 회원가입 페이지 접속
    UI->>User: 회원가입 폼 표시

    User->>UI: 정보 입력 및 제출
    UI->>API: POST /api/users/register

    API->>Validator: 입력값 검증 요청
    Validator->>Validator: username 검증 (4-40자, 영문/숫자/.-만)
    Validator->>Validator: email 검증 (유효한 이메일 형식)
    Validator->>Validator: password 검증 (8-128자)
    Validator->>Validator: display_name 검증 (2-40자)

    alt 유효성 검사 실패
        Validator-->>API: 검증 오류 반환
        API-->>UI: 400 Bad Request
        UI-->>User: 오류 메시지 표시
    else 유효성 검사 통과
        Validator-->>API: 검증 통과

        API->>DB: username 중복 확인
        alt Username 중복
            DB-->>API: 중복 존재
            API-->>UI: 409 Conflict (Username exists)
            UI-->>User: "사용자명이 이미 존재합니다"
        else Username 사용 가능
            DB-->>API: 중복 없음

            API->>DB: email 중복 확인
            alt Email 중복
                DB-->>API: 중복 존재
                API-->>UI: 409 Conflict (Email exists)
                UI-->>User: "이메일이 이미 존재합니다"
            else Email 사용 가능
                DB-->>API: 중복 없음

                alt display_name 미입력
                    API->>API: 무작위 8글자 생성
                end

                API->>API: 비밀번호 해시 처리
                API->>DB: 계정 생성 (INSERT)
                DB-->>API: 생성 완료

                API-->>UI: 201 Created<br/>{username, display_name, is_host}
                UI-->>User: 회원가입 성공 메시지
                UI->>User: 로그인 페이지로 리디렉션
            end
        end
    end
```

---

## 6. State Diagram - Account Status

```mermaid
stateDiagram-v2
    [*] --> 폼_입력중: 사용자가 회원가입 시작

    폼_입력중 --> 검증_대기중: 폼 제출

    검증_대기중 --> 검증_실패: 유효성 검사 실패
    검증_대기중 --> 중복_확인중: 유효성 검사 통과

    검증_실패 --> 폼_입력중: 오류 메시지 표시 후 재입력

    중복_확인중 --> 중복_발견: Username 또는 Email 중복
    중복_확인중 --> 계정_생성중: 중복 없음

    중복_발견 --> 폼_입력중: 중복 오류 메시지 표시

    계정_생성중 --> 생성_완료: DB 저장 성공
    계정_생성중 --> 생성_실패: DB 오류

    생성_실패 --> 폼_입력중: 시스템 오류 메시지

    생성_완료 --> [*]: 대시보드로 리디렉션
```

---

## 다이어그램 설명

1. **Successful Registration Flow**: 전체 회원가입 프로세스 (성공 및 오류 경로 포함)
2. **Simplified Happy Path**: 성공 경로만 간단히 표현
3. **User Journey**: 사용자 관점에서의 회원가입 경험 여정
4. **Error Handling Flow**: 각 검증 단계별 오류 처리 흐름
5. **Sequence Diagram**: 시스템 컴포넌트 간 상호작용 순서
6. **State Diagram**: 계정 생성 프로세스의 상태 전환

