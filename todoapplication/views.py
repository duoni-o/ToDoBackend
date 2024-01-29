from django.shortcuts import render
#클래스형 View를 만들기 위해서 import
from django.views import View

#csrf 설정을 위한 import
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#데이터 모델을 가져오기 위한 import
from .models import Todo

#날짜와 시간을 사용하기 위한 import
from datetime import datetime

#JSON으로 응답하기 위한 importa
from django.http import JsonResponse

#클라이언트 정보를 JSON 문자열로 만들기 위한 import
import json 

# Todo 클래스의 인스턴스를 딕셔너리로 변환해주는 함수
#JsonRepose로 JSON 데이터를 출력하고자 하면 빠르게 JSON 문자열로 만들 때 dict만 가능하기 떄문
#dict는 JSON 문자열과 표현 방법이 같기 때문입니다.

#python application 개발자가 될거라면 함수를 만들 때 매개 변수에 자료형을 기재하고
#return type을 기재하는 형태로 만들어주는 것이 좋습니다.
def todoDictionary(todo:Todo) -> dict :
  result = {
    "id": todo.id,
    "userid": todo.userId,
    "title": todo.title,
    "done": todo.done,
    "regDate": todo.regDate,
    "modDate": todo.modDate
  }

# csrf 설정으로 클라이언트 애플리케이션을 별도로 구현하는 경우
@method_decorator(csrf_exempt, name='dispatch')
class TodoView(View):
    def post(self, request):
        # 클라이언트의 데이터를 json 형식으로 가져오기
        request = json.loads(request.body)

        # userId와 title 매개변수 값을 읽어서 저장
        # 클라이언트에서 입력해주는 데이터만 읽어오면 됩니다.
        userId = request["userId"]
        title = request["title"]

        # 모델 인스턴스 생성
        todo = Todo()
        todo.userId = userId
        todo.title = title
        
        todo.save()

        # userId와 일치하는 데이터만 추출
        todos = Todo.objects.filter(userId = userId)

        # 결과 리턴
        return JsonResponse({"list":list(todos.values())})
    
    def get(self, request):
       # GET 방식에서 userId라는 파라미터를 읽기
       userId = request.GET["userId"]
       todos = Todo.objects.filter(userId = userId)
       return JsonResponse({"list":list(todos.values())})
    
    def put(self, request):
        # 클라이언트의 데이터를 json 형식으로 가져오기
        request = json.loads(request.body)

        # userId와 title 매개변수 값을 읽어서 저장
        # 클라이언트에서 입력해주는 데이터만 읽어오면 됩니다.
        userId = request["userId"]
        id = request["id"]
        done = request["done"]

        # 모델 인스턴스 생성
        todo = Todo()
        todo.userId = userId
        todo.id = id
        todo.done = done
        
        # 수정할 데이터를 찾아옵니다.
        todo = Todo.objects.get(id = id)
        # 수정할 내용을 대입
        todo.userId = userId
        todo.done = done
        # save는 기본키의 값이 있으면 수정하고 없으면 삽입합니다.
        todo.save()

        # userId와 일치하는 데이터만 추출
        todos = Todo.objects.filter(userId = userId)

        # 결과 리턴
        return JsonResponse({"list":list(todos.values())})

    def delete(self, request):
       # 클라이언트의 데이터를 json 형식으로 가져오기
        request = json.loads(request.body)

        # userId와 id 값을 읽어서 저장
        # 클라이언트에서 입력해주는 데이터만 읽어오면 됩니다.
        userId = request["userId"]
        id = request["id"]
        
        # 수정할 데이터를 찾아옵니다.
        todo = Todo.objects.get(id = id)

        # user를 확인해서 삭제
        if userId == todo.userId:
            todo.delete()

        # userId와 일치하는 데이터만 추출
        todos = Todo.objects.filter(userId = userId)

        # 결과 리턴
        return JsonResponse({"list":list(todos.values())})