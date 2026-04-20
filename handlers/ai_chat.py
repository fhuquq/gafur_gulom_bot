import os
import re
import json
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import main_menu

router = Router()

class SearchState(StatesGroup):
    waiting = State()

BOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media", "books")
JSON_PATH = os.path.join(BOOKS_DIR, "gafur_data.json")
_json_cache = None
_txt_cache = None

# ═══════════════════════════════════════
# JSON MA'LUMOTLAR BAZASINI O'QISH
# ═══════════════════════════════════════

def load_json() -> dict:
    global _json_cache
    if _json_cache is not None:
        return _json_cache
    if not os.path.exists(JSON_PATH):
        _json_cache = {}
        return {}
    try:
        for enc in ["utf-8", "utf-8-sig"]:
            try:
                with open(JSON_PATH, "r", encoding=enc) as f:
                    _json_cache = json.load(f)
                return _json_cache
            except Exception:
                continue
    except Exception:
        pass
    _json_cache = {}
    return {}

def json_to_text(data, prefix="") -> str:
    """JSON ni tekis matn ko'rinishiga o'tkazish"""
    lines = []
    if isinstance(data, dict):
        for key, val in data.items():
            label = key.replace("_", " ").replace("-", " ")
            if isinstance(val, (dict, list)):
                lines.append(f"{prefix}{label}:")
                lines.append(json_to_text(val, prefix + "  "))
            else:
                lines.append(f"{prefix}{label}: {val}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(json_to_text(item, prefix))
            else:
                lines.append(f"{prefix}- {item}")
    else:
        lines.append(f"{prefix}{data}")
    return "\n".join(lines)

# ═══════════════════════════════════════
# TXT FAYLLARNI O'QISH
# ═══════════════════════════════════════

def load_txts() -> dict:
    global _txt_cache
    if _txt_cache is not None:
        return _txt_cache
    result = {}
    if not os.path.exists(BOOKS_DIR):
        _txt_cache = {}
        return {}
    for filename in sorted(os.listdir(BOOKS_DIR)):
        if not filename.lower().endswith(".txt"):
            continue
        filepath = os.path.join(BOOKS_DIR, filename)
        content = None
        for enc in ["utf-8", "utf-8-sig", "cp1251", "cp1252", "latin-1"]:
            try:
                with open(filepath, "r", encoding=enc) as f:
                    content = f.read().strip()
                if content:
                    break
            except Exception:
                continue
        if content:
            title = filename.replace(".txt", "").replace("_", " ").replace("-", " ").title()
            result[title] = content
    _txt_cache = result
    return result

# ═══════════════════════════════════════
# QIDIRUV TIZIMI
# ═══════════════════════════════════════

def get_snippet(text: str, word: str, radius: int = 500) -> str:
    """So'z topilgan joydan radius belgi oldin/keyin matn olish"""
    idx = text.lower().find(word.lower())
    if idx == -1:
        return ""
    start = max(0, idx - radius)
    end = min(len(text), idx + len(word) + radius)
    if start > 0:
        nl = text.rfind('\n', 0, start)
        if nl != -1:
            start = nl + 1
    if end < len(text):
        nl = text.find('\n', end)
        if nl != -1:
            end = nl
    snippet = text[start:end].strip()
    prefix = "...\n" if start > 0 else ""
    suffix = "\n..." if end < len(text) else ""
    return prefix + snippet + suffix

def search_json(query: str) -> list:
    """JSON dan qidirish — tarkibiy ma'lumot"""
    data = load_json()
    if not data:
        return []

    query_clean = query.strip().rstrip("?؟").strip().lower()
    words = [w for w in re.findall(r'\w+', query_clean) if len(w) > 2]
    if not words:
        return []

    results = []

    def search_in_section(obj, section_name: str):
        text = json_to_text(obj).lower()
        # To'liq ibora
        if query_clean in text:
            snippet = get_snippet(json_to_text(obj), query_clean, radius=400)
            results.append((20, f"📋 {section_name}", snippet))
            return
        # So'zlar bo'yicha
        score = sum(text.count(w) * (2 if len(w) > 4 else 1) for w in words)
        if score >= len(words):
            best = max(words, key=lambda w: len(w))
            snippet = get_snippet(json_to_text(obj), best, radius=400)
            if snippet:
                results.append((score, f"📋 {section_name}", snippet))

    # Bo'limlar bo'yicha qidirish
    sections = {
        "Shaxs ma'lumotlari": data.get("shaxs", {}),
        "Oilasi": data.get("oilasi", {}),
        "Hayot tarixi": data.get("hayot_tarixi", {}),
        "She'riyati": data.get("ijodi", {}).get("she_riyati", {}),
        "Nasriy asarlari": data.get("ijodi", {}).get("nasriy_asarlari", {}),
        "Tarjimonlik": data.get("tarjimonlik", {}),
        "Tanqidchilar baholari": data.get("tanqidchilar_baholari", {}),
        "Xotiralar va voqealar": data.get("qisqa_xotiralar_va_voqealar", {}),
        "Xalqaro aloqalar": data.get("adabiy_aloqalar_xalqaro", {}),
        "Shaxsiyati": data.get("shaxsiyat_va_xarakter", {}),
        "Asarlar ro'yxati": data.get("asarlar_ro'yxati_to'liq", {}),
        "Qo'shimcha ma'lumotlar": data.get("qo'shimcha_ma'lumotlar", {}),
    }

    for name, section in sections.items():
        if section:
            search_in_section(section, name)

    return results

def search_txt(query: str) -> list:
    """TXT fayllardan qidirish — badiiy matnlar"""
    txts = load_txts()
    if not txts:
        return []

    query_clean = query.strip().rstrip("?؟").strip()
    query_lower = query_clean.lower()
    words = [w for w in re.findall(r'\w+', query_lower) if len(w) > 2]
    if not words:
        return []

    results = []
    for title, content in txts.items():
        # Vikipediya va umumiy tarix fayllarini o'tkazib yuborish
        title_lower = title.lower()
        if any(s in title_lower for s in ["vikipediya", "wikipedia", "hayoti ijodi", "hayot ijod", "fikrlar"]):
            continue
        content_lower = content.lower()
        # To'liq ibora
        if query_lower in content_lower:
            snippet = get_snippet(content, query_clean, radius=500)
            results.append((20, f"📖 {title}", snippet))
            continue
        # So'zlar bo'yicha
        best = max(words, key=lambda w: len(w))
        if best in content_lower:
            score = sum(content_lower.count(w) for w in words if w in content_lower)
            snippet = get_snippet(content, best, radius=500)
            if snippet:
                results.append((score, f"📖 {title}", snippet))

    return results

def combined_search(query: str) -> list:
    """JSON + TXT birlashgan qidiruv"""
    json_results = search_json(query)
    txt_results = search_txt(query)
    all_results = json_results + txt_results
    all_results.sort(key=lambda x: x[0], reverse=True)

    # Takrorlarni olib tashlash
    seen = set()
    unique = []
    for score, title, snippet in all_results:
        key = snippet[:60].strip()
        if key not in seen and snippet.strip():
            seen.add(key)
            unique.append((score, title, snippet))

    return unique[:4]

def format_answer(query: str, results: list) -> str:
    if not results:
        return (
            f"❌ *'{query}'* haqida hech narsa topilmadi.\n\n"
            "💡 Boshqa so'z bilan sinab ko'ring:\n"
            "• Isim: `Toshbibi`, `G'afur G'ulom`\n"
            "• Asar: `Shum bola`, `Sen yetim emassan`\n"
            "• Mavzu: `urush`, `1903`, `mukofot`\n"
            "• Shaxs: `Oybek`, `Said Ahmad`"
        )

    if len(results) == 1:
        _, title, snippet = results[0]
        return f"{title}\n\n{snippet}"

    response = f"🔍 *'{query}'* bo'yicha *{len(results)} ta* natija:\n\n"
    for i, (_, title, snippet) in enumerate(results, 1):
        short = snippet[:600] + "\n..." if len(snippet) > 600 else snippet
        response += f"*{i}. {title}*\n{short}\n\n{'─' * 20}\n\n"
    return response

# ═══════════════════════════════════════
# HANDLERS
# ═══════════════════════════════════════

@router.message(F.text == "🔍 Qidirish")
async def start_search(message: Message, state: FSMContext):
    global _json_cache, _txt_cache
    _json_cache = None
    _txt_cache = None

    data = load_json()
    txts = load_txts()
    json_ok = "✅" if data else "❌"
    txt_count = len(txts)

    await state.set_state(SearchState.waiting)
    await message.answer(
        "🔍 *Qidirish*\n\n"
        f"{json_ok} JSON ma'lumotlar bazasi\n"
        f"📚 TXT fayllar: *{txt_count} ta*\n\n"
        "So'z yoki ibora yozing:\n\n"
        "💡 *Misol:*\n"
        "• `Toshbibi` — shaxs ismi\n"
        "• `Sen yetim emassan` — asar nomi\n"
        "• `mukofot` — mavzu\n"
        "• `Said Ahmad` — shaxs\n"
        "• `1903` — sana\n\n"
        "❌ Tugatish: /stop",
        parse_mode="Markdown"
    )

@router.message(F.text == "/stop")
async def stop_search(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("✅ Qidirish tugatildi.", reply_markup=main_menu())

@router.message(SearchState.waiting)
async def do_search(message: Message):
    query = message.text.strip()
    if not query:
        return

    wait_msg = await message.answer("🔍 Qidiryapman...")
    results = combined_search(query)
    await wait_msg.delete()

    response = format_answer(query, results)
    response += "\n\n💬 _Yangi so'z yozing yoki /stop bosing_"

    if len(response) > 4096:
        for chunk in [response[i:i+4000] for i in range(0, len(response), 4000)]:
            await message.answer(chunk, parse_mode="Markdown")
    else:
        await message.answer(response, parse_mode="Markdown")
