from django.db import models


class DemoRequest(models.Model):
    name = models.CharField("姓名", max_length=50)
    phone = models.CharField("电话", max_length=20)
    kindergarten = models.CharField("园所名称", max_length=100)
    city = models.CharField("城市", max_length=50)
    created_at = models.DateTimeField("提交时间", auto_now_add=True)

    class Meta:
        verbose_name = "预约演示"
        verbose_name_plural = "预约演示"

    def __str__(self):
        return f"{self.name} - {self.kindergarten}"


class SchemeRequest(models.Model):
    name = models.CharField("姓名", max_length=50)
    phone = models.CharField("电话", max_length=20)
    kindergarten = models.CharField("园所名称", max_length=100)
    city = models.CharField("城市", max_length=50)
    demand = models.TextField("索取内容", help_text="想索取哪些方案/资料")
    created_at = models.DateTimeField("提交时间", auto_now_add=True)
    is_processed = models.BooleanField("是否已处理", default=False)
    note = models.TextField("备注", blank=True, default="")

    class Meta:
        verbose_name = "索取方案"
        verbose_name_plural = "索取方案"

    def __str__(self):
        return f"{self.name} - {self.kindergarten}"


class DownloadLead(models.Model):
    created_at = models.DateTimeField("下载时间", auto_now_add=True)
    name = models.CharField("姓名", max_length=50)
    phone = models.CharField("电话", max_length=20)
    kindergarten = models.CharField("园所名称", max_length=100)
    city = models.CharField("城市", max_length=50)
    product_name = models.CharField("产品名", max_length=100)
    file_name = models.CharField("文件名", max_length=255)
    file_type = models.CharField("文件类型", max_length=20, blank=True)
    file_path = models.CharField("文件路径", max_length=500)
    ip_address = models.GenericIPAddressField("IP", null=True, blank=True)
    user_agent = models.TextField("User-Agent", blank=True, default="")

    class Meta:
        verbose_name = "资料下载记录"
        verbose_name_plural = "资料下载记录"

    def __str__(self):
        return f"{self.name} - {self.file_name}"
