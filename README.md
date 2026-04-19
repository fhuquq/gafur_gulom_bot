# 🌟 G'AFUR G'ULOM TELEGRAM BOTI

Buyuk o'zbek shoiri va yozuvchisi G'afur G'ulom haqida AI-powered Telegram boti.

## ✨ Imkoniyatlar

- 🤖 **Claude AI** bilan suhbat — G'afur G'ulom haqida istalgan savol
- 📚 **Elektron kitoblar** — PDF formatda asarlar
- 🎧 **Audio hikoyalar** — MP3 formatda asarlar  
- 📖 **Asarlar ma'lumoti** — She'rlar, hikoyalar, romanlar haqida
- ℹ️ **Tarjimayi hol** — To'liq biografiya
- 🎭 **She'rlar** — Mashhur she'rlar tahlili

---

## 🚀 O'RNATISH VA ISHGA TUSHIRISH

### 1-QADAM: Telegram Bot yaratish

1. Telegramda **@BotFather** ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting: `Gafur Gulom Bot`
4. Bot username kiriting: `gafur_gulom_uz_bot`
5. **TOKEN** ni nusxalab oling (misol: `7123456789:AAHxxx...`)

### 2-QADAM: Anthropic API kaliti olish

1. [console.anthropic.com](https://console.anthropic.com) ga kiring
2. Ro'yxatdan o'ting (Google/Email bilan)
3. **API Keys** bo'limiga o'ting
4. **"Create Key"** tugmasini bosing
5. Kalitni nusxalab oling (`sk-ant-...`)

> 💡 Anthropic yangi hisoblarga $5 bepul kredit beradi!

---

## ☁️ RAILWAY.APP DA DEPLOY (BEPUL SERVER)

Railway — bepul bulut server. Botingiz 24/7 ishlaydi, noutbukingizsiz!

### 3-QADAM: Railway ro'yxati

1. [railway.app](https://railway.app) ga kiring
2. **"Login with GitHub"** tugmasini bosing
3. GitHub hisobingiz bilan kiring (agar yo'q bo'lsa, [github.com](https://github.com) da ro'yxatdan o'ting)

### 4-QADAM: GitHub ga yuklash

**GitHub Desktop yoki Git orqali:**

```bash
# Git o'rnatilgan bo'lsa:
cd gafur_gulom_bot
git init
git add .
git commit -m "G'afur G'ulom bot"

# GitHub da yangi repository yarating, so'ng:
git remote add origin https://github.com/SIZNING_USERNAME/gafur-gulom-bot.git
git push -u origin main
```

**GitHub Desktop (osonroq):**
1. [desktop.github.com](https://desktop.github.com) dan GitHub Desktop yuklab oling
2. "Add existing repository" → bot papkasini tanlang
3. "Publish repository" → nomini kiriting → Publish

### 5-QADAM: Railway da Deploy

1. [railway.app](https://railway.app) → **"New Project"**
2. **"Deploy from GitHub repo"** → botingiz repo sini tanlang
3. **"Variables"** bo'limiga o'ting → **"Add Variable"**:
   ```
   BOT_TOKEN = 7123456789:AAHxxx...
   ANTHROPIC_API_KEY = sk-ant-api03-xxx...
   ```
4. **"Deploy"** → tayyor! 🎉

Bot avtomatik ishga tushadi va 24/7 ishlaydi!

---

## 💻 LOCAL (MAHALLIY) ISHGA TUSHIRISH

Agar test qilmoqchi bo'lsangiz:

```bash
# Python 3.10+ kerak
pip install -r requirements.txt

# .env fayl yarating:
cp .env.example .env
# .env faylini oching va tokenlarni kiriting

# Botni ishga tushiring:
python bot.py
```

---

## 📁 KITOB VA AUDIO QO'SHISH

Kitob yoki audio fayllaringizni qo'shish uchun:

```
gafur_gulom_bot/
├── media/
│   ├── books/          ← PDF kitoblarni shu yerga
│   │   ├── shum_bola.pdf
│   │   ├── navoiy.pdf
│   │   └── ...
│   └── audio/          ← MP3 fayllarni shu yerga
│       ├── shum_bola_audio.mp3
│       └── ...
```

**Fayl nomlari:**
| Asar | Kitob fayli | Audio fayli |
|------|------------|-------------|
| Shum bola | `shum_bola.pdf` | `shum_bola_audio.mp3` |
| O'g'rigina bolam | `ogrigina_bolam.pdf` | - |
| Ko'cha bolasi | `kucha_bolasi.pdf` | - |
| Sariq devlar | `sariq_devlar.pdf` | - |
| Navoiy | `navoiy.pdf` | - |
| She'rlar | - | `sherlar.mp3` |
| Hikoyalar | - | `hikoyalar.mp3` |

---

## 🔧 MUAMMOLAR VA YECHIMLAR

**Bot javob bermayapti:**
- BOT_TOKEN to'g'riligini tekshiring
- Railway logs ni ko'ring

**AI javob bermayapti:**
- ANTHROPIC_API_KEY to'g'riligini tekshiring
- Anthropic balansingizni tekshiring

**Kitob/audio yuklanmayapti:**
- Fayl nomini `media/books/` yoki `media/audio/` ga to'g'ri joylashtiring
- Fayl nomi yuqoridagi jadval bilan bir xil bo'lsin

---

## 📞 YORDAM

Muammo bo'lsa GitHub Issues ga yozing.

## 📄 Litsenziya

MIT License — erkin foydalanishingiz mumkin.
