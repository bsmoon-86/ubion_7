## sav파일 로드 
install.packages('foreign')
install.packages('readxl')

library(foreign)
library(readxl)

welfare = read.spss(file ="./csv/Koweps_hpc10_2015_beta1.sav", 
                    to.data.frame = T)

View(welfare)

welfare = rename(welfare, 
                 gender = h10_g3, 
                 birth = h10_g4, 
                 marriage = h10_g10, 
                 religion = h10_g11, 
                 income = p1002_8aq1, 
                 code_job = h10_eco9, 
                 code_region = h10_reg7)

welfare %>% 
  select(gender, birth, marriage, religion, 
         income, code_job, code_region) -> welfare_copy

View(welfare_copy)

# 성별 컬럼데이터를 확인 
table(welfare_copy$gender)

ifelse(welfare_copy$gender == 1, 'male', 'female') -> welfare_copy$gender

table(welfare_copy$gender)

# 성별을 기준으로 월급이 평균이 어떻게 되는가?
# income이 0이면 수익이 존재하지 않는다. -> 결측치로 변경
# income이 9999면 극단치로 생각해서 결측치로 변경
ifelse(welfare_copy$income == 0 | welfare_copy$income == 9999, 
       NA, 
       welfare_copy$income) -> welfare_copy$income

# 결측치를 확인 
table(is.na(welfare_copy$income))

# income의 결측치를 제외하고
# 성별로 그룹화
# income 평균을 출력

welfare_copy %>% 
  filter(!is.na(income)) %>% 
  group_by(gender) %>% 
  summarise(income_mean = mean(income)) -> gender_income

## 데이터의 시각화
ggplot(data = gender_income, 
       aes(x = gender, y = income_mean)) + geom_col()


## 나이별 월급의 차이가 존재하는가?

# 결측치 제거 
# 파생변수 나이를 생성
# 나이로 그룹화
# income 평균
welfare_copy %>% 
  filter(!is.na(income)) %>% 
  mutate(age = 2023 - birth) %>% 
  group_by(age) %>% 
  summarise(income_mean = mean(income)) -> age_income



# 시각화
ggplot(data=age_income, 
       aes(x = age, y = income_mean)) + geom_line()

age_income %>% arrange(desc(income_mean)) %>% head(5)


# 연령대를 추가
# ageg 나이가 30미만이면 'young'
# 30이상 60미만이면 'middle'
# 60이상이면 'old'
# 연령대별 월급의 평균이 어떻게 되는가?
# 시각화 (막대그래프)

welfare_copy %>% 
  mutate(age = 2023 - birth) %>% 
  mutate(ageg = ifelse(age < 30, 'young', 
                       ifelse(age < 60, 'middle', 'old'))) %>% 
  group_by(ageg) %>% 
  summarise(income_mean = mean(income, na.rm=T)) -> ageg_income

ggplot(data = ageg_income, 
       aes(x = ageg, y = income_mean)) + geom_col() +
  scale_x_discrete(limits = c('young', 'middle', 'old'))

welfare_copy %>% 
  mutate(age = 2023 - birth) %>% 
  mutate(ageg = ifelse(age < 30, 'young', 
                       ifelse(age < 60, 'middle', 'old'))) -> welfare_copy

# 연령대, 성별 월급 평균
welfare_copy %>% 
  filter(!is.na(income)) %>% 
  group_by(ageg, gender) %>% 
  summarise(income_mean = mean(income)) -> ageg_gender_income

ggplot(data= ageg_gender_income, 
       aes(x = ageg, y = income_mean, fill=gender)) +
  geom_col(position = 'dodge') + 
  scale_x_discrete(limits=c('young', 'middle', 'old'))


# 나이, 성별 월급 평균을 비교 

welfare_copy %>% 
  filter(!is.na(income)) %>% 
  group_by(age, gender) %>% 
  summarise(income_mean = mean(income)) -> age_gender_income

ggplot(data =age_gender_income, 
       aes(x = age, y = income_mean, color=gender)) + geom_line()


## 직업별로 평균 월급이 어떻게 되는가?
welfare_copy$code_job

list_job = read_excel("./csv/Koweps_Codebook.xlsx", sheet=2, col_names = T)
# 2개의 데이터프레임을 조인 결합
left_join(welfare_copy, list_job, by='code_job') -> welfare_copy
View(welfare_copy)

## 직업별 평균 월급 
## 직업이 결측치이고 월급이 결측치인 경우는 제외
## 직업 기준으로 그룹화
## 월급의 평균 값
welfare_copy %>% 
  filter(!is.na(job) & !is.na(income)) %>% 
  group_by(job) %>% 
  summarise(income_mean = mean(income)) %>% 
  arrange(-income_mean) -> job_income

  
# 평균 월급이 높은 상위 직업군 10개를 시각화
# 낮은 하위 직업군 10개를 시각화
ggplot(data = head(job_income, 10), 
       aes(x = reorder(job, income_mean), y=income_mean)) + 
  geom_col() +
  coord_flip()

ggplot(data = tail(job_income, 10), 
       aes(x = reorder(job, income_mean), y=income_mean)) + 
  geom_col() +
  coord_flip()

# 성별 직업의 빈도수를 체크하여 상위 10개 출력

welfare_copy %>% 
  filter(!is.na(job) & gender == 'male') %>% 
  group_by(job) %>% 
  summarise(count = n()) %>% 
  arrange(desc(count)) %>% 
  head(10) -> male_top10
male_top10

welfare_copy %>% 
  filter(!is.na(job) & gender == 'female') %>% 
  group_by(job) %>% 
  summarise(count = n()) %>% 
  arrange(desc(count)) %>% 
  head(10) -> female_top10
female_top10


### marriage : 3인 경우 이혼 
# 새로운 파생변수 (group_marriage) 생성하여 
# marriage가 3이면 divorce
# 1이면 marriage

#연령대 별 이혼율 출력 시각화

ifelse(welfare_copy$marriage == 1, 'marriage', 
       ifelse(welfare_copy$marriage == 3, 'divorce', NA)) -> welfare_copy$group_marriage

welfare_copy %>% 
  filter(!is.na(group_marriage)) %>% 
  group_by(ageg, group_marriage) %>% 
  summarise(cnt = n()) %>% 
  mutate(total_count = sum(cnt)) %>% 
  mutate(pct = cnt/total_count*100)



