-- ============================================================
-- FOR HIM — Supabase schema + RLS + product seed
-- Supabase 대시보드 > SQL Editor 에 붙여넣고 실행하세요.
-- 실행 후 app 의 st.secrets 에 SUPABASE_URL / SUPABASE_ANON_KEY 를 넣으면
-- 프론트엔드가 products 테이블에서 카탈로그를 읽어옵니다.
-- (secrets 가 없으면 앱은 내장 카탈로그로 그대로 동작합니다.)
-- ============================================================

-- ---------- 1) 제품 카탈로그 ----------
create table if not exists public.products (
  id       text primary key,
  brand    text not null,
  name     text not null,
  cats     text[] not null default '{}',
  pop      int  not null default 70,
  tag      text default '',
  img_url  text,
  color    text default '#8b6f47',
  aff      jsonb not null default '{}'::jsonb
);

-- ---------- 2) 사용자 프로필 (auth.users 확장) ----------
create table if not exists public.profiles (
  id         uuid primary key references auth.users(id) on delete cascade,
  nickname   text,
  age        int,
  created_at timestamptz not null default now()
);

-- ---------- 3) 분석 이력 ----------
create table if not exists public.analyses (
  id         bigint generated always as identity primary key,
  user_id    uuid references auth.users(id) on delete cascade,
  concerns   text[] not null default '{}',
  scores     jsonb  not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

-- ---------- 4) 커뮤니티 (지금은 localStorage 로 동작.
--             나중에 서버 동기화로 옮길 때 사용) ----------
create table if not exists public.posts (
  id         bigint generated always as identity primary key,
  user_id    uuid references auth.users(id) on delete set null,
  author     text,
  category   text not null,
  title      text not null,
  body       text not null,
  photo_url  text,
  skin_tags  text[] not null default '{}',
  created_at timestamptz not null default now()
);

create table if not exists public.comments (
  id         bigint generated always as identity primary key,
  post_id    bigint references public.posts(id) on delete cascade,
  user_id    uuid references auth.users(id) on delete set null,
  author     text,
  body       text not null,
  created_at timestamptz not null default now()
);

-- ============================================================
-- RLS (Row Level Security) — 반드시 켜세요.
-- 안 켜면 anon 키로 누구나 수정/삭제할 수 있습니다.
-- ============================================================
alter table public.products  enable row level security;
alter table public.profiles  enable row level security;
alter table public.analyses  enable row level security;
alter table public.posts     enable row level security;
alter table public.comments  enable row level security;

-- products: 누구나 읽기만
drop policy if exists products_read on public.products;
create policy products_read on public.products for select using (true);

-- profiles: 본인 것만 읽고 쓰기
drop policy if exists profiles_self on public.profiles;
create policy profiles_self on public.profiles
  for all using (auth.uid() = id) with check (auth.uid() = id);

-- analyses: 본인 것만
drop policy if exists analyses_self on public.analyses;
create policy analyses_self on public.analyses
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- posts: 읽기는 전체, 작성은 로그인 사용자, 수정/삭제는 본인 글만
drop policy if exists posts_read   on public.posts;
drop policy if exists posts_insert on public.posts;
drop policy if exists posts_owner  on public.posts;
drop policy if exists posts_delete on public.posts;
create policy posts_read   on public.posts for select using (true);
create policy posts_insert on public.posts for insert with check (auth.uid() = user_id);
create policy posts_owner  on public.posts for update using (auth.uid() = user_id);
create policy posts_delete on public.posts for delete using (auth.uid() = user_id);

-- comments: 읽기는 전체, 작성은 로그인 사용자
drop policy if exists comments_read   on public.comments;
drop policy if exists comments_insert on public.comments;
create policy comments_read   on public.comments for select using (true);
create policy comments_insert on public.comments for insert with check (auth.uid() = user_id);

-- ============================================================
-- 제품 시드 (프론트엔드 내장 카탈로그와 동일한 28개)
-- ============================================================
insert into public.products (id, brand, name, cats, pop, tag, img_url, color, aff) values
('cosrx','코스알엑스','더 6 펩타이드 스킨 부스터 세럼','{serum}',96,'결·컨디션 개선','https://dn5hzapyfrpio.cloudfront.net/product/a97/a97c0080-1b38-11f0-a461-e9e3e4353caa.jpeg?w=426','#8b6f47','{"pore":2,"texture":3,"acne":2,"blemish":2,"pigment":2,"dull":2,"spot":1,"scar":1}'),
('toriden','토리든','다이브인 저분자 히알루론산 세럼','{serum}',94,'저분자 수분 진정','https://dn5hzapyfrpio.cloudfront.net/product/302/3029f520-5fed-11f1-94d9-bb4c387ac818.jpeg?w=426','#5c7a8b','{"dryness":3,"texture":2,"redness":2,"flake":2,"darkcircle":1}'),
('anua','아누아','PDRN 히알루론산 캡슐 100 세럼','{serum}',90,'PDRN 재생 케어','https://dn5hzapyfrpio.cloudfront.net/product/18f/18f9d910-e811-11ef-b7ff-9d94b272a52e.jpeg?w=426','#7a8b5c','{"scar":3,"pigment":2,"elastic":2,"tone":2,"darkcircle":1,"spot":2}'),
('anuaTuner','아누아','어성초 77 토너','{toner}',82,'모공·진정 토너',null,'#7a8b5c','{"pore":3,"oil":2,"acne":2,"ingrown":2,"flake":2,"texture":2,"blackhead":2}'),
('mediheal','메디힐','마데카소사이드 수분 선세럼','{sun}',85,'저자극 선케어','https://dn5hzapyfrpio.cloudfront.net/product/bf9/bf9d94f0-77ef-11f0-ba45-05d1d2abb09d.jpeg?w=426','#6b8b6f','{"oil":2,"redness":2,"acne":2}'),
('ahc','AHC','마스터즈 에어 리치 선스틱','{sun}',88,'산뜻한 선스틱','https://dn5hzapyfrpio.cloudfront.net/product/417/417b9320-49b2-11f1-ab05-f74f22f2eff9.jpeg?w=426','#4a7a9b','{"oil":2,"dull":1}'),
('goodalSun','구달','맑은 어성초 진정 수분 선크림','{sun}',80,'민감성 선크림','https://dn5hzapyfrpio.cloudfront.net/product/6f3/6f3891e0-c8cb-11f0-b07b-5b53b651bab0.jpeg?w=426','#7a9b6f','{"oil":2,"redness":2,"acne":2}'),
('goodalVitaC','구달','청귤 비타C 잡티 세럼','{serum}',87,'비타민C 브라이트닝',null,'#c9915c','{"spot":3,"pigment":3,"tone":2,"dull":2,"blemish":2}'),
('jsm','정샘물','에센셜 스킨 누더 쿠션','{cushion}',89,'자연스러운 피부 보정','https://dn5hzapyfrpio.cloudfront.net/product/5f6/5f61dd30-7850-11ee-b842-db65e1eeb438.jpeg?w=426','#c9915c','{"cover":3,"tone":2,"dull":1}'),
('hera','헤라','블랙 쿠션 파운데이션','{cushion}',84,'커버 + 지속력','https://dn5hzapyfrpio.cloudfront.net/product/fe1/fe18aa80-ebc8-11ee-8b0a-6d2974cceb54.jpeg?w=426','#9b7a4a','{"cover":3,"tone":2,"scar":1}'),
('clioCushion','클리오','킬커버 파운웨어 쿠션','{cushion}',83,'모공 커버','https://dn5hzapyfrpio.cloudfront.net/product/a88/a88ee6f0-846b-11f0-b021-b5dec3c00b35.jpeg?w=426','#b58b5c','{"cover":3,"pore":1,"tone":2}'),
('lumir','루미르','라이트 온 아이즈 섀도우 팔레트','{eye}',72,'퍼스널컬러 팔레트','https://dn5hzapyfrpio.cloudfront.net/product/629/629e9f90-47ff-11ef-9c5c-759480f80bcd.jpeg?w=426','#9b6f8b','{}'),
('peripera','페리페라','올테이크 무드 팔레트','{eye}',78,'데일리 아이 컬러','https://dn5hzapyfrpio.cloudfront.net/product/d34/d3475980-92e5-11f0-9444-11e570e33be4.jpeg?w=426','#c15c5c','{}'),
('clioEye','클리오','프로 아이 팔레트 에어','{eye}',76,'데일리 섀도우','https://dn5hzapyfrpio.cloudfront.net/product/9cb/9cbc3980-4242-11ee-88cc-5d4011facace.jpeg?w=426','#a85c6f','{}'),
('medicubeAger','메디큐브','AGE-R 부스터 프로','{device}',79,'리프팅 디바이스',null,'#5c6f8b','{"elastic":3,"wrinkle":2,"dull":1}'),
('vflab','브이플랩','브이토닝 디바이스','{device}',70,'얼굴 라인 관리',null,'#6f5c8b','{"elastic":2}'),
('wellbeing','웰빙시크릿','4D 페이스 마사지기','{device}',68,'붓기 케어',null,'#5c8b7a','{"darkcircle":2,"elastic":1}'),
('estraCream','에스트라','아토베리어365 크림','{cream}',86,'장벽 강화 크림',null,'#6b7a8b','{"dryness":3,"redness":2,"elastic":2,"flake":2}'),
('origins','오리진스','메가 버섯 퍼스트 에센스','{serum}',74,'탄력 영양 에센스',null,'#8b7a5c','{"elastic":2,"dull":2,"texture":2}'),
('medicubeMist','메디큐브','PDRN 핑크 콜라겐 젤리 미스트 세럼','{serum}',81,'PDRN 재생 미스트','https://dn5hzapyfrpio.cloudfront.net/product/adb/adbe3440-984e-11f0-9b5e-4999a7af4d26.jpeg?w=426','#a86f7a','{"elastic":2,"darkcircle":2,"dryness":2,"dull":1,"scar":1}'),
('esnature','에스네이처','아쿠아 스쿠알란 수분크림','{cream}',77,'수분 진정 크림',null,'#6b8b8b','{"dryness":3,"redness":1,"flake":1}'),
('drg','닥터지','레드 블레미쉬 클리어 수딩 토너','{toner}',88,'트러블 진정 토너','https://dn5hzapyfrpio.cloudfront.net/product/c67/c671e760-8bd2-11ed-a6ae-7f4a9ccf8e92.jpeg?w=426','#a85c5c','{"acne":3,"blemish":2,"redness":3,"shave":2}'),
('roundlabMadeca','라운드랩','마데카 크림','{cream}',85,'재생 진정 크림',null,'#5c8b6f','{"redness":2,"acne":2,"shave":2,"ingrown":2,"elastic":1}'),
('cosrxBHA','코스알엑스','BHA 블랙헤드 파워 리퀴드','{toner}',84,'모공 각질 케어',null,'#8b6f47','{"blackhead":3,"pore":2,"flake":2,"ingrown":2,"texture":2}'),
('innisfree','이니스프리','그린티 클렌징폼','{cleanser}',75,'산뜻한 세안',null,'#5c8b6f','{"blackhead":2,"oil":2}'),
('estraCleanser','에스트라','아토베리어365 클렌징폼','{cleanser}',76,'저자극 클렌징',null,'#6b7a8b','{"dryness":2,"redness":1}'),
('roundlabBirch','라운드랩','자작나무 수분크림','{cream}',80,'수분 진정',null,'#5c8b6f','{"dryness":2,"ingrown":1,"redness":1}'),
('physiogel','피지오겔','데일리 모이스쳐 테라피 에센스 인 토너','{toner}',78,'저자극 수분 토너','https://dn5hzapyfrpio.cloudfront.net/product/b1f/b1fc6de0-b9f2-11f0-97cf-eb8f804ad159.jpeg?w=426','#a86f6f','{"dryness":2,"redness":2,"shave":2,"darkcircle":1,"flake":2}')
on conflict (id) do update set
  brand=excluded.brand, name=excluded.name, cats=excluded.cats, pop=excluded.pop,
  tag=excluded.tag, img_url=excluded.img_url, color=excluded.color, aff=excluded.aff;
