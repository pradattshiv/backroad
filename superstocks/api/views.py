from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from superstocks.models import Retailer
from superstocks.api.serializers import RetailerSerializer
from superstocks.api.serializers import loginSerializer



@api_view(['GET', ])
def api_detail_retailer_view(request,Retailer_id):
    try:
        retailer = Retailer.objects.get(Retailer_id=Retailer_id)
        print('==================',retailer)
    except Retailer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = RetailerSerializer(retailer)
        return Response(serializer.data) 

@api_view(['POST', ])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes((IsAuthenticated,))
def login_view(request, format=None):
    if request.method == 'POST':
        print('XXXXXXXXXXXXXXXXXXXXXXx', request)
        d1 = request.data['email']
        d2 = request.data['password']
        print('this is request data from the views ', d1,"and password :", d2)
        # head = request.headers
        # print('this the head======', head)
        d3 = Retailer.objects.get(Retailer_id=d1)
        serializer = loginSerializer(d3)
        data = {}
        all_details = Retailer.objects.all()
        Retailer_email = [ss.Email for ss in all_details]
        Retailer_password =[ss.Password for ss in all_details]
        print(Retailer_email, Retailer_password)
        if d1 in Retailer_email:
            

        data['code'] = "200"
        data['status'] = "success"
        data['Retailer_details'] = serializer.data
        
        return Response(data)
