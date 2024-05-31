import asyncio
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def print_excel_info(file_path):
    df = pd.read_excel(file_path, usecols='R')
    num_rows = df.shape[0]
    print(f'O arquivo Excel possui {num_rows} linhas.')

print_excel_info('jardiel_base.xlsx')
placas_df = pd.read_excel('jardiel_base.xlsx', usecols='R')
placas = placas_df.iloc[:, 0].dropna().tolist()
df_all_info = pd.read_excel('jardiel_base.xlsx')

def check_placa_info(placa):
    resultados = []
    for index, row in df_all_info.iterrows():
        if str(row.iloc[17]).strip().upper() == placa:
            resultados.append(row.to_dict())
            return resultados
    resultados.append(None)
    return resultados

async def start(update, context):
    await update.message.reply_text('Envie uma placa de carro para verificar se ela está na planilha.')

async def verificar_placa(update, context):
    placa = update.message.text.strip().upper()

    if not placa:
        await update.message.reply_text('Por favor, envie uma placa válida.')
        return

    resultados = await asyncio.to_thread(check_placa_info, placa)

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

async def main():
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, verificar_placa))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    asyncio.run(main())
