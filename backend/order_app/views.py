# to talk to Stripe API
from django.http import HttpResponse, HttpResponseNotFound, StreamingHttpResponse
import stripe
from django.conf import settings

# drf imports
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

# import Order serializers
from tracks_app.serializers import GetPurchasedTrackSerializer

# import track and flp models
from order_app.models import *
from flps_app.models import *
from tracks_app.models import *

# import modules to zip up multiple files
import zipfile
# send thank you email to user after purchase
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# import env vars
import environ
env = environ.Env()
environ.Env.read_env()

# import logger
import logging

# Get the logger named 'main' as defined in settings.py
logger = logging.getLogger('main')

# can turn emails off for testing
EMAIL_ON = True
FRONTEND_DOMAIN = None

if env('DEV_MODE') == 'True':
    FRONTEND_DOMAIN = env('FRONTEND_DEV_DOMAIN')
else:
    FRONTEND_DOMAIN = env('FRONTEND_DOMAIN')


# zip up mulitple files
# sample: https://stackoverflow.com/questions/12881294/django-create-a-zip-of-multiple-files-and-make-it-downloadable
# https://www.youtube.com/watch?v=6HjHPvmwiSs
def createZip(fileList):

    list_of_files = fileList
    tmp_path = '/tmp/'
    zip_file = zipfile.ZipFile(tmp_path + 'sheriff_crandy_downloadables.zip', 'w')
    # loop through list
    for file in list_of_files:

        # get the filename only
        fdir, fname = os.path.split(file)
        try:
            zip_file.write(str(file), str(fname), compress_type= zipfile.ZIP_DEFLATED)
        except Exception as e:
            logger.exception("File in order_app/views.py/createZip() function failed to zip:")
            return
    zip_file.close()
    return (tmp_path + 'sheriff_crandy_downloadables.zip')


# returns one of the following from the cart view:
# - one free/paid .wav file
# - one free/paid single FLP as a .zip file
# - multiple free/paid tracks and/or FLPs as a .zip file
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def cartCheckout(request, id, isSingleFile, isfree):

    # free cart download
    if isfree == 'true':

        # a single free wav or flp download
        if isSingleFile == 'true':

            # one free track
            if len(request.data.get('track_items', [])) > 0:
                free_track = Track.objects.get(pk=id)
                free_track.downloads += 1
                free_track.save()

                # set order
                free_download_order = Order.objects.create(user=request.user, free_download=True)
                free_download_order.track.set([free_track])  # Wrap track in a list        
                free_download_order.save()

                return Response(status=status.HTTP_200_OK)
            
            
            # one free flp
            else:
                free_flp = Flp.objects.get(pk=id)
                free_flp.downloads += 1
                free_flp.save()     

                # set order
                free_download_order = Order.objects.create(user=request.user, free_download=True)
                free_download_order.flp.set([free_flp])  # Wrap track in a list        
                free_download_order.save()

                return Response(status=status.HTTP_200_OK)
        
        # multiple free files download. Return zip
        else:

            order_dict = request.data
            response = None

            # processing paid flps and tracks together
            try:

                freeTrackList = []
                freeFlpList = []
                queriedTrackObjs = None
                queriedFlpObjs = None

                # check if there are any flp_items
                if len(order_dict.get('flp_items', [])) > 0:

                    for item in order_dict.get('flp_items', []):
                        flp_id = item.get('flp')
                        current_flp = Flp.objects.get(pk=flp_id)
                        current_flp.downloads += 1
                        freeFlpList.append(current_flp.pk)
                        current_flp.save()  
                    
                    queriedFlpObjs = Flp.objects.filter(pk__in=freeFlpList)

                # check if there are any track_items
                if len(order_dict.get('track_items', [])) > 0:

                    for item in order_dict.get('track_items', []):
                        track_id = item.get('track')
                        current_track = Track.objects.get(pk=track_id)
                        current_track.downloads += 1
                        freeTrackList.append(current_track.pk)
                        current_track.save()  

                    queriedTrackObjs = Track.objects.filter(pk__in=freeTrackList)

                try:

                    tracksAndFlpsForZip = []

                    if queriedTrackObjs is not None:
                        for item in queriedTrackObjs:
                            # gets the absolute path
                            tracksAndFlpsForZip.append(item.track.path)
                    
                    if queriedFlpObjs is not None:
                        for item in queriedFlpObjs:
                            # gets the absolute path
                            tracksAndFlpsForZip.append(item.flp_zip.path)
                
                    # if this was a single wav purchase 

                    zip = createZip(tracksAndFlpsForZip)

                    # open this zip file as byte data and setting the byte data to variable for delivering to client via http
                    with open(zip, 'rb') as f:
                        file_data = f.read()

                    print('zip file: ' + str(zip) + '\n')
                    print('file_data type: ' + str(type(file_data)) + '\n')
                    response = HttpResponse(file_data, content_type='application/zip')
                    response['Content-Disposition'] = 'attachment; filename=sheriff_crandy_downloadables.zip'
                                            
                    os.remove(zip)

                    # save order
                    free_download_order = Order.objects.create(user=request.user, free_download=True)
                    if queriedFlpObjs is not None:
                        free_download_order.flp.set(queriedFlpObjs)

                    if queriedTrackObjs is not None:
                        free_download_order.track.set(queriedTrackObjs)

                        
                    free_download_order.save()

                    music_url = f'{FRONTEND_DOMAIN}/music'
                    template = render_to_string('../templates/thankyou.html', {'name':request.user.first_name, 'music_url': music_url})
                    # send thankyou email to user
                    email = EmailMessage(
                        # email subject title default is 'subject'
                        'Thank you! -- ありがとうございます！',
                        # email template default is 'body'
                        template,
                        settings.EMAIL_HOST_USER,
                        # recipient list
                        [request.user.email],
                    )
                    email.fail_silently=False
                    # only send email if this flag is true
                    if EMAIL_ON:
                        email.send()            

                    # finally send response back to client      
                    return response
                except Exception as e:
                    logger.exception("In checkout multiple paid tracks and flps block. Failed to zip up and return a multiple paid tracks and flps to frontend")

                    error_message = "The server failed to deliver the content requested. We apologize for the inconvenince and we are working diligently to fix this."
                    response_data = {
                        "error": error_message
                    }
                    return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:

                logger.exception("Failed to post stripe charge or send thankyou email to user")

                error_message = "The server failed to deliver the content requested. We apologize for the inconvenince and we are working diligently to fix this."
                response_data = {
                    "error": error_message
                }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST) 


    # purchased cart download
    else:

        # bool to check if this is a US or Japan payment
        isUsd = None
        # get the amounts paid in the proper formats
        TOTAL_USD_PAID = float(str(request.data.pop('usd_paid_amount')).strip(' "'))
        TOTAL_JPY_PAID = int(str(request.data.pop('jpy_paid_amount')).strip(' "'))
        response = None

        # check if this is a usd or jpy purchase
        # if TOTAL_JPY_PAID > 1 and TOTAL_USD_PAID == 0.0:
        #     isUsd = False
        # else:
        #     isUsd = True

        isUsd = False if TOTAL_JPY_PAID > TOTAL_USD_PAID else True

        order_dict = request.data
        paid_download_order = None

        # single purchased file
        if isSingleFile == 'true':

            # one free track
            if order_dict['track_items']:
                
                paid_track = Track.objects.get(pk=id)
                paid_track.downloads += 1
                paid_track.save()

                # set order
                paid_download_order = Order.objects.create(
                    user=request.user, 
                    name=request.data.get('name'),
                    email=request.data.get('email'),
                    # phone=request.data.get('phone'),
                    address1=request.data.get('address1'),
                    address2=request.data.get('address2'),
                    statePref=request.data.get('statePref'),
                    country=request.data.get('country'),
                    zipcode=request.data.get('zipcode'),
                    stripe_token=request.data.get('stripe_token'),
                    usd_paid_amount=TOTAL_USD_PAID, 
                    jpy_paid_amount=TOTAL_JPY_PAID, 
                    free_download=False)
                paid_download_order.track.set([paid_track])  # Wrap track in a list        
                paid_download_order.save()
                
            
            # one free flp
            else:
                             
                paid_flp = Flp.objects.get(pk=id)
                paid_flp.downloads += 1
                paid_flp.save()     

                # set order
                paid_download_order = Order.objects.create(
                    user=request.user, 
                    name=request.data.get('name'),
                    email=request.data.get('email'),
                    # phone=request.data.get('phone'),
                    address1=request.data.get('address1'),
                    address2=request.data.get('address2'),
                    statePref=request.data.get('statePref'),
                    country=request.data.get('country'),
                    zipcode=request.data.get('zipcode'),
                    stripe_token=request.data.get('stripe_token'),
                    usd_paid_amount=TOTAL_USD_PAID, 
                    jpy_paid_amount=TOTAL_JPY_PAID, 
                    free_download=False)
                paid_download_order.flp.set([paid_flp])  # Wrap track in a list        
                paid_download_order.save()
            
            # processing single paid track or flp from cart
            try:

                charge = createStripeCharge(TOTAL_USD_PAID, TOTAL_JPY_PAID, isUsd, request.data.get('stripe_token'), request.data.get('email'), request.data.get('name'))

                music_url = f'{FRONTEND_DOMAIN}/music'
                template = render_to_string('../templates/thankyou.html', {'name':request.user.first_name, 'music_url': music_url})
                # send thankyou email to user
                email = EmailMessage(
                    # email subject title default is 'subject'
                    'Thank you! -- ありがとうございます！',
                    # email template default is 'body'
                    template,
                    settings.EMAIL_HOST_USER,
                    # recipient list
                    [request.user.email],
                )
                email.fail_silently=False
                # only send email if this flag is true
                if EMAIL_ON:
                    email.send()            

                # finally send response back to client      
                return Response(status=status.HTTP_200_OK)

            except Exception as e:

                logger.exception("Failed to post stripe charge or send thankyou email to user")

                error_message = "The server failed to deliver the content requested. We apologize for the inconvenince and we are working diligently to fix this."
                response_data = {
                    "error": error_message
                }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST) 



        # multiple purchased files download. Return zip
        else:

            # processing paid flps and tracks together
            try:

                purchasedTracksList = []
                purchasedFlpList = []
                queriedTrackObjs = None
                queriedFlpObjs = None

                # check if there are any flp_items
                if len(order_dict.get('flp_items', [])) > 0:

                    for item in order_dict.get('flp_items', []):
                        flp_id = item.get('flp')
                        current_flp = Flp.objects.get(pk=flp_id)
                        current_flp.downloads += 1
                        purchasedFlpList.append(current_flp.pk)
                        current_flp.save()  
                    
                    queriedFlpObjs = Flp.objects.filter(pk__in=purchasedFlpList)

                # check if there are any track_items
                if len(order_dict.get('track_items', [])) > 0:

                    for item in order_dict.get('track_items', []):
                        track_id = item.get('track')
                        current_track = Track.objects.get(pk=track_id)
                        current_track.downloads += 1
                        purchasedTracksList.append(current_track.pk)
                        current_track.save()  

                    queriedTrackObjs = Track.objects.filter(pk__in=purchasedTracksList)

                try:

                    tracksAndFlpsForZip = []

                    if queriedTrackObjs is not None:
                        for item in queriedTrackObjs:
                            # gets the absolute path
                            tracksAndFlpsForZip.append(item.track.path)
                    
                    if queriedFlpObjs is not None:
                        for item in queriedFlpObjs:
                            # gets the absolute path
                            tracksAndFlpsForZip.append(item.flp_zip.path)
                
                    # if this was a single wav purchase 

                    zip = createZip(tracksAndFlpsForZip)

                    # open this zip file as byte data and setting the byte data to variable for delivering to client via http
                    with open(zip, 'rb') as f:
                        file_data = f.read()

                    print('zip file: ' + str(zip) + '\n')
                    print('file_data type: ' + str(type(file_data)) + '\n')
                    response = HttpResponse(file_data, content_type='application/zip')
                    response['Content-Disposition'] = 'attachment; filename=sheriff_crandy_downloadables.zip'
                                            
                    os.remove(zip)

                    charge = createStripeCharge(TOTAL_USD_PAID, TOTAL_JPY_PAID, isUsd, request.data.get('stripe_token'), request.data.get('email'), request.data.get('name'))

                    # save order
                    paid_download_order = Order.objects.create(
                        user=request.user, 
                        name=request.data.get('name'),
                        email=request.data.get('email'),
                        # phone=request.data.get('phone'),
                        address1=request.data.get('address1'),
                        address2=request.data.get('address2'),
                        statePref=request.data.get('statePref'),
                        country=request.data.get('country'),
                        zipcode=request.data.get('zipcode'),
                        stripe_token=request.data.get('stripe_token'),
                        usd_paid_amount=TOTAL_USD_PAID, 
                        jpy_paid_amount=TOTAL_JPY_PAID, 
                        free_download=False)
                    if queriedFlpObjs is not None:
                        paid_download_order.flp.set(queriedFlpObjs)

                    if queriedTrackObjs is not None:
                        paid_download_order.track.set(queriedTrackObjs)

                        
                    paid_download_order.save()

                    music_url = f'{FRONTEND_DOMAIN}/music'
                    template = render_to_string('../templates/thankyou.html', {'name':request.user.first_name, 'music_url': music_url})
                    # send thankyou email to user
                    email = EmailMessage(
                        # email subject title default is 'subject'
                        'Thank you! -- ありがとうございます！',
                        # email template default is 'body'
                        template,
                        settings.EMAIL_HOST_USER,
                        # recipient list
                        [request.user.email],
                    )
                    email.fail_silently=False
                    # only send email if this flag is true
                    if EMAIL_ON:
                        email.send()            

                    # finally send response back to client      
                    return response
                except Exception as e:
                    logger.exception("In checkout multiple paid tracks and flps block. Failed to zip up and return a multiple paid tracks and flps to frontend")

                    error_message = "The server failed to deliver the content requested. We apologize for the inconvenince and we are working diligently to fix this."
                    response_data = {
                        "error": error_message
                    }
                    return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:

                logger.exception("Failed to post stripe charge or send thankyou email to user")

                error_message = "The server failed to deliver the content requested. We apologize for the inconvenince and we are working diligently to fix this."
                response_data = {
                    "error": error_message
                }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST) 


# returns a single .wav file from the 
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def trackCheckout(request, id, isfree):

    # get the track object to update its download count
    track = Track.objects.get(pk=id)
    track.downloads += 1
    track.save()

    # single free download
    if isfree == 'true':

        free_download_order = Order.objects.create(user=request.user, free_download=True)
        free_download_order.track.set([track])  # Wrap track in a list        
        free_download_order.save()

        return Response(status=status.HTTP_200_OK)

    # single track purchase
    else:

        # bool to check if this is a US or Japan payment
        isUsd = None
        # get the amounts paid in the proper formats
        TOTAL_USD_PAID = float(str(request.data.pop('usd_paid_amount')).strip(' "'))
        TOTAL_JPY_PAID = int(str(request.data.pop('jpy_paid_amount')).strip(' "'))
        
        response = None
        # check if this is a usd or jpy purchase
        # if TOTAL_JPY_PAID > 1 and TOTAL_USD_PAID == 0.0:
        #     isUsd = False
        # else:
        #     isUsd = True
        isUsd = False if TOTAL_JPY_PAID > TOTAL_USD_PAID else True

        # processing single track paid or free
        try:

            charge = createStripeCharge(TOTAL_USD_PAID, TOTAL_JPY_PAID, isUsd, request.data.get('stripe_token'), request.data.get('email'), request.data.get('name'))

            # save order
            paid_download_order = Order.objects.create(
                user=request.user, 
                name=request.data.get('name'),
                email=request.data.get('email'),
                # phone=request.data.get('phone'),
                address1=request.data.get('address1'),
                address2=request.data.get('address2'),
                statePref=request.data.get('statePref'),
                country=request.data.get('country'),
                zipcode=request.data.get('zipcode'),
                stripe_token=request.data.get('stripe_token'),
                usd_paid_amount=TOTAL_USD_PAID, 
                jpy_paid_amount=TOTAL_JPY_PAID, 
                free_download=False)
            paid_download_order.track.set([track])      
            paid_download_order.save()


            music_url = f'{FRONTEND_DOMAIN}/music'
            template = render_to_string('../templates/thankyou.html', {'name':request.user.first_name, 'music_url': music_url})
            # send thankyou email to user
            email = EmailMessage(
                # email subject title default is 'subject'
                'Thank you! -- ありがとうございます！',
                # email template default is 'body'
                template,
                settings.EMAIL_HOST_USER,
                # recipient list
                [request.user.email],
            )
            email.fail_silently=False
            # only send email if this flag is true
            if EMAIL_ON:
                email.send()            

            # finally send response back to client      
            return Response(status=status.HTTP_200_OK)

        except Exception as e:

            logger.exception("Failed to post stripe charge or send thankyou email to user")

            error_message = "The server failed to deliver the content requested. We apologize for the inconvenince and we are working diligently to fix this."
            response_data = {
                "error": error_message
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST) 


# returns a single FLP .zip file
@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def flpCheckout(request, id, isfree):


    # get the track object to update its download count
    flp = Flp.objects.get(pk=id)
    flp.downloads += 1
    flp.save()

    # single free download
    if isfree == 'true':

        free_download_order = Order.objects.create(user=request.user, free_download=True)
        free_download_order.flp.set([flp])  # Wrap track in a list        
        free_download_order.save()

        return Response(status=status.HTTP_200_OK)
    
    else:

        # bool to check if this is a US or Japan payment
        isUsd = None
        # get the amounts paid in the proper formats
        TOTAL_USD_PAID = float(str(request.data.pop('usd_paid_amount')).strip(' "'))
        TOTAL_JPY_PAID = int(str(request.data.pop('jpy_paid_amount')).strip(' "'))
        
        response = None
        # check if this is a usd or jpy purchase
        # if TOTAL_JPY_PAID > 1 and TOTAL_USD_PAID == 0.0:
        #     isUsd = False
        # else:
        #     isUsd = True
        isUsd = False if TOTAL_JPY_PAID > TOTAL_USD_PAID else True

        # processing single track paid or free
        try:

            charge = createStripeCharge(TOTAL_USD_PAID, TOTAL_JPY_PAID, isUsd, request.data.get('stripe_token'), request.data.get('email'), request.data.get('name'))

            # save order
            paid_download_order = Order.objects.create(
                user=request.user, 
                name=request.data.get('name'),
                email=request.data.get('email'),
                # phone=request.data.get('phone'),
                address1=request.data.get('address1'),
                address2=request.data.get('address2'),
                statePref=request.data.get('statePref'),
                country=request.data.get('country'),
                zipcode=request.data.get('zipcode'),
                stripe_token=request.data.get('stripe_token'),
                usd_paid_amount=TOTAL_USD_PAID, 
                jpy_paid_amount=TOTAL_JPY_PAID, 
                free_download=False)
            paid_download_order.flp.set([flp])      
            paid_download_order.save()


            music_url = f'{FRONTEND_DOMAIN}/music'
            template = render_to_string('../templates/thankyou.html', {'name':request.user.first_name, 'music_url': music_url})
            # send thankyou email to user
            email = EmailMessage(
                # email subject title default is 'subject'
                'Thank you! -- ありがとうございます！',
                # email template default is 'body'
                template,
                settings.EMAIL_HOST_USER,
                # recipient list
                [request.user.email],
            )
            email.fail_silently=False
            # only send email if this flag is true
            if EMAIL_ON:
                email.send()            

            # finally send response back to client      
            return Response(status=status.HTTP_200_OK)

        except Exception as e:

            logger.exception("Failed to post stripe charge or send thankyou email to user")

            error_message = "The server failed to deliver the content requested. We apologize for the inconvenince and we are working diligently to fix this."
            response_data = {
                "error": error_message
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)             


# utility method to process stripe charges
def createStripeCharge(total_usd_paid, total_jpy_paid, isUsd, stripe_token, customer_email, customer_name):
    
    stripe.api_key = settings.STRIPE_SK
    charge = stripe.Charge.create(
        # if it's usd, stripe takes amount in cents, otherwise leave it whole number for JPY
        amount = int(total_usd_paid * 100) if isUsd is True else total_jpy_paid,
        # usd or jpy
        currency= 'USD' if isUsd is True else 'JPY',
        description='Sheriff Crandy flp/audio file digital download charge',
        # stripe token we get from frontend
        source = stripe_token,
        receipt_email=customer_email,
        metadata= {'customer_name': customer_name}
    )
    
    return charge


# get user track orders to unlock full song
# pass in the user, get a list of tracks that they bought
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_track_orders(request):
    
    # get the orders for this user
    orders = Order.objects.filter(user=request.user)
    # get the track IDs while avoiding duplicates
    track_items = orders.values_list('track', flat=True).distinct()

    # Retrieve the tracks using the track item IDs
    tracks = Track.objects.filter(id__in=track_items)

    if not tracks: # check if queryset is empty

        response = Response([])
        # prevent vuejs from caching cart data
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Expires'] = '0'
        return response
    
    # convert these objects into a JSON obj for frontend. Pass in tracks and set many=True because we may have more than one obj
    serializer = GetPurchasedTrackSerializer(tracks, many=True)
    response = Response(serializer.data)
    # added this to prevent vuejs from caching cart data
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    return response
