# Secrets 정리 (FOR HIM)

Streamlit `st.secrets` 로 읽는 값 모음. **실제 값은 git 에 넣지 말 것** — 코드에서 참조하는 키만 정리합니다.
템플릿: [`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example) 복사 → 값 채워서 사용.

## 키 목록 (총 3그룹 7개)

| 키 | 그룹 | 용도 | 어디서 얻나 |
|---|---|---|---|
| `SUPABASE_URL` | Supabase | 커뮤니티 글/댓글 서버 | Supabase → Settings → API (현재: `oyekdzxedtbiartqntum.supabase.co`) |
| `SUPABASE_ANON_KEY` | Supabase | 위와 동일(anon/publishable) | 〃 (`sb_publishable_...`) |
| `[auth].redirect_uri` | 구글 OIDC | OAuth 콜백 = **앱URL + `/oauth2callback`** | 앱 배포 URL에서 조합 |
| `[auth].cookie_secret` | 구글 OIDC | 세션 쿠키 서명 | 임의 랜덤(예: `openssl rand -hex 32`) |
| `[auth].client_id` | 구글 OIDC | OAuth 클라이언트 | Google Cloud Console → 사용자 인증 정보 |
| `[auth].client_secret` | 구글 OIDC | 〃 | 〃 |
| `[auth].server_metadata_url` | 구글 OIDC | 구글 디스커버리(고정) | `https://accounts.google.com/.well-known/openid-configuration` |

- `SUPABASE_*` 없으면 → 커뮤니티는 localStorage 로컬 저장으로 동작(공유 X).
- `[auth]` 없으면 → 구글 로그인 버튼이 시뮬레이션(데모)으로 동작.
- 둘 다 **선택**이며, 없어도 앱은 정상 실행됨.

## 앱별로 어떤 secrets 가 필요한가

| 앱 (main file path) | Supabase | 구글 `[auth]` | 비고 |
|---|---|---|---|
| `app.py` (원본) | ✅ | ✅ | 현재 운영 중 |
| `designs/clean-full/app.py` | ✅ | ✅ | 원본과 **동일한 키 이름** 사용 |
| `designs/clean/app.py` | ❌ | ❌ | 순수 디자인 목업 — secrets 불필요 |
| `designs/playful/app.py` | ❌ | ❌ | 〃 |

> `app.py` 와 `clean-full` 은 **같은 Supabase 프로젝트/스키마**(`supabase_schema.sql`)와 **같은 구글 OAuth 클라이언트**를 공유해도 됩니다.

## ⚠️ 여러 앱을 배포할 때 (중요)

Streamlit Cloud 앱은 각각 **URL 이 다릅니다.** 그래서:

1. **`redirect_uri` 는 앱마다 달라야 함** — 그 앱의 실제 URL + `/oauth2callback`.
   - 예) clean-full 앱 URL 이 `https://forhim-clean.streamlit.app` 이면
     `redirect_uri = "https://forhim-clean.streamlit.app/oauth2callback"`.
2. **Google Cloud Console → 승인된 리디렉션 URI** 에 각 앱의 `.../oauth2callback` 을 **모두 등록**.
3. `client_id` / `client_secret` / `cookie_secret` / Supabase 키는 앱 간 **공유 가능**.

## 보안 메모
- `client_secret` 은 과거 채팅에 한 번 노출된 적 있음 → **재발급 권장**(Google Console에서 secret 재생성 후 secrets 갱신).
- 실제 `secrets.toml` 은 `.gitignore` 로 커밋 차단됨.
- Supabase 이메일 provider 의 **"Confirm email" 을 꺼두면** 구글→커뮤니티 자동 브리지가 매끄럽게 동작(켜져 있으면 커뮤니티에서 이메일 로그인 모달이 뜸).
