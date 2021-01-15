from django.contrib import admin

from api_token.models import Token


class TokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Token, TokenAdmin)
