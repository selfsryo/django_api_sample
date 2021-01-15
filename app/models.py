from django.db import models


class Office(models.Model):
    """事務所"""
    name = models.CharField('事務所名', max_length=255)

    def __str__(self):
        return self.name


class Combi(models.Model):
    """コンビ"""
    name = models.CharField('コンビ名', max_length=255)
    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        verbose_name='所属事務所'
    )

    def to_dict(self, fields=['id', 'name', 'office']):
        combi_dict = {}
        if 'id' in fields:
            combi_dict['id'] = self.id
        if 'name' in fields:
            combi_dict['name'] = self.name
        if 'office' in fields:
            combi_dict['office'] = self.office.name
        return combi_dict

    def __str__(self):
        return self.name
