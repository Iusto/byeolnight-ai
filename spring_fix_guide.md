# 스프링 서버 수정 가이드

## 🚨 발생한 문제
- `Column 'created_at' cannot be null` 에러
- JWT 인증 필터에서 Authorization 헤더 누락 경고

## 🛠️ 해결 방법

### 1. Post 엔티티 수정 (필수)

Post 엔티티에 다음 어노테이션을 추가하세요:

```java
@Entity
@Table(name = "posts")
public class Post {
    
    @CreationTimestamp  // 추가 필요
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp    // 추가 필요
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;
    
    // 또는 @PrePersist, @PreUpdate 사용
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
```

### 2. Security 설정 수정 (권장)

SecurityConfig에서 public 엔드포인트 허용:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()  // public API 허용
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            );
        return http.build();
    }
}
```

### 3. PostService.createNewsPost 메서드 확인

```java
@Service
public class PostService {
    
    public void createNewsPost(String title, String content, Post.Category category, User user) {
        Post post = Post.builder()
            .title(title)
            .content(content)
            .category(category)
            .writer(user)
            .viewCount(0)
            .likeCount(0)
            .isDeleted(false)
            .blinded(false)
            // createdAt, updatedAt은 @CreationTimestamp/@UpdateTimestamp로 자동 설정
            .build();
            
        postRepository.save(post);
    }
}
```

## ✅ 수정 후 테스트

1. 스프링 서버 재시작
2. FastAPI에서 테스트 실행:
   ```bash
   python test_connection.py
   ```

## 📝 참고사항

- **Public 엔드포인트 사용 권장**: JWT 인증 없이 간단하게 연동 가능
- **Admin 엔드포인트**: API 키 인증이 필요하지만 더 안전함
- **created_at 필드**: 반드시 자동 설정되도록 어노테이션 추가 필요