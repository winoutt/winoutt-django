# Library Import
from rest_framework import serializers, fields

# Model Imports
from .models import User, EndUser, Website, Setting, Connection, Note, PeopleUnfollow, GENDERS

# Utils Imports
import base64
from .utils import UserUtil, ConnectionUtil, PeopleUnfollowUtil
from django.core.files.base import ContentFile


# User Serailizers


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = "__all__"


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = "__all__"


class EndUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUser
        fields = (
            "end_user_id",
            "avatar",
            "avatar_original",
            "bio",
            "city",
            "country",
            "created_at",
            "date_of_birth",
            "deleted_at",
            "gender",
            "title",
            "session_at",
            "is_online",
            "updated_at",
            "is_connected",
            "is_received",
            "is_requested",
            "is_unfollowed",
            "is_user",
            "mutual_connections_count",
            "stars_count",
        )

    avatar = serializers.SerializerMethodField("get_avatar_url")
    avatar_original = serializers.SerializerMethodField("get_avatar_original_url")
    
    is_connected = serializers.SerializerMethodField("get_is_connected")
    is_received = serializers.SerializerMethodField("get_is_received")
    is_requested = serializers.SerializerMethodField("get_is_requested")
    is_unfollowed = serializers.SerializerMethodField("get_is_unfollowed")
    is_user = serializers.SerializerMethodField("get_is_user")
    mutual_connections_count = serializers.SerializerMethodField(
        "get_mutual_connections_count"
    )
    stars_count = serializers.SerializerMethodField("get_stars_count")
    gender = serializers.SerializerMethodField("get_gender")


    def get_gender(self, obj):
        if obj.gender is None:
            return None
        return dict(GENDERS)[obj.gender]

    def get_avatar_url(self, obj):
        return obj.avatar.name

    def get_avatar_original_url(self, obj):
        return obj.avatar_original.name

    def get_is_connected(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        try:
            connection = ConnectionUtil.check_connection_exist(obj.user, request.user)
            return connection.first().accepted_at is not None
        except Exception as error:
            return False

    def get_is_received(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        return ConnectionUtil.is_pending_connection(obj.user, request.user)


    def get_is_requested(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        return ConnectionUtil.is_pending_connection(request.user, obj.user)
        

    def get_is_unfollowed(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False
        return PeopleUnfollowUtil.is_user_unfollowed(request.user, obj.user)

    def get_is_user(self, obj):
        if self.context.get("request", None) is None:
            return False
        return self.context["request"].user == obj.user

    def get_mutual_connections_count(self, obj):
        if self.context.get("request", None) is None:
            return False
        return ConnectionUtil.get_mutual_paginator(self.context["request"].user, obj.user.id).count()

    def get_stars_count(self, obj):
        return 0


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "full_name",
        )
        extra_kwargs = {
            "password": {"write_only": True, "allow_null":False, "allow_blank":False},
            "email": {"required": True, "allow_null":False, "allow_blank":False},
            "username": {"required": False, "allow_null":False, "allow_blank":False},
        }

    full_name = serializers.CharField(write_only=True, required=True)

    def __init__(self, *args, **kwargs):
        super(CreateUserSerializer, self).__init__(*args, **kwargs)
        self.fields["email"].error_messages["required"] = "Email is required."  # set the custom error message
        self.fields["email"].error_messages["blank"] = "Email cannot be empty."  # set the custom error message
        self.fields["password"].error_messages["required"] = "Password is required."  # set the custom error message
        self.fields["password"].error_messages["blank"] = "Password cannot empty."  # set the custom error message
        self.fields["full_name"].error_messages["required"] = "Full Name is required."  # set the custom error message
        self.fields["full_name"].error_messages["blank"] = "Full Name cannot be empty."  # set the custom error message


    def validate(self, data):
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("This email already exists.")
        if len(data["password"]) < 8:
            raise serializers.ValidationError(
                "Password must be atleast 8 characters long."
            )
        if UserUtil.is_valid_username(data["full_name"].replace(" ", "")) == False:
            raise serializers.ValidationError(
                "Full name can only be composed of alphabets, numerics, dashes and underscrores."
            )
        if len(data["full_name"].split()) < 2:
            raise serializers.ValidationError("Please enter your full name.")
        return data

    def create(self, validated_data):
        full_name = validated_data.pop("full_name")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        first_name, last_name = UserUtil.split_full_name(full_name)
        username = UserUtil.generate_username(full_name)

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save()
        end_user = EndUser.objects.create(user=user)
        website = Website.objects.create(user=user)
        setting = Setting.objects.create(user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_active",
            "first_name",
            "last_name",
            "full_name",
            "connections_count",
            "posts_count",
            "settings",
            "website",
            "end_user",
        )

    end_user = serializers.SerializerMethodField("get_end_user")

    full_name = serializers.SerializerMethodField("get_full_name")

    connections_count = serializers.SerializerMethodField("get_connections_count")
    posts_count = serializers.SerializerMethodField("get_posts_count")

    settings = serializers.SerializerMethodField("get_settings")
    website = serializers.SerializerMethodField("get_website")

    def get_full_name(self, obj):
        return obj.first_name + " " + obj.last_name

    def get_connections_count(self, obj):
        requested_accepted_connection = (
            UserUtil.get_requested_accepted_connections_count(obj.id)
        )
        received_accepted_connection = UserUtil.get_received_accepted_connections_count(
            obj.id
        )
        return requested_accepted_connection + received_accepted_connection

    def get_posts_count(self, obj):
        return UserUtil.get_posts_count(obj.id)

    def get_settings(self, obj):
        setting = UserUtil.get_settings(obj.id)
        if setting is None:
            return None
        return SettingSerializer(setting).data

    def get_website(self, obj):
        website = UserUtil.get_website(obj.id)
        if website is None:
            return None
        return WebsiteSerializer(website).data

    def get_end_user(self, obj):
        end_user = UserUtil.get_end_user(obj.id)
        if end_user is None:
            return None
        return EndUserSerializer(end_user, context={'request': self.context.get("request", None) }).data


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "bio",
            "date_of_birth",
            "gender",
            "city",
            "country",
            "title",
            # "avatar",
            "website_personal",
            "website_company",
            'base64_image'
        )
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            # "avatar": {"required": False},
        }

    full_name = serializers.CharField(write_only=True, required=True)
    title = serializers.CharField(write_only=True, required=True)
    bio = serializers.CharField(write_only=True, required=True)
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    country = serializers.CharField(required=True)

    base64_image = serializers.CharField(required=False)

    website_personal = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    website_company = serializers.URLField(required=False, allow_blank=True, allow_null=True)

    # avatar = serializers.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(EditUserSerializer, self).__init__(*args, **kwargs)
        self.fields["email"].error_messages["required"] = "Email is required."  # set the custom error message
        self.fields["username"].error_messages["required"] = "Username is required."  # set the custom error message
        self.fields["first_name"].error_messages["required"] = "First Name is required."  # set the custom error message
        self.fields["last_name"].error_messages["required"] = "Last Name is required."  # set the custom error message
        self.fields["bio"].error_messages["required"] = "Bio is required."  # set the custom error message
        self.fields["bio"].error_messages["required"] = "Bio is required."  # set the custom error message
        self.fields["date_of_birth"].error_messages["required"] = "Date of Birth is required."  # set the custom error message
        self.fields["gender"].error_messages["required"] = "Gender is required."  # set the custom error message
        self.fields["city"].error_messages["required"] = "City is required."  # set the custom error message
        self.fields["country"].error_messages["required"] = "Country is required."  # set the custom error message
        self.fields["title"].error_messages["required"] = "Define Yourself is required."  # set the custom error message

    def validate(self, data):
        if len(data["full_name"].split()) < 2:
            raise serializers.ValidationError("Please enter your full name.")
        if len(data["bio"]) > 2500:
            raise serializers.ValidationError("Bio can only be 2500 characters long.")
        if not UserUtil.is_valid_gender(data["gender"]):
            raise serializers.ValidationError("Provide valid gender value.")
        return data

    def update(self, user, validated_data):
        user.username = validated_data.get("username", user.username)
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)
        user.email = validated_data.get("email", user.email)
        user.save()

        # Update EndUser
        end_user = UserUtil.get_end_user(user)
        end_user.bio = validated_data.get("bio", end_user.bio)
        end_user.date_of_birth = validated_data.get(
            "date_of_birth", end_user.date_of_birth
        )
        end_user.gender = UserUtil.get_gender_value(
            validated_data.get("gender", end_user.gender)
        )
        end_user.city = validated_data.get("city", end_user.city)
        end_user.country = validated_data.get("country", end_user.country)
        end_user.title = validated_data.get("title", end_user.title)
        # end_user.avatar = validated_data.get("avatar", end_user.avatar)
        if end_user.avatar != validated_data.get("base64_image", end_user.avatar):
            format, imgstr = validated_data.get("base64_image").split(';base64,') 
            ext = format.split('/')[-1] 
            data = ContentFile(base64.b64decode(imgstr), name='avatar.' + ext)
            end_user.avatar = data
            end_user.avatar_original = data
        end_user.save()

        # Update Website
        website = UserUtil.get_website(user)
        website.personal = validated_data.get("website_personal", website.personal)
        website.company = validated_data.get("website_company", website.company)
        website.save()

        return user


# Connection Serializers


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ConnectionSerializer, self).__init__(*args, **kwargs)
        self.fields["user_connection"].error_messages[
            "does_not_exist"
        ] = "Unable to send connection request"  # set the custom error message

    def validate(self, data):
        if data["user"] == data["user_connection"]:
            raise serializers.ValidationError(
                "You can't send connect request to yourself."
            )
        if ConnectionUtil.is_already_connected(data["user"], data["user_connection"]):
            raise serializers.ValidationError("Already connected or sent request")
        return data

    def create(self, validated_data):
        return Connection.objects.create(**validated_data)


class ConnectionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            "username",
            "email",
            "is_active",
            "first_name",
            "last_name",
            "full_name",
            "connections_count",
            "posts_count",
            "settings",
            "website",
            "end_user",
            "pivot",
        )

    end_user = serializers.SerializerMethodField("get_end_user")
    id = serializers.SerializerMethodField("get_id")

    full_name = serializers.SerializerMethodField("get_full_name")

    connections_count = serializers.SerializerMethodField("get_connections_count")
    posts_count = serializers.SerializerMethodField("get_posts_count")

    settings = serializers.SerializerMethodField("get_settings")
    website = serializers.SerializerMethodField("get_website")

    pivot = serializers.SerializerMethodField("get_pivot")

    def get_full_name(self, obj):
        return obj.first_name + " " + obj.last_name

    def get_id(self, obj):
        return obj.id

    def get_connections_count(self, obj):
        requested_accepted_connection = (
            UserUtil.get_requested_accepted_connections_count(obj.id)
        )
        received_accepted_connection = UserUtil.get_received_accepted_connections_count(
            obj.id
        )
        return requested_accepted_connection + received_accepted_connection

    def get_posts_count(self, obj):
        return UserUtil.get_posts_count(obj.id)

    def get_settings(self, obj):
        setting = UserUtil.get_settings(obj.id)
        if setting is None:
            return None
        return SettingSerializer(setting).data

    def get_website(self, obj):
        website = UserUtil.get_website(obj.id)
        if website is None:
            return None
        return WebsiteSerializer(website).data

    def get_end_user(self, obj):
        end_user = UserUtil.get_end_user(obj.id)
        if end_user is None:
            return None
        return EndUserSerializer(end_user, context={'request': self.context.get("request", None)}).data

    def get_pivot(self, obj):
        connection = self.context["connection"]
        return ConnectionSerializer(connection).data


# Note Serializers


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

    def create(self, validated_data):
        return Note.objects.create(**validated_data)

    def update(self, note, validated_data):
        note.content = validated_data.get("content", note.content)
        note.user = validated_data.get("user", note.user)
        note.save()

        return note
