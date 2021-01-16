import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import Office, Combi
from app.forms import (
    get_error_dict,
    CombiCreateAPIForm,
)
from api_token import authentications as auth


@csrf_exempt
def combi_create(request):
    """
    POSTに対応
    リクエストのJSONを辞書に変換してフォームに渡し、オブジェクト作成
    成功したらメッセージをJSONで返す
    拡張（他メソッドの使用）に備え@require_POSTは不使用
    """
    if request.method != 'POST':
        return JsonResponse({}, status=200)

    if not auth.has_token(request):
        return JsonResponse({'message': 'トークンを取得してください'}, status=400)

    if auth.check_valid_token(request) is None:
        return JsonResponse({'message': 'リクエストヘッダにトークンが含まれていません'}, status=400)
    elif not auth.check_valid_token(request):
        return JsonResponse({'message': 'トークンが異なります'}, status=400)

    params = json.loads(request.body)
    form = CombiCreateAPIForm(params)

    if not form.is_valid():
        return JsonResponse({
            'message': get_error_dict(form.errors)
        }, status=400)

    if not form.clean_office():
        return JsonResponse({'message': 'officeを含めてください'}, status=400)

    combi = form.save(commit=False)
    office, _ = Office.objects.get_or_create(name=params.get('office'))
    combi.office = office
    combi.save()

    return JsonResponse({'message': f'{combi.name}を作成しました'}, status=201)


def combi_list(request):
    """GET（一覧）に対応
    """
    return JsonResponse([
        combi.to_dict(fields=['id', 'name', 'office'])
        for combi in Combi.objects.all()
    ], safe=False)


def combi_detail(request, pk):
    """GET（詳細）に対応
    """
    try:
        combi = Combi.objects.get(pk=pk)
    except Combi.DoesNotExist:
        return JsonResponse({'message': '存在しないコンビです'}, status=404)
    return JsonResponse(combi.to_dict())


@csrf_exempt
def combi_delete(request, pk):
    """DELETEに対応
    """
    if request.method != 'DELETE':
        return JsonResponse({'message': 'DELETEメソッドのみ受け付けます'}, status=405)

    if not auth.has_token(request):
        return JsonResponse({'message': 'トークンを取得してください'}, status=400)

    if auth.check_valid_token(request) is None:
        return JsonResponse({'message': 'リクエストヘッダにトークンが含まれていません'}, status=400)
    elif not auth.check_valid_token(request):
        return JsonResponse({'message': 'トークンが異なります'}, status=400)

    try:
        combi = Combi.objects.get(pk=pk)
    except Combi.DoesNotExist:
        return JsonResponse({'message': '存在しないコンビです'}, status=404)

    combi.delete()
    return JsonResponse({'message': f'{combi.name}を削除しました'})
