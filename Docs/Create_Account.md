### 목표: 
회원가입에 대한 사용자 스토리와 시나리오를 작성하기.

### User model 정의:
```python
class User(SQLModel, table=True):
    __tablename__ = "users" # type: ignore[arg-type]
    __table_args__ = (
        UniqueConstraint("email", name="uq_email"),
    )

    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=40, description="User Account ID")
    email: EmailStr = Field(max_length=128, description="User Email Address")
    display_name: str = Field(max_length=40, description="User Display Name")
    password: str = Field(max_length=128, description="User Password")
    is_host: bool = Field(default=False, description="Check Host")
```

### 회원가입 과정에서 일어나는 시나리오:
- 모든 입력 항목을 유요한 값으로 입력하면 계정이 생성되고 그 계정 데이터를 반환합니다.
- 사용자명: 4글자 이상, 40글자 이하, 영문, 숫자, 마침표, 빼기 기호만 가능.
- 표시명: 2글자 이상, 40글자 이하
- 비밀번호: 8글자 이상, 128글자 이하
- E-mail: 유효한 이메일 주소
- 생성 확인은 user_detail API로 합니다.
- 사용자명이 유효하지 않으면 사용자명이 유효하지 않다는 메시지를 담은 오류를 일으킵니다.
- 표시명이 유효하지 않으면 표시명이 유효하지 않다는 메시지를 담은 오류를 일으킵니다.
- 비밀번호가 유효하지 않으면 비밀번호가 유효하지 않다는 메시지를 담은 오류를 일으킵니다.
- 이메일(e-mail)이 유효하지 않으면 이메일이 유효하지 않다는 메시지를 담은 오류를 일으킵니다.
- 계정 ID(username)가 중복되면 중복 계정 ID 오류를 일으킵니다.
- 표시명을 입력하지 않으면 무작위 문자열 8글자로 대신합니다
- 응답 결과에는 username, display_name, is_host만 출력합니다.