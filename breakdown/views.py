import json

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.db.utils import IntegrityError as DjangoIntegrityError
from django.http import JsonResponse

from rest_framework import viewsets, permissions, status, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from DB.db_manager import db
from .models import Survey, Course
from .serializers import UserSerializer, SurveySerializer, CourseSerializer


class UserView:
    class UserList(generics.ListAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer

    class UserDetail(generics.RetrieveAPIView):
        queryset = User.objects.all()
        serializer_class = UserSerializer

    class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all().order_by('-date_joined')
        serializer_class = UserSerializer

    @staticmethod
    @api_view(['POST', ])
    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((permissions.AllowAny,))
    def login(request):
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        username = body['username']
        password = body['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                django_login(request, user)
                res = db.check_credentials(username, password)
                if not res:
                    return Response("Wrong login or password", status=status.HTTP_400_BAD_REQUEST)
                token, created = Token.objects.get_or_create(user=user)
                res["token"] = token.key
                print(res, token)
                return JsonResponse(res, status=status.HTTP_200_OK)
            else:
                return Response("Inactive account", status=status.HTTP_410_GONE)
        else:
            return Response("Invalid login", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['GET', ])
    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((permissions.IsAuthenticated,))
    def logout(request):
        auth.logout(request)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(['POST', ])
    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((permissions.AllowAny,))
    def register(request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body['username']
        password = body['password']
        first_name = body['firstName']
        last_name = body['lastName']
        try:
            user = User.objects.create_user(username=username, password=password,
                                            email=username, first_name=first_name, last_name=last_name)
        except DjangoIntegrityError:
            return Response("User already exists", status=status.HTTP_405_METHOD_NOT_ALLOWED)
        django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        res = dict(zip(["id", "username"], [user.id, user.get_username()]))
        return JsonResponse(res, status=status.HTTP_200_OK, safe=False)

    @staticmethod
    @api_view(['GET', 'POST', ])
    @authentication_classes((SessionAuthentication, BasicAuthentication))
    @permission_classes((permissions.IsAuthenticatedOrReadOnly,))
    def account(request):
        return Response(status=status.HTTP_202_ACCEPTED)


class SurveyView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    class CourseList(generics.ListAPIView):
        queryset = Course.objects.all()
        serializer_class = CourseSerializer

    # TODO delete after integrating getting user
    @staticmethod
    @api_view(["GET", ])
    def get_list_of_surveys(request):
        surveys = db.get_surveys()
        serializer = SurveySerializer(surveys, many=True)
        # TODO remove data layer and
        res = {"data": serializer.data}
        return JsonResponse(res, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(["GET", ])
    def get_all_surveys(request, user_id):
        if db.is_instructor(user_id):
            surveys = db.get_ta_surveys(user_id)
            print(surveys)
            serializer = SurveySerializer(surveys, many=True)
            # TODO remove data layer and
            res = {"data": serializer.data}
            return JsonResponse(res, status=status.HTTP_200_OK)
        else:
            surveys = db.get_student_surveys(user_id)
            for x in surveys:
                print(x)
                polls = db.get_student_polls(user_id, x["survey_id"])[0]
                print("polls", polls)
                x.update(polls)
            return JsonResponse(surveys, status=status.HTTP_200_OK, safe=False)

    @staticmethod
    @api_view(['POST', ])
    def create_survey(request):
        print(request.body)

        body_unicode = request.body.decode("utf-8")
        print(body_unicode)
        body = json.loads(body_unicode)
        user_id = body["user_id"]
        del body["user_id"]
        try:
            survey_id = db.create_survey(user_id=user_id, survey_info=body)
            res = {"survey_id": survey_id}
            print(res)
            return JsonResponse(res, status=status.HTTP_200_OK)
        except AssertionError:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    @api_view(['GET', 'PUT', 'DELETE', ])
    def manage_survey(request, user_id=None, survey_id=None):
        if request.method == "GET":
            return SurveyView.get_survey(request._request, user_id, survey_id)
        elif request.method == "PUT":
            return SurveyView.update_survey(request._request, user_id, survey_id)
        elif request.method == "DELETE":
            return SurveyView.delete_survey(request._request, user_id, survey_id)
        else:
            return Response("Wrong method", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    @api_view(["GET", ])
    def get_survey(request, user_id, survey_id):
        if db.is_instructor(user_id):
            survey = db.get_survey_by_id(survey_id)
            serializer = SurveySerializer(survey, many=False)
            res = {"data": {**serializer.data, **{"survey_id": survey_id}}}
            return JsonResponse(res, status=status.HTTP_200_OK)
        else:
            survey = db.get_survey_by_id(survey_id)
            poll = db.get_student_polls(user_id, survey_id)[0]
            print(survey, poll)
            res = {**survey, **poll}
            return JsonResponse(res, status=status.HTTP_200_OK)

    @staticmethod
    @api_view(["PUT", ])
    def update_survey(request, user_id, survey_id):
        if db.is_instructor(user_id):
            body_unicode = request.body.decode("utf-8")
            body = json.loads(body_unicode)
            del body["user_id"]  # TODO add checking to having access
            db.update_survey(survey_id=survey_id, survey_info=body)
            return Response(status=status.HTTP_200_OK)
        else:
            body_unicode = request.body.decode("utf-8")
            body = json.loads(body_unicode)
            poll_id = db.get_student_polls(user_id, survey_id)[0]
            print(poll_id)
            poll_id = poll_id["poll_id"]
            db.modify_poll(user_id, poll_id, body)
            return Response(status=status.HTTP_200_OK)

    @staticmethod
    @api_view(["DELETE", ])
    def delete_survey(request, user_id, survey_id):
        if not db.is_instructor(user_id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        print(survey_id)
        db.delete_survey(survey_id)
        return Response(status=status.HTTP_200_OK)


class TeamView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @staticmethod
    @api_view(["GET", ])
    def form_teams(request, user_id, survey_id):  # TODO add method to DB_manager
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    @api_view(["GET", ])
    def get_all_teams(request, user_id, survey_id):
        res = db.get_all_teams(survey_id)
        print("teams", res)
        return JsonResponse(res, status=status.HTTP_200_OK, safe=False)

    @staticmethod
    @api_view(["GET", "PUT", "DELETE", ])
    def manage_team(request, user_id, survey_id, team_id):
        if request.method == "GET":
            return TeamView.get_team_by_id(request._request, user_id, survey_id, team_id)
        elif request.method == "PUT":
            return TeamView.update_team(request._request, user_id, survey_id, team_id)
        elif request.method == "DELETE":
            return TeamView.delete_team(request._request, user_id, survey_id, team_id)
        else:
            return Response("Wrong method", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @staticmethod
    @api_view(["GET", ])
    def get_team_by_id(request, user_id, survey_id, team_id):  # TODO: test with Yuriy
        res = db.get_team(team_id)
        return JsonResponse(res, status=status.HTTP_200_OK, safe=False)

    @staticmethod
    @api_view(["PUT", ])
    def update_team(request, user_id, survey_id, team_id):  # TODO: test with Yuriy
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)

        db.update_team(team_id=team_id, data=body)
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    @api_view(["DELETE", ])
    def delete_team(request, user_id, survey_id, team_id):  # TODO: test with Yuriy
        pass


survey_view = SurveyView()
team_view = TeamView()
user_view = UserView()
