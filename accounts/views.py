
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import UserModel
import re


def signup(request):
    if request.method == 'GET':  # GET 메서드로 요청이 들어 올 경우
        return render(request, 'accounts/signup.html')

    elif request.method == 'POST':  # POST 메서드로 요청이 들어 올 경우
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        regex_email = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+[.]?\w{2,3}$'
        check_email = re.search(regex_email, email)
        if not check_email:
            return render(request, 'accounts/signup.html', {'error': '이메일 형식을 확인해주세요'})
        if password != password2:
            return render(request, 'accounts/signup.html', {'error': '비밀번호를 확인해주세요!'})
        else:
            if username == '' or password == '':
                return render(request, 'accounts/signup.html', {'error': '사용자 이름과 비밀번호는 필수 입력 사항입니다.'})
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'accounts/signup.html', {'error': '이미 존재하는 이름입니다.'})
            else:
                UserModel.objects.create_user(username=username, password=password, email=email)
        return redirect('/user_login')

def user_login(request):
# 로그인 view
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = authenticate(request, username=username, password=password)
        if me is not None:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            login(request, me)
            return redirect('/')
        else:  # 로그인이 실패하면 다시 로그인 페이지를 보여주기
            return render(request, 'accounts/signin.html', {'error':"유저 이름 또는 비밀번호를 확인해주세요."})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/') # 로그아웃
        else:
            return render(request, 'accounts/signin.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')