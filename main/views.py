from rest_framework.response import Response
from unittest                import result
from django.shortcuts 		 import render
from django.http 			 import HttpResponse ,JsonResponse
from rest_framework 		 import status
from rest_framework.views  	 import APIView
from .serializers 			 import Itemserializer ,UserRegistrationSerializer  , UserLoginSerializer

from .models 	  			 import  User, UserProfile ,BikeDetails ,TypesBikes ,Accessories
# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView


from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view #permission_classes
# from django.contrib.auth import logout



@api_view(['GET'])
def HomePage( request ):
	#data = Items.objects.all()
	# return HttpResponse(data)
	#return Response( serialdata.data , safe= False )
	#return HttpResponse("welcome to my Home page")
	# url = ""
	# req = requests.get(url)
	context = {
	}
	return render(request , 'main/index.html', context )



# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def User_logout(request):
#     request.user.auth_token.delete()
#     logout(request)
#     return Response('User Logged out successfully')




class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)



class UserLoginView( APIView ): # RetrieveAPIView
    
    

        # return Response({'error':'no such thing'},status=status.HTTP_204_NO_CONTENT)
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        # email = request.data['email']
        # queryset = User.objects.filter(email=email).first()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)	
    

class UserProfileView( APIView ): # RetrieveAPIView
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'age': user_profile.age,
                    'gender': user_profile.gender,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)



class ListItem( APIView ):
	def get( self , request ) :
		data = BikeDetails.objects.all()
		dataserial = Itemserializer(data , many=True)
		return Response(dataserial.data , status=status.HTTP_200_OK )

		#def post(self , request ) :







class CycleItemsViews( APIView ) :
	def post(self, request):
		serial = Itemserializer( data=request.data ) 
		if serial.is_valid():
			serial.save()
			return Response({"status": "success", "data": serial.data}, status=status.HTTP_200_OK)
		else:
			return Response({"status": "error", "data": serial.errors}, status=status.HTTP_400_BAD_REQUEST)


	def get( self, request , id=None ):
		if id:
			item = BikeDetails.objects.get(id=id)
			serializer = Itemserializer(item)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		items = BikeDetails.objects.all()
		serializer = Itemserializer(items, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)



