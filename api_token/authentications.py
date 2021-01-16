import hashlib

from api_token.models import Token


def create_token(request):
    """トークンを作成
    """
    username = request.user.username
    email = request.user.email
    hs = hashlib.md5((username + email).encode()).hexdigest()

    return Token.objects.create(token=hs, user=request.user)


def has_token(request):
    """ユーザーがトークンを持つかどうかをboolで返す
    """
    return hasattr(request.user, 'token')


def check_valid_token(request):
    """
    トークンが正しいか検証
    リクエストヘッダにトークンが含まれていない場合Noneを返す
    """
    hd_token = request.META.get('HTTP_AUTHORIZATION')

    if hd_token is None:
        return hd_token

    if 'Bearer ' in hd_token:
        hd_token = hd_token.strip('Bearer ')
    else:
        return False

    return request.user.token.token == hd_token
