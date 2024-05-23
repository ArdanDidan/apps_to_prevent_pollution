import discord
from discord.ext import commands
import pytz
from datetime import datetime, timedelta
import os
import random
import requests
import asyncio
from bot_logic import gen_pass

# NewsAPI key
newsapi_key = 'Token'

description = '''An example bot to showcase the discord.ext.commands extension module. There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Membuat klien bot
bot = commands.Bot(command_prefix='>', description=description, intents=intents)

# Menambahkan perintah untuk mendapatkan waktu berdasarkan zona waktu tertentu
@bot.command()
async def waktu(ctx, zona_waktu: str):
    try:
        timezone = pytz.timezone(zona_waktu)
        waktu_sekarang = datetime.now(timezone)
        waktu_format = waktu_sekarang.strftime('%H:%M')
        await ctx.send(f"Waktu saat ini di {zona_waktu} adalah {waktu_format}")
    except pytz.UnknownTimeZoneError:
        await ctx.send("Zona waktu tidak valid. Silakan coba lagi.")

# Menambahkan perintah untuk menetapkan pengingat waktu
@bot.command()
async def ingat(ctx, waktu: str, zona_waktu: str):
    try:
        timezone = pytz.timezone(zona_waktu)
        waktu_ingat = datetime.strptime(waktu, '%H:%M')
        waktu_ingat = timezone.localize(waktu_ingat)
        # Menghitung selisih waktu untuk pengingat
        now = datetime.now(timezone)
        selisih_waktu = waktu_ingat - now
        if selisih_waktu.total_seconds() <= 0:
            # Jika waktu sudah lewat, tambahkan 1 hari ke waktu yang diminta
            waktu_ingat += timedelta(days=1)
            selisih_waktu = waktu_ingat - now
        # Mengatur pengingat
        await asyncio.sleep(selisih_waktu.total_seconds())
        await ctx.send(f"Waktu yang diingatkan! Saat ini adalah {waktu_ingat.strftime('%H:%M')} di zona waktu {zona_waktu}.")
    except ValueError:
        await ctx.send("Format waktu tidak valid. Gunakan format HH:MM (misalnya, 10:30)")

# adding two numbers
@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

# spamming word
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)
        
# password generator        
@bot.command()
async def pw(ctx):
    await ctx.send(f'Kata sandi yang dihasilkan: {gen_pass(10)}')

# coinflip
@bot.command()
async def coinflip(ctx):
    num = random.randint(1,2)
    if num == 1:
        await ctx.send('It is Head!')
    if num == 2:
        await ctx.send('It is Tail!')

# rolling dice
@bot.command()
async def dice(ctx):
    nums = random.randint(1,6)
    if nums == 1:
        await ctx.send('It is 1!')
    elif nums == 2:
        await ctx.send('It is 2!')
    elif nums == 3:
        await ctx.send('It is 3!')
    elif nums == 4:
        await ctx.send('It is 4!')
    elif nums == 5:
        await ctx.send('It is 5!')
    elif nums == 6:
        await ctx.send('It is 6!')

# overwriting kalimat.txt
@bot.command()
async def tulis(ctx, *, my_string: str):
    with open('kalimat.txt', 'w', encoding='utf-8') as t:
        text = ""
        text += my_string
        t.write(text)

# append kalimat.txt
@bot.command()
async def tambahkan(ctx, *, my_string: str):
    with open('kalimat.txt', 'a', encoding='utf-8') as t:
        text = "\n"
        text += my_string
        t.write(text)

# reading kalimat.txt
@bot.command()
async def baca(ctx):
    with open('kalimat.txt', 'r', encoding='utf-8') as t:
        document = t.read()
        await ctx.send(document)

# random local meme image
@bot.command()
async def meme(ctx):
    img_name = random.choice(os.listdir('meme'))
    with open(f'meme/{img_name}', 'rb') as f:
    # with open(f'meme/enemies-meme.jpg', 'rb') as f:
        # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!
        picture = discord.File(f)
    await ctx.send(file=picture)

# API to get random dog image 
def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('dog')
async def dog(ctx):
    '''Setiap kali permintaan dog (anjing) dipanggil, program memanggil fungsi get_dog_image_url'''
    image_url = get_dog_image_url()
    await ctx.send(image_url)
# API to get random duck image
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('duck')
async def duck(ctx):
    '''Setiap kali permintaan duck (bebek) dipanggil, program memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)
# API to get random cat image
def get_cat_image_url():
    url = 'https://api.thecatapi.com/v1/images/search'
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        if data:  # Memastikan data tidak kosong
            return data[0]['url']
    return None
@bot.command('cat')
async def cat(ctx):
    '''Setiap kali permintaan Cat (Kucing) dipanggil, program memanggil fungsi get_cat_image_url'''
    image_url = get_cat_image_url()
    if image_url:
        await ctx.send(image_url)
    else:
        await ctx.send("Maaf, gagal mendapatkan gambar kucing.")
# API to get random Absurd Meme image
def get_memeabsurd_image_url():
    url = 'https://api.imgflip.com/get_memes'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        memes = data['data']['memes']
        meme = random.choice(memes)
        return meme['url']
    else:
        return None
@bot.command()
async def memeabsurd(ctx):
    """Sends a random absurd meme."""
    absurd_meme_url = get_memeabsurd_image_url()
    if absurd_meme_url:
        await ctx.send(absurd_meme_url)
    else:
        await ctx.send("Failed to fetch absurd meme.")

# welcome message
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

# Fungsi untuk mendapatkan artikel terkait polusi sampah dari NewsAPI
def get_trash_pollution_info():
    url = f'https://newsapi.org/v2/everything?q=trash%20pollution&apiKey={newsapi_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        if articles:
            article = random.choice(articles)
            return f"**{article['title']}**\n{article['description']}\n{article['url']}"
        else:
            return "Tidak ada artikel yang ditemukan tentang polusi sampah."
    else:
        return f"Terjadi kesalahan saat mengambil data: {response.status_code}"
# Menambahkan perintah untuk mendapatkan informasi tentang polusi sampah
@bot.command()
async def trashinfo(ctx):
    """Memberikan informasi tentang polusi sampah dan dampaknya menggunakan NewsAPI."""
    info = get_trash_pollution_info()
    await ctx.send(info)

# Menambahkan perintah untuk mendapatkan tips tentang cara mengurangi sampah harian
@bot.command()
async def tipssampah(ctx):
    """Memberikan tips tentang cara mengurangi sampah harian."""
    tips = [
        "Gunakan botol minum dan tas belanja yang dapat digunakan ulang.",
        "Pisahkan sampah organik dan non-organik untuk proses daur ulang yang lebih baik.",
        "Kurangi penggunaan kantong plastik dengan membawa tas belanja sendiri.",
        "Hindari pembelian produk dalam kemasan sekali pakai sebisa mungkin.",
        "Gunakan produk yang dapat diisi ulang seperti sabun cuci, shampoo, dan deterjen.",
        "Pilih barang-barang dengan kemasan minimal atau tanpa kemasan untuk mengurangi limbah kemasan.",
        "Kurangi penggunaan kertas dengan menggunakan email daripada surat fisik.",
        "Hemat penggunaan listrik dengan mematikan perangkat elektronik saat tidak digunakan.",
        "Gunakan alat dapur yang dapat digunakan kembali, seperti botol plastik bekas untuk menyimpan makanan atau menyimpan barang kecil.",
        "Beralih ke pembungkus makanan yang dapat digunakan kembali, seperti bungkus lilin lebah atau tas kain yang bisa dicuci.",
        "Gunakan produk pembersih yang ramah lingkungan dan dapat didaur ulang.",
        "Beli barang-barang bekas atau barang second-hand untuk mengurangi pembelian barang baru yang berpotensi menjadi sampah.",
        "Daftarlah ke dalam program pengambilan sampah yang dapat didaur ulang oleh pemerintah setempat jika tersedia."
    ]
    tip = random.choice(tips)
    await ctx.send(tip)

# Daftar panduan cara mendaur ulang sampah anorganik
panduan_daur_ulang = [
    "1. Pisahkan sampah anorganik seperti kertas, plastik, dan logam ke dalam tempat sampah terpisah.",
    "2. Gunakan kembali kemasan plastik bekas untuk menyimpan barang-barang kecil atau membuat kerajinan tangan.",
    "3. Daur ulang kertas bekas menjadi kertas baru dengan mengirimkannya ke tempat daur ulang kertas terdekat.",
    "4. Logam seperti kaleng dapat didaur ulang untuk membuat produk logam yang baru.",
    "5. Jika memungkinkan, gunakan kembali atau daur ulang peralatan elektronik bekas.",
    "6. Hindari membuang sampah elektronik ke tempat sampah umum, carilah tempat daur ulang elektronik yang terpercaya.",
    "7. Bila memungkinkan, gunakan kembali atau daur ulang kaca bekas untuk mengurangi limbah kaca.",
    "8. Simpan limbah elektronik beracun seperti baterai dan lampu pijar terpisah untuk didaur ulang dengan aman.",
    "9. Daur ulang plastik bekas dengan cara mengirimkannya ke pabrik daur ulang plastik atau menggunakan kembali produk plastik."
]
# Menambahkan perintah untuk memberikan panduan cara mendaur ulang sampah anorganik
@bot.command()
async def panduandaurulang(ctx):
    """Memberikan panduan cara mendaur ulang sampah anorganik."""
    # Memilih panduan secara acak dari daftar panduan
    panduan_terpilih = random.choice(panduan_daur_ulang)
    await ctx.send(panduan_terpilih)

bot.run('Token')
