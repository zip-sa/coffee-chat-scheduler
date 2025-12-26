# User Scenarios: Create Account

## Scenario 1: Successful Account Creation (Happy Path)

**Context:** Sarah wants to join the coffee chat platform to book meetings with mentors.

**Steps:**
1. Sarah navigates to the registration page
2. She enters the following information:
   - Username: `sarah.kim`
   - Email: `sarah.kim@example.com`
   - Display Name: `Sarah Kim`
   - Password: `SecurePass123!`
   - is_host: `false` (default)
3. She clicks "Create Account" button
4. System validates all inputs (all valid)
5. System checks username uniqueness (available)
6. System checks email uniqueness (available)
7. System hashes the password
8. System creates user account in database
9. System returns response:
   ```json
   {
     "username": "sarah.kim",
     "display_name": "Sarah Kim",
     "is_host": false
   }
   ```
10. Sarah is redirected to login page or dashboard
11. Sarah can verify account using user_detail API

**Expected Result:** ✅ Account created successfully

---

## Scenario 2: Account Creation with Auto-generated Display Name

**Context:** John wants to create an account quickly without providing a display name.

**Steps:**
1. John navigates to the registration page
2. He enters:
   - Username: `john-doe`
   - Email: `john@example.com`
   - Display Name: _(left empty)_
   - Password: `MyPassword2024`
3. He clicks "Create Account" button
4. System detects missing display_name
5. System auto-generates random 8-character string: `X7k9Qp2M`
6. System creates account with auto-generated display_name
7. System returns response:
   ```json
   {
     "username": "john-doe",
     "display_name": "X7k9Qp2M",
     "is_host": false
   }
   ```

**Expected Result:** ✅ Account created with auto-generated display name

---

## Scenario 3: Invalid Username Format

**Context:** Mike tries to create an account with an invalid username.

**Steps:**
1. Mike navigates to the registration page
2. He enters:
   - Username: `mi` _(only 2 characters, minimum is 4)_
   - Email: `mike@example.com`
   - Display Name: `Mike`
   - Password: `Password123`
3. He clicks "Create Account" button
4. System validates username
5. System detects username is too short (< 4 characters)
6. System returns error:
   ```json
   {
     "error": "Username is invalid",
     "details": "Username must be 4-40 characters"
   }
   ```

**Expected Result:** ❌ Account creation fails with validation error

**Alternative Invalid Scenarios:**
- Username with special characters: `mike@123` → Error
- Username > 40 characters → Error
- Username with spaces: `mike smith` → Error

---

## Scenario 4: Duplicate Username

**Context:** Lisa tries to register with a username that already exists.

**Steps:**
1. Lisa navigates to the registration page
2. She enters:
   - Username: `sarah.kim` _(already exists from Scenario 1)_
   - Email: `lisa@example.com`
   - Display Name: `Lisa`
   - Password: `LisaPass2024`
3. She clicks "Create Account" button
4. System validates inputs (all valid format)
5. System checks username uniqueness
6. System finds existing user with username `sarah.kim`
7. System returns error:
   ```json
   {
     "error": "Username already exists"
   }
   ```

**Expected Result:** ❌ Account creation fails due to duplicate username

---

## Scenario 5: Invalid Email Format

**Context:** David enters an invalid email address.

**Steps:**
1. David navigates to the registration page
2. He enters:
   - Username: `david.lee`
   - Email: `invalid-email` _(missing @ and domain)_
   - Display Name: `David Lee`
   - Password: `SecurePass123`
3. He clicks "Create Account" button
4. System validates email format
5. System detects invalid email format
6. System returns error:
   ```json
   {
     "error": "Email is invalid",
     "details": "Please enter a valid email address"
   }
   ```

**Expected Result:** ❌ Account creation fails with email validation error

---

## Scenario 6: Duplicate Email Address

**Context:** Emma tries to register with an email that's already in use.

**Steps:**
1. Emma navigates to the registration page
2. She enters:
   - Username: `emma.wilson`
   - Email: `sarah.kim@example.com` _(already exists from Scenario 1)_
   - Display Name: `Emma Wilson`
   - Password: `EmmaPass123`
3. She clicks "Create Account" button
4. System validates inputs
5. System checks email uniqueness (database constraint)
6. System detects duplicate email
7. System returns error:
   ```json
   {
     "error": "Email already exists"
   }
   ```

**Expected Result:** ❌ Account creation fails due to duplicate email

---

## Scenario 7: Invalid Password (Too Short)

**Context:** Tom tries to create an account with a weak password.

**Steps:**
1. Tom navigates to the registration page
2. He enters:
   - Username: `tom.jones`
   - Email: `tom@example.com`
   - Display Name: `Tom`
   - Password: `pass` _(only 4 characters, minimum is 8)_
3. He clicks "Create Account" button
4. System validates password
5. System detects password is too short (< 8 characters)
6. System returns error:
   ```json
   {
     "error": "Password is invalid",
     "details": "Password must be 8-128 characters"
   }
   ```

**Expected Result:** ❌ Account creation fails with password validation error

---

## Scenario 8: Invalid Display Name (Too Short)

**Context:** Amy provides a display name that's too short.

**Steps:**
1. Amy navigates to the registration page
2. She enters:
   - Username: `amy.park`
   - Email: `amy@example.com`
   - Display Name: `A` _(only 1 character, minimum is 2)_
   - Password: `AmyPass2024`
3. She clicks "Create Account" button
4. System validates display_name
5. System detects display_name is too short (< 2 characters)
6. System returns error:
   ```json
   {
     "error": "Display name is invalid",
     "details": "Display name must be 2-40 characters"
   }
   ```

**Expected Result:** ❌ Account creation fails with display name validation error

---

## Scenario 9: Host Account Creation

**Context:** Dr. Martinez wants to create an account as a host to offer mentoring sessions.

**Steps:**
1. Dr. Martinez navigates to the registration page
2. He enters:
   - Username: `dr.martinez`
   - Email: `martinez@example.com`
   - Display Name: `Dr. Martinez`
   - Password: `HostPassword123`
   - is_host: `true` _(selects host option)_
3. He clicks "Create Account" button
4. System validates all inputs (all valid)
5. System creates account with is_host=true
6. System returns response:
   ```json
   {
     "username": "dr.martinez",
     "display_name": "Dr. Martinez",
     "is_host": true
   }
   ```
7. Dr. Martinez is redirected to host onboarding page

**Expected Result:** ✅ Host account created successfully

---

## Scenario 10: Account Verification via API

**Context:** After creating an account, Sarah verifies it using the user_detail API.

**Steps:**
1. Sarah successfully creates account (username: `sarah.kim`)
2. She receives account creation response
3. She calls user_detail API:
   ```
   GET /api/users/sarah.kim
   ```
4. System retrieves user details from database
5. System returns:
   ```json
   {
     "username": "sarah.kim",
     "email": "sarah.kim@example.com",
     "display_name": "Sarah Kim",
     "is_host": false
   }
   ```
6. Sarah confirms account details match registration

**Expected Result:** ✅ Account verified successfully via API

**Note:** Password is NOT returned in the response for security reasons.
