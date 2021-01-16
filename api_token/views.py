from django.http import JsonResponse

from api_token.authentications import create_token


def token_create(request):
    """APIトークン作成
    """
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'ログインしてください'}, status=403)

    if hasattr(request.user, 'token'):
        return JsonResponse({
            'message': '既にトークンがあります',
            'token': request.user.token.token
            })

    tk = create_token(request)

    return JsonResponse({
        'message': 'トークンを作成しました',
        'token': tk.token
        }, status=201)
