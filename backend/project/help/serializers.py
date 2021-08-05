from rest_framework_recaptcha.fields import ReCaptchaField
from rest_framework.serializers import Serializer

class V3Serializer(Serializer):
    recaptcha = ReCaptchaField()