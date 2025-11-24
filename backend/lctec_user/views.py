from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from lctec_user.models import Cart
from tracks_app.models import Track
from flps_app.models import Flp
from django.contrib.auth import get_user_model
from tracks_app.serializers import TrackSerializer
from flps_app.serializers import FlpSerializer
from lctec_user.serializers import *
from django.core.mail import EmailMessage
# converts html template to a string message for emails
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
from sheriff_crandy_project import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework import permissions, status
from django.middleware.csrf import get_token
from django.http import JsonResponse
# for saving profilepic
from PIL import Image
from django.core.files import File
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.permissions import AllowAny
import urllib.request
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import os
import random
# import logger
import logging
logger = logging.getLogger('main')


user = get_user_model()


EMAIL_ON = False
URL = settings.env('DEV_DOMAIN') if settings.env('DEV_MODE') == 'True' else 'https://sheriffcrandymusic.com'





# save user pfp on signup. I tried to save this in my create_user method but the 
# image file was not available in the extra_fields param for some reason
# SaveUserProfilePicture API view
# SaveUserProfilePicture API view
class SaveCustomBasicUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            profile_pic = request.FILES.get('profile_pic', None)        
            if profile_pic:            
                profile_pic.file.seek(0)
                image = Image.open(BytesIO(profile_pic.read()))
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                pfp_name = serializer.validated_data['username'] + '_pfp'
                buffer = BytesIO()
                image.save(buffer, format='JPEG')
                image_file = InMemoryUploadedFile(
                    buffer, None, pfp_name + '.jpg', 'image/jpeg',
                    buffer.getbuffer().nbytes, None
                )
                # Call create_user method of custom user manager to create user instance
                user = Lctec_CustomUserManager().create_user(
                    email=serializer.validated_data['email'],
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password'],
                    profile_pic=image_file,
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    favorite_color=serializer.validated_data['favorite_color']
                )
                return Response(status=status.HTTP_200_OK)
            else:

                # save user without profile pic
                user = Lctec_CustomUserManager().create_user(
                    email=serializer.validated_data['email'],
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password'],
                    profile_pic=None,
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    favorite_color=serializer.validated_data['favorite_color']
                )
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get user pfp on login
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_user_pfp(request):
    current_user = user.objects.get(pk=request.user.pk)
    user_pfp_serializer = GetUserPfpSerializer(current_user)

    response = Response(user_pfp_serializer.data, status=status.HTTP_200_OK)
    # added this to prevent vuejs from caching cart data
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'


    return response


# delete user account
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def delete_user_account_data(request):

    # use first to prevent exception from being raised
    try:

        user_to_be_deleted = user.objects.get(pk=request.user.pk)
        user_to_be_deleted.delete()
        # return no content, everything worked
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    except:
        return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)


# update user account info
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def update_user_account_data(request):

    # get the user
    current_user = user.objects.get(pk=request.user.pk)
    # Deserialize incoming data
    # serializer = UpdateUserAccountDataSerializer(data=request.data)
    serializer = UpdateUserAccountDataSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():

        # get the img file
        profile_pic = request.FILES.get('profile_pic', None)

        if profile_pic:
            
            profile_pic.file.seek(0)
            # Open the uploaded image file
            image = Image.open(BytesIO(profile_pic.read()))

            # Convert RGBA to RGB mode if it exists
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            pfp_name = current_user.username + '_pfp' + str(random.randint(10, 100000))

            buffer = BytesIO()
            image.save(buffer, format='JPEG')
            image_file = InMemoryUploadedFile(
                buffer, None, pfp_name + '.jpg', 'image/jpeg',
                buffer.getbuffer().nbytes, None
            )

            # delete current profile pic if it exists
            if current_user.profile_pic:
                profile_pic_path = os.path.join(settings.MEDIA_ROOT, str(current_user.profile_pic))
                logger.debug(str(profile_pic_path))
                if os.path.exists(profile_pic_path):
                    logger.debug("PFP Exists: " + str(os.path.exists(profile_pic_path)))
                    os.remove(profile_pic_path)

            # Save the new profile picture
            current_user.profile_pic.save(pfp_name + '.jpg', image_file)

        else:
            print('\n\n Image does not exist')
        # save the rest of the text fields
        # Update user fields
        # validated_data is a dictionary that holds validated data ready to be saved to db
        current_user.username = serializer.validated_data.get('username', current_user.username)
        current_user.email = serializer.validated_data.get('email', current_user.email)
        current_user.first_name = serializer.validated_data.get('first_name', current_user.first_name)
        current_user.last_name = serializer.validated_data.get('last_name', current_user.last_name)
        current_user.favorite_color = serializer.validated_data.get('favorite_color', current_user.favorite_color)

        current_user.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get user account data
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_user_account_data(request):

    current_user = user.objects.get(pk=request.user.pk)
    user_serializer = GetUserSerializer(current_user)

    response = Response(user_serializer.data, status=status.HTTP_200_OK)
    # added this to prevent vuejs from caching cart data
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'


    return response

# reset password
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password(request):

    try:
        
        uid = force_str(urlsafe_base64_decode(request.data.get('uidb64')))

        current_user = user.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        current_user = None

    # Check if the token is valid
    if current_user is not None and default_token_generator.check_token(current_user, request.data.get('token')):
        # Set the new password for the user
        password = request.data.get('password')
        current_user.set_password(password)
        current_user.save()

        template = render_to_string('../templates/changed_account_notice_email.html', {'name':current_user.first_name})
        email = EmailMessage(
            # email subject title default is 'subject'
            'There was a change to your account -- アカウント情報変更のお知らせ',
            # email template default is 'body'
            template,
             
            settings.EMAIL_HOST_USER,
            # recipient list
            [current_user.email],
        )
        email.fail_silently=False
        # eonly send email if this flag is true
        if EMAIL_ON:
            email.send()

        return Response({'success': 'Password reset successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)


# send password reset link
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_password_reset_link(request):
    
    # get the email address from the POST request
    email = request.data.get('potential_email_address')

    # check if the email address is valid
    try:
        get_user = user.objects.get(email=email)

        # creating a password reset url unique for each user
        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(get_user.pk))
        token = token_generator.make_token(get_user)
        # create the password reset URL using the generated token
        password_reset_url = f'{URL}{request.data.get("password_reset_url")}/{uidb64}/{token}/'



        EMAIL_ON = True
        template = render_to_string('../templates/password-reset-email.html', {'name':get_user.first_name, 'password_reset_url': password_reset_url})
        email = EmailMessage(
            # email subject title default is 'subject'
            'Password Reset -- パスワードのリセット',
            # email template default is 'body'
            template,
            settings.EMAIL_HOST_USER,
            # recipient list
            [get_user.email],
        )
        email.fail_silently=False
        # only send email if this flag is true
        if EMAIL_ON:
            email.send()
        # just return a 200 response
        return HttpResponse(status=200)
    except user.DoesNotExist:
        # handle the case where the user does not exist
        return Response({'error': 'User does not exist'}, status=200)
    
    except Exception as e:
        return Response({'error': 'Unknown error occurred'}, status=500)


# get user data
@api_view(['GET'])
def get_user_device(request):


    user_ip = request.META.get('HTTP_X_FORWARDED_FOR')

    if user_ip is not None:
        ip = user_ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    '''
    valid fields to consume i.e.
    status
    country
    countryCode
    region
    regionName
    city
    zip
    lat
    lon
    timezone
    isp
    org
    as
    query
    
    '''
    GEO_IP_API_URL = 'http://ip-api.com/json/'

    # live
    IP_TO_SEARCH = ip
    # japan test
    # IP_TO_SEARCH = '203.10.99.206'
    # usa test
    # IP_TO_SEARCH = '24.117.191.114'
    # random country test
    # IP_TO_SEARCH = '1.177.255.255'
    # admin test 
    # IP_TO_SEARCH = settings.env('ADMIN_IP')

    req = urllib.request.Request(GEO_IP_API_URL+IP_TO_SEARCH)

    response = urllib.request.urlopen(req).read()

    json_response = json.loads(response.decode('utf-8'))        

    BASE_DIR = Path(__file__).resolve().parent.parent
    ip_file_log = str(BASE_DIR) + '/backend_logger/' + settings.env('IP_RECORD_FILE')

    # 5GB
    MAX_FILE_SIZE = 5 * 1024 *1024 *1024
    now_mst = datetime.now(ZoneInfo("America/Denver"))
    formatted = now_mst.strftime("%Y-%m-%d %H:%M:%S")
    # Print country
    try:
        
        country = str(json_response['country'])
        data = {}
        if country != 'United States' and country != 'Japan':
            data = {'user_country': 'United States'}
        else:
            data = {'user_country': country}     

        # write region data to log
        # if the file does not exist, a+ will create it. Write the log
        # if the file exists and it's smaller than MAX_FILE_SIZE, write the log
        # if the file exists but it's larger than MAX_FILE_SIZE, don't write the log
        # if the IP in question is the ADMIN_IP, don't write log
        if (not os.path.exists(ip_file_log) or os.stat(ip_file_log).st_size < MAX_FILE_SIZE) and str(IP_TO_SEARCH) != settings.env('ADMIN_IP'):
            with open(ip_file_log,"a+", encoding="utf-8") as text_file:

                text_file.write(
                    f"[{formatted}]\t"
                    f"IP: {IP_TO_SEARCH}\t"
                    f"COUNTRY: {json_response['country']}\t"
                    f"REGION: {json_response['regionName']}\t"
                    f"CITY: {json_response['city']}\t"
                    f"POST CODE: {json_response['zip']}\t"
                    f"ISP: {json_response['isp']}\n"
                )

        return Response(data)
    
    except Exception as e:       
        if settings.env('DEV_MODE') == 'True':
            # return Response({'user_country': 'United States'})
            # return Response({'user_country': 'Japan'})
            logger.exception(str(e))
            return Response({'user_country': 'Other Country'})
        else:

            with open(ip_file_log,"a+", encoding="utf-8") as text_file:
                text_file.write(f"IP: {IP_TO_SEARCH}")     

            logger.exception(str(e))
            return Response({'user_country': 'United States'})

# get user's cart data after they have authenticated (logged in)
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_user_cart(request):

        # get user's cart data
        cart_data = get_cart_data(request.user)

        print(str(len(cart_data) > 0))

        response = Response({
            'username': request.user.username,
            'cart': cart_data
        })
        # added this to prevent vuejs from caching cart data
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Expires'] = '0'

        return response

# get user's cart data, if any
def get_cart_data(user):
    # get the cart, use filter().first() to avoid NotFound error. 
    # will return None if not found
    cart = Cart.objects.filter(user=user).first()
    cart_data = []
    if cart:
        # get all the track cart items via serializer
        for item in cart.tracks_in_cart.all():
            track_serializer = TrackSerializer(item)
            cart_data.append(track_serializer.data)
        for item in cart.flps_in_cart.all():
            flp_serializer = FlpSerializer(item)
            cart_data.append(flp_serializer.data)

    return cart_data


# delete user's cart when they log out if the cart was empty
# called on logout if the user's cart was empty
# in the cart view if the user clears the cart
# and when the user removes the last cart item from the cart
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def delete_cart(request):

    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        # clear all tracks and flps from cart
        cart.tracks_in_cart.clear()
        cart.flps_in_cart.clear()

        # reset cart counts
        cart.flp_cart_quantity = 0
        cart.track_cart_quantity = 0
        cart.total_cart_quantity = 0

        cart.save()

    return HttpResponse(status=200)



# checking username in form validation
# need to include the request or else there will be an error
@api_view(['GET'])
def check_username(request, username):
    username_available = not user.objects.filter(username=username).exists()

    response = Response({'available': username_available})
    # added this to prevent vuejs from caching cart data
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'

    return response

# checking username in form validation
@api_view(['GET'])
def check_email(request, email):
    email_available = not user.objects.filter(email=email).exists()

    response = Response({'available': email_available})
    # added this to prevent vuejs from caching cart data
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'

    return response

# de-authenticate user by deleting auth token, and storing/updating and then saving the user's cart data
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):

        cart_data = request.data
        number_of_flps = 0
        number_of_tracks = 0

        # populate track and flp lists from request data
        incoming_tracks_in_cart = [item.get('title')  for item in cart_data.get('cart', []) if 'title' in item]
        number_of_tracks = len(incoming_tracks_in_cart)

        incoming_flps_in_cart = [item.get('flp_name') for item in cart_data.get('cart', []) if 'flp_name' in item]
        number_of_flps = len(incoming_flps_in_cart)

        # check if this user has a cart object associated with it
        # using this to set cart to None if no object exists instead of raising a DoesNotExist exception
        cart = Cart.objects.filter(user=request.user).first()

        if cart:
            # get all the tracks/flps currently in user's saved cart
            current_tracks_in_cart = [item.title for item in cart.tracks_in_cart.all()]
            current_flps_in_cart = [item.flp_name for item in cart.flps_in_cart.all()]

            # if the carts match, there was no change, just log the user out
            if incoming_tracks_in_cart == current_tracks_in_cart and incoming_flps_in_cart == current_flps_in_cart:
                
                # delete auth token
                user = request.user
                Token.objects.filter(user=user).delete()
                return Response({'success': 'Logged out successfully.'})
            else:

                # if the cart is empty, delete the cart
                if number_of_tracks == 0 and number_of_flps == 0:

                    cart.delete()
                    # delete auth token
                    user = request.user
                    Token.objects.filter(user=user).delete()
                    return Response({'success': 'Logged out successfully.'})

                # else cart is not empty, but the cart contents are different
                else:
                    tracks = Track.objects.filter(title__in=incoming_tracks_in_cart)

                    flps = Flp.objects.filter(flp_name__in=incoming_flps_in_cart)

                    cart.tracks_in_cart.set(tracks)
                    cart.flps_in_cart.set(flps)
                    cart.flp_cart_quantity = number_of_flps
                    cart.track_cart_quantity = number_of_tracks

                    cart.total_cart_quantity = number_of_flps + number_of_tracks    

                    cart.save()

                    # delete auth token
                    user = request.user
                    Token.objects.filter(user=user).delete()
                    return Response({'success': 'Logged out successfully.'})

        # user doesn't have cart, create one
        else:
            # if the incoming cart is empty, don't make a new one
            if number_of_tracks == 0 and number_of_flps == 0:

                # delete auth token
                user = request.user
                Token.objects.filter(user=user).delete() 
                return Response({'success': 'Logged out successfully.'})        
            
            else:
                # pass in lists from frontend to get list of track/Flp objs
                tracks = Track.objects.filter(title__in=incoming_tracks_in_cart)

                flps = Flp.objects.filter(flp_name__in=incoming_flps_in_cart)

                cart = Cart.objects.create(user=request.user)
                cart.tracks_in_cart.set(tracks)
                cart.flps_in_cart.set(flps)
                cart.flp_cart_quantity = number_of_flps

                cart.track_cart_quantity = number_of_tracks

                cart.total_cart_quantity = number_of_flps + number_of_tracks  

                cart.save()

                # delete auth token
                user = request.user
                Token.objects.filter(user=user).delete()
                return Response({'success': 'Logged out successfully.'})