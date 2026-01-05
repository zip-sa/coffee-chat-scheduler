# Signup API 테스트 구현 과정

## 개요
signup API의 보안 강화 및 테스트 구현 과정에서 발생한 문제 분석과 해결 방법을 기록한 개발 로그.

---

## 1. 문제 발견

### 1.1 초기 상황
`SignupPayload` 스키마 도입 후 기존 test_signup.py의 모든 테스트 실패.

```bash
AttributeError: 'dict' object has no attribute 'username'
```

### 1.2 근본 원인
- `endpoints.py`의 `signup` 함수: `SignupPayload` 객체 타입 기대
- `test_signup.py`: 여전히 `dict` 타입 전달
- 타입 불일치로 인한 속성 접근 불가

---

## 2. 해결 접근 방식

### 2.1 전략 선택
기존 유닛 테스트를 수정하는 대신, **새로운 API 레벨 테스트 파일 작성** 선택.

**선택 이유:**
- FastAPI의 TestClient는 자동으로 dict를 스키마 객체로 변환
- 실제 HTTP 요청/응답 흐름 테스트 가능
- API 계약(contract) 검증에 더 적합

### 2.2 테스트 레벨 분리

| 테스트 파일 | 테스트 방법 | 검증 대상 | 상태 |
|------------|-----------|----------|------|
| test_signup.py | `signup(dict, session)` 직접 호출 | 함수 로직, DB 저장 | 실패 (현재) |
| test_signup_api.py | `client.post()` HTTP 호출 | HTTP 응답, API 계약 | 통과 |

---

## 3. 보안 강화: UserOut 스키마

### 3.1 보안 이슈
API 응답에 민감한 정보(email, password)가 노출되는 문제 발견.

### 3.2 해결 방법
응답 전용 스키마 `UserOut` 도입:

```python
class UserOut(SQLModel):
    username: str
    display_name: str
    is_host: bool

@router.post("/signup", response_model=UserOut)
async def signup(payload: SignupPayload, session: DbSessionDep) -> UserOut:
    # ...
```

**효과:**
- FastAPI가 자동으로 응답 필터링
- username, display_name, is_host만 클라이언트로 전송
- email, password 등 민감 정보 제외

---

## 4. 테스트 구현 시 발견한 문제

### 4.1 테스트 케이스 모순
초기 `test_signup_api.py`의 두 테스트가 상충하는 요구사항 검증.

```python
# 테스트 1: email이 응답에 포함되길 기대
assert data["email"] == payload["email"]  # X UserOut에 email 없음

# 테스트 2: username, display_name, is_host만 포함되길 기대
expected_keys = frozenset(["username", "display_name", "is_host"])
assert response_keys == expected_keys  # O 올바른 요구사항
```

**문제:** `response_model=UserOut` 설정 시 두 테스트는 동시에 통과 불가.

### 4.2 email/password 검증 딜레마
"API 응답에서 제외한 email과 password는 어떻게 검증해야 하는가?"

**해결책: 간접 검증 패턴**

```python
# 1. 회원가입 API 호출 (UserOut 응답)
response = client.post("/account/signup", json=payload)
assert response.status_code == status.HTTP_201_CREATED
assert data["username"] == payload["username"]

# 2. GET API로 재조회 (User 전체 응답)
response = client.get(f"/account/users/{payload['username']}")
assert user_data["email"] == payload["email"]  # O 간접 검증
```

**핵심 원칙:**
- API 테스트는 해당 API의 응답만 직접 검증
- 내부 상태(DB 저장 여부)는 다른 엔드포인트를 통해 간접 검증
- DB를 직접 조회하는 것은 API 테스트의 범위를 벗어남

---

## 5. 최종 구현

### 5.1 테스트 커버리지

**test_signup_api.py:**
1. `test_signup_successfully`: 정상 회원가입 및 간접 검증
2. `test_signup_password_mismatch`: password 불일치 시 422 에러
3. `test_응답_결과에는_username_display_name_is_host_만_출력한다`: 응답 필드 검증

### 5.2 개선 사항
- API 응답 검증: UserOut 스키마 필드만 확인
- 데이터 저장 검증: GET API를 통한 간접 확인
- 보안 검증: 민감 정보 비노출 확인
- 예외 케이스: password 불일치 등

---

## 6. 의문점 및 추가 고민

### 6.1 현재 상황
`test_signup_api.py` 작성 후, 기존 `test_signup.py`는 모두 실패 상태.

```
7 failed in 0.10s
- test_signup_successfully: FAILED
- test_signup_invalid_username: FAILED (3 cases)
- test_signup_if_id_exists: FAILED
- test_signup_if_email_exists: FAILED
- test_signup_no_display_name: FAILED
```

### 6.2 선택지 비교

| 옵션 | 장점 | 단점 | 고려사항 |
|-----|------|------|---------|
| test_signup.py 수정 | 유닛/API 테스트 모두 보유 | 중복된 테스트 케이스 | 유지보수 비용 증가 |
| test_signup.py 삭제 | 단순하고 명확한 구조 | 유닛 테스트 부재 | API 테스트만으로 충분한가? |
| 현재 상태 유지 | 변경 없음 | 실패하는 테스트 방치 | 기술 부채 발생 |

### 6.3 핵심 질문
**"FastAPI 프로젝트에서 유닛 테스트와 API 테스트를 모두 유지하는 것이 best practice인가?"**

**추가 고려사항:**
- test_endpoints.py는 함수 직접 호출과 HTTP 호출 테스트를 모두 포함
- 하지만 `user_detail` 엔드포인트는 `response_model` 설정이 없어서 양쪽 테스트가 동일한 응답 수신
- `signup`은 `response_model=UserOut`으로 인해 두 테스트가 다른 응답 수신

**판단 필요:**
- 함수 로직만 테스트: test_signup.py 수정하여 SignupPayload 객체 전달
- API 계약만 검증: test_signup.py 제거
- 실무에서의 일반적인 접근 방식?

---

## 7. 학습 내용

### 7.1 테스트 설계 원칙
1. **테스트 레벨 명확화**: 유닛 vs 통합 vs API 테스트 구분
2. **간접 검증 패턴**: API 테스트에서 다른 엔드포인트 활용
3. **보안과 테스트의 균형**: response_model로 보안 확보, 간접 검증으로 커버리지 유지

### 7.2 FastAPI 특성 이해
1. TestClient의 자동 스키마 변환
2. response_model을 통한 자동 필터링
3. Pydantic 검증과 HTTP 422 응답

### 7.3 실용적 교훈
- 기존 코드 패턴(`test_endpoints.py`) 참고의 중요성
- 테스트 케이스 간 요구사항 일관성 확인 필요
- 테스트 실패 이유를 명확히 이해하고 접근

---

## 참고 파일
- `/tests/apps/account/test_signup.py` - 유닛 테스트 (현재 실패 상태)
- `/tests/apps/account/test_signup_api.py` - API 테스트 (통과)
- `/tests/apps/account/test_endpoints.py` - 참고한 테스트 패턴
- `/appserver/apps/account/endpoints.py` - signup 엔드포인트 구현
- `/appserver/apps/account/schemas.py` - SignupPayload, UserOut 스키마
