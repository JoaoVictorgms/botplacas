import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import pandas as pd
import threading
from telegram import Update

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Função para ler apenas a coluna R do arquivo Excel e imprimir o número de linhas
def print_excel_info(file_path):
    df = pd.read_excel(file_path, usecols='R')
    num_rows = df.shape[0]
    print(f'O arquivo Excel possui {num_rows} linhas.')

print_excel_info('jardiel_base.xlsx')
placas_df = pd.read_excel('jardiel_base.xlsx', usecols='R')
placas = placas_df.iloc[:, 0].dropna().tolist()
df_all_info = pd.read_excel('jardiel_base.xlsx')

def check_placa_info(placa, resultados):
    for index, row in df_all_info.iterrows():
        if str(row.iloc[17]).strip().upper() == placa:
            resultados.append(row.to_dict())
            return
    resultados.append(None)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Envie uma placa de carro para verificar se ela está na planilha.')

async def verificar_placa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    placa = update.message.text.strip().upper()

    if not placa:
        await update.message.reply_text('Por favor, envie uma placa válida.')
        return

    num_threads = 10
    resultados = []
    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=check_placa_info, args=(placa, resultados))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if any(resultados):
        result = next((res for res in resultados if res is not None), None)
        if result:
            response = f'A placa {placa} está na planilha.\nInformações:\n'
            for key, value in result.items():
                response += f'{key}: {value}\n'
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(f'A placa {placa} não está na planilha.')
    else:
        await update.message.reply_text(f'A placa {placa} não está na planilha.')

async def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verificar_placa))
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
