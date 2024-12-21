import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Função para buscar informações usando a URL da imagem
def search_image(url):
    api_url = "https://api.camgirlfinder.net/search"
    params = {"url": url}
    headers = {"User-Agent": "TelegramBot/1.0"}
    response = requests.get(api_url, params=params, headers=headers)
    return response.json()

# Função para buscar modelos por nome
def search_models(query):
    api_url = f"https://api.camgirlfinder.net/models/search?model={query}"
    headers = {"User-Agent": "TelegramBot/1.0"}
    response = requests.get(api_url, headers=headers)
    return response.json()

# Função do comando /foto (enviar a foto para o bot)
async def foto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        # Baixando a imagem enviada
        photo_file = update.message.photo[-1].get_file()
        photo_url = photo_file.file_path
        await update.message.reply_text(f"Recebi a foto! URL da imagem: {photo_url}")
        
        # Buscando pela imagem na API
        result = search_image(photo_url)
        await update.message.reply_text(f"Resultados para a foto: {result}")
    else:
        await update.message.reply_text("Por favor, envie uma foto com o comando /foto.")

# Função do comando /url (usar uma URL de imagem)
async def url_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Por favor, envie o comando assim: /url URL_DA_IMAGEM")
        return
    
    image_url = context.args[0]
    await update.message.reply_text(f"Pesquisando informações para a URL: {image_url}...")
    
    try:
        result = search_image(image_url)
        await update.message.reply_text(f"Resultados: {result}")
    except Exception as e:
        await update.message.reply_text(f"Ocorreu um erro: {str(e)}")

# Função do comando /perfil (buscar modelos)
async def perfil_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Por favor, envie o comando assim: /perfil NOME_DO_MODELO")
        return
    
    model_name = context.args[0]
    await update.message.reply_text(f"Buscando modelos para: {model_name}...")
    
    try:
        result = search_models(model_name)
        await update.message.reply_text(f"Modelos encontrados: {result}")
    except Exception as e:
        await update.message.reply_text(f"Ocorreu um erro: {str(e)}")

# Inicialização do bot
TOKEN = "7312259953:AAEiWZ7yLPRt5vTxArIksUWpBhNtvDx7pzU"  # Substitua pelo token do BotFather

app = ApplicationBuilder().token(TOKEN).build()

# Adicionando os handlers para cada comando
app.add_handler(CommandHandler("foto", foto_command))
app.add_handler(CommandHandler("url", url_command))
app.add_handler(CommandHandler("perfil", perfil_command))

# Iniciar o bot
print("Bot está funcionando!")
app.run_polling()
