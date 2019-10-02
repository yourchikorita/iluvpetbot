# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 21:55:55 2019

@author: EJ
"""

import requests



def festival_list_date(userDate):

    #서비스키
    serviceKey='SZuXUHfZNLEJqiAh4mF9Cjh8iBjzM1s1kBakiqF9P9PXglB6upcm17zFu00%2FjMNA6nodWV76bS4J6fZl0tVZYg%3D%3D'
    #20행 보기
    numOfRows=9
    #목록으로 보기
    listYN='Y'
    #조회순 보기(B)=조회순,A=제목순)
    arrange='O'  #대표이미지가 반드시 있는 정렬
    eventStartDate=userDate[:8]
    eventEndDate=userDate[8:16]
    url='http://api.visitkorea.or.kr/openapi/service/rest/KorService/searchFestival?serviceKey={}&numOfRows={}&MobileOS=ETC&MobileApp=AppTest&arrange={}&listYN={}&eventStartDate={}&eventEndDate={}&_type=json'.format(
        serviceKey,numOfRows,arrange,listYN,eventStartDate,eventEndDate)
    resp = requests.get(url)
    data = resp.json()
    #festival list 원본 데이타
    fv_origin_data = data['response']['body']['items']['item']
    
    festivalList = []
   
    for fv_origin_data_row in fv_origin_data:
        festivalList.append({
                'cat3':fv_origin_data_row['cat3'], 
                'firstimage':fv_origin_data_row['firstimage'],
                'title':fv_origin_data_row['title'],
                'eventstartdate':fv_origin_data_row['eventstartdate'],'eventenddate':fv_origin_data_row['eventenddate'], 
                'addr1':fv_origin_data_row['addr1']
                })
    
    
    i = 1
    #festivalListShow 사용자에게 보여지는 축제리스트,문자열이다. 
    festivalListShow=''
    
    for item in festivalList:
        festivalListShow = festivalListShow + f'{i}'+'번 '+ item['title'] +'.'+ '\n'
        i += 1
    print('==========festivalListShow함수불로옴  ')
    return festivalListShow, festivalList
    



      #파라미터가 문화관광축제면, festival list 에서 문화관광축제를 찾아서 내보냄
         

festival_list_date('2019101020191111')
#if __name__ == "__main__":
 #   print('here')
   