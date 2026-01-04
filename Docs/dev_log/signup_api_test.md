# Signup API 테스트 구현 과정

## 개요
signup API의 테스트를 구현하면서 발생한 문제들과 해결 과정을 정리한 문서입니다.

---

## Q1: 처음 발견한 문제는 무엇이었나?

### 문제 배경
test_signup.py를 pytest로 실행했을 때 모든 테스트가 실패했습니다.

```
AttributeError: 'dict' object has no attribute 'username'
```

### 원인
- `endpoints.py`의 `signup` 함수가 `SignupPayload` 스키마 객체를 기대
- 하지만 `test_signup.py`는 여전히 `dict`를 전달
- `payload.username` 같은 속성 접근이 불가능

### 해결 방향
"test_signup.py를 수정하는 대신, 새로운 API 레벨 테스트 파일을 만들자."

---

## Q2: 왜 새로운 테스트 파일을 만들었나?

### 배경
- 기존 `test_signup.py`는 함수를 직접 호출하는 **유닛 테스트**
- HTTP API를 테스트하는 **API 테스트**가 필요했음

### 해결 방법
`test_signup_api.py` 생성:
- `client.post("/account/signup", json=payload)` 사용
- FastAPI가 자동으로 dict를 SignupPayload로 변환
- 실제 HTTP 요청/응답 흐름 테스트

### 핵심 발상
"두 가지 테스트 레벨을 분리하자"
- `test_signup.py`: 함수 직접 호출 (유닛 테스트)
- `test_signup_api.py`: HTTP API 호출 (API 테스트)

---

## Q3: UserOut 스키마는 왜 필요했나?

### 문제 배경
API 응답에 민감한 정보(email, password)가 노출되는 보안 문제

### 해결 방법
```python
class UserOut(SQLModel):
    username: str
    display_name: str
    is_host: bool

@router.post("/signup", response_model=UserOut)
```

- `response_model=UserOut` 설정
- FastAPI가 자동으로 응답을 필터링
- username, display_name, is_host만 전송

### 확인된 사실
"UserOut은 User 모델을 위한 전송용 스키마가 맞아?"
→ **정답: 맞습니다. API 응답 전용 스키마입니다.**

---

## Q4: response_model 때문에 테스트가 충돌하지 않나?

### 문제 발견
`test_signup_api.py`의 두 테스트가 모순적이었습니다:

1. 첫 번째 테스트: `assert data["email"] == payload["email"]` (email 기대)
2. 두 번째 테스트: `expected_keys = ["username", "display_name", "is_host"]` (email 제외 기대)

### 의문점
"response_model을 User로 하면 첫 번째 통과, UserOut으로 하면 실패... 의도된 동작인가?"

### 결론
아니요, 테스트가 잘못되었습니다. 두 테스트가 동시에 통과할 수 없습니다.

---

## Q5: 그럼 email, password는 어떻게 테스트하나?

### 핵심 질문
"signup API 테스트에서 password와 password_again 검증까지 포함하려면 어떻게 해야 해?"

### 해결 방법
다른 API를 활용한 **간접 검증**:

```python
# 1. 회원가입 API 호출
response = client.post("/account/signup", json=payload)
assert response.status_code == status.HTTP_201_CREATED

# 2. GET API로 재조회하여 DB 저장 확인
response = client.get(f"/account/users/{payload['username']}")
assert user_data["email"] == payload["email"]
```

### 핵심 인사이트
- API 테스트는 **API 응답만** 검증
- email/password 같은 내부 데이터는 **다른 엔드포인트**를 통해 간접 검증
- 이것이 API 레벨 테스트의 올바른 방식
- "signup API 테스트 파일인데, DB를 직접 조회할 필요가 있을까?" → **맞습니다. API 테스트는 다른 API로 간접 검증하는 것이 올바릅니다.**

---

## Q6: test_signup.py vs test_signup_api.py 차이는?

### 최종 구조

| 파일 | 테스트 방법 | 검증 대상 |
|------|------------|-----------|
| test_signup.py | `signup(dict, session)` 직접 호출 | 함수 로직, DB 저장 (유닛) |
| test_signup_api.py | `client.post()` HTTP 호출 | HTTP 응답, API 계약 (API) |

---

## Q7: 추가한 테스트와 개선 사항

### 추가한 테스트
```python
async def test_signup_password_mismatch(client: TestClient):
    # password != password_again 케이스
    payload = {
        "username": "test",
        "email": "test@example.com",
        "password": "test테스트1234",
        "password_again": "다른비밀번호",
    }
    response = client.post("/account/signup", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
```

### 개선 사항
1. email 체크 라인 제거 (API 응답에 없음)
2. GET API로 재조회 로직 추가 (email 간접 검증)
3. is_host 검증 추가
4. password 불일치 테스트 추가

---

## 핵심 교훈 (Key Takeaways)

1. **테스트 레벨 분리**: 유닛 테스트 vs API 테스트의 명확한 구분
2. **보안과 테스트의 균형**: response_model로 보안 확보, 다른 API로 검증
3. **API 테스트 원칙**: API는 API로 검증 (DB 직접 조회 지양)
4. **실용적 접근**: test_endpoints.py 패턴 참고하여 일관된 테스트 작성

이 과정을 통해 **"API 레벨에서 무엇을, 어떻게 테스트할 것인가"**에 대한 명확한 기준을 세웠습니다.

---

## 참고 파일
- `/tests/apps/account/test_signup.py` - 유닛 테스트
- `/tests/apps/account/test_signup_api.py` - API 테스트
- `/tests/apps/account/test_endpoints.py` - 참고한 테스트 패턴
- `/appserver/apps/account/endpoints.py` - signup 엔드포인트
- `/appserver/apps/account/schemas.py` - SignupPayload, UserOut 스키마
