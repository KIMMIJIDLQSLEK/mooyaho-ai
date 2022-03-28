from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Post
import pandas as pd
import pymysql
from sklearn.metrics.pairwise import cosine_similarity
from mooyahoai.my_settings import MY_DATABASES
from django.db.models import Q

def make_dataframe():
    # post = pd.read_csv('post_test2.csv', encoding='cp949')  # 임의의 csv

    #db연결
    db = pymysql.connect(
        host=MY_DATABASES['default']['HOST'],
        port=int(MY_DATABASES['default']['PORT']),
        user=MY_DATABASES['default']['USER'],
        passwd=MY_DATABASES['default']['PASSWORD'],
        db=MY_DATABASES['default']['NAME'],
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor,
        init_command='SET NAMES UTF8'  # UTF8 로  가져오기
    )
    # print(db)

    # 특정 TABLE 데이터 가져오기
    TABLE_NAME = 'mooyaho_post'  # table명
    cursor = db.cursor()
    # 디비 가져오기
    sql = f"SELECT * FROM {TABLE_NAME}"  #해당되는 테이블 필드 전체
    cursor.execute(sql)
    table_data = cursor.fetchall()
    # print(table_data)

    #데이터프레임으로 만들기
    df = pd.DataFrame(table_data)
    # print(df)

    return df


@csrf_exempt
def userpost(request):
    user_id = request.POST.get("userid") #userid가져오기
    if Post.objects.filter(Q(user=user_id) & Q(deleted=0)).exists():  #게시물이 있다면
        post=make_dataframe()
        post.drop(post.loc[post['deleted']==1].index,inplace=True)  #가져온 데이터프레임에서 삭제된 게시물은 없애기
        # print(post)

        user_rating = post.pivot_table('rating', index='author_id', columns='mountain_id')
        user_rating = user_rating.fillna(0)
        user_based_collab = cosine_similarity(user_rating, user_rating)  # 한명씩 모든 유저와 유사성 비교
        user_based_collab = pd.DataFrame(user_based_collab, index=user_rating.index, columns=user_rating.index)
        # print(user_based_collab)
        user = user_based_collab[int(user_id)].drop(int(user_id))  #자기자신을 제외한 비슷한 유저 가져오기
        user = user.sort_values(ascending=False).head(3).index.tolist()  #가장 비슷한 유저 3명 가져오기
        print(user)

        return JsonResponse({'data': 1, 'user':user})

    else: #없으므로 게시물에 올리라고 권유
        print("없음")
        return JsonResponse({'data':0})




