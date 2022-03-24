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

    #2-2
    mountain_id_list = sorted(mountain_id_list.items(), key=lambda x: x[1], reverse=True)

    return mountain_id_list

#2-3. mountain_id_list중 5개만 돌리기 위해 리스트안의 개수 구하기->만약 5개가 안되면 있는 값만 가져온다
def bring_mountian_id_count(mountain_id_list):
    count = 5
    if len(mountain_id_list) < 5:
        count = len(mountain_id_list)

    return count

#3-1. 벡터화를 이용해 유사한 구하고 csv로 저장
#3-2. csv 데이터 프레임으로 만들기
df = pd.read_csv('mountain_recommend1.csv')

#3-3. 산의 리스트 돌리면서 각 산과 유사한 산 리스트에 저장하기
def bring_mountain_similarity(mountain_id_list,mountain_id_list_count):
    #3-3
    find_count=pd.DataFrame()

    for count in range(mountain_id_list_count):
        mountain_id=mountain_id_list[count][0]
        # print(mountain_id)
        find_mountain=df.loc[df['mountian_id']==mountain_id]
        # print(f'{mountain_id}인 행 모두 가져오기:\n{find_mountain}')

        find_count_add=find_mountain['mountian_similarity'].value_counts()
        find_count=pd.concat([find_count,find_count_add])

    find_count=find_count.index.value_counts()[:10]
    list = find_count.index.tolist()
    return list

#4. 추천산 10개 리스트를 가져와 keyword하나 가져오는 함수
#4-1. 추천산 10개 리스트의 각각의 산의 token을 df에서 가져와서 token_df에 저장
#4-2. token_df에 들어가있는 token 하나씩 넣기
#4-3. 많이 반복된 키워드 3개 가져오기
def bring_keyword_similarity(mountain_similarity):
    #4-1
    token_df = []
    for index in mountain_similarity:
        tokens=df[(df['mountian_id']==index)&(df['mountian_similarity']==index)]['mountain_tokens']
        # print(f'mountain_id {index}의 tokens: {tokens}')
        token_df.extend(tokens)
    # print(token_df)

    #4-2
    token_list=[]
    for i in token_df:
        token_list.extend(i[1:-1].replace("\'","").split(','))
    # print(token_list)

    #4-3
    keyword_list=[]
    keyword=Counter(token_list).most_common(3)
    for index in range(3):
        keyword_list.append(keyword[index][0])
    # print(keyword_list)

    return keyword_list

@csrf_exempt
def userviewlog(request):
    user=request.POST.get("userid")
    user_id=MooyahoUser.objects.get(id=user)
    # print(user_id)

    # 1, 2-1, 2-2
    mountain_id_list=bring_mountain_id(user_id)
    # 2-3
    mountain_id_list_count=bring_mountian_id_count(mountain_id_list)
    #3
    mountain_similarity=bring_mountain_similarity(mountain_id_list,mountain_id_list_count)
    #4
    keyword_similarity=bring_keyword_similarity(mountain_similarity)
    # print(f'mountain_similarity:{mountain_similarity}\nkeyword_similarity:{keyword_similarity}')

    return JsonResponse({'mountain':mountain_similarity,'keyword': keyword_similarity})