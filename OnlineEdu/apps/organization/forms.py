from django import forms
from operation.models import UserAsk

import re


class UserAskForm(forms.ModelForm):
    # 还可以新增字段
    # price = forms.CharField(required=True, min_length=2, max_length=20)

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # def clean_name(self):
    # def clean_course_name(self):
    def clean_mobile(self):
        # 手机号验证
        mobile = self.cleaned_data['mobile']
        p = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
        if p.match(mobile):
            # 这里还能返回外键
            return mobile
        raise forms.ValidationError('手机号码格式不对', code='mobile_inval')

