from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from .models import Board

# �⺻ Ȩ ������ �� (����)
def index(request):
    return render(request, 'board/index.html')

# �Խñ� ��� �� ����¡ ó�� ��
def list(request):
    board_list = Board.objects.all().order_by('-id')
    paginator = Paginator(board_list, 10)  # �������� 10���� �Խñ��� �����ݴϴ�.

    page_number = request.GET.get('page')  # URL���� ������ ��ȣ�� �����ɴϴ�.
    page_obj = paginator.get_page(page_number)  # �ش� �������� ��ü�� �����ɴϴ�.

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'board/list.html', context)

# �Խñ� �б� ��
def read(request, id):
    board = Board.objects.get(pk=id)
    board.incrementReadCount()  # ��ȸ�� ���� �Լ� (�𵨿� �����Ǿ�� ��)
    return render(request, 'board/read.html', {'board': board})

# �Խñ� ��� ��
def regist(request):
    if request.method == 'POST':
        title = request.POST['title']
        writer = request.POST.get('writer')
        content = request.POST['content']
        Board(title=title, writer=writer, content=content).save()
        return redirect(reverse('board:list'))

    else:
        return render(request, 'board/regist.html')

# �Խñ� ���� ��
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

# �Խñ� ���� ��
def remove(request, id):
    board = Board.objects.get(pk=id)
    if request.method == 'POST':
        board.delete()
        return redirect(reverse('board:list'))
    else:
        return render(request, 'board/remove.html', {'board': board})