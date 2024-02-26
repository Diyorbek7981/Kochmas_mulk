from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *
from geopy.geocoders import Nominatim
from rest_framework.exceptions import ValidationError


class SearchSerializer(ModelSerializer):
    class Meta:
        model = SearchModel
        fields = '__all__'


class HomeListSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(
        source='owner.username')
    # avtor maydoni yaratib unga userni qiymatini beramiz get requestda ko'rib turish uchun

    me_like = serializers.SerializerMethodField('get_me_liked')  # like bosgan yoki yoqligini ko'rish uchun
    location_latlong = serializers.SerializerMethodField('get_location')
    user_phone_number = serializers.ReadOnlyField(source='owner.phone_number')

    class Meta:
        model = HomeModel
        fields = ['id', 'type', 'home_type', 'location', 'location_latlong', 'count_rooms', 'area', 'floor',
                  'building_floor', 'repair', 'building_material', 'price', 'description', 'comforts', 'author',
                  'owner', 'user_phone_number', 'created',
                  'updated', 'me_like']

    def get_me_liked(self, obj):
        # Request berayotgan user saytda ro'yhatdan o'tgan bolsa homeni likelarini ko'radi
        # va un shu userga tegishlimi yoki yo'qmi tekshiradi (true yoki false qaytaradi)
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                HomeLike.objects.get(home=obj, author=request.user)
                return True
            except HomeLike.DoesNotExist:
                return False

        return False

    @staticmethod
    def get_location(self):
        location1 = self.location
        geolocator = Nominatim(user_agent="address_geocoder")
        location1 = geolocator.geocode(location1)
        lat = location1.latitude
        long = location1.longitude
        location = [lat, long]

        return location


class HomeCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    # user mizni yashirib unga aktiv bo'lgan foydalanuvchini o'rnatish uchun
    author = serializers.ReadOnlyField(
        source='owner.username')

    class Meta:
        model = HomeModel
        fields = ['id', 'type', 'home_type', 'location', 'count_rooms', 'area', 'floor', 'building_floor', 'repair',
                  'building_material', 'price', 'description', 'comforts', 'author', 'owner', 'created',
                  'updated']

    def validate_location(self, location):
        location1 = location
        geolocator = Nominatim(user_agent="address_geocoder")
        location1 = geolocator.geocode(location1)
        if location1 is None:
            data = {
                'success': False,
                'message': "Joylashuv joyingizni to'g'ri kiriting"
            }
            raise ValidationError(data)
        return location


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
