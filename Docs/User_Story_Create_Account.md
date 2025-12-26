# User Story: Create Account

## User Model
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=40, description="User Account ID")
    email: EmailStr = Field(max_length=128, description="User Email Address")
    display_name: str = Field(max_length=40, description="User Display Name")
    password: str = Field(max_length=128, description="User Password")
    is_host: bool = Field(default=False, description="Check Host")
```

---

## User Stories

### US-001: Basic Account Creation
**As a** new user
**I want to** create an account with username, email, and password
**So that** I can access the coffee chat scheduling system

**Acceptance Criteria:**
- Username must be 4-40 characters, only alphanumeric, dots, and hyphens allowed
- Email must be a valid email address (max 128 characters)
- Password must be 8-128 characters
- Display name must be 2-40 characters
- System returns user details (username, display_name, is_host) upon successful creation

---

### US-002: Display Name Auto-generation
**As a** new user
**I want to** optionally skip providing a display name
**So that** the system can auto-generate one for me if I prefer

**Acceptance Criteria:**
- If display_name is not provided, system generates a random 8-character string
- Auto-generated display name is included in the response

---

### US-003: Duplicate Username Prevention
**As a** new user
**I want to** be notified immediately if my chosen username is already taken
**So that** I can choose a different username without confusion

**Acceptance Criteria:**
- System checks for duplicate usernames before account creation
- Returns clear error message: "Username already exists"
- No account is created when username is duplicate

---

### US-004: Email Uniqueness Enforcement
**As a** new user
**I want to** register with a unique email address
**So that** I can maintain a single, identifiable account

**Acceptance Criteria:**
- Email must be unique in the system (database constraint)
- Returns clear error message if email already exists

---

### US-005: Input Validation Feedback
**As a** new user
**I want to** receive specific error messages for invalid inputs
**So that** I know exactly what to correct

**Acceptance Criteria:**
- Invalid username → "Username is invalid" error message
- Invalid display_name → "Display name is invalid" error message
- Invalid password → "Password is invalid" error message
- Invalid email → "Email is invalid" error message
- Each error message is descriptive and actionable

---

### US-006: Account Verification
**As a** new user
**I want to** verify my account was created successfully
**So that** I can confirm I can proceed to use the system

**Acceptance Criteria:**
- Account creation returns user details (username, display_name, is_host)
- User can verify account via user_detail API endpoint
- Password is NOT included in the response
