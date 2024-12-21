import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Função para buscar informações usando a URL da imagem
def search_image(url):
    api_url = "https://api.camgirlfinder.net/search"
    params = {"url": url}  # Passa a URL da imagem como parâmetro
    headers = {"User-Agent": "TelegramBot/1.0"}  # Cabeçalho de User-Agent
    response = requests.get(api_url, params=params, headers=headers)  # Faz a requisição GET
    return response.json()  # Retorna a resposta como um JSON

# Função para buscar modelos por nome
def search_models(query):
    api_url = f"https://api.camgirlfinder.net/models/search?model={query}"  # URL para buscar por modelos
    headers = {"User-Agent": "TelegramBot/1.0"}  # Cabeçalho de User-Agent
    response = requests.get(api_url, headers=headers)  # Faz a requisição GET
    return response.json()  # Retorna a resposta como um JSON

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
        result = search_image(image_url)  # Chama a função que usa a API
        
        # Formata a resposta da API de forma legível
        if result.get('success'):  # Verifica se a API retornou um sucesso
            data = result.get('data', [])
            if data:
                # Caso a resposta contenha dados, formate-os e envie-os
                response_text = "Resultados encontrados:\n"
                for item in data:
                    response_text += f"Link da Imagem: {item.get('image_url')}\n"
                    response_text += f"Modelo: {item.get('model_name')}\n\n"
                await send_long_message(update, response_text)
            else:
                await update.message.reply_text("Nenhum resultado encontrado para essa URL.")
        else:
            await update.message.reply_text(f"Erro ao buscar a imagem: {result.get('error', 'Desconhecido')}")
    
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

# Função para enviar mensagens longas
async def send_long_message(update, text):
    # Envia a resposta em múltiplas mensagens se for longa
    max_length = 4000  # Limite de caracteres por mensagem no Telegram
    for i in range(0, len(text), max_length):
        await update.message.reply_text(text[i:i+max_length])

# Inicialização do bot
TOKEN = os.getenv("TELEGRAM_TOKEN")  # Usa a variável de ambiente para o token

# Criação do bot
app = ApplicationBuilder().token(TOKEN).build()

# Adicionando os handlers para cada comando
app.add_handler(CommandHandler("foto", foto_command))
app.add_handler(CommandHandler("url", url_command))
app.add_handler(CommandHandler("perfil", perfil_command))

# Iniciar o bot
print("Bot está funcionando!")
app.run_polling()
