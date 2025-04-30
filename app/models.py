from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField  # PostgreSQLの場合


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lifted_account_number = models.BooleanField(default=False, verbose_name="アカウント数制限解除(16)")
    gmail_account = models.EmailField(null=True, blank=True, verbose_name="Gmailアドレス")
    gmail_account_password = models.CharField(max_length=30, blank=True, null=True, verbose_name="Gmailアプリパスワード")
    user_email = models.EmailField(null=True, blank=True, verbose_name="受信用メールアドレス")
    h_schedule_time = ArrayField(models.CharField(max_length=15), blank=True, null=True, verbose_name="ハッピー予約時間") 
    p_schedule_time = ArrayField(models.CharField(max_length=15), blank=True, null=True, verbose_name="PCMAX予約時間") 
    registration_subscribe_date = models.DateField(verbose_name="課金日", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="ハッピー再投稿、足跡返し")
    check_mail = models.BooleanField(default=False, verbose_name="新着チェック")

    def save_model(self, request, obj, form, change):
      if not obj.user_id:  # user フィールドが未設定の場合
          obj.user = request.user  # 管理者自身を設定
      super().save_model(request, obj, form, change)
      
    class Meta:
      managed = True
      verbose_name = "ユーザーオプション"
      verbose_name_plural = "ユーザーオプション"

    def __str__(self):
        return self.user.username

class Happymail(models.Model):
  age_list = [
    ("ナイショ","ナイショ"),
    ("18～19歳", "18～19歳"), 
    ("20代前半", "20代前半"),
    ("20代半ば","20代半ば"), 
    ("20代後半", "20代後半"), 
  ]
  activity_area_list = [
    ("東京都", "東京都")
    # "神奈川県", "埼玉県", "千葉県"
    ]
  blood_type_list = [
    ("指定しない","指定しない"), ("Ａ型","Ａ型"), 
    ("Ｂ型","Ｂ型"), ("Ｏ型","Ｏ型"), ( "ＡＢ型", "ＡＢ型"), 
    ("わからない","わからない"), ("ナイショ","ナイショ")
    ]
  height_list = [
    ("150～154","150～154"), ("155～159","155～159"), 
    ("160～164","160～164"), ("165～169","165～169"), ("ナイショ", "ナイショ")
  ]
  intention_to_marry_list =[
    ("すぐにでもしたい","すぐにでもしたい"), ("2～3年のうちに","2～3年のうちに"), 
    ("良い人がいればしたい","良い人がいればしたい"), ("わからない","わからない"), 
  ]
  sake_list = [
    ("たしなむ程度","たしなむ程度"), ("飲まない","飲まない"), ("ときどき飲む","ときどき飲む"), ("ナイショ","ナイショ"),
      ]
  car_ownership_list = [("ない", "ない"), ("ナイショ", "ナイショ")]
  brothers_and_sisters_list = [("長女", "長女"), ("間っ子", "間っ子"), ("末っ子", "末っ子"), ("一人っ子", "一人っ子"),  ("その他", "その他"), ]
  until_we_met_list = [("まずは会いたい", "まずは会いたい"), ("気が合えば会いたい", "気が合えば会いたい"), ]
  date_expenses_list = [("男性が全て払う", "男性が全て払う"), ("男性が多めに払う", "男性が多めに払う"), ("割り勘", "割り勘"), ("持っている人が払う", "持っている人が払う"),  ("相手と相談して決める", "相手と相談して決める"), ]
  
  
  id = models.BigAutoField(primary_key=True)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=30, blank=True, null=True, verbose_name="名前")
  login_id = models.CharField(max_length=30, blank=True, null=True, verbose_name="ログインID")
  password = models.CharField(max_length=30, blank=True, null=True, verbose_name="パスワード")
  fst_message = models.TextField(blank=True, null=True, verbose_name="1stメール")
  return_foot_message = models.TextField(blank=True, null=True, verbose_name="足跡返し")
  conditions_message = models.TextField(blank=True, null=True, verbose_name="2stメール")
  post_title = models.CharField(max_length=30,blank=True, null=True, verbose_name="掲示板タイトル")
  post_contents = models.TextField(blank=True, null=True, verbose_name="掲示板内容文")
  is_active = models.BooleanField(default=True, verbose_name="アクティブ")
  chara_image = models.ImageField(upload_to='chara_images/', null=True, blank=True, verbose_name="送付画像")
  fst_message = models.TextField(blank=True, null=True, verbose_name="1stメール")
  second_message = models.TextField(blank=True, null=True, verbose_name="2stメール")
  age = models.CharField(max_length=6, choices=age_list, blank=True, null=True, verbose_name="年齢")
  activity_area = models.CharField(max_length=5, choices=activity_area_list, null=True, blank=True, verbose_name="居住地")
  detail_activity_area = models.CharField(max_length=10, blank=True, null=True, verbose_name="詳細エリア")
  birth_place  = models.CharField(max_length=10, blank=True, null=True, verbose_name="出身地")
  blood_type = models.CharField(max_length=5, choices=blood_type_list, null=True, blank=True, verbose_name="血液型")
  constellation = models.CharField(max_length=6,  null=True, blank=True, verbose_name="星座")
  height = models.CharField(max_length=10,  choices=height_list, null=True, blank=True, verbose_name="身長")
  style = models.CharField(max_length=10,  null=True, blank=True, verbose_name="スタイル")
  looks = models.CharField(max_length=10,  null=True, blank=True, verbose_name="ルックス")
  cup = models.CharField(max_length=10,  null=True, blank=True, verbose_name="カップ")
  job = models.CharField(max_length=25,  null=True, blank=True, verbose_name="職業")
  education  = models.CharField(max_length=25,  null=True, blank=True, verbose_name="学歴")
  holiday = models.CharField(max_length=20,  null=True, blank=True, verbose_name="休日")
  relationship_status = models.CharField(max_length=20,  null=True, blank=True, verbose_name="交際ステータス")
  having_children = models.CharField(max_length=10,  null=True, blank=True, verbose_name="子ども")
  intention_to_marry = models.CharField(max_length=20, choices=intention_to_marry_list, null=True, blank=True, verbose_name="結婚に対する意思")
  smoking = models.CharField(max_length=20, null=True, blank=True, verbose_name="たばこ")
  sake = models.CharField(max_length=20, choices=sake_list, null=True, blank=True, verbose_name="お酒")
  car_ownership = models.CharField(max_length=20, choices=car_ownership_list, null=True, blank=True, verbose_name="クルマ")
  roommate = models.CharField(max_length=20,  null=True, blank=True, verbose_name="同居人")
  brothers_and_sisters = models.CharField(max_length=20, choices=brothers_and_sisters_list, null=True, blank=True, verbose_name="兄弟姉妹")
  until_we_met = models.CharField(max_length=20, choices=until_we_met_list, null=True, blank=True, verbose_name="出会うまでの希望")
  date_expenses = models.CharField(max_length=20, choices=date_expenses_list, null=True, blank=True, verbose_name="初回デート費用")
  memo = models.CharField(max_length=30,blank=True, null=True, verbose_name="メモ")

  def __str__(self):
    return self.name  # ここで表示したいフィールドを選択します

  class Meta:
    managed = True
    db_table = 'happymail'
    verbose_name = "ハッピーメール"
    verbose_name_plural = "ハッピーメール"

class Pcmax(models.Model):
  
  body_shape_list = [
    ("普通", "普通"),
    ("未設定","未設定"),
    ("スリム", "スリム"), 
    ("やや細め","やや細め"), 
    ("グラマー", "グラマー"), 
    ("ややぽっちゃり", "ややぽっちゃり"), 
    ("太め","太め"),
    ]
  blood_type_list = [("A","A"), ("B","B"), ("O","O"), ( "AB", "AB"), ("秘密","秘密")]
  activity_area_list = [
    ("東京都", "東京都")
    # "神奈川県", "埼玉県", "千葉県"
    ]
  detail_activity_area_tokyo = [
    ("千代田区","千代田区"), ( "中央区", "中央区"), ("港区","港区"), ( "新宿区", "新宿区"), ( "文京区", "文京区"),
    ("台東区","台東区"), ("品川区","品川区"), ( "目黒区", "目黒区"), ( "大田区", "大田区"), ( "世田谷区", "世田谷区"),
    ( "渋谷区", "渋谷区"), (  "中野区",  "中野区"), ( "杉並区" "杉並区"), ("豊島区","豊島区"), ( "北区", "北区"),
    ("荒川区","荒川区"), ( "板橋区", "板橋区"), ("練馬区","練馬区"), ("武蔵野市",  "武蔵野市"),   
  ]
  freetime_list = [
    ("不規則で決まってない","不規則で決まってない"), ("秘密","秘密"), ("平日の昼間","平日の昼間"), ("平日の夜","平日の夜")
      ]
  car_ownership_list = [
    ("ない", "ない"),("車がある", "車がある"),("バイクがある", "バイクがある"),("車とバイク両方ある", "車とバイク両方ある"),
    ]
  smoking_list = [
    ("未選択", "未選択"),("吸わない(喫煙は気にしない)", "吸わない(喫煙は気にしない)"),
    ("吸わない(喫煙は気になる)", "吸わない(喫煙は気になる)"),("吸わない(喫煙は許せない)", "吸わない(喫煙は許せない)"),
    ("吸わない(喫煙は気にしない)", "吸わない(喫煙は気にしない)"),("吸う（1日1箱くらい）", "吸う（1日1箱くらい）"),
    ("吸う（1日1箱以上）", "吸う（1日1箱以上）"),("吸う（2～3日に1箱）", "吸う（2～3日に1箱）"),("吸う（気が向いた時だけ）", "吸う（気が向いた時だけ）"),
    ("吸う（電子タバコ）", "吸う（電子タバコ）"),("禁煙中", "禁煙中"),("非喫煙者の前では吸わない", "非喫煙者の前では吸わない"),
    ]
  ecchiness_level_list = [
    ("積極的で経験豊か","積極的で経験豊か"),("積極的で好奇心旺盛","積極的で好奇心旺盛"),("普通だし気持ちが大切","普通だし気持ちが大切"),("奥手だけど興味あり","奥手だけど興味あり"),
     ("普通だけど刺激が欲しい","普通だけど刺激が欲しい"), ("普通だけど相性は大事","普通だけど相性は大事"),
     ("奥手だし苦手です","奥手だし苦手です"),("まだ未経験です","まだ未経験です"),("奥手だし下ﾈﾀもNG","奥手だし下ﾈﾀもNG"),

      ]
  sake_list = [
    ("未回答","未回答"),("好き","好き"),("たしなむ程度","たしなむ程度"),
    ("相手に合わせたい","相手に合わせたい"), ("飲めない","飲めない"), ("飲めないが場は好き","飲めないが場は好き")
      ]
  process_before_meeting_list =[
    ("まずは会ってみたい","まずは会ってみたい"), ("気が合いそうなら会ってみたい","気が合いそうなら会ってみたい")
     ]
  first_date_cost_list = [
    ("未回答", "未回答"),("自分が全部払う", "自分が全部払う"),("自分が多めに払う", "自分が多めに払う"),
    ("割り勘", "割り勘"),("お相手に全部払ってもらう", "お相手に全部払ってもらう"),("お相手に多めに払ってもらう", "お相手に多めに払ってもらう"),
    ("持っている方が払う", "持っている方が払う"),("相手と相談して決める", "相手と相談して決める"),
    ]
  travel_list = [
    ("未回答", "未回答"),("仲良くなってからなら", "仲良くなってからなら"),("予定が合えば", "予定が合えば"),("雰囲気で決める", "雰囲気で決める"),
    ("宿泊は無理", "宿泊は無理"),("むしろ泊めて欲しい", "むしろ泊めて欲しい"),
    ]
  education_list = [
    ("未回答", "未回答"),("高卒", "高卒"),("短大/専門学校", "短大/専門学校"),("大学", "大学"),
    ("大学院", "大学院"),("その他", "その他"),
    ]
  annual_income_list = [
    ("未回答", "未回答"),("200万円未満", "200万円未満"),("200万円以上～400万円未満", "200万円以上～400万円未満"),("400万円以上～600万円未満", "400万円以上～600万円未満"),
    ("600万円以上～800万円未満", "600万円以上～800万円未満"),("800万円以上～1000万円未満", "800万円以上～1000万円未満"),
    ("1000万円以上～1500万円未満", "1000万円以上～1500万円未満"),("1500万円以上～2000万円未満", "1500万円以上～2000万円未満"),
    ("2000万円以上", "2000万円以上"),
    ]
  roommate_list = [
    ("未回答", "未回答"),("一人暮らし", "一人暮らし"),("友達と一緒", "友達と一緒"),("家族と一緒", "家族と一緒"),
    ("兄弟姉妹と一緒", "兄弟姉妹と一緒"),("ペットと一緒", "ペットと一緒"),
    ("その他", "その他"),
    ]
  marry_list = [
    ("未回答", "未回答"),("すぐにでもしたい", "すぐにでもしたい"),("2～3年のうちに", "2～3年のうちに"),("良い人がいればしたい", "良い人がいればしたい"),
    ("今のところ結婚は考えていない", "今のところ結婚は考えていない"),("相手と相談して決めたい", "相手と相談して決めたい"),
    ("以前結婚していた", "以前結婚していた"),("未婚だけどパートナーが居る", "未婚だけどパートナーが居る"),("既婚者です", "既婚者です"),
    ]
  child_list = [
    ("未回答", "未回答"),("絶対に子供が欲しい", "絶対に子供が欲しい"),("どちらかというと子供が欲しい", "どちらかというと子供が欲しい"),("子供は欲しくない", "子供は欲しくない"),
    ("相手と相談して決めたい", "相手と相談して決めたい"),("同居中の子供がいる", "同居中の子供がいる"),
    ("別居中の子供がいる", "別居中の子供がいる"),("子供だけ欲しい（パートナー不要）", "子供だけ欲しい（パートナー不要）"),
    ]
  housework_list = [
    ("未回答", "未回答"),("積極的に参加したい", "積極的に参加したい"),("できれば参加したい", "できれば参加したい"),("できれば相手に任せたい", "できれば相手に任せたい"),
    ("相手に任せたい", "相手に任せたい"),("相手と相談して決めたい", "相手と相談して決めたい"),
    ]
  sociability_list = [
    ("未回答", "未回答"),("大人数が好き", "大人数が好き"),("小人数が好き", "小人数が好き"),("ひとりが好き", "ひとりが好き"),
    ("すぐに仲良くなる", "すぐに仲良くなる"),("徐々に仲良くなる", "徐々に仲良くなる"),
    ]
  name = models.CharField(max_length=30, blank=True, null=True, verbose_name="名前")
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)  
  login_id = models.CharField(max_length=30, blank=True, null=True, verbose_name="ログインID")
  password = models.CharField(max_length=30, blank=True, null=True, verbose_name="パスワード")
  fst_mail = models.TextField( blank=True, null=True, verbose_name="1stメール")
  mail_img = models.CharField(max_length=100, blank=True, null=True, verbose_name="画像送付")
  post_title = models.CharField(max_length=30, blank=True, null=True, verbose_name="掲示板タイトル")
  post_content = models.TextField( blank=True, null=True, verbose_name="掲示板内容文")
  second_message = models.TextField(blank=True, null=True, verbose_name="2stメール")
  condition_message = models.TextField(blank=True, null=True, verbose_name="アドレス内1stメール")
  return_foot_message = models.TextField(blank=True, null=True, verbose_name="足跡返し")
  mail_address = models.EmailField(blank=True, null=True, verbose_name="Gmailアドレス")
  gmail_password = models.CharField(max_length=20,blank=True, null=True, verbose_name="Gmailパスワード")
  date_of_birth = models.IntegerField(blank=True, null=True, verbose_name="誕生日(８桁の数字)")
  self_promotion = models.TextField(blank=True, null=True, verbose_name="自己紹介")
  height = models.IntegerField(blank=True, null=True, verbose_name="身長")
  body_shape = models.CharField(max_length=20, choices=body_shape_list, null=True, blank=True, verbose_name="体重")
  blood_type = models.CharField(max_length=5, choices=blood_type_list, null=True, blank=True, verbose_name="血液型")
  activity_area = models.CharField(max_length=5, choices=activity_area_list, null=True, blank=True, verbose_name="活動地域")
  detail_activity_area = models.CharField(max_length=10, blank=True, null=True, verbose_name="活動エリア(詳細)")
  profession = models.CharField(blank=True, null=True, verbose_name="職業")
  freetime = models.CharField(max_length=20, choices=freetime_list, null=True, blank=True, verbose_name="ヒマな時間帯")
  car_ownership = models.CharField(max_length=20, choices=car_ownership_list, null=True, blank=True, verbose_name="車の所有")
  smoking = models.CharField(max_length=20, choices=smoking_list, null=True, blank=True, verbose_name="喫煙")
  ecchiness_level = models.CharField(max_length=20, choices=ecchiness_level_list, null=True, blank=True, verbose_name="エッチ度")
  sake = models.CharField(max_length=20, choices=sake_list, null=True, blank=True, verbose_name="お酒")
  process_before_meeting = models.CharField(max_length=20, choices=process_before_meeting_list, null=True, blank=True, verbose_name="会うまでのプロセス")
  first_date_cost = models.CharField(max_length=20, choices=first_date_cost_list, null=True, blank=True, verbose_name="初回デート費用")
  travel = models.CharField(max_length=20, choices=travel_list, null=True, blank=True, verbose_name="旅行・宿泊")
  birth_place = models.CharField(max_length=10,  null=True, blank=True, verbose_name="出身地")
  education = models.CharField(max_length=20, choices=education_list, null=True, blank=True, verbose_name="学歴")
  annual_income = models.CharField(max_length=20, choices=annual_income_list, null=True, blank=True, verbose_name="年収")
  roommate = models.CharField(max_length=20, choices=roommate_list, null=True, blank=True, verbose_name="同居人")
  marry = models.CharField(max_length=20,  choices=marry_list, null=True, blank=True, verbose_name="結婚")
  child = models.CharField(max_length=20,  choices=child_list, null=True, blank=True, verbose_name="子供")
  housework = models.CharField(max_length=20,  choices=housework_list, null=True, blank=True, verbose_name="家事・育児")
  sociability = models.CharField(max_length=20,  choices=sociability_list, null=True, blank=True, verbose_name="社交性")

  is_active = models.BooleanField(default=True, verbose_name="アクティブ")
  memo = models.CharField(max_length=30,blank=True, null=True, verbose_name="メモ")

  
  def __str__(self):
    return self.name  # ここで表示したいフィールドを選択します
  
  class Meta:
    managed = True
    db_table = 'pcmax'
    verbose_name = "PCMAX"
    verbose_name_plural = "PCMAX"

class Jmail(models.Model):

  name = models.CharField(max_length=30, blank=True, null=True, verbose_name="名前")
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)  
  login_id = models.CharField(max_length=30, blank=True, null=True, verbose_name="ログインID")
  password = models.CharField(max_length=30, blank=True, null=True, verbose_name="パスワード")
  fst_message = models.TextField(blank=True, null=True, verbose_name="1stメール")
  chara_image = models.ImageField(upload_to='chara_images/', null=True, blank=True, verbose_name="送付画像")
  return_foot_message = models.TextField(blank=True, null=True, verbose_name="足跡返し")
  conditions_message = models.TextField(blank=True, null=True, verbose_name="2stメール")
  post_title = models.CharField(max_length=30,blank=True, null=True, verbose_name="掲示板タイトル")
  post_contents = models.TextField(blank=True, null=True, verbose_name="掲示板内容文")
  is_active = models.BooleanField(default=True, verbose_name="アクティブ")
  memo = models.CharField(max_length=30,blank=True, null=True, verbose_name="メモ")
  
  def __str__(self):
    return self.name  # ここで表示したいフィールドを選択します
  
  class Meta:
    managed = True
    db_table = 'jmail'
    verbose_name = "Jmail"
    verbose_name_plural = "Jmail"

class Ikukuru(models.Model):
  name = models.CharField(max_length=30, blank=True, null=True, verbose_name="名前")
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)  
  login_mail_address = models.EmailField(null=True, blank=True, verbose_name="ログインメールアドレス")
  password = models.CharField(max_length=30, blank=True, null=True, verbose_name="ログインパスワード")
  fst_message = models.TextField(blank=True, null=True, verbose_name="1stメール")
  second_message = models.TextField(blank=True, null=True, verbose_name="2stメール")
  condition_message = models.TextField(blank=True, null=True, verbose_name="アドレス内1stメール")
  gmail_address = models.EmailField(null=True, blank=True, verbose_name="gmailアドレス")
  gmail_password = models.CharField(max_length=20,blank=True, null=True, verbose_name="Gmailパスワード")
  is_active = models.BooleanField(default=True, verbose_name="アクティブ")
  memo = models.CharField(max_length=30,blank=True, null=True, verbose_name="メモ")
  
  def __str__(self):
    return "イククル" # ここで表示したいフィールドを選択します
  
  class Meta:
    managed = True
    db_table = 'Ikukuru'
    verbose_name = "Ikukuru"
    verbose_name_plural = "Ikukuru"