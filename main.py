import telebot
import os
import pci_ti

API_KEY = os.environ["API_TELEGRAM_BOT"]
bot = telebot.TeleBot(API_KEY)
msg = 'Olá, eu sou o ConcursosTIBot'
msg2 = "Criado por Eduardo Vítor, meu objetivo é trazer concursos de todo o Brasil que ofertam vagas para a área de TI (Tecnologia da informação) do site PCI Concursos",
msg3 = 'Você têm 4 comandos nesse bot:\n/vagasanalista: concursos com vagas de analista de tecnologia e analista de sistemas\n/vagasprofessor: concursos com vagas de professor de TI efetivo e substituto\n/vagastecnico: concursos com vagas de técnico em informática\n/help: mostra novamente essa ajuda\n'

def construir_markup(item1, item2):
  markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
  btn1 = telebot.types.KeyboardButton(item1)
  btn2 = telebot.types.KeyboardButton(item2)
  markup.add(btn1,btn2)
  return markup
  
@bot.message_handler(commands=['start'])
def welcome(message):
  bot.send_message(message.chat.id, msg)
  bot.send_message(message.chat.id, msg2)
  bot.send_message(message.chat.id, msg3)

@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, msg3)

def handle_concursos(msg):
    if msg.text in pci_ti.CARGOS:
        return True

@bot.message_handler(commands=['vagasanalista'])
def vagas_analista(message):
  markup = construir_markup(pci_ti.CARGOS_ANALISTA[0],pci_ti.CARGOS_ANALISTA[1])
  bot.send_message(message.chat.id, "Escolha uma opção:",reply_markup=markup)

@bot.message_handler(commands=['vagasprofessor'])
def vagas_professor(message):
  markup = construir_markup(pci_ti.CARGOS_PROFESSOR[0],pci_ti.CARGOS_PROFESSOR[1])
  bot.send_message(message.chat.id, "Escolha uma opção:",reply_markup=markup)

@bot.message_handler(commands=['vagastecnico'])
def vagas_tecnico(message):
  markup = construir_markup(pci_ti.CARGOS_TECNICO[0],pci_ti.CARGOS_TECNICO[1])
  bot.send_message(message.chat.id, "Escolha uma opção:",reply_markup=markup)

@bot.message_handler(func=handle_concursos)
def get_concursos(message):
    concursos = pci_ti.scrapy_vagas(pci_ti.VAGAS_LINK_DIC[message.text])
    msg_resposta = pci_ti.formatar_msg(concursos)
    try:
       bot.send_message(message.chat.id,msg_resposta)
    except telebot.apihelper.ApiTelegramException as error:
       print(error)
       bot.send_message(message.chat.id,"Infelizmente, o Telegram possui um tamanho máximo de mensagem, a quantidade de vagas desse cargo é muito grande, logo não poderão ser exibidas aqui, verifique o site do PCI Concursos para ver os concursos disponíveis para a vaga.")
    

bot.infinity_polling(50)
