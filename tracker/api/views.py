from rest_framework.views import APIView
from rest_framework import permissions,authentication
from rest_framework.response import Response
from rest_framework import generics,status
from ..models import User,Admin,Application,Customer,Level
from .serializers import UserSerializer,ApplicationSerializer,CustomerSerializer,LevelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings



class CustomerRegisterView(generics.GenericAPIView):

    serializer_class=CustomerSerializer
    def post(self,request):
        data=request.data
        serializer=self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data=serializer.data
        user=User.objects.get(phone_no=user_data['user']['phone_no'])
        
        token=RefreshToken.for_user(user)
        login_data= {'refresh': str(token),
        'access': str(token.access_token),
            }
        
        return Response({**user_data,**login_data},status=status.HTTP_201_CREATED)


    
class LoginView(APIView):
    
    permission_classes= []
    authentication_classes= []

    def post(self, request, *args, **kwargs):
        phone_no= request.data.get('phone_no')
        password= request.data.get('password')
        obj= User.objects.get(phone_no= phone_no)
     
        
        if obj.check_password(password):
            user = obj
            token=RefreshToken.for_user(user).access_token
        
            return Response({
                                # "id": user.id,
                                    "token": str(token),
                                    "user": UserSerializer(user).data,
                                    # "regNum": user.customer.regNum,
                                    # "is_admin": user.customer.is_admin                                          
                                    }, status=201)
        else:
              

            return Response({"error": "Invalid phone_no or password"}, status=401)
       
class CreateApplication(CreateAPIView):

    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class=ApplicationSerializer
 
    permission_classes= [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
       


class Approve(APIView):
    permission_classes= [IsAuthenticated]

    def post(self, request):
        user=request.user
        if Admin.objects.get(user=user):
            app=Application.objects.get(id=request.data.get('id'))
            applevel=app.level
            current_level=Level.objects.get(id=applevel.id)
            level_num=current_level.stage.split(' ')[1]
            
            

            if int(level_num)==1:
                reg_num=f"NG/{app.site_LGA}/00{app.id}"
             
                # customer=Customer.objects.get(user=user)
                app.reg_num=reg_num
                app.save()
           
            elif int(level_num)==8:
                file=request.FILES['C_of_O']
                app.C_of_O=file
                app.save()



            current_level.status=True
            current_level.current_level=False
            current_level.updated_needed=False
            current_level.save()
            new_level=Level.objects.create(stage=f'stage {int(level_num)+1}',current_level=True)
            
            app.level=new_level
            app.save()
            return Response(ApplicationSerializer(app).data)


        else:
           return Response({"error": "Unauthorized"}, status=403)


    # decode_token= jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])

    
class Decline(APIView):
    permission_classes= [IsAuthenticated]
    def post(self, request):
        user=request.user
        id=request.data.get('id',None)
        feedback=request.data.get('feedback',None)
        if not id:
                return Response({"error": "Provide ID"}, status=400)
        if not feedback:
                return Response({"error": "Provide feedback"}, status=400)

        if hasattr(user,'admin'):     
            app=Application.objects.get(id=request.data.get('id'))
            app_level=app.level
           
            current_level=Level.objects.get(id=app_level.id,current_level=True)
           
            # level_num=current_level.stage.split(' ')[1]
            # prev=Level.objects.get(stages=f'stage {int(level_num)-1}')
            # current_level.current_level=False
            current_level.status=False
            current_level.feedback=request.data.get('feedback')
            current_level.updated_needed=True
            current_level.save()
            
            # prev.current_level=True
            app.level=current_level
            app.save()
          
            
            return Response(ApplicationSerializer(app).data)
           


        else:
           return Response({"error": "Unauthorized"}, status=403)

class UserLandView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self,request):
        app=Application.objects.filter(user=request.user.customer)
        app_parse=ApplicationSerializer(app,many=True).data
        return Response(app_parse)

class AdminLandView(APIView):
    permission_classes= [IsAuthenticated]
    def get(self,request):
        Application_list=[]
        admin_stages=Admin.objects.get(user=request.user).role["stages"]
        split_stages=admin_stages.split(',')
        

        

        for i in admin_stages.split(','):
            app_queryset=Application.objects.filter(level__stage=f'stage {i}', level__current_level=True).exclude(level__status=True,level__updated_needed=True)
          
        
            app=ApplicationSerializer(app_queryset,many=True)
            # print(app.data)
            new_dict={'stage':i,'application':[]}
            for j in app.data:
                
                new_dict['application'].append(j)

            Application_list.append(new_dict)
            # print(app.data.level)
         

        return Response(Application_list)


# new_list={'stage':app.data.level.stage,'application':app.data}
                
#             Application_list.append(**new_list)
         
