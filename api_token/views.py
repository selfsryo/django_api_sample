import hashlib

from django.http import JsonResponse

from api_token.models import Token


def token_create(request):
    """
    APIトークン作成
    """
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'ログインしてください'}, status=403)

    if hasattr(request.user, 'token'):
        return JsonResponse({
            'message': '既にトークンがあります',
            'token': request.user.token.token
            })

    username = request.user.username
    email = request.user.email
    hs = hashlib.md5((username + email).encode()).hexdigest()

    tk = Token.objects.create(token=hs, user=request.user)
    return JsonResponse({
        'message': 'トークンを作成しました',
        'token': tk.token
        }, status=201)
