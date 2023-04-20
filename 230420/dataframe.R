# csv 파일을 로드 
df = read.csv("./csv/example.csv")
df

# 상위 6개 출력
head(df)
head(df, 3)

# 하위 6개 출력
tail(df)
tail(df, 3)

# 뷰어창에 데이터프레임 확인
View(df)
view(df)

# 데이터프레임 크기를 출력하는 함수
dim(df)

# 데이터프레임에 기초 통계정보 출력
summary(df)

# 데이터 프레임의 정보를 출력
str(df)

library(dplyr)

# 컬럼의 이름 변경 
rename(df, '이름' = Name)

df = read.csv("./csv/csv_exam.csv")
df

# 새로운 파생변수 하나 생성
# 전체 점수의 합계 (total_score)
# 전체 점수의 평균 (mean_score)

total_score = df$math + df[['english']] + df[[5]]
total_score

cbind(df, total_score)
data.frame(df, total_score)
df$total_score = total_score
df

df$mean_score = df$total_score/3
df

# 평균 점수가 60점 이상이면 pass, 아니면 fail
# res 컬럼을 생성
# ifelse(조건식, 참인 경우의 값, 거짓인 경우의 값)
df$res = ifelse(df$mean_score >= 60, 'pass', 'fail')
df

# 1학년 중에 평균 점수가 가장 높은 사람의 정보를 출력
df2 = df[df$class == 1,]
df3 = df2[order(df2$mean_score, decreasing = TRUE),]
df3[1,]
head(df3, 1)

# dplyr 패키지를 사용

df = read.csv("./csv/csv_exam.csv")
df

# filter
df %>% filter(class == 1)

# 오름차순 정렬
df %>% arrange(math)

# 내림차순 정렬
df %>% arrange(-math)
df %>% arrange(desc(math))

# 정렬의 기준이 여러개인 경우
df %>% arrange(math, english)

# class를 기준으로 내림차순, math를 기준으로는 오름차순
df %>% arrange(-class, math)
df %>% arrange(desc(class), math)

# 특정 컬럼만 출력
df %>% select(math)

df %>% arrange(desc(class)) %>% select(math, english)

# 특정 컬럼만 삭제
df %>% select(-id)

# 파생변수 생성
df %>% mutate(total_score = math + english + science, 
              mean_score = total_score / 3) -> df

df %>% 
  filter(class == 1) %>% 
  arrange(desc(mean_score)) %>% 
  head(1)

# group화 summarise
df %>% 
  group_by(class) %>% 
  summarise(mean_math = mean(math), 
            mean_english = mean(english)) %>% 
  arrange(-mean_math) %>% 
  head(1)

# join 
df1 = data.frame(id = 1:5, 
                 score = c(80, 70, 40, 60, 50))
df2 = data.frame(id = 1:5, 
                 weight = c(80, 65, 70, 55, 90))
df3 = data.frame(id = 1:3, 
                 class = c(1,1,2))
inner_join(df1, df2, by='id')
inner_join(df1, df3, by='id')

left_join(df1, df3, by='id')

right_join(df1, df3, by='id')

# 유니언 결합 (python에서는 concat)
rbind(df1, df2)
bind_rows(df1, df2)

