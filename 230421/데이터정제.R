library(dplyr)
library(ggplot2)

# 극단치 
View(mpg)

# 극단치를 확인(시각화)
boxplot(mpg$cty)
# 극단치를 수치로 표현
boxplot(mpg$cty)$stats


mpg = ggplot2::mpg

# 이상치는 26초과이거나 9미만인 경우
# 이상치를 결측치로 변환
# 결측치의 개수를 확인
ifelse(mpg$cty > 26 | mpg$cty < 9, NA, mpg$cty) -> mpg$cty
table(is.na(mpg$cty))

# dplyr 패키지를 이용하여 
# 결측치를 제거하고 
# 제조사별(manufacturer)로 그룹화 
# 도심연비(cty)의 평균
# 도심연비가 좋은 상위 5개의 제조사를 확인

mpg %>% 
  filter(!is.na(cty)) %>% 
  group_by(manufacturer) %>% 
  summarise(cty_mean = mean(cty)) %>% 
  arrange(desc(cty_mean)) %>% 
  head(5)

mpg = ggplot2::mpg

# total 파생변수 생성
# total은 (cty + hwy) / 2

# test 파생 변수 생성
# total이 30이상이면 'A'
# 20이상이고 30 미만이면 'B'
# 20 미만이면 'C'

