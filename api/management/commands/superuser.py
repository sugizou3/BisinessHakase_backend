from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
# User = settings.AUTH_USER_MODEL
# User = User(User)



class Command(BaseCommand):
    def handle(self,*args,**options):
        if not User.objects.filter(email=settings.SUPERUSER_EMAIL).exists():
            User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD,
            )
            print("スーパーユーザー作成")
        else:
            print("すでに作成済み")



# class Command(BaseCommand):  # Django標準のcreatesuperuserコマンドを継承

#     def handle(self, *args, **options):  # コマンド実行時のメイン処理
#         options.setdefault('interactive', False)
#         email=settings.SUPERUSER_EMAIL,
#         password=settings.SUPERUSER_PASSWORD,
#         database = options.get('database')

#         user_data = {
#             'email': email,
#             'password': password,
#         }

#         # 既に同じユーザー名のユーザーが存在するか確認。なければユーザー作成
#         exists = self.UserModel._default_manager.db_manager(database).filter(email=email).exists()
#         if not exists:
#             self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)