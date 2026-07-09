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

## 현재 적용 범위 / 다음 단계
- **적용됨**: 제품 카탈로그 읽기(`products`) — 매칭 엔진은 DB 데이터로 동일하게 동작.
- **스키마만 준비됨**: `profiles`(계정) · `analyses`(분석 이력) · `posts`/`comments`(커뮤니티).
- **커뮤니티**는 현재 요구사항대로 **localStorage + 더미데이터**로 동작합니다. 서버 동기화로 옮기려면
  `posts`/`comments` 테이블 + Supabase Auth 로그인을 붙이고, 커뮤니티 JS의 `cmSave`/`cmLoad`를
  fetch 호출로 교체하면 됩니다.
