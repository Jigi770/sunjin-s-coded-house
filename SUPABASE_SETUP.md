# Supabase 연동 가이드

이 데모는 **Supabase 없이도 그대로 동작**합니다(내장 카탈로그로 폴백). 아래는 실제 DB를 붙일 때만 필요합니다.

## 1. 프로젝트 만들기
1. https://supabase.com 에서 프로젝트 생성
2. **SQL Editor** 열기 → [`supabase_schema.sql`](supabase_schema.sql) 전체를 붙여넣고 실행
   - 테이블(products / profiles / analyses / posts / comments) + RLS + 제품 28개 시드가 한 번에 생성됩니다.

## 2. 키 넣기 (Streamlit secrets)
`Project Settings > API` 에서 **Project URL** 과 **anon public** 키를 복사한 뒤,
Streamlit Cloud 의 **Settings > Secrets** (또는 로컬 `.streamlit/secrets.toml`)에 추가:

```toml
SUPABASE_URL = "https://xxxx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOi..."   # anon public 키
```

앱을 새로고침하면 프론트엔드가 `products` 테이블에서 카탈로그를 불러옵니다.
불러오기에 실패하면 자동으로 내장 카탈로그를 사용하므로 화면이 깨지지 않습니다.

## 3. 보안 주의
- 프론트엔드(브라우저)에는 **anon public 키만** 넣습니다. 공개돼도 되는 키입니다.
- **`service_role` 키는 절대 프론트/secrets 로 노출하지 마세요.** RLS를 우회합니다.
- 위 스키마의 RLS 정책이 "products 읽기 전용, posts는 본인 글만 수정" 등을 강제합니다. RLS를 끄면 안 됩니다.

## 4. 커뮤니티 실시간 공유(로그인) 켜기
커뮤니티 글·댓글을 **여러 사용자가 서로 보게** 하려면 이메일 로그인이 필요합니다.
`secrets`에 URL·anon 키를 넣으면 커뮤니티가 자동으로 Supabase 모드로 전환됩니다
(넣기 전까지는 localStorage 모드로 동작).

1. Supabase 대시보드 > **Authentication > Providers > Email** 활성화
2. **Authentication > Sign In / Providers > Email > "Confirm email" 옵션 끄기**
   - 데모에서 이메일 인증 메일 없이 바로 가입·로그인되게 하려면 꺼야 합니다.
   - 켜두면 가입 후 메일의 링크를 눌러야 로그인됩니다.
3. 앱 커뮤니티 우측 상단 **로그인** 버튼으로 가입/로그인 → 글·댓글 작성 가능
   - 작성 즉시 `posts`/`comments` 테이블에 저장되고, 다른 사용자 화면에도 **자동 반영**됩니다(아래 4-1 참고).

### 4-1. 실시간 반영 (Realtime)
앱은 두 단계로 다른 사용자의 글·댓글을 자동 반영합니다:
- **Supabase Realtime(웹소켓)**: `posts`/`comments` 변경 이벤트를 구독해 **즉시** 갱신.
  활성화하려면 SQL Editor에서 `supabase_schema.sql` 하단의
  `alter publication supabase_realtime add table posts, comments` 블록을 실행하거나,
  대시보드 **Database > Replication** 에서 두 테이블의 Realtime을 켜세요.
- **폴링 폴백**: Realtime이 꺼져 있거나 웹소켓이 차단된 환경에서는 커뮤니티 화면이
  열려 있는 동안 12초 간격으로 자동 재조회합니다. 별도 설정이 필요 없습니다.

> 참고: 로그인 안 한 사용자도 글·댓글 **읽기**는 가능합니다(공개). 쓰기만 로그인 필요.
> 액세스 토큰은 약 1시간 후 만료됩니다. 만료 후 저장 실패 시 다시 로그인하세요.

## 5. 실제 구글 로그인 (Streamlit `st.login` / OIDC)
구글 로그인은 iframe 안이 아니라 **Streamlit(Python) 레이어**에서 동작합니다. 설정하면 앱 상단에
"Google 계정으로 로그인" 버튼이 나타나고, 로그인하면 실제 이메일·이름이 iframe에 전달되어
프로필 설정(닉네임/나이 입력) → 마이페이지로 이어집니다. **미설정 시에는 앱이 기존 데모(가상 소셜 로그인)로
그대로 동작**합니다.

### 5-1. Google Cloud에서 OAuth 클라이언트 만들기
1. Google Cloud Console > **APIs & Services > Credentials > Create OAuth client ID**
2. 유형: **Web application**
3. **Authorized redirect URI** 에 앱 주소 + `/oauth2callback` 추가
   - 예) 로컬: `http://localhost:8501/oauth2callback`
   - 예) 배포: `https://<your-app>.streamlit.app/oauth2callback`
4. 생성된 **Client ID / Client secret** 복사

### 5-2. `.streamlit/secrets.toml` 에 `[auth]` 추가
```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"   # 배포 시 배포 URL로
cookie_secret = "아무_긴_랜덤_문자열_32자이상"
client_id = "구글 Client ID"
client_secret = "구글 Client secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```
> `requirements.txt`에 `Authlib>=1.3.2`가 포함돼 있어야 합니다(이미 추가됨).
> Streamlit 1.42+ 필요(현재 1.59.0).

### 5-3. 동작
- 상단 **[Google 계정으로 로그인]** → 구글 동의 → 앱으로 복귀 → `st.user`에 이메일/이름 채워짐
- iframe이 이를 받아 **프로필 설정**(닉네임 입력, 나이 입력; 이메일은 구글에서 자동) → 마이페이지
- 상단 **[로그아웃]** 으로 세션 종료

### 참고 / 한계
- **카카오·네이버**는 이 방식의 실제 연동에 포함하지 않았습니다(구글만). 앱 내 카카오/네이버 버튼은 데모 시뮬레이션으로 남아 있습니다.
- **나이**는 구글 OIDC 기본 스코프로 제공되지 않아, 프로필 단계에서 입력받습니다(이메일·이름만 자동).

## 현재 적용 범위
- **적용됨(코드)**: 제품 카탈로그 읽기(`products`) + 커뮤니티 글·댓글 읽기/쓰기(`posts`/`comments`) + 이메일 로그인.
  → secrets가 없으면 카탈로그는 내장 배열, 커뮤니티는 localStorage로 자동 폴백.
- **적용됨(실시간)**: 커뮤니티 글·댓글 자동 반영 — Realtime 구독 + 12초 폴링 폴백 (4-1 참고).
- **스키마만 준비됨**: `profiles`(프로필) · `analyses`(분석 이력) — 필요 시 연결.
- **주의**: `supabase_schema.sql`의 products 시드는 예전 28개 카탈로그 기준입니다. 원격 카탈로그는
  같은 id의 내장 항목을 덮어쓰므로, 시드를 실행했던 프로젝트라면 최신 100개 카탈로그와 어긋날 수
  있습니다(미실행 시 무관 — 내장 카탈로그 사용).
