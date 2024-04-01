from rest_framework import serializers
from account.models import User,UserOTP
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util



domain = "https://mcq.gastii.com"

class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = User
        fields = ['id', 'name','email','password','phone_No','avatar','avatar_url','is_admin','is_user']

    def get_image_url(self, obj):
        if obj.avatar:
          return f'{domain}{obj.avatar.url}'


class UserRegistrationSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'password', 'password2', 'phone_No']
    extra_kwargs={
      'password':{'write_only':True}
    }

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password don't match !")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name','phone_No','avatar']


class UserChangePasswordSerializer(serializers.Serializer):
  oldPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  newPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirmPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['oldPassword', 'newPassword','confirmPassword']
    




import random
import datetime
from django.utils import timezone
class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))

      otp_code = str(random.randint(1000, 9999))

      expiration_time = timezone.now() + datetime.timedelta(minutes=5)

      userotp =UserOTP.objects.filter(user=user).first()
      print("OTP Code:",otp_code)
      print(timezone.now())
      print("Expired time:",expiration_time)
      print(userotp)
      if userotp:
        userotp.otp_code = otp_code
        userotp.otp_code_expiration = expiration_time
        userotp.save()
      else:
         userotp = UserOTP.objects.create(user=user,otp_code = otp_code,otp_code_expiration = expiration_time)

      # Send the email with the OTP
      body = f'Your OTP code for password reset is: {otp_code}'
      data = {
          'subject': 'Reset Your Password',
          'body': body,
          'to_email': user.email
      }

      # Send email using your Util class
      Util.send_email(data)

      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')




# otp validatin serializer
class OTPValidationSerializer(serializers.Serializer):

  otp_code = serializers.CharField(max_length=150, style={'type': 'number'}, write_only=True)

  class Meta:
      fields = ['otp_code']

  def validate(self, attrs):
      try:
          otp_code = attrs.get('otp_code')
          otp_details = UserOTP.objects.get(otp_code=otp_code)
          userotp = UserOTP.objects.get(user=otp_details.user.id)

          if userotp.otp_code != otp_code:
              raise serializers.ValidationError('Invalid OTP code')

          if userotp.otp_code_expiration is not None and userotp.otp_code_expiration < timezone.now():
              raise serializers.ValidationError('OTP code has expired')

          attrs['user'] = otp_details.user 
          return attrs
      except UserOTP.DoesNotExist:
          raise serializers.ValidationError('Invalid OTP code')
      except Exception as e:
          raise serializers.ValidationError('Failed to validate OTP code')

  

  



class UserPasswordResetSerializer(serializers.Serializer):
  newPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirmPassword = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['newPassword', 'confirmPassword']

  def validate(self, attrs):
    try:
        password = attrs.get('newPassword')
        confirmPassword = attrs.get('confirmPassword')
        user = self.context.get('user')
        print(user)
        userotp = UserOTP.objects.get(user=user)

        if password != confirmPassword:
            raise serializers.ValidationError("Password and Confirm Password don't match")


        if userotp.otp_code_expiration is not None and userotp.otp_code_expiration < timezone.now():
            raise serializers.ValidationError('OTP code has expired')

        user.set_password(password)
        user.set_password(confirmPassword)
        user.save()

        return attrs
    except Exception as e:
        print(e)
        raise serializers.ValidationError('Failed to reset the password')
