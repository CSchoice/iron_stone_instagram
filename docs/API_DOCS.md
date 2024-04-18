# API 명세서


1. [API 문서](#API_문서)
2. [DB 모델](#DB_모델)

## API_문서 

### 유저 API

|         URL       |Method|설명 |
| ----------------- |------| ---------------------- |
| /accounts/login/   |POST| 유저 로그인  |
| /accounts/logout/   |POST| 유저 로그아웃  |
| /accounts/{user_pk}/control   |GET| 회원정보 수정 페이지  |
| /accounts/{user_pk}/control   |POST| 회원정보 수정  |
| /accounts/{tar_user_pk}/follow/   |POST| 유저 팔로우  |
| /accounts/check_login/   |POST| 유저 로그인여부 확인  |




### 게시글 API

|         URL       |Method|설명 |
| ----------------- |------| ---------------------- |
| /contents/   |GET| 메인 페이지  |
| /contents/{tar_user_pk}/profile/   |GET| 회원 프로필 페이지  |
| /accounts/{tar_user_pk}/followings/   |GET| 대상이 팔로잉 중인 유저 조회  |
| /accounts/{tar_user_pk}/followers/   |GET| 대상을 팔로우 중인 유저 조회  |
| /contents/create/   |POST| 게시글 작성  |
| /contents/{article_pk}/   |GET| 게시글 상세 정보  |
| /contents/{article_pk}/edit/   |PUT| 게시글 수정  |
| /contents/{article_pk}/edit/   |delete| 게시글 삭제  |
| /contents/{article_pk}/comment/   |POST| 댓글 작성  |
| /contents/{article_pk}/comment/{comment_pk}/   |PUT| 댓글 수정  |
| /contents/{article_pk}/comment/{comment_pk}/   |delete| 댓글 삭제  |
| /contents/{article_pk}/like/   |POST| 게시글 좋아요  |








## DB_모델

### 유저

| Name  | Type | Des |DB관계 |
| ------|------ |------|------|
| username     | Text   | 사용자의 로그인 이름        |    |
| password     | Text   | 사용자의 비밀번호       |    |
| email        | Text   | 사용자의 이메일 주소    |    |
| name         | Text(20)   | 사용자의 이름             |    |
| nickname     | Text(20)   | 사용자의 닉네임           |    |
| introduce    | Text   | 사용자 소개           |    |
| profile_img  | Image  | 사용자 프로필 이미지           |    |
| created_at  | Date  | 사용자 가입 날짜           |    |
| updated_at  | Date  | 사용자 정보 수정 날짜           |    |
| followings  | Foreign_key  | 사용자가 팔로우 하는 유저           |유저:유저=N:M    |



### 게시글

| Name  | Type | Des |DB관계 |
| ------|------ |------|------|
| content     | Text   | 게시글 내용     |    |
| image     | Image   | 게시글 사진       |    |
| created_at     | Date   | 게시글 작성 시간  |    |
| updated_at  | Date  | 게시글 수정 시간           |    |
| like_user     | Foreign_key   | 게시글 좋아요  |유저:게시글=N:M|
| author     | Foreign_key   | 게시글 작성자  |유저:게시글=1:N|



### 댓글

| Name  | Type | Des |DB관계 |
| ------|------ |------|------|
| content     | Text   | 댓글 내용     |    |
| created_at     | Date   | 댓글 작성 시간  |    |
| updated_at  | Date  | 댓글 수정 날짜           |    |
| author     | Foreign_key   | 댓글 작성자  |유저:댓글=1:N|
| article     | Foreign_key   | 댓글이 달릴 게시글  |게시글:댓글=1:N|
