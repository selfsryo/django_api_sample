def has_token(request):
    """トークンを持つユーザーかチェック
    """
    return hasattr(request.user, 'token')


def check_valid_token(request):
    """
    トークン検証
    リクエストヘッダにトークンが含まれていない場合Noneを返す
    """
    hd_token = request.META.get('HTTP_AUTHORIZATION')

    if hd_token is None:
        return hd_token

    return request.user.token.token == hd_token
