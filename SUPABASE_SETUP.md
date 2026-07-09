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
   - 작성 즉시 `posts`/`comments` 테이블에 저장되고, 다른 사용자는 **화면을 열거나 새로고침하면** 보입니다.

> 참고: 로그인 안 한 사용자도 글·댓글 **읽기**는 가능합니다(공개). 쓰기만 로그인 필요.
> 액세스 토큰은 약 1시간 후 만료됩니다. 만료 후 저장 실패 시 다시 로그인하세요.

## 현재 적용 범위
- **적용됨(코드)**: 제품 카탈로그 읽기(`products`) + 커뮤니티 글·댓글 읽기/쓰기(`posts`/`comments`) + 이메일 로그인.
  → secrets가 없으면 카탈로그는 내장 배열, 커뮤니티는 localStorage로 자동 폴백.
- **스키마만 준비됨**: `profiles`(프로필) · `analyses`(분석 이력) — 필요 시 연결.
- **실시간(새로고침 없이 자동 반영)**이 필요하면 Supabase Realtime 구독을 추가로 붙이면 됩니다.
