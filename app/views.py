from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class IndexView(TemplateView):
    template_name = 'index.html'

def how_to_use_view(request):
    template_name = 'how_to_use.html'
    return render(request, template_name)

def terms_of_service_view(request):
    template_name = 'terms_of_service.html'
    return render(request, template_name)


class UserDataView(APIView):
    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=name)
            user_option = UserProfile.objects.get(user=user)
            
            if not user_option.is_active:
                return Response({'error': '有効期限が切れています。'}, status=status.HTTP_204_NO_CONTENT)

            if user.check_password(password):
                userprofile_data = UserProfile.objects.filter(user=user)
                userprofile_serializer = UserProfileSerializer(userprofile_data, many=True)

                # 次回のアップデートでuser_emailと統合する
                userprofile_serializer.data[0]["recieve_mailaddress"] = userprofile_serializer.data[0]["user_email"]

                happymail_data = Happymail.objects.filter(user_id=user.id, is_active=True)
                # happymail_serializer = HappymailSerializer(happymail_data, many=True)
                # リクエストコンテキストをシリアライザに渡す
                happymail_serializer = HappymailSerializer(happymail_data, many=True, context={'request': request})
                
                pcmax_data = Pcmax.objects.filter(user_id=user.id, is_active=True)
                pcmax_serializer = PcmaxSerializer(pcmax_data, many=True)

                jmail_data = Jmail.objects.filter(user_id=user.id, is_active=True)
                jmail_serializer = JmailSerializer(jmail_data, many=True)

                ikukuru_data = Ikukuru.objects.filter(user_id=user.id, is_active=True)
                ikukuru_serializer = IkukuruSerializer(ikukuru_data, many=True)

                # print(userprofile_serializer.data,)
                return Response({
                    'happymail': happymail_serializer.data,
                    'pcmax': pcmax_serializer.data,
                    'jmail': jmail_serializer.data,
                    'ikukuru': ikukuru_serializer.data,
                    "user":userprofile_serializer.data,

                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')  # URLからuser_idを取得
        try:
            user = User.objects.get(id=user_id)
            user_profile = UserProfile.objects.get(user=user)
            
            # リクエストからh_schedule_time,p_schedule_timeを判別して更新
            if request.data.get('h_schedule_time', []) != []:
                h_schedule_time = request.data.get('h_schedule_time', [])
                if not isinstance(h_schedule_time, list):
                    return Response({'error': 'h_schedule_time should be a list'}, status=status.HTTP_400_BAD_REQUEST)
                # h_schedule_timeを更新
                user_profile.h_schedule_time = h_schedule_time
                user_profile.save()
                return Response({'message': 'h_schedule_time updated successfully'}, status=status.HTTP_200_OK)
            elif request.data.get('p_schedule_time', []) != []:
                p_schedule_time = request.data.get('p_schedule_time', [])
                if not isinstance(p_schedule_time, list):
                    return Response({'error': 'p_schedule_time should be a list'}, status=status.HTTP_400_BAD_REQUEST)
                # p_schedule_timeを更新
                user_profile.p_schedule_time = p_schedule_time
                user_profile.save()
                return Response({'message': 'h_schedule_time updated successfully'}, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)