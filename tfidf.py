# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 22:03:55 2019

@author: EJ
"""

import math, sys
from konlpy.tag import Okt

class Filter:

    def __init__(self):
        self.words = set()  #잘라낸 온갖 단어들 들어있는 가방
        self.word_dict = {} #추출해낸 단어들 갯수 사전
        self.category_dict = {}

    def split(self, text): 
        '''
        text:문장
        문장에서 형태소별로 잘라서 명사,형용사,동사만 추출해서 리스트로 만들어냄
        <결과예시>
        "파격 세일 - 오늘까지만 30% 할인" ->  ['파격', '세', '일', '오늘', '30%', '할인']
        '''
        results = []
        twitter = Okt() #Okt 형태소분석기
        malist = twitter.pos(text, norm=True, stem=True)  # pos =품사태깅 stem=True 면 형용사/동사의 기본원형으로 바꿔줌(찾아온->찾아오다)
        #결과는 list형태를 가지고있고 각 요소는 ()튜플 형태이다. (형태소,품사)
        #malist= [('파격', 'Noun'), ('세', 'Modifier'), ('일', 'Noun'), ('-', 'Punctuation'), ('오늘', 'Noun'), ('까지만', 'Josa'), ('30%', 'Number'), ('할인', 'Noun')]
        # 실습 2
        # 아래 for 문을 한줄짜리 for 문으로 바꿔보세요 List Comprehension
        for word in malist:
            #word= ('파격', 'Noun')
            #word[1]='Noun,Adjective,josa'
            if not word[1] in ["Josa", "Emoi","Punctuation"]: #태깅된게 조사,어미,펑튜에이션이 아니면(즉,명사,형용사,동사 면) results리스트에다가 해당 형태소를 담는다.
                results.append(word[0])

        #results = [ word[0] if not word[1] in ['Josa','Eomi','Punctuation'] for word in malist ]
     
        return results



##inc_word,inc_category숫자를 올림

    def inc_word(self, word, category): 
        '''
        word를 세는것
        word:파격,세,일,오늘,~~ 
        category:광고
        가방을 새로 생성
        '''
        if not category in self.word_dict:
            #self.word_dict= {'광고': {'파격': 1, '세': 3, '일': 3, '오늘': 1, '30%': 1, '할인': 1, '쿠폰': 1, '선물': 1, '무료': 1, '배송': 1,,,,,,}}
            self.word_dict[category] = {} #카테고리를 키로 받아옴.
            
        if not word in self.word_dict[category]: 
            self.word_dict[category][word] = 0        #만약 word_dict[category] 에 없는 단어라면 0
        self.word_dict[category][word] += 1 #이미 존재하는 형태소라면 숫자 1씩 높임 파격:1
        self.words.add(word)
        

    def inc_category(self, category): 
        '''
        카테고리를 세는것
        카테고리를 받아서 없는거면 카테고리 만들고 있는거면 숫자를 높인다.
        '''
        if not category in self.category_dict:
            #print('self.category_dict====^^^',self.category_dict)
            #{'광고': 6, '중요': 5}
            self.category_dict[category] = 0
        self.category_dict[category] += 1
        #print('self.category_dict[category]|=',self.category_dict[category])
        
    def fit(self, text, category):
        '''
        text:파격 세일 - 오늘까지만 30% 할인
        category:광고
        클래스안에서 정의했던 split(),inc_word(),inc_category()함수 실행
        '''
        word_list = self.split(text) #split()실행
        #word_list=['파격', '세', '일', '오늘', '30%', '할인']
      
        for word in word_list:
            self.inc_word(word,category)
        self.inc_category(category)

    def score(self, words, category):
        score = math.log(self.category_prob(category))
        #print('words=##',words,'category=',category,'score####=',score)
        #score####= -0.916290731874155
        for word in words:
            score += math.log(self.word_prob(word, category))
            
        return score

    def predict(self, text):#텍스트받아와서 카테고리 예측
        best_category = None  #None으로 비워둔다.
        max_score = -sys.maxsize#컴퓨터에서 가져올수잇는 마이너스 무한대
        words = self.split(text)#리스트 형식으로 다시 넣어줌
        score_list = []
        #준비끝
        for category in self.category_dict.keys():  #광고'
            score = self.score(words, category)
            score_list.append((category,score))
            if score > max_score:
                max_score = score
                best_category = category
        return best_category, score_list

    def get_word_count(self, word, category):
        if word in self.word_dict[category]:
            return self.word_dict[category][word]
        else:
            return 0

    def category_prob(self, category):
        '''
         전체중에 몇번등장했는지.
        '''
        sum_categories = sum(self.category_dict.values())#category_dict : 광고가 몇번 등장했는지 / 의 횟수 >> 광고+중요+소셜 = 6+5+4 = 15
   
        #self.category_dic 는 {'광고': 6, '중요': 5}이걸 다 더한값
        category_v = self.category_dict[category] # 광고 : 6
       
        return category_v / sum_categories  #6/15 전체에서 광고 가 나올 확률

    def word_prob(self, word, category):#해당카테고리에서(광고) word가 (파격)몇번나왔는지.
        n = self.get_word_count(word, category) + 1 #로그에서 0이 정의되지않아가지구 1, 1은 오류를 없애기위한것임. 공평하게 다 1을 더해주겠다능..여기서 더하기 1이 계쏙되니까 
        d = sum(self.word_dict[category].values()) + len(self.words)#전체에다가 지금들어온 거의 길이..여기서도 분자랑 똑같이 len으로  더해줌
        return n/d
    
    
    
    bf = Filter()
    
    bf.fit("파격 세일 - 오늘까지만 30% 할인","광고")
    bf.fit("쿠폰 선물 & 무료 배송", "광고")
    bf.fit("현대 백화점 세일", "광고")
    bf.fit("봄과 함께 찾아온 따뜻한 신제품 소식", "광고")
    bf.fit("회원님에게만 추천 드리는 상품", "광고")
    bf.fit("인기 제품 기간 한정 세일", "광고")
    bf.fit("오늘 일정 확인", "중요")
    bf.fit("프로젝트 진행 상황 보고", "중요")
    bf.fit("계약 잘 부탁드립니다", "중요")
    bf.fit("회의 일정이 등록되었습니다", "중요")
    bf.fit("오늘 일정이 없습니다", "중요")
    bf.fit("1촌 신청을 기다립니다", "소셜")
    bf.fit("반가워", "인사")
    bf.fit("ㅎㅇ", "인사")
    bf.fit("안녕하세요", "인사")
    bf.fit("목줄 안한 강아지 신고 과태료 납부", "과태료")
    bf.fit("동물 등록 미이행시 벌금 부과 ", "과태료")
    bf.fit("배설물 수거 미이행", "과태료")
    bf.fit("목줄 미착용", "과태료")
    bf.fit("맹견은 목줄 착용 의무화", "과태료")
    bf.fit("산책시 목줄 의무화, 미착용시 과태료 부과", "과태료")    