from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from .models import Board

# 기본 홈 페이지 뷰 (예시)
def index(request):
    return render(request, 'board/index.html')

# 게시글 목록 및 페이징 처리 뷰
def list(request):
    board_list = Board.objects.all().order_by('-id')
    paginator = Paginator(board_list, 10)  # 페이지당 10개의 게시글을 보여줍니다.

    page_number = request.GET.get('page')  # URL에서 페이지 번호를 가져옵니다.
    page_obj = paginator.get_page(page_number)  # 해당 페이지의 객체를 가져옵니다.

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'board/list.html', context)

# 게시글 읽기 뷰
def read(request, id):
    board = Board.objects.get(pk=id)
    board.incrementReadCount()  # 조회수 증가 함수 (모델에 구현되어야 함)
    return render(request, 'board/read.html', {'board': board})

# 게시글 등록 뷰
def regist(request):
    if request.method == 'POST':
        title = request.POST['title']
        writer = request.POST.get('writer')
        content = request.POST['content']
        Board(title=title, writer=writer, content=content).save()
        return redirect(reverse('board:list'))

    else:
        return render(request, 'board/regist.html')

# 게시글 수정 뷰
def edit(request, id):
    board = Board.objects.get(pk=id)

    if request.method == 'POST':
        board.title = request.POST['title']
        board.writer = request.POST.get('writer')
        board.content = request.POST['content']
        board.save()
        return redirect(reverse('board:read', args=(id,)))

    else:
        return render(request, 'board/edit.html', {'board': board})

# 게시글 삭제 뷰
def remove(request, id):
    board = Board.objects.get(pk=id)
    if request.method == 'POST':
        board.delete()
        return redirect(reverse('board:list'))
    else:
        return render(request, 'board/remove.html', {'board': board})
