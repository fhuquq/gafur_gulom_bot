# G'afur G'ulom haqida testlar
# Har bir test: savol, 4 variant (A,B,C,D), to'g'ri javob indeksi (0=A, 1=B, 2=C, 3=D), izoh

TESTS = [
    # BIOGRAFIYA
    {
        "savol": "G'afur G'ulom qaysi yilda tug'ilgan?",
        "variantlar": ["1900-yil", "1903-yil", "1905-yil", "1910-yil"],
        "togri": 1,
        "izoh": "G'afur G'ulom 1903-yil 10-mayda Toshkentda tug'ilgan."
    },
    {
        "savol": "G'afur G'ulom qaysi shaharda tug'ilgan?",
        "variantlar": ["Samarqand", "Buxoro", "Toshkent", "Namangan"],
        "togri": 2,
        "izoh": "U Toshkent shahrining Qo'rg'ontegi mahallasida tug'ilgan."
    },
    {
        "savol": "G'afur G'ulom nechanchi yilda vafot etgan?",
        "variantlar": ["1960-yil", "1963-yil", "1966-yil", "1970-yil"],
        "togri": 2,
        "izoh": "G'afur G'ulom 1966-yil 10-iyunda vafot etgan, 63 yoshida."
    },
    {
        "savol": "G'afur G'ulom nechanchi yoshida otasidan yetim qolgan?",
        "variantlar": ["5 yoshida", "7 yoshida", "9 yoshida", "12 yoshida"],
        "togri": 2,
        "izoh": "Otasi 1912-yilda vafot etgan, G'afur G'ulom o'shanda 9 yoshda edi."
    },
    {
        "savol": "G'afur G'ulomning onasining ismi nima?",
        "variantlar": ["Zulfiya", "Toshbibi", "Muharram", "Maryam"],
        "togri": 1,
        "izoh": "Onasining ismi Toshbibi Shoyusuf qizi bo'lgan."
    },
    {
        "savol": "G'afur G'ulomning rafiqasining ismi nima?",
        "variantlar": ["Zulfiya", "Toshbibi", "Muharram", "Dilnoza"],
        "togri": 2,
        "izoh": "Rafiqasi Muharram G'ulomova 1995-yilda vafot etgan."
    },
    {
        "savol": "G'afur G'ulom qaysi qabristonga dafn etilgan?",
        "variantlar": ["Ming o'rik qabristoni", "Zangiota qabristoni", "Chig'atoy qabristoni", "Ko'kkamari qabristoni"],
        "togri": 2,
        "izoh": "U Toshkent shahri Chig'atoy qabristoniga dafn etilgan."
    },
    {
        "savol": "G'afur G'ulomning asl to'liq ismi nima?",
        "variantlar": ["G'afur G'ulomov", "Abdulg'afur G'ulom Mirzo Orif o'g'li", "G'afur Mirzo G'ulomov", "Abdug'afur G'ulomov"],
        "togri": 1,
        "izoh": "Uning asl ismi Abdulg'afur G'ulom Mirzo Orif o'g'li."
    },

    # TA'LIM VA MEHNAT
    {
        "savol": "G'afur G'ulom qaysi institutni tamomlagan?",
        "variantlar": ["Toshkent davlat universiteti", "Toshkent pedagogika instituti", "O'rta Osiyo universiteti", "Samarqand universiteti"],
        "togri": 1,
        "izoh": "U Toshkent pedagogika institutini tamomlagan."
    },
    {
        "savol": "G'afur G'ulom bosmaxonada qanday lavozimda ishlagan?",
        "variantlar": ["Muharrir", "Naborshik (harf teruvchi)", "Kotib", "Nashriyotchi"],
        "togri": 1,
        "izoh": "U keksa ishchi Abdurahmon Soyiboyev ustozligida naborshik — harf teruvchi bo'lib ishlay boshlagan."
    },
    {
        "savol": "G'afur G'ulom 1923-yilda qaysi muassasaga rahbar bo'lgan?",
        "variantlar": ["Maktab direktori", "150 bolalik internat mudiri", "Nashriyot direktori", "Kutubxona mudiri"],
        "togri": 1,
        "izoh": "1923-yilda unga 150 bolalik yetimlar internati topshirilgan."
    },
    {
        "savol": "G'afur G'ulom O'zbekiston Fanlar akademiyasiga qachon a'zo bo'lgan?",
        "variantlar": ["1940-yil", "1943-yil", "1946-yil", "1950-yil"],
        "togri": 1,
        "izoh": "U 1943-yilda O'zbekiston Fanlar akademiyasiga haqiqiy a'zo (akademik) bo'lgan."
    },

    # ASARLARI
    {
        "savol": "'Shum bola' asari qaysi yilda yozila boshlangan?",
        "variantlar": ["1930-yil", "1933-yil", "1936-yil", "1940-yil"],
        "togri": 2,
        "izoh": "'Shum bola' 1936-yilda yozila boshlangan va 1962-yilgacha davom etgan."
    },
    {
        "savol": "'Shum bola' qanday janrdagi asar?",
        "variantlar": ["Roman", "Avtobiografik qissa", "Hikoya", "Doston"],
        "togri": 1,
        "izoh": "'Shum bola' — G'afur G'ulomning avtobiografik qissasi."
    },
    {
        "savol": "'Sen yetim emassan' she'ri qaysi yilda yozilgan?",
        "variantlar": ["1940-yil", "1941-yil", "1942-yil", "1945-yil"],
        "togri": 2,
        "izoh": "Bu she'r 1942-yilda Ikkinchi Jahon urushi paytida yozilgan."
    },
    {
        "savol": "'Sen yetim emassan' she'ri kimga bag'ishlangan?",
        "variantlar": ["Frontdagi askarlarga", "Urushda ota-onasini yo'qotgan bolalarga", "Onalarga", "Vatanga"],
        "togri": 1,
        "izoh": "She'r urushda ota-onasini yo'qotib yetim qolgan bolalarga bag'ishlangan."
    },
    {
        "savol": "'Vaqt' she'ri qaysi yilda yozilgan?",
        "variantlar": ["1942-yil", "1943-yil", "1944-yil", "1945-yil"],
        "togri": 3,
        "izoh": "'Vaqt' she'ri 1945-yil 18-19 sentabrda yozilgan."
    },
    {
        "savol": "'Men yahudiyman' she'ri qachon nashr etilgan?",
        "variantlar": ["1939-yil", "1940-yil", "1941-yil", "1942-yil"],
        "togri": 2,
        "izoh": "'Men yahudiyman' she'ri 1941-yil 26-iyunda nashr etilgan."
    },
    {
        "savol": "'Netay' qissasi qaysi yilda yozilgan?",
        "variantlar": ["1928-yil", "1930-yil", "1932-yil", "1935-yil"],
        "togri": 1,
        "izoh": "'Netay' qissasi 1930-yilda yozilgan."
    },
    {
        "savol": "'Mening o'g'rigina bolam' hikoyasi qaysi yilda yozilgan?",
        "variantlar": ["1955-yil", "1960-yil", "1963-yil", "1965-yil"],
        "togri": 3,
        "izoh": "'Mening o'g'rigina bolam' 1965-yilda yozilgan."
    },
    {
        "savol": "G'afur G'ulomning birinchi she'ri qanday nomlanadi?",
        "variantlar": ["Sen yetim emassan", "Feliks farzandlari", "Go'zallik qayerda", "Vaqt"],
        "togri": 1,
        "izoh": "Birinchi she'ri 'Feliks farzandlari' 1923-yilda yozilgan — yetim bolalar internati uchun."
    },
    {
        "savol": "G'afur G'ulomning 'Dinamo' she'riy to'plami qaysi yilda chiqgan?",
        "variantlar": ["1929-yil", "1931-yil", "1933-yil", "1935-yil"],
        "togri": 1,
        "izoh": "'Dinamo' to'plami 1931-yilda nashr etilgan."
    },

    # MUKOFOTLAR
    {
        "savol": "G'afur G'ulom SSSR Davlat mukofotini qaysi yilda olgan?",
        "variantlar": ["1943-yil", "1946-yil", "1950-yil", "1953-yil"],
        "togri": 1,
        "izoh": "U 1946-yilda SSSR Davlat mukofotiga sazovor bo'lgan."
    },
    {
        "savol": "G'afur G'ulom qaysi unvonga ega?",
        "variantlar": ["O'zbekiston xalq yozuvchisi", "O'zbekiston xalq shoiri", "O'zbekiston xalq qahramoni", "O'zbekiston xalq artisti"],
        "togri": 1,
        "izoh": "U O'zbekiston xalq shoiri unvoniga sazovor bo'lgan."
    },
    {
        "savol": "G'afur G'ulomning qaysi asari uchun Davlat mukofoti berilgan?",
        "variantlar": ["Shum bola", "Sen yetim emassan", "Sharqdan kelayotirman to'plami", "Vaqt she'ri"],
        "togri": 2,
        "izoh": "'Sharqdan kelayotirman' to'plami uchun 1946-yilda SSSR Davlat mukofoti berilgan."
    },

    # TARJIMONLIK
    {
        "savol": "G'afur G'ulom Shekspirning qaysi asarini tarjima qilgan?",
        "variantlar": ["Hamlet", "Romeo va Juletta", "Otello va Qirol Lir", "Makbet"],
        "togri": 2,
        "izoh": "U Shekspirning 'Otello' (1940) va 'Qirol Lir' (1956) asarlarini tarjima qilgan."
    },
    {
        "savol": "G'afur G'ulom Mayakovskiyning qaysi asarini tarjima qilgan?",
        "variantlar": ["Bulut shimda", "Vo ves golos — Hayqiriq", "Vladimir Ilich Lenin", "Yaxshi!"],
        "togri": 1,
        "izoh": "U Mayakovskiyning 'Vo ves golos' poemasini 'Hayqiriq' nomi bilan 1930-yilda tarjima qilgan."
    },
    {
        "savol": "G'afur G'ulom Navoiyning qaysi asarini zamonaviy tilga o'girgan?",
        "variantlar": ["Layli va Majnun", "Farhod va Shirin", "Sab'ai sayyor", "Saddi Iskandariy"],
        "togri": 1,
        "izoh": "U 1940-yilda Navoiyning 'Farhod va Shirin' dostonini zamonaviy o'zbek tiliga tabdil qilgan."
    },

    # OILASI VA FARZANDLARI
    {
        "savol": "G'afur G'ulomning o'g'li Ulug' G'ulomov qaysi soha olimi edi?",
        "variantlar": ["Tarix", "Adabiyotshunoslik", "Fizika", "Matematika"],
        "togri": 2,
        "izoh": "Ulug' G'ulomov (1933-1990) fizika fanlari doktori, O'zbekiston FA Yadro fizikasi instituti direktori edi."
    },
    {
        "savol": "G'afur G'ulomning qaysi farzandi O'zbekiston mudofaa vaziri bo'lgan?",
        "variantlar": ["Ulug' G'ulomov", "Qodir G'ulomov", "Mirzo G'ulomov", "Holida G'ulomova"],
        "togri": 1,
        "izoh": "Qodir G'ulomov 2000-2005-yillarda O'zbekiston mudofaa vaziri bo'lgan."
    },
    {
        "savol": "G'afur G'ulomning qaysi farzandi uy-muzeyga rahbarlik qilgan?",
        "variantlar": ["Toshxon Yo'ldosheva", "Holida G'ulomova", "Olmos Axmedova", "Muharram G'ulomova"],
        "togri": 2,
        "izoh": "Qizi Olmos Axmedova G'afur G'ulom uy-muzeyi direktori bo'lgan."
    },

    # QO'SHIMCHA
    {
        "savol": "'Shum bola' BBCning qaysi ro'yxatiga kiritilgan?",
        "variantlar": ["Eng mashhur romalar", "100 ta eng buyuk bolalar kitoblari", "Eng yaxshi tarjima asarlar", "Eng ko'p o'qilgan kitoblar"],
        "togri": 1,
        "izoh": "'Shum bola' BBCning 'Barcha davrlarning 100 ta eng buyuk bolalar kitoblari' ro'yxatiga kiritilgan."
    },
    {
        "savol": "Isroilning qaysi shahrida G'afur G'ulom maydoni tashkil etilgan?",
        "variantlar": ["Tel-Aviv", "Quddus", "Kiriyat Gat", "Xayfa"],
        "togri": 2,
        "izoh": "2005-yilda Isroilning Kiriyat Gat shahrida 'Men yahudiyman' she'ri sharafiga G'afur G'ulom maydoni ochildi."
    },
    {
        "savol": "G'afur G'ulom haykali qayerda joylashgan?",
        "variantlar": ["Mustaqillik maydoni", "Amir Temur maydoni", "Adiblar xiyoboni", "O'zbekiston milliy bog'i"],
        "togri": 2,
        "izoh": "Haykali Adiblar xiyobonida joylashgan — do'ppini qiyshiq qo'ndirgan alpqomat shoir timsolida."
    },
    {
        "savol": "'Sen yetim emassan' she'ri necha tilga tarjima qilingan?",
        "variantlar": ["10 tilga", "20 tilga", "30 tilga", "50 tilga"],
        "togri": 2,
        "izoh": "Bu she'r 30 ga yaqin tilga tarjima qilingan."
    },
    {
        "savol": "G'afur G'ulom o'zining ijodiy ustozi sifatida kimni ko'rsatgan?",
        "variantlar": ["Pushkin", "Lermontov", "Mayakovskiy", "Navoiy"],
        "togri": 2,
        "izoh": "G'afur G'ulom she'r qurilishi va uslub sohasida Mayakovskiyning shogirdi ekanini aytgan."
    },
]
