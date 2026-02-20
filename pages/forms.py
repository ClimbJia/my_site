import re

from django import forms

from .models import DemoRequest, SchemeRequest


def validate_phone(value):
    if not re.match(r"^1\d{10}$", str(value).strip()):
        raise forms.ValidationError("请输入正确的11位手机号")


class DemoRequestForm(forms.ModelForm):
    class Meta:
        model = DemoRequest
        fields = ["name", "phone", "kindergarten", "city"]
        labels = {
            "name": "姓名",
            "phone": "电话",
            "kindergarten": "园所名称",
            "city": "城市",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "请输入姓名"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "请输入联系电话"}
            ),
            "kindergarten": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "请输入园所名称"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "请输入城市"}
            ),
        }


class SchemeRequestForm(forms.ModelForm):
    class Meta:
        model = SchemeRequest
        fields = ["name", "phone", "kindergarten", "city", "demand"]
        labels = {
            "name": "姓名",
            "phone": "电话",
            "kindergarten": "园所名称",
            "city": "城市",
            "demand": "索取内容",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "请输入姓名"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "请输入11位手机号"}
            ),
            "kindergarten": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "请输入园所名称"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "请输入城市"}
            ),
            "demand": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "placeholder": "请描述您想索取的方案或资料",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].validators.append(validate_phone)
        self.fields["website"] = forms.CharField(
            required=False,
            widget=forms.HiddenInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
            label="",
        )

    def clean_website(self):
        val = self.cleaned_data.get("website", "").strip()
        if val:
            raise forms.ValidationError("无效提交")
        return val


class DownloadLeadForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label="姓名",
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "请输入姓名"}
        ),
    )
    phone = forms.CharField(
        max_length=20,
        label="电话",
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "请输入11位手机号"}
        ),
    )
    kindergarten = forms.CharField(
        max_length=100,
        label="园所名称",
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "请输入园所名称"}
        ),
    )
    city = forms.CharField(
        max_length=50,
        label="城市",
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "请输入城市"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].validators.append(validate_phone)
