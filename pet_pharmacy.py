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
    endpoint ='http://openapi.seoul.go.kr:8088/{}/json/animalPharmacyInfo/1/400'.format(serviceKey)
    resp=requests.get(endpoint)
    #print(resp.status_code)
    data = resp.json()
    pharm_data=data['animalPharmacyInfo']['row']
    #print(pharm_data)
    
    #str 로 출력해줄 리스트 만든다.
    i=1
    pharm_show_list_str=''
    for item in pharm_data:
       pharm_show_list_str = pharm_show_list_str + item['NM']+' / 주소:'+item['ADDR']+'\n'
    
    
    #str을 list로 변경해준다.
    from_str_to_list = pharm_show_list_str.split('\n')  
    userLocList=''
    #user 지역검색결과
    for item in from_str_to_list:
        if userLoc in item:
            userLocList=userLocList+'{}'.format(i)+'번 '+item+'\n'
            i=i+1
   
   
    print('함수가 호출됨!')
    return pharm_show_list_str,userLocList
    



#pet_pharm_api('서초구')
#if __name__ == "__main__":
 #   print('here')
   