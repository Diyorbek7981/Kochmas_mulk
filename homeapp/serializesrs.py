from rest_framework import serializers, request
from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework.exceptions import ValidationError


class SearchSerializer(ModelSerializer):
    class Meta:
        model = SearchModel
        fields = '__all__'


class HomeSerializer(ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault())  # user mizni yashirib unga aktiv bo'lgan foydalanuvchini o'rnatish uchun
    author = serializers.ReadOnlyField(
        source='owner.username')  # avtor maydoni yaratib unga userni qiymatini beramiz get requestda ko'rib turish uchun

    me_like = serializers.SerializerMethodField('get_me_liked')  # like bosgan yoki yoqligini ko'rish uchun

    class Meta:
        model = HomeModel
        fields = ['id', 'type', 'home_type', 'location', 'count_rooms', 'area', 'floor', 'building_floor', 'repair',
                  'building_material', 'price', 'description', 'comforts', 'author', 'owner', 'created',
                  'updated', 'me_like']

    def get_me_liked(self, obj):
        # Request berayotgan user saytda ro'yhatdan o'tgan bolsa homeni likelarini ko'radi
        # va un shu userga tegishlimi yoki yo'qmi tekshiradi (true yoki false qaytaradi)
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                like = HomeLike.objects.get(home=obj, author=request.user)
                return True
            except HomeLike.DoesNotExist:
                return False

        return False


class PictureSerializer(ModelSerializer):
    pic = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=[
        'jpg', 'jpeg', 'png', 'heic', 'heif'
    ])])

    class Meta:
        model = PictureModel
        fields = ['pic', 'home', 'created', 'updated']


class TypeSerializer(ModelSerializer):
    class Meta:
        model = TypeModel
        fields = ['name', 'created', 'updated']


class HomeTypeSerializer(ModelSerializer):
    class Meta:
        model = HomeTypeModel
        fields = ['name', 'created', 'updated']


class ConforTypeSerializer(ModelSerializer):
    class Meta:
        model = ComforsTypeModel
        fields = ['name', 'created', 'updated']


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Users
        fields = ('id', 'username', 'photo')
        ref_name = 'hi'
        # shunga o'xshash serializer yana boshqa joyda bo'lsa ref_name qo'yiladi


class HomeLikeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = HomeLike
        fields = ("id", "author", "home")
