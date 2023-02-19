# Michael-bnb BE API
- DRF로 API를 구현
- Render에서 배포
- https://hoody-coder.store 의 Header에서 Swagger확인 가능
<br>

## Version Guide
***
버전별 특징 (V)

### V0
    - 모델 디자인 
    - 베이스 상태의 API만 구현한 상태 
    - 폴더 트리의 분리가 세분화되어있지않으며, Model, Serializer, View 단별 로직이 분리되어있지 않음
    - Social Login
***

### V1 (In Progress)
    - 로직 관리 폴더의 세분화
        - API Request, Response 관련 로직은 View
        - 비지니스 로직은 Service
        - Query관련 로직은 Selector
    - 모든 Serialzer는 CustomSerializer로 핸들링
    - 테스트 코드 작성
    - Swagger를 통한 API 문서화
***

### V2
    - User 모델 새로작성(기존 AbstractUser 는 Admin으로만 활용)
    - 기존 Serializer -> Pydentic 을 통한 핸들링으로 변경
    - JWT 로직 커스텀 및 로그인 방식 변경
    - V0, V1에서 필요하다고 생각되는 기능들 추가(Admin에서 추가하는 것들도 프론트에서 추가)


<br>

### V0 Actions
***
- Utility
  - [x] Render Deploy

- [x] Booking
- [x] Room
- [x] User
- [x] Review
- [x] Category
- [x] Media
- [x] Uploads
- [x] WishList

### V1 Actions (InProgress)
***
- Utility
  - [x] Custom Exception Handler
  - [x] Custom Serializer
  - [x] Apply Swagger
  - [x] Apply Https Domain 
  - [x] Guest, Host Mode Toggle(After Login)

- API
  - [x] Booking
  - [] Room
  - [] User
  - [] Review
  - [] Category
  - [] Media
  - [] Uploads
  - [] WishList



<br>

## How to Start:
1. poetry install
2. python manage.py migrate
3. python mange.py runserver





# Reference
- Style Guide: https://github.com/HackSoftware/Django-Styleguide-Example
- FE Repo: https://github.com/MichaelYcCho/michael-bnb-frontend