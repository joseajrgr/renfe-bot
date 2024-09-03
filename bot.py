# bot.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
import asyncio
import re
from datetime import datetime, timedelta
from config import API_TOKEN, STATIC_JS_FILE, UPDATE_FREQUENCY
from utils.selenium_utils import buscar_trenes

# Leer el contenido del archivo .js
with open(STATIC_JS_FILE, "r", encoding="utf-8") as f:
    contenido_js = f.read()

# Extraer la parte relevante usando una expresión regular
patron = re.compile(r'estacionesEstatico\s*=\s*(\[[\s\S]*\]);', re.MULTILINE)
coincidencia = patron.search(contenido_js)

if coincidencia:
    estaciones_json = coincidencia.group(1)
    estaciones_json = estaciones_json.replace('null', 'None')
    estaciones = eval(estaciones_json)
else:
    estaciones = []

# Función para generar el teclado de estaciones
def generar_teclado_estaciones(tipo):
    botones = []
    for estacion in estaciones[:10]:  # Limitado a 10 estaciones 
        botones.append([
            InlineKeyboardButton(estacion["desgEstacion"], callback_data=f"{tipo}_{estacion['desgEstacion']}")
        ])
    return InlineKeyboardMarkup(botones)

# Función para generar el teclado de fechas
def generar_teclado_fechas():
    fechas = []
    for i in range(7):  # Mostrar las próximas 7 fechas
        fecha = (datetime.now() + timedelta(days=i)).strftime("%d/%m/%Y")
        fechas.append([
            InlineKeyboardButton(fecha, callback_data=f"fecha_{fecha}")
        ])
    return InlineKeyboardMarkup(fechas)

# Función para generar el teclado de trenes
def generar_teclado_trenes(trenes):
    botones = []
    for tren in trenes:
        botones.append([
            InlineKeyboardButton(f"Tren {tren['numero']}: {tren['hora_salida']}", callback_data=f"monitor_{tren['numero']}")
        ])
    return InlineKeyboardMarkup(botones)

# Función para manejar la selección de la estación de origen
async def seleccionar_origen(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Selecciona la estación de origen:", reply_markup=generar_teclado_estaciones("origen"))

# Función para manejar la selección de la estación de destino
async def seleccionar_destino(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Selecciona la estación de destino:", reply_markup=generar_teclado_estaciones("destino"))

# Función para manejar la selección de la fecha
async def seleccionar_fecha(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Selecciona la fecha de ida:", reply_markup=generar_teclado_fechas())

# Función para manejar la respuesta a los botones
async def boton_presionado(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("origen_"):
        context.user_data["origen"] = data.split("_")[1]
        await query.edit_message_text(text=f"Origen seleccionado: {data.split('_')[1]}")
        await seleccionar_destino(query, context)
    elif data.startswith("destino_"):
        context.user_data["destino"] = data.split("_")[1]
        await query.edit_message_text(text=f"Destino seleccionado: {data.split('_')[1]}")
        await seleccionar_fecha(query, context)
    elif data.startswith("fecha_"):
        context.user_data["fecha"] = data.split("_")[1]
        await query.edit_message_text(text=f"Fecha seleccionada: {data.split('_')[1]}")
        
        asyncio.create_task(buscar_y_mostrar_trenes(update, context))
    elif data.startswith("monitor_"):
        tren_numero = int(data.split("_")[1])
        context.user_data["tren_monitorizado"] = tren_numero
        await query.edit_message_text(text=f"Monitorizando el tren {tren_numero}. Te informaremos si hay disponibilidad.")
        asyncio.create_task(monitorizar_tren(update, context))

# Función para buscar y mostrar trenes usando Selenium
async def buscar_y_mostrar_trenes(update: Update, context: CallbackContext) -> None:
    origen = context.user_data.get("origen")
    destino = context.user_data.get("destino")
    fecha = context.user_data.get("fecha")

    trenes = buscar_trenes(origen, destino, fecha)

    if trenes:
        await update.callback_query.message.reply_text("Trenes disponibles:")
        await update.callback_query.message.reply_text("Selecciona el tren que deseas monitorizar:", reply_markup=generar_teclado_trenes(trenes))
        context.user_data["trenes"] = trenes  # Guardar trenes en el contexto
    else:
        await update.callback_query.message.reply_text("No se encontraron trenes disponibles.")

# Función para monitorizar el tren seleccionado
async def monitorizar_tren(update: Update, context: CallbackContext):
    tren_numero = context.user_data.get("tren_monitorizado")
    origen = context.user_data.get("origen")
    destino = context.user_data.get("destino")
    fecha = context.user_data.get("fecha")

    while True:
        trenes = buscar_trenes(origen, destino, fecha)
        tren_a_monitorizar = next((tren for tren in trenes if tren["numero"] == tren_numero), None)
        
        if tren_a_monitorizar:
            tren_disponible = tren_a_monitorizar["completo"] == 'Disponible'
            if tren_disponible:
                await update.callback_query.message.reply_text(f"Tren {tren_numero} está disponible.")
                break  # Detenemos la monitorización si el tren está disponible
            else:
                await update.callback_query.message.reply_text(f"Tren {tren_numero} sigue sin disponibilidad.")
        else:
            await update.callback_query.message.reply_text(f"No se encontró el tren {tren_numero}.")
        
        # Esperar X segundos antes de volver a buscar
        await asyncio.sleep(UPDATE_FREQUENCY)

# Función principal que configura el bot
def main() -> None:
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("origen", seleccionar_origen))
    application.add_handler(CommandHandler("destino", seleccionar_destino))
    application.add_handler(CommandHandler("fecha", seleccionar_fecha))
    application.add_handler(CallbackQueryHandler(boton_presionado))

    application.run_polling()

if __name__ == '__main__':
    main()