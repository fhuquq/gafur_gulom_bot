import os
import json
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import main_menu
from data.gafur_data import BIOGRAPHY

router = Router()

BOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "books")
JSON_PATH = os.path.join(BOOKS_DIR, "gafur_data.json")

def load_json() -> dict:
    if not os.path.exists(JSON_PATH):
        return {}
    for enc in ["utf-8", "utf-8-sig"]:
        try:
            with open(JSON_PATH, "r", encoding=enc) as f:
                return json.load(f)
        except Exception:
            continue
    return {}

# ═══════════════════════════════════════
# SHE'RLAR — TO'LIQ MATNLAR
# ═══════════════════════════════════════

SHERLAR = {
    "sen_yetim": {
        "nomi": "SEN YETIM EMASSAN (1942)",
        "matn": """(Ulug' Vatan urushining ota-onasiz qolgan go'daklarga)

Sen yetim emassan,
Tinchlan, jigarim.
Quyoshday mehribon
Vataning-onang,
Zaminday vazminu
Mehnatkash, mushfiq
Istagan narsangni tayerlaguvchi
Xalq bor- otang bor.
Cho'chima, jigarim,
O'z uyingdasan,
Bu yerda
Na g'urbat, na ofat, na g'am.
Bunda bor: harorat, muhabbat, shafqat
Va mehnat nonini ko'ramiz baham,
Sen yetim emassan,
Uxla, jigarim.

Bu yerda muzlagan
Ajdar halqumli
Vahshat to'plarining
Qahqahasi yo'q.
Bu yerda — odamzod
shaklida yurgan
manfur, yukumli, maraz namoyishi
topolmas huquq.

Ulug' jang kunidir,
Jangki, beomon,
Lashkar degan axir
Bexatar bo'lmas,
Otang o'lgan bo'lsa,
Qayg'urma, qo'zim,
Ko'zim usti
Minnating boshimga durra.
Shu sog'lom havoda
Salomat-omon,
Xo'rsinmay, erkinlab
Ola bera nafas.

Ey, ulug' naslimning
Yuragi, joni,
Kiprigingga ilinmas
Yig'idan zarra.
Sen yetim emassan,
Uxla, jigarim.

Yetimlik nimadir-
Bizlardan so'ra,
O'ninchi yillarning
Sargardonligi
Isitma aralash
Qo'rqinch tush kabi
Xayol ko'zgusidan
Uchmaydi sira.

Men yetim o'tganman,
Oh, u yetimlik…
Voy, bechora jonim,
Desam arziydi.
Boshimni silashga
Bir mehribon qo'l,
Bir og'iz shirin so'z
Nondek arzanda.
Men odam edim-ku,
Inson farzandi…
Sen yetim emassan,
Uxla jigarim.

Ko'zimga o'yquning
Mudroq ovchisi
To'rin solmasdan, —
(Birinchi gudokka
Ikki soat bor)-
Otalik hissining
Bebaho, laziz
To'lqinlar ichra
G'arq bo'lib ketib,
Aziz boshing ustida
Termulmakdaman,
Sen yetim emassan,
Uxla, jigarim.

Nega cho'chib tushding,
Murg'ak xayolingga
Nimalar keldi?
Balki Odess dahshati,
Kerch fojiasi,
Yovvoyi maxluqlar,
Qonxo'r vahshiylar…
Mammasi kesilgan
Sho'rlik onangning
Pajmurda gavdasi
Ko'zing o'ngida
Butun dahshati-la
Aks etar endi.

Onang xo'rlandimi,
Otang o'ldimi,
Sen yetim qoldingmi,
Qayg'urma, qo'zim,
Ko'zim usti,
Minnating boshimga durra.

Ota-onasining
Tayini ham yuq,
Sut ko'r qilgur, haromi
Gitler oqpadar
Farzandning qadrini
Qayerdan bilsin?
Bir qo'ng'iz mo'ylovli,
Baroq soch mal'un,
Jigar rang bir mundir
Istagi uchun,
Nahotki yerimiz
Chappa aylanib,
Nahotki daryolar
Oqar teskari,
Nahotki odamlar
Kezar darbadar?!

Axir, juda yaqin
Qonli intiqom,
Alhazar, alhazar,
Ko'pirar tomirlarda qon,
Va portlar hademay
Bu o'tli vulqon.

Sen yetim emassan,
Uxla, jigarim.
Sen kulayotibsan,
Balki bu kulgi
So'nggi oylar ichra
birinchi chechak.
La'li labingdagi
G'uncha tabassum
Albat toleingga
Muhr bo'ladi
Va bunda aks etar
Porloq kelajak.
Tong yaqin, tong yaqin,
oppoq tong yaqin.
Bir nafas orom ol,
Uxla, jigarim.

Oq oydin tong oldi,
Uxlamoqdasen.
Lablaring shivirlar,
Izlamokdalar
Balki bir erkalash,
Bir ona bo'sa,
Ulug' oilaning
go'dak farzandi,
bilib qo'y endi:
Sen tezda ulg'ayib,
Olam kezasan.
Manglayda porlagan
Toleing — quyosh,
Butun yer yuzini
Qilur munavvar.
Xaqorat yemrilur,
Zulm yanchilur,
Jahonda bo'lurmiz
Ozod, muzaffar.
Sen yetim emassan,
Mening Jigarim!"""
    },
    "vaqt": {
        "nomi": "VAQT",
        "matn": """
G'uncha ochilguncha o'tgan fursatni
Kapalak umriga qiyos etgulik,
Ba'zida bir nafas olg'ulik muddat —
Ming yulduz so'nishi uchun yetgulik.

Yashash soatining oltin kapgiri
Har borib kelishi bir olam zamon.
Koinot shu damda o'z kurrasidan
Yasab chiqa olur yangidan jahon.

Yarim soat ichida tug'ilib, o'sib,
Yashab, umr ko'rib o'tguvchilar bor;
Ko'z ochib yumguncha o'tgan dam — qimmat,
Bir lahza mazmuni bir butun bahor.

Bir onning bahosin o'lchamoq uchun
Oltindan tarozu, olmosdan tosh oz.
Nurlar qadami-la chopgan sekundning
Barini tutolmas ay(yu)hannos ovoz.

Yigit termiladi qizning ko'ziga,
Kiprik suzilishi, mayin tabassum…
Qo'sha qarimoqqa muhr bo'ladi
Hayotda ikki lab qovushgan bir zum.

Yashash darbozasi ostonasidan
Zarhal kitob kabi ochilur olam,
Tiriklik ko'rkidir mehnat, muhabbat,
Fursatdir qilguvchi aziz, mukarram.

Bebaho damlarning tirik joni biz,
Har oni o'tmishning yuz yiliga teng.
O'zbekning barhayot avlodlarimiz,
Har nafas mazmuni fazolardan keng.

Qatrada osmon aks etganidek
Jahonday ma'nodor qorachig'imiz.
G'olib asrimizga kuyoshdan mash'al,
Zamon ko'rasining so'nmas cho'g'imiz.

Zamona soati zang urar mudom,
Minglab hodisalar minutlarga qayd,
Qahramon tug'ildi, shahar olindi,
Bir gigant qurildi sharafli bu payt.

Reyxstag ustiga g'alaba tug'in
Qadashda otilgan adolat o'qi —
Yalt etgan umri-la barqaror qildi
Basharning muqaddas, oliy huquqin.

G'alaba amri-la, mag'lub nemisning
Generali qo'l qo'ydi. Uch sekund faqat…
Shu mal'un imzoda odamlar o'qir
Million yil fashistning umriga lan'at.

Aziz asrimizning aziz onlari
Aziz odamlardan so'raydi qadrin.
Fursat g'animatdir, shoh satrlar-la
Bezamoq chog'idir umr daftarin.

Shuhrat qoldirmoqqa Gerostratdek
Diana ma'badin yoqmoq shart emas.
Ko'plarning baxtiga o'zlikni jamlab,
Shu ulug' binoga bir g'isht qo'ysak bas.

Har lahza zamonlar umridek uzun,
Asrlar taqdiri lahzalarda hal,
Umrdan o'tajak har lahza uchun
Qudratli qo'l bilan qo'yaylik haykal.

Hayot sharobidan bir qultum yutay,
Damlar g'animatdir, umrzoq soqiy.
Quyosh-ku falakda kezib yuribdi,
Umrimiz boqiydir, umrimiz boqiy."""
    },
    "soginish": {
        "nomi": "SOG'INISH",
        "matn": """Zo'r karvon yo'liada yetim bo'tadek,
Intizor ko'zlarda halqa-halqa yosh.
Eng kichik zarradan Yupitergacha
O'zing murabbiysan, xabar ber, Quyosh!

Uzilgan bir kiprik abad yo'qolmas,
Shunchalar mustahkam xonai xurshid.
Bugun sabza bo'ldi qishdagi nafas,
Hozir qonda kezar ertagi umid.

Xoki anjir tugab, qovun g'arq pishgan
Baxtli tong otar chog' uni kuzatdim,
Bir mal'un gulshanga qadam qo'ymishkan,
Joni bir jondoshlar qolarmidi jim!

Unda yetuk edi meros mard g'urur,
Ostonani o'pib, qasamyod qildi.
Ukalarin erkalab, o'zimday mag'rur,
Ya'ni obod uyimni u dilshod qildi…

Iblisning g'arazi bo'lgan bu urush
Albatta, yetadi o'zin boshiga.
O'g'lim omon kelar, g'olib, muzaffar,
Gard ham qo'ndirmasdan qora qoshiga.

Ne qilsa otamen, meros hissiyot…
Jondan sog'inishga uning haqqi bor,
Kutaman, uzoqdan ko'rinsa bir ot,
Kelayapti, deyman ko'rinsa g'ubor.

Bahor novdasida bo'rtgan har kurtak
Sog'ingan ko'ngilga berar tasalli.
Ko'chatlar qomatin eslatganidek,
Nafasin ufurar tong otar yeli.

Kechqurun osh suzsak bir nasiba kam,
Qo'msayman birovni — allakimimni,
Doimo umidim bardam bo'lsa ham,
Ba'zan vasvasalar bosar dilimni.

Balki bir g'alat o'q yo xavfu xatar
Xazinai umrimdan yo'qotdi olmos…
Yo'q, u o'lmas, qadami olam yaratar,
Hayotiy bu olam sizu bizga xos.

Tong otar chogida juda sog'inib,
Bedil o'qir edim, chikdi oftob.
Loyqa xayolotlar chashmaday tindi,
Pok-pokiza yurak bir qatra simob.

O'rog'u gulqaychi, istak ko'tarib,
Hovrimni bosishga boqqa jo'nadim.
Hasharchi qo'shni qiz — uning sevgani,
Ma'yus bosar edi orqamdan odim.

Bog'da sarvinozim yo'q edi garchand,
Ko'makchim arg'uvon yoring Nafisa,
Seni sog'inganda qildim gul payvand —
Bu bahordan hayot olardi bo'sa.

Dur bo'lib taqilur yoring bo'yniga,
Sadafday ko'zimda, behuda bu yosh.
Ikkoving ikki yosh, labing labiga
Qo'yar, vasvasamdan kuladi quyosh.

Asaldan ajragan mumday sarg'ayib,
Ini yo'q aridek to'zg'iganim yo'q.
Ulug' e'tiqodda o'laman qarib,
Abaddir mendagi padariy huquq.

Sizlarni keldi, deb eshitgan kuni —
O'zing to'qib ketgan katta savatda
To'latib shaftoli uzib chiqaman,
G'alaba kunlari yaqin, albatta.

Yayov, ko'ksim ochiq, boshda shaftolu,
Xuddi mo'ylabingdek mayin tuki bor,
Har bitta shaftolu misoli kulgu,
Shafaqday nim pushti, sarin, beg'ubor.

Suyganing labida reza ter kabi
Unda titrab turar sabuhiy shabnam.
Munchalik mazani topa olmaydi
Uyquda tamshangan chaqaloqlar ham.

Yo o'g'lim, jonginang salomat bo'lsin,
O'z bog'ing, o'z mevang, danagin saqla.
Shu meros bog'ingni o'z qo'lingga ol,
Menga topshirilgan merosiy haq-la.

Bog'da tovus kabi xiromon bo'lib,
Umid danagini birga ekingiz,
G'olib kelajakni sayr qilaylik
Mushfiq onaginang bilan ikkimiz."""
    },
    "yahudiy": {
        "nomi": "MEN YAHUDIY",
        "matn": """(Berlindan berilgan bir radio eshittirishiga javob)

I
Men yahudiyman!
Nomimni tilingga olma,
e, olchoq!
Kimligimni eng katta
buvingdan so'ra.
Bobolaring
boshiga shox taqib yurib,
Bilmasdan
tuz nima,
o't nima,
lungi...
Va Nibelungi,
Vahsat masjidida
gotik naqshlar
Hali sodda
va hali bo'lganda g'o'ra;
Asriy aqidada momaqaldiroq
Yarataroq
Bir xudo bo'lib,
tavrot yozgan yahudiy,
men yahudiyman.
Eh-he...
Bilolsayding
qancha mashaqqat,
G'urbatda kezganman
bilonihoya...
Uzoqbir umrki,
doim darbadar
Aqlini orqalab olgan
bir karvon...
Fir'avnlar quvlarkan,
Nilninglabida
O'z zehnim, fikrimning
g'arib mardudi,
men yahudiyman!
Nega so'ylamasdan
turmokdasan tin,
E, Baytulmuqaddas,
sen bergal xabar,
Yig'i devorlari
ko'hna Falastin...
Besh ming yil ilgari,
chorak asr oldin,
Tarix betlarida
javrab kelguvchi,
O'zi soqov
kdp'ai Bobil singari,
Aytib kelganman:
Men ham odamman!
Kderda,
qaydadir,
Ayting, fir'avnlar,
Shu tuproq zaminda
mening vatanim?
Yoinki,
kamolot — tuhmat bo'larak
Ko'milsinmi muallaq
osmonda tanim?
Jim!
Fir'avn jim, xoqon jim!
Paygambarlar,
sulaymonlar jim.
Bir xabar keltirmas,
umid hududi,
Men yahudiyman...

II
Men yahudiyman!
Nomimni tilingga olma,
e olchoq!
Beda tamaida
bo'ynini cho'zib,
Boshi jodi ichra qolgan
eshakday
Manfur, chinqiroq
Ovozingni radiodan
hamma eshitdi.
"...Unday yahudiy,
bunday yahudiy..."
Bali, yahudiy
Men yahudiyman...
Inson qoni aralash
millionlar karra
Va mening qonim ham
xalqgtardan zarra.
"...Irqu dinu millat..."
Tag'in nimadir?
Bilsangedi, bularningbarisin
bizda;
Sen itdan —
to'ngizni ajratish uchun
Baytariy ilmida
bobi zammadir.
Inson irqidanman,
inson millati,
Menda yo'q afyunning pinaklaridan
yaralgan dinlarning
zarra illati.
Shu tuproq zamindir
mening vatanim.
Tug'ilish, yashayish,
mehnatva nasl,
Muhabbat ham g'azab...
Insonda ne xislat
bor bo'lsa mavjud;
Bariga qobil,
barchasiga bop.
Shu tuproq zaminda
qolajak tanim.
Bilgil, e mardud,
Bizlarmiz olamda
xalqlar mas'udi,
Men yahudiyman.
Bu erkka intilgan
xalqpar tuprog'i —
Muqaddas, daxlsiz,
buni bilib qo'y.
Sen siflis tumshuqni
suqmoqchi bo'lib,
to'rt oyoqlab
O'rningdan qo'zg'algan chog'i
Zaharli nayzaga aylanib ketdi
Bizning badandagi
har bir tola mo'y.
Qo'zg'aldi butun xalq,
RUs,
ukrain,
o'zbek,
yahudiy;
Ikki yuz millionli
yuz ellik millat,
Uzoq falsafaning
hech hojati yo'q;
Zamin tarbuzidan
fashizm — illat
Yo'qolur
juda tez,
mutlaq abadiy.
Shunda sening
murdor taning bir umr
bo'lur jahannam,
fir'avnlar barham,
G'oliblar safida
turarak men ham.
Ya'ni sodda formula:
yahudiy - odam.
Mening kimligimni olam olqishlar.
Ko'zimda baxtimning
quyosh - surudi,
men yahudiyman"""
    }
}

POEMS_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📜 Sen yetim emassan (1942)", callback_data="sher_sen_yetim")],
    [InlineKeyboardButton(text="📜 Vaqt (1945)", callback_data="sher_vaqt")],
    [InlineKeyboardButton(text="📜 Sog'inish (1942)", callback_data="sher_soginish")],
    [InlineKeyboardButton(text="📜 Men yahudiy (1941)", callback_data="sher_yahudiy")],
    [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_main")]
])

# ═══════════════════════════════════════
# HANDLERS
# ═══════════════════════════════════════

@router.message(F.text == "ℹ️ Tarjimayi hol")
async def cmd_bio(message: Message):
    data = load_json()
    if data:
        s = data.get("shaxs", {})
        joy = s.get("tug_ilgan_joy", {})
        unvonlar = "\n".join([f"• {u}" for u in s.get("unvonlar", [])])
        mukofotlar = "\n".join([
            f"• {m.get('nom', '')} {m.get('yil', '')}"
            for m in s.get("mukofotlar", [])
        ])
        bio = (
            f"👤 *G'AFUR G'ULOM*\n\n"
            f"📛 *To'liq ismi:* {s.get('asl_ismi', '')}\n"
            f"📅 *Tug'ilgan:* {s.get('tug_ilgan_sana', '')}\n"
            f"📍 *Joy:* {joy.get('shahar', '')}, {joy.get('mahalla', '')}\n"
            f"⚰️ *Vafot:* {s.get('vafot_sana', '')} ({s.get('vafot_yoshi', '')} yoshida)\n"
            f"🏛️ *Dafn:* {s.get('dafn_etilgan', '')}\n\n"
            f"🏆 *Unvonlari:*\n{unvonlar}\n\n"
            f"🎖️ *Mukofotlari:*\n{mukofotlar}"
        )
        await message.answer(bio, parse_mode="Markdown", reply_markup=main_menu())
    else:
        await message.answer(BIOGRAPHY, parse_mode="Markdown", reply_markup=main_menu())

@router.message(F.text == "🎭 She'rlar")
async def show_poems(message: Message):
    await message.answer(
        "🎭 *G'AFUR G'ULOM SHE'RLARI*\n\n"
        "Jami: *4 ta* to'liq she'r mavjud\n"
        "She'r tanlang 👇",
        reply_markup=POEMS_KEYBOARD,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("sher_"))
async def show_sher(callback: CallbackQuery):
    key = callback.data[5:]
    sher = SHERLAR.get(key)
    if not sher:
        await callback.answer("Topilmadi!", show_alert=True)
        return

    header = f"📜 *{sher['nomi']}*\n_G'afur G'ulom_\n\n"
    full_text = header + sher["matn"]

    # 4096 belgidan uzun bo'lsa bo'laklarga bo'lish
    if len(full_text) > 4096:
        chunks = [full_text[i:i+4000] for i in range(0, len(full_text), 4000)]
        for chunk in chunks:
            await callback.message.answer(chunk, parse_mode="Markdown")
    else:
        await callback.message.answer(full_text, parse_mode="Markdown")

    await callback.answer()

@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.answer("Asosiy menyu:", reply_markup=main_menu())
    await callback.answer()

@router.message(F.text & ~F.text.startswith("/"))
async def handle_general(message: Message):
    skip = [
        "📚 Kitoblar", "🎧 Audio hikoyalar", "📖 Asarlari haqida",
        "ℹ️ Tarjimayi hol", "🎭 She'rlar", "❓ Yordam", "🔍 Qidirish"
    ]
    if message.text in skip:
        return
    await message.answer(
        "💡 Menyudan tanlang:",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )
