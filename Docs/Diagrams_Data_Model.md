# Data Model Diagrams

## 1. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    User ||--o| Calendar : "has"
    User ||--o{ Booking : "makes"
    Calendar ||--o{ TimeSlot : "contains"
    TimeSlot ||--o{ Booking : "has"

    User {
        int id PK
        string username UK "4-40자, 영문/숫자/.-만"
        string email UK "유효한 이메일, 최대 128자"
        string display_name "2-40자"
        string password "해시된 비밀번호, 8-128자"
        bool is_host "호스트 여부"
    }

    Calendar {
        int id PK
        int host_id FK "users.id, unique"
        json topics "대화 주제 목록"
        string google_calendar_id "Google Calendar ID"
        datetime created_at
        datetime updated_at
    }

    TimeSlot {
        int id PK
        int calendar_id FK "calendars.id"
        time start_time "시작 시간"
        time end_time "종료 시간"
        json weekdays "예약 가능한 요일 (0-6)"
        datetime created_at
        datetime updated_at
    }

    Booking {
        int id PK
        int time_slot_id FK "time_slots.id"
        int guest_id FK "users.id"
        date when "예약 날짜"
        string topic "대화 주제"
        text description "상세 설명"
        datetime created_at
        datetime updated_at
    }
```

---

## 2. Database Schema (Detailed)

```mermaid
classDiagram
    class User {
        +int id
        +string username
        +EmailStr email
        +string display_name
        +string password
        +bool is_host
        +Calendar calendar
        +List~Booking~ bookings
        __tablename__ = "users"
        UniqueConstraint("email")
    }

    class Calendar {
        +int id
        +List~string~ topics
        +string google_calendar_id
        +int host_id
        +User host
        +List~TimeSlot~ time_slots
        +AwareDatetime created_at
        +AwareDatetime updated_at
        __tablename__ = "calendars"
    }

    class TimeSlot {
        +int id
        +time start_time
        +time end_time
        +List~int~ weekdays
        +int calendar_id
        +Calendar calendar
        +List~Booking~ bookings
        +AwareDatetime created_at
        +AwareDatetime updated_at
        __tablename__ = "time_slots"
    }

    class Booking {
        +int id
        +date when
        +string topic
        +Text description
        +int time_slot_id
        +TimeSlot time_slot
        +int guest_id
        +User guest
        +AwareDatetime created_at
        +AwareDatetime updated_at
        __tablename__ = "bookings"
    }

    User "1" -- "0..1" Calendar : host_id
    User "1" -- "0..*" Booking : guest_id
    Calendar "1" -- "0..*" TimeSlot : calendar_id
    TimeSlot "1" -- "0..*" Booking : time_slot_id
```

---

## 3. User Type Hierarchy

```mermaid
graph TD
    User[User<br/>기본 사용자 계정] --> Guest[Guest<br/>is_host = false]
    User --> Host[Host<br/>is_host = true]

    Guest --> GuestActions[가능한 작업]
    GuestActions --> GA1[다른 호스트의 캘린더 조회]
    GuestActions --> GA2[예약 가능한 시간대 확인]
    GuestActions --> GA3[커피챗 예약 생성]
    GuestActions --> GA4[자신의 예약 조회/관리]

    Host --> HostActions[가능한 작업]
    HostActions --> HA1[캘린더 생성/관리]
    HostActions --> HA2[대화 주제 설정]
    HostActions --> HA3[시간대 설정]
    HostActions --> HA4[예약 현황 조회]
    HostActions --> HA5[게스트 활동도 가능]

    style User fill:#e1e5ff
    style Guest fill:#e1f5e1
    style Host fill:#fff4e1
```

---

## 4. Data Flow - Account Creation to Booking

```mermaid
flowchart LR
    subgraph Registration["1. 계정 생성"]
        R1[User 생성<br/>is_host 설정]
    end

    subgraph HostSetup["2. 호스트 설정 (is_host=true만)"]
        H1[Calendar 생성]
        H2[Topics 설정]
        H3[TimeSlots 생성]
        H1 --> H2 --> H3
    end

    subgraph GuestBooking["3. 게스트 예약"]
        G1[호스트 캘린더 조회]
        G2[TimeSlot 선택]
        G3[Booking 생성]
        G1 --> G2 --> G3
    end

    R1 -->|is_host=true| H1
    R1 -->|is_host=false| G1
    H3 -.->|TimeSlots 제공| G2

    style Registration fill:#e1f5e1
    style HostSetup fill:#fff4e1
    style GuestBooking fill:#e1e5ff
```

---

## 5. Relationship Cardinality

```mermaid
graph LR
    subgraph One_to_One["1:1 관계"]
        U1[User<br/>host] ---|unique constraint| C1[Calendar]
    end

    subgraph One_to_Many_1["1:N 관계 - Calendar"]
        C2[Calendar] -->|1| TS1[TimeSlot]
        C2 -->|N| TS2[TimeSlot]
        C2 -->|...| TS3[TimeSlot]
    end

    subgraph One_to_Many_2["1:N 관계 - User as Guest"]
        U2[User<br/>guest] -->|1| B1[Booking]
        U2 -->|N| B2[Booking]
        U2 -->|...| B3[Booking]
    end

    subgraph One_to_Many_3["1:N 관계 - TimeSlot"]
        TS4[TimeSlot] -->|1| B4[Booking]
        TS4 -->|N| B5[Booking]
        TS4 -->|...| B6[Booking]
    end

    style One_to_One fill:#ffe1e1
    style One_to_Many_1 fill:#e1f5e1
    style One_to_Many_2 fill:#e1e5ff
    style One_to_Many_3 fill:#fff4e1
```

---

## 6. Field Type Overview

```mermaid
mindmap
  root((Coffee Chat<br/>Scheduler))
    User
      id: int PK
      username: str UK
      email: EmailStr UK
      display_name: str
      password: str hashed
      is_host: bool
    Calendar
      id: int PK
      host_id: int FK
      topics: JSON array
      google_calendar_id: str
      timestamps
    TimeSlot
      id: int PK
      calendar_id: int FK
      start_time: time
      end_time: time
      weekdays: JSON array
      timestamps
    Booking
      id: int PK
      time_slot_id: int FK
      guest_id: int FK
      when: date
      topic: str
      description: Text
      timestamps
```

---

## 다이어그램 설명

1. **ERD**: 테이블 간 관계와 주요 필드 표시
2. **Database Schema**: 클래스 다이어그램 형식으로 상세 필드 및 관계 표현
3. **User Type Hierarchy**: 게스트와 호스트의 차이점 및 가능한 작업
4. **Data Flow**: 계정 생성부터 예약까지의 데이터 흐름
5. **Relationship Cardinality**: 각 관계의 카디널리티(1:1, 1:N) 설명
6. **Field Type Overview**: 마인드맵 형식으로 전체 데이터 구조 개요

