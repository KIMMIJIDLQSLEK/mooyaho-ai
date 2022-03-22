from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from userpost.models import MooyahoUser,Mountain,Post
from .models import UserViewLog
from collections import Counter
# Create your views here.
import pandas as pd


# 1. UserViewLog DB에서 user_id가 본 mountain_id 모두 가져온다
# 2-1.(mountain_id, 개수)로 저장된 mountain_id_list 횟수로 가져온다.
# 2-2. 개수기준으로 내림차순으로 정렬
def bring_mountain_id(user_id):
    mountain_id_list = {} #딕셔너리 형태로 저장

    # 1, 2-1
    for i in range(1, 101):
        # mountain db에서, post db에서 user가 본 mountain_id의 개수 가져오기
        # mountain_id: 산 상세페이지에 들어간 산의 id, post_id: 게시물에 써진 산의 id
        mountain_count = (UserViewLog.objects.filter(user_id=user_id, mountain_id=i) | UserViewLog.objects.filter(
            user_id=user_id, post_id=i)).count()
        if mountain_count != 0:
            mountain_id_list[i] = mountain_count
    # print(mountain_id_list)

    #2-2
    mountain_id_list = sorted(mountain_id_list.items(), key=lambda x: x[1], reverse=True)
    # print(mountain_id_list)

    return mountain_id_list

#2-3. mountain_id_list중 5개만 돌리기 위해 리스트안의 개수 구하기->만약 5개가 안되면 있는 값만 가져온다

def bring_mountian_count(mountain_id_list):
    count = 5
    if len(mountain_id_list) < 5:
        count = len(mountain_id_list)
    return count

#3-1. 벡터화를 이용해 유사한 구하고 csv로 저장
#3-2. csv 데이터 프레임으로 만들기
df = pd.read_csv('mountain_recommend1.csv')
# print(df)

#3-3. 산의 리스트 돌리면서 각 산과 유사한 산 리스트에 저장하기
def bring_mountain_similarity(mountain_id_list,mountain_id_count):
    #3-3
    find_count1=pd.DataFrame()
    # print(mountain_id_list)
    for count in range(mountain_id_count):

        mountain_id=mountain_id_list[count][0]
        # print(mountain_id)
        find_mountain=df.loc[df['mountian_id']==mountain_id]  #https://liveyourit.tistory.com/246
        # print(find_mountain)


        find_count2=find_mountain['mountian_similarity'].value_counts()  #https://bigdaheta.tistory.com/46
        # print(find_count2)
        find_count1=pd.concat([find_count1,find_count2]) #합치기  #https://yganalyst.github.io/data_handling/Pd_12/
        # print(find_count1)

    find_count=find_count1.index.value_counts().sort_values(ascending=False) #인덱스의 중복값은 갯수 합치고 갯수기준 내림차순으로 정렬
    #https://koreadatascientist.tistory.com/15
    # print(find_count)
    list = find_count[:10].index.tolist()
    # print(list)

    return list

#4. 추천산 10개 리스트를 가져와 keyword하나 가져오는 함수
def bring_keyword_similarity(mountain_similarity):
    token_df = []
    for index in mountain_similarity:
        # print(index)
        tokens=df[(df['mountian_id']==index)&(df['mountian_similarity']==index)]['mountain_tokens']

        # print(tokens)

        token_df.extend(tokens)

    token_list=[]
    # print(token_df)

    for i in token_df:
        # print(type(i))
        token_list.extend(i[1:-1].replace("\'","").split(','))

    # print(token_list)
    keyword=Counter(token_list).most_common(1)[0][0] #갯수 세고 내림차순 정렬을 Counter가 알아서 해줌
    # Counter=> https://jsikim1.tistory.com/218
    # most_common=> https: // dongdongfather.tistory.com / 70
    # print(keyword)

    return keyword

@csrf_exempt
def userviewlog(request):
    user=request.POST.get("userid")

    # MooyahoUser에서 userid와 같은 객체 가져오기
    user_id=MooyahoUser.objects.get(id=user)
    print(user_id)

    # 1, 2-1, 2-2
    mountain_id_list=bring_mountain_id(user_id)
    # 2-3
    mountain_id_count=bring_mountian_count(mountain_id_list)
    #3
    mountain_similarity=bring_mountain_similarity(mountain_id_list,mountain_id_count)
    #4
    keyword_similarity=bring_keyword_similarity(mountain_similarity)


    return JsonResponse({'mountain':mountain_similarity,'keyword': keyword_similarity})
