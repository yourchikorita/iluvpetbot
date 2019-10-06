# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 21:55:55 2019

@author: EJ
"""
import requests



def pet_pharm_api(userLoc):
    '''
    동물약국 api 불러오기.
    userLoc : userLocation (도봉구)
    '''
    serviceKey='587a69416c736565313032584762564d'
    endpoint ='http://openapi.seoul.go.kr:8088/{}/json/animalPharmacyInfo/1/25'.format(serviceKey)
    resp=requests.get(endpoint)
    #print(resp.status_code)
    data = resp.json()
    pharm_data=data['animalPharmacyInfo']['row']
    #print(pharm_data)
    
    #str 로 출력해줄 리스트 만든다.
    i=1
    pharm_show_list_str='' #전체 데이타 리스트. 지역과는 상관없음.
    for item in pharm_data:
       pharm_show_list_str = pharm_show_list_str + item['NM']+' / 주소:'+item['ADDR']+' / 전화번호:'+item['TEL']+' / 인허가일자:'+item['PERMISSION_DT']+' / 인허가번호:'+item['PERMISSION_NO']+'\n'
    

    pharm_show_title_str='' #전체 데이타 리스트. 지역과는 상관없음.
    for item in pharm_data:
       pharm_show_title_str = pharm_show_title_str + item['NM']+' / 주소:'+item['ADDR']+'\n'
            
       
    #str을 list로 변경해준다.
    from_str_to_list = pharm_show_list_str.split('\n')  
    from_str_to_list_title=pharm_show_title_str.split('\n')
    userLocList=''
    userTitle=''
    #user 지역검색결과
    for item in from_str_to_list:
        if userLoc in item:
            userLocList=userLocList+'{}'.format(i)+'번 '+item+'\n'
            i=i+1
   
    
    i=1
    for item in from_str_to_list_title:
        if userLoc in item:
            userTitle=userTitle+'{}'.format(i)+'번 '+item+'\n'
            i=i+1
   
    print('함수가 호출됨!')
    #print(userTitle,'===========userTitle')
    #print(userLocList,'==userLocList~~~~~~~~~~~~`')
    return userTitle,userLocList
    
#pet_pharm_api('노원구')
#if __name__ == "__main__":
 #   print('here')
   