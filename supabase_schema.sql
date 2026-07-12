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
  aff      jsonb not null default '{}'::jsonb,
  ing      text[] not null default '{}',   -- 핵심 성분 (성분→효능 매핑으로 추천 가중치 자동 보강)
  oy_url   text                            -- 올리브영 상세페이지 URL (없으면 검색 폴백)
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
-- 제품 시드 (프론트엔드 내장 카탈로그와 동일한 100개 · app.py에서 자동 생성)
-- ============================================================
-- 성분(ing)·올리브영 상세페이지(oy_url) 컬럼 — 구버전 프로젝트도 재실행만으로 반영
alter table public.products add column if not exists ing text[] not null default '{}';
alter table public.products add column if not exists oy_url text;

-- 구버전 시드에만 있던 미입점·데모용 제품 정리
delete from public.products where id in ('vflab','wellbeing','origins','roundlabMadeca','foretPerfume','tamburinsPerfume','granhandPerfume','ceraveBody','jejuFoot','scholFoot','niveaDeo','domeDeo','cosrxBHA');

insert into public.products (id, brand, name, cats, pop, tag, img_url, color, aff, ing, oy_url) values
('cosrx','코스알엑스','더 6 펩타이드 스킨 부스터 세럼','{"serum"}',96,'결·컨디션 개선','https://dn5hzapyfrpio.cloudfront.net/product/a97/a97c0080-1b38-11f0-a461-e9e3e4353caa.jpeg?w=426','#8b6f47','{"pore":2,"texture":3,"acne":2,"blemish":2,"pigment":2,"dull":2,"spot":1,"scar":1}','{"펩타이드","나이아신아마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000204071'),
('toriden','토리든','다이브인 저분자 히알루론산 세럼','{"serum"}',94,'저분자 수분 진정','https://dn5hzapyfrpio.cloudfront.net/product/302/3029f520-5fed-11f1-94d9-bb4c387ac818.jpeg?w=426','#5c7a8b','{"dryness":3,"texture":2,"redness":2,"flake":2,"darkcircle":1}','{"히알루론산","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000190326'),
('anua','아누아','PDRN 히알루론산 캡슐 100 세럼','{"serum"}',90,'PDRN 재생 케어','https://dn5hzapyfrpio.cloudfront.net/product/18f/18f9d910-e811-11ef-b7ff-9d94b272a52e.jpeg?w=426','#7a8b5c','{"scar":3,"pigment":2,"elastic":2,"tone":2,"darkcircle":1,"spot":2}','{"PDRN","히알루론산"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000210655'),
('anuaTuner','아누아','어성초 77 토너','{"toner"}',82,'모공·진정 토너','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0014/A00000014733901ko.jpg','#7a8b5c','{"pore":3,"oil":2,"acne":2,"ingrown":2,"flake":2,"texture":2,"blackhead":2}','{"어성초"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000147339'),
('mediheal','메디힐','마데카소사이드 수분 선세럼','{"sun"}',85,'저자극 선케어','https://dn5hzapyfrpio.cloudfront.net/product/bf9/bf9d94f0-77ef-11f0-ba45-05d1d2abb09d.jpeg?w=426','#6b8b6f','{"oil":2,"redness":2,"acne":2}','{"마데카소사이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000223423'),
('ahc','AHC','마스터즈 에어 리치 선스틱','{"sun"}',88,'산뜻한 선스틱','https://dn5hzapyfrpio.cloudfront.net/product/417/417b9320-49b2-11f1-ab05-f74f22f2eff9.jpeg?w=426','#4a7a9b','{"oil":2,"dull":1}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000182989'),
('goodalSun','구달','맑은 어성초 진정 수분 선크림','{"sun"}',80,'민감성 선크림','https://dn5hzapyfrpio.cloudfront.net/product/6f3/6f3891e0-c8cb-11f0-b07b-5b53b651bab0.jpeg?w=426','#7a9b6f','{"oil":2,"redness":2,"acne":2}','{"어성초"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000198527'),
('goodalVitaC','구달','청귤 비타C 잡티 세럼','{"serum"}',87,'비타민C 브라이트닝','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0022/A00000022979001ko.jpg','#c9915c','{"spot":3,"pigment":3,"tone":2,"dull":2,"blemish":2}','{"비타민C"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000229790'),
('jsm','정샘물','에센셜 스킨 누더 쿠션','{"cushion"}',89,'자연스러운 피부 보정','https://dn5hzapyfrpio.cloudfront.net/product/5f6/5f61dd30-7850-11ee-b842-db65e1eeb438.jpeg?w=426','#c9915c','{"cover":3,"tone":2,"dull":1}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000139063'),
('hera','헤라','블랙 쿠션 파운데이션','{"cushion"}',84,'커버 + 지속력','https://dn5hzapyfrpio.cloudfront.net/product/fe1/fe18aa80-ebc8-11ee-8b0a-6d2974cceb54.jpeg?w=426','#9b7a4a','{"cover":3,"tone":2,"scar":1}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000202777'),
('clioCushion','클리오','킬커버 파운웨어 쿠션','{"cushion"}',83,'모공 커버','https://dn5hzapyfrpio.cloudfront.net/product/a88/a88ee6f0-846b-11f0-b021-b5dec3c00b35.jpeg?w=426','#b58b5c','{"cover":3,"pore":1,"tone":2}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000232098'),
('lumir','루미르','라이트 온 아이즈 섀도우 팔레트','{"eye"}',72,'퍼스널컬러 팔레트','https://dn5hzapyfrpio.cloudfront.net/product/629/629e9f90-47ff-11ef-9c5c-759480f80bcd.jpeg?w=426','#9b6f8b','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000208498'),
('peripera','페리페라','올테이크 무드 팔레트','{"eye"}',78,'데일리 아이 컬러','https://dn5hzapyfrpio.cloudfront.net/product/d34/d3475980-92e5-11f0-9444-11e570e33be4.jpeg?w=426','#c15c5c','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000204450'),
('clioEye','클리오','프로 아이 팔레트 에어','{"eye"}',76,'데일리 섀도우','https://dn5hzapyfrpio.cloudfront.net/product/9cb/9cbc3980-4242-11ee-88cc-5d4011facace.jpeg?w=426','#a85c6f','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000188988'),
('medicubeAger','메디큐브','AGE-R 부스터 프로','{"device"}',79,'리프팅 디바이스','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0021/A00000021295912ko.jpg?l=ko','#5c6f8b','{"elastic":3,"wrinkle":2,"dull":1}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000212959'),
('estraCream','에스트라','아토베리어365 크림','{"cream"}',86,'장벽 강화 크림','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0019/A00000019832009ko.jpg?l=ko','#6b7a8b','{"dryness":3,"redness":2,"elastic":2,"flake":2}','{"세라마이드","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000198320'),
('medicubeMist','메디큐브','PDRN 핑크 콜라겐 젤리 미스트 세럼','{"serum"}',81,'PDRN 재생 미스트','https://dn5hzapyfrpio.cloudfront.net/product/adb/adbe3440-984e-11f0-9b5e-4999a7af4d26.jpeg?w=426','#a86f7a','{"elastic":2,"darkcircle":2,"dryness":2,"dull":1,"scar":1}','{"PDRN","콜라겐"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000233228'),
('esnature','에스네이처','아쿠아 스쿠알란 수분크림','{"cream"}',77,'수분 진정 크림','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0015/A00000015204661ko.jpg?l=ko','#6b8b8b','{"dryness":3,"redness":1,"flake":1}','{"스쿠알란","히알루론산"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000152046'),
('drg','닥터지','레드 블레미쉬 클리어 수딩 토너','{"toner"}',88,'트러블 진정 토너','https://dn5hzapyfrpio.cloudfront.net/product/c67/c671e760-8bd2-11ed-a6ae-7f4a9ccf8e92.jpeg?w=426','#a85c5c','{"acne":3,"blemish":2,"redness":3,"shave":2}','{"병풀(시카)","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000154177'),
('innisfree','이니스프리','그린티 클렌징폼','{"cleanser"}',75,'산뜻한 세안','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0019/A00000019059003ko.jpg','#5c8b6f','{"blackhead":2,"oil":2}','{"녹차"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000190590'),
('estraCleanser','에스트라','아토베리어365 클렌징폼','{"cleanser"}',76,'저자극 클렌징','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0024/A00000024504601ko.jpg','#6b7a8b','{"dryness":2,"redness":1}','{"세라마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000245046'),
('roundlabBirch','라운드랩','자작나무 수분크림','{"cream"}',80,'수분 진정','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0014/A00000014557901ko.jpg','#5c8b6f','{"dryness":2,"ingrown":1,"redness":1}','{"자작나무 수액"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000145579'),
('physiogel','피지오겔','데일리 모이스쳐 테라피 에센스 인 토너','{"toner"}',78,'저자극 수분 토너','https://dn5hzapyfrpio.cloudfront.net/product/b1f/b1fc6de0-b9f2-11f0-97cf-eb8f804ad159.jpeg?w=426','#a86f6f','{"dryness":2,"redness":2,"shave":2,"darkcircle":1,"flake":2}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000148899'),
('illiyoonLotion','일리윤','세라마이드 아토 로션','{"lotion","bodylotion"}',83,'세라마이드 보습','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0015/A00000015782001ko.jpg','#8ba0b0','{"dryness":3,"flake":2,"redness":1}','{"세라마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000157820'),
('cnpLotion','CNP','프로폴리스 트리트먼트 앰플 에센스','{"serum"}',78,'프로폴리스 광채','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0015/A00000015928001ko.jpg','#c9a86a','{"dryness":2,"dull":2,"elastic":1}','{"프로폴리스"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000159280'),
('roundlabLotion','라운드랩','1025 독도 로션','{"lotion"}',84,'약산성 수분 로션','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0014/A00000014557601ko.jpg','#5c7a8b','{"dryness":2,"redness":1,"flake":1}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000145576'),
('clioBrow','클리오','킬브로우 오토 하드 브로우 펜슬','{"brow"}',88,'자연스러운 눈썹','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/550/10/0000/0001/A00000001559701ko.jpg','#6b5744','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000015597'),
('etudeBrow','에뛰드','더 리얼 아이브로우 오토펜슬','{"brow"}',82,'입문용 브로우','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0017/A00000017111401ko.jpg','#7a6248','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000171114'),
('ridleBrow','롬앤','한올 샤프 브로우','{"brow"}',75,'디테일 표현','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0014/A00000014824901ko.jpg','#5c4a38','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000148249'),
('aveenoBody','아비노','데일리 모이스처라이징 바디로션','{"bodylotion"}',85,'귀리 보습','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0019/A00000019112701ko.jpg','#6b8b8b','{"dryness":3,"flake":2}','{"콜로이드 오트밀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000191127'),
('sensodyneBody','존슨즈','베이비 핑크 로션','{"bodylotion"}',74,'순한 데일리 보습','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0000/A00000000074901ko.jpg','#9b8b7a','{"dryness":2}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000000749'),
('madecaTimeReverseCream','센텔리안24','마데카 크림 타임 리버스','{"cream"}',92,'진정 흔적 케어','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0019/A00000019889201ko.jpg','#5c8b6f','{"scar":3,"redness":2,"wrinkle":2,"elastic":1}','{"마데카소사이드","병풀(시카)"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000198892'),
('anuaHeartleaf70Cream','아누아','어성초 70 수딩 크림','{"cream"}',90,'어성초 진정','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0020/A00000020826501ko.jpg','#7a8b5c','{"redness":3,"acne":2,"dryness":1}','{"어성초","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000208265'),
('torridenDiveInCream','토리든','다이브인 저분자 히알루론산 수딩 크림','{"cream"}',94,'속수분 충전','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0016/A00000016931301ko.jpg','#5c7a8b','{"dryness":3,"redness":2,"flake":2}','{"히알루론산","판테놀","알란토인"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000169313'),
('skin1004CentellaCream','스킨1004','마다가스카르 센텔라 수딩 크림','{"cream"}',89,'시카 진정','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0016/A00000016157301ko.jpg','#6b8b6f','{"redness":3,"acne":2,"oil":1}','{"병풀(시카)","마데카소사이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000161573'),
('physiogelDmtCream','피지오겔','DMT 페이셜 크림','{"cream"}',87,'장벽 보습','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0001/A00000001288101ko.jpg','#a86f6f','{"dryness":3,"flake":3,"redness":1}','{"세라마이드","스쿠알란"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000012881'),
('atopalmMleCream','아토팜','MLE 크림','{"cream"}',84,'민감 장벽크림','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0013/A00000013105101ko.jpg','#c9915c','{"dryness":3,"redness":2,"flake":2}','{"세라마이드","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000131051'),
('medicubePdrnCapsuleCream','메디큐브','PDRN 핑크 콜라겐 캡슐크림','{"cream"}',89,'탄력 물광크림','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0022/A00000022395201ko.jpg','#a86f7a','{"elastic":3,"wrinkle":2,"dull":2,"tone":1}','{"PDRN","콜라겐","나이아신아마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000223952'),
('isoiBlemishCream','아이소이','블레미쉬 케어 흔적크림','{"cream"}',82,'잡티 흔적케어','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0022/A00000022321507ko.jpg','#9b6f8b','{"spot":3,"blemish":3,"pigment":2,"scar":2,"tone":1}','{"나이아신아마이드","마데카소사이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000223215'),
('manyoPureCleansingOil','마녀공장','퓨어 클렌징 오일','{"cleanser"}',96,'블랙헤드 용해','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0010/A00000010767901ko.jpg','#8b7a5c','{"blackhead":3,"pore":2,"oil":2,"dull":1}','{"올리브 오일"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000107679'),
('banilaCleanItZeroBalm','바닐라코','클린잇제로 오리지널 클렌징밤','{"cleanser"}',92,'메이크업 클렌징','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0020/A00000020267501ko.jpg','#c98ba0','{"blackhead":2,"dull":2,"pore":1,"texture":1}','{"아세로라 추출물"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000202675'),
('roundlabDokdoCleanser','라운드랩','1025 독도 클렌저','{"cleanser"}',91,'약산성 순세안','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0015/A00000015118501ko.jpg','#5c7a8b','{"redness":2,"dryness":2,"flake":1}','{"해양심층수"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000151185'),
('anuaSuccinicFoam','아누아','어성초 석시닉 모이스처 클렌징폼','{"cleanser"}',81,'촉촉 약산성폼','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0021/A00000021119401ko.jpg','#7a8b5c','{"oil":2,"acne":2,"redness":2,"dryness":1}','{"어성초"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000211194'),
('drgRedBlemishFoam','닥터지','약산성 레드 블레미쉬 클리어 수딩 폼','{"cleanser"}',88,'진정 세안폼','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0014/A00000014572801ko.jpg','#a85c5c','{"redness":3,"acne":2,"blemish":2,"dryness":1}','{"병풀(시카)","히알루론산"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000145728'),
('aesturaAtoBarrierLotion','에스트라','아토베리어365 로션','{"lotion"}',93,'장벽 데일리','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0019/A00000019832101ko.jpg','#6b7a8b','{"dryness":3,"redness":2,"flake":2}','{"세라마이드","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000198321'),
('physiogelDmtLotion','피지오겔','DMT 데일리 보습 페이셜 로션','{"lotion"}',83,'산뜻 보습로션','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0001/A00000001280901ko.jpg','#a86f6f','{"dryness":3,"flake":2}','{"세라마이드","스쿠알란"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000012809'),
('atopalmMleLotion','아토팜','MLE 로션','{"lotion"}',80,'온가족 보습','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0000/A00000000978801ko.jpg','#c9915c','{"dryness":3,"redness":2,"flake":1}','{"세라마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000009788'),
('numbuzinNo3Serum','넘버즈인','3번 보들보들 결 세럼','{"serum"}',91,'결 개선 세럼','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0019/A00000019177401ko.jpg','#8b8b6f','{"pore":2,"texture":3,"dryness":1,"tone":1}','{"갈락토미세스","나이아신아마이드","베타글루칸"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000191774'),
('cellfusionToningC','셀퓨전씨','토닝 C 잡티세럼','{"serum"}',85,'비타민 토닝','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018281501ko.jpg','#c9a05c','{"spot":3,"pigment":3,"tone":2,"dull":2}','{"비타민C","나이아신아마이드","글루타치온"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000182815'),
('anuaTxaSerum','아누아','TXA 나이아신 흔적 세럼','{"serum"}',88,'흔적 미백','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0020/A00000020870801ko.jpg','#7a8b5c','{"blemish":3,"spot":2,"pigment":3,"tone":2}','{"나이아신아마이드","트라넥삼산"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000208708'),
('dalbaWhiteTruffleSerum','달바','화이트 트러플 퍼스트 스프레이 세럼','{"serum"}',90,'광채 미스트','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0013/A00000013001301ko.jpg','#b5a06a','{"dryness":2,"dull":2,"elastic":1}','{"히알루론산","프로폴리스"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000130013'),
('manyoGalacNiacin','마녀공장','갈락 나이아신 2.0 에센스','{"serum"}',86,'투명 광채','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0013/A00000013701601ko.jpg','#8b7a5c','{"tone":2,"dull":3,"texture":2,"spot":1}','{"갈락토미세스","나이아신아마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000137016'),
('skin1004CentellaAmpoule','스킨1004','마다가스카르 센텔라 앰플','{"serum"}',93,'시카 진정 앰플','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0016/A00000016158101ko.jpg','#6b8b6f','{"redness":3,"acne":2,"dryness":1}','{"병풀(시카)"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000161581'),
('wellageBlueAmpoule','웰라쥬','리얼 히알루로닉 블루 100 앰플','{"serum"}',87,'속건조 해결','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0014/A00000014780901ko.jpg','#5c7a9b','{"dryness":3,"flake":2,"texture":1}','{"히알루론산"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000147809'),
('esnatureSqualaneSerum','에스네이처','아쿠아 스쿠알란 세럼','{"serum"}',82,'수분 결광','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0017/A00000017031201ko.jpg','#6b8b8b','{"dryness":3,"texture":2,"dull":1}','{"스쿠알란","히알루론산"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000170312'),
('bringgreenZincteca','브링그린','징크테카 트러블 세럼','{"serum"}',84,'트러블 진정','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0022/A00000022651501ko.jpg','#5c8b6f','{"acne":3,"redness":2,"blemish":1}','{"병풀(시카)","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000226515'),
('goodalHeartleafEssence','구달','맑은 어성초 진정 에센스','{"serum"}',83,'어성초 진정','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0016/A00000016511801ko.jpg','#7a9b6f','{"redness":3,"acne":2,"dryness":2}','{"어성초"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000165118'),
('iopeRetinolSerum','아이오페','레티놀 슈퍼 바운스 세럼','{"serum"}',89,'레티놀 탄력','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0023/A00000023642201ko.jpg','#8b5c5c','{"wrinkle":3,"elastic":3,"pore":1}','{"레티놀","콜라겐"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000236422'),
('medicubePdrnPinkAmpoule','메디큐브','PDRN 핑크 앰플','{"serum"}',91,'톤업 미백 앰플','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0022/A00000022649802ko.jpg','#a86f7a','{"tone":2,"elastic":2,"dull":2,"pigment":1}','{"PDRN","나이아신아마이드","콜라겐"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000226498'),
('biohealBohLiftingAmpoule','바이오힐 보','프로바이오덤 3D 리프팅 앰플','{"serum"}',88,'리프팅 앰플','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0019/A00000019833901ko.jpg','#6f5c8b','{"elastic":3,"wrinkle":2,"dryness":1}','{"락토바실러스","펩타이드","세라마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000198339'),
('abibBifidaSerum','아비브','부활초 비피다 세럼 퍼밍 드롭','{"serum"}',83,'모공 탄력','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0019/A00000019138701ko.jpg','#7a6f8b','{"elastic":2,"pore":2,"dryness":2}','{"비피다","히알루론산"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000191387'),
('drgHyalCicaSerum','닥터지','레드 블레미쉬 히알 시카 수딩 세럼','{"serum"}',85,'수분 진정','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0022/A00000022432902ko.jpg','#a85c5c','{"redness":3,"dryness":2,"acne":1}','{"히알루론산","병풀(시카)","마데카소사이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000224329'),
('formentCottonHug','포맨트','시그니처 퍼퓸 코튼허그','{"perfume"}',95,'포근한 코튼향','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0022/A00000022167502ko.jpg','#8ba0b0','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000221675'),
('wdressroomNo49','더블유드레스룸','드레스퍼퓸 No.49 피치블러썸','{"perfume"}',86,'옷에도 향기를','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0001/A00000001609501ko.jpg','#c98ba0','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000016095'),
('grafenTattooPerfume','그라펜','타투 퍼퓸','{"perfume"}',81,'하루종일 잔향','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0019/A00000019121401ko.jpg','#5c5c7a','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000191214'),
('cetaphilMoisturizing','세타필','모이스춰라이징 로션','{"bodylotion"}',90,'온가족 저자극','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0016/A00000016561601ko.jpg','#5c7a8b','{"dryness":3}','{"글리세린"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000165616'),
('niveaSosLotion','니베아','SOS 케어 바디로션','{"bodylotion"}',84,'속건조 케어','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0000/A00000000852501ko.jpg','#5c6f8b','{"dryness":2,"redness":1}','{"판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000008525'),
('onthebodyFootShampoo','온더바디','발을씻자 코튼 풋샴푸','{"foot"}',89,'상쾌한 발세정','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0011/A00000011739902ko.jpg','#6b8b8b','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000117399'),
('fillimilliFootFile','필리밀리','전동 발각질 제거기','{"foot"}',80,'매끈한 발뒤꿈치','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018596901ko.jpg','#8b6f5c','{"flake":2}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000185969'),
('niveaDeoRollOn','니베아','데오드란트 롤온','{"deo"}',88,'겨드랑이 보송','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0000/A00000000701101ko.jpg','#5c6f8b','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000007011'),
('crystalDeoStick','크리스탈','데오드란트 스틱','{"deo"}',76,'무향 미네랄','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0017/A00000017788601ko.jpg','#7a7a8b','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000177886'),
('medicubeUsseraDeepShot','메디큐브','에이지알 유쎄라 딥 샷','{"device"}',92,'홈 리프팅샷','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0019/A00000019076301ko.jpg','#5c6f8b','{"elastic":3,"wrinkle":2}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000190763'),
('medicubeBoosterHealer','메디큐브','에이지알 부스터 힐러','{"device"}',87,'흡수력 부스터','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0019/A00000019075901ko.jpg','#6f5c8b','{"elastic":2,"wrinkle":1}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000190759'),
('joseonRiceSun','조선미녀','맑은쌀 선크림','{"sun"}',95,'맑은쌀 광채','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018861001ko.jpg','#c9a86a','{"tone":2,"dull":2,"dryness":2}','{"쌀 추출물","나이아신아마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000188610'),
('roundlabBirchSun','라운드랩','자작나무 수분 선크림','{"sun"}',94,'수분 선크림','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0014/A00000014913501ko.jpg','#5c8b6f','{"dryness":3,"redness":1,"flake":1}','{"히알루론산","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000149135'),
('drgGreenMildSun','닥터지','그린 마일드 업 선 플러스','{"sun"}',92,'순한 무기자차','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018016201ko.jpg','#6b8b6f','{"redness":3,"dryness":2,"acne":1}','{"병풀(시카)","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000180162'),
('skin1004SunSerum','스킨1004','센텔라 히알루-시카 워터핏 선세럼','{"sun"}',93,'촉촉 선세럼','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0016/A00000016949901ko.jpg','#6b8b6f','{"oil":2,"redness":2,"dryness":2}','{"병풀(시카)","히알루론산"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000169499'),
('cellfusioncToningSun','셀퓨전씨','토닝 썬스크린','{"sun"}',88,'톤업 썬케어','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0012/A00000012185201ko.jpg','#c9a05c','{"tone":3,"dull":2,"oil":1}','{"나이아신아마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000121852'),
('aesturaDermaUvSun','에스트라','더마UV365 장벽수분 선크림','{"sun"}',87,'장벽 진정썬','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018107801ko.jpg','#6b7a8b','{"redness":3,"dryness":3}','{"세라마이드","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000181078'),
('tirtirRedCushion','티르티르','마스크 핏 레드 쿠션','{"cushion"}',95,'초밀착 커버','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0021/A00000021423103ko.jpg','#b5453a','{"cover":3,"tone":2,"blemish":2}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000214231'),
('clioMeshGlowCushion','클리오','킬커버 메쉬 글로우 쿠션','{"cushion"}',91,'물광 커버','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0017/A00000017775901ko.jpg','#b58b5c','{"cover":3,"dull":2,"tone":2}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000177759'),
('hincePinkCushion','힌스','커버 마스터 핑크 쿠션','{"cushion"}',89,'핑크빛 보정','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0022/A00000022991301ko.jpg','#c98ba0','{"cover":3,"tone":2,"blemish":2}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000229913'),
('espoirBeGlowCushion','에스쁘아','프로 테일러 비글로우 쿠션','{"cushion"}',88,'윤광 베이스','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0012/A00000012893101ko.jpg','#9b7a4a','{"cover":2,"tone":2,"dull":2,"dryness":1}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000128931'),
('dasiquePalette','데이지크','섀도우 팔레트','{"eye"}',94,'데일리 음영','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0014/A00000014780101ko.jpg','#a86f8b','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000147801'),
('romandBetterPalette','롬앤','베러 댄 팔레트','{"eye"}',92,'블렌딩 팔레트','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0014/A00000014839001ko.jpg','#a85c6f','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000148390'),
('periperaSkinnyBrow','페리페라','스피디 스키니 브로우','{"brow"}',90,'초슬림 눈썹','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0013/A00000013867101ko.jpg','#6b5744','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000138671'),
('misshaBrowStyler','미샤','퍼펙트 아이브로우 스타일러','{"brow"}',89,'국민 브로우','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0021/A00000021956307ko.jpg','#5c4a38','{}','{}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000219563'),
('roundlabDokdoToner','라운드랩','1025 독도 토너','{"toner"}',95,'국민 수분토너','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0012/A00000012550701ko.jpg','#5c7a8b','{"dryness":3,"flake":2,"texture":1,"redness":1}','{"판테놀","알란토인"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000125507'),
('torridenDiveInToner','토리든','다이브인 저분자 히알루론산 토너','{"toner"}',94,'속수분 채움','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0017/A00000017026601ko.jpg','#5c7a8b','{"dryness":3,"dull":1,"flake":1}','{"히알루론산","판테놀","알란토인"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000170266'),
('medicubeZeroPorePad','메디큐브','제로 모공 패드 2.0','{"toner"}',93,'모공각질 케어','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0016/A00000016168101ko.jpg','#a86f7a','{"pore":3,"blackhead":3,"texture":2,"oil":2}','{"살리실산(BHA)","PHA"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000161681'),
('anuaHeartleafClearPad','아누아','어성초 77 클리어 패드','{"toner"}',92,'진정 닦토패드','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0020/A00000020788801ko.jpg','#7a8b5c','{"redness":3,"pore":2,"acne":2,"texture":1}','{"어성초","PHA","마데카소사이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000207888'),
('numbuzin1ClearToner','넘버즈인','1번 진정 맑게담은 청초토너','{"toner"}',87,'예민 진정수','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0017/A00000017775701ko.jpg','#8b8b6f','{"redness":3,"acne":2,"dryness":2}','{"어성초","병풀(시카)"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000177757'),
('abibHeartleafToner','아비브','어성초 카밍 토너 스킨부스터','{"toner"}',91,'쿨링 진정토너','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0014/A00000014658901ko.jpg','#7a6f8b','{"redness":3,"acne":2,"dryness":2}','{"어성초","히알루론산","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000146589'),
('wellageHyaluronicToner','웰라쥬','리얼 히알루로닉 100 토너','{"toner"}',84,'속건조 토너','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018887402ko.jpg','#5c7a9b','{"dryness":3,"flake":1,"dull":1}','{"히알루론산","베타글루칸","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000188874'),
('manyoBifidaToner','마녀공장','비피다 바이옴 앰플 토너','{"toner"}',88,'장벽 탄력케어','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0013/A00000013607701ko.jpg','#8b7a5c','{"elastic":2,"dryness":2,"dull":2,"wrinkle":1}','{"비피다","락토바실러스","히알루론산"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000136077'),
('skinfoodCarrotPad','스킨푸드','캐롯 카로틴 카밍 워터 패드','{"toner"}',89,'당근 진정패드','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0014/A00000014328501ko.jpg','#c9764a','{"redness":3,"acne":2,"dryness":1}','{"베타카로틴","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000143285'),
('bringgreenTeaTreeToner','브링그린','티트리 시카 수딩 토너','{"toner"}',86,'지성 진정토너','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018918101ko.jpg','#5c8b6f','{"acne":3,"oil":2,"redness":2,"flake":1}','{"티트리","병풀(시카)","판테놀"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000189181'),
('onethingHeartleafToner','원씽','어성초 추출물 토너','{"toner"}',80,'어성초 원액','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0015/A00000015450601ko.jpg','#7a8b5c','{"redness":2,"acne":2,"oil":1}','{"어성초"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000154506'),
('onethingNiacinamideToner','원씽','나이아신아마이드 10% 토너','{"toner"}',77,'톤결 광채','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0015/A00000015832201ko.jpg','#c9a05c','{"tone":3,"spot":2,"dull":2,"blemish":1}','{"나이아신아마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000158322'),
('goodalVitaCPad','구달','청귤 비타C 잡티케어 패드','{"toner"}',85,'잡티케어 패드','https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/10/0000/0018/A00000018917501ko.jpg','#c9915c','{"spot":3,"tone":2,"dull":2,"blemish":2}','{"비타민C","나이아신아마이드"}','https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000189175')
on conflict (id) do update set
  brand=excluded.brand, name=excluded.name, cats=excluded.cats, pop=excluded.pop,
  tag=excluded.tag, img_url=excluded.img_url, color=excluded.color, aff=excluded.aff,
  ing=excluded.ing, oy_url=excluded.oy_url;

-- ---------------------------------------------------------------
-- 커뮤니티 실시간 반영 (Supabase Realtime)
-- posts/comments 변경 이벤트를 웹소켓으로 구독할 수 있게 publication에 추가.
-- (앱은 이 설정이 없으면 12초 폴링으로 자동 폴백하므로 선택 사항)
-- 이미 추가된 상태에서 재실행해도 오류가 나지 않게 예외를 무시한다.
do $$ begin
  alter publication supabase_realtime add table posts;
exception when duplicate_object then null; end $$;
do $$ begin
  alter publication supabase_realtime add table comments;
exception when duplicate_object then null; end $$;
