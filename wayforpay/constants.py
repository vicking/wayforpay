API_URL = "https://api.wayforpay.com/api"
PURCHASE_URL = "https://secure.wayforpay.com/pay"
REGULAR_API = "https://api.wayforpay.com/regularApi"
LANGUAGE = {'RU', 'UA', 'EN'}
PAYMENT_SYSTEM = {'card', 'privat24', 'lpTerminal', 'btc', 'credit', 'payParts', 'qrCode', 'masterPass',
                  'visaCheckout', 'googlePay', 'applePay'}
CURRENCY = {'UAH', 'USD', 'EUR', 'RUB', "AUD","BTC","BYN","CAD","CHF","CNY","CZK","EUR","GBP","HKD","ILS","JPY","KZT","PLN","RUB","SGD","USD"}
API_VERSION = 1

# https://wiki.wayforpay.com/pages/viewpage.action?pageId=852131

ERROR_CODES = {
    1100: "Операция выполнена без ошибок",
    1101: "Не удалось произвести оплату. Свяжитесь с вашим банком или воспользуйтесь другой картой",
    1102: "Не удалось произвести оплату.\nПожалуйста, убедитесь в правильности ввода параметров и повторите попытку",
    1103: "Не удалось произвести оплату.\nСвяжитесь с вашим банком или воспользуйтесь другой картой.\nПожалуйста, убедитесь в правильности ввода параметров и повторите попытку",
    1104: "Не удалось произвести оплату.\nНедостаточно средств на карте",
    1105: "Не удалось произвести оплату.\nСвяжитесь с вашим банком или воспользуйтесь другой картой.\nПожалуйста, убедитесь в правильности ввода параметров и повторите попытку",
    1106: "Не удалось произвести оплату.\nСвяжитесь с вашим банком или воспользуйтесь другой картой",
    1107: "",
    1108: "Свяжитесь с вашим банком или воспользуйтесь другой картой",
    1109: "Не удалось произвести оплату.\nПовторите попытку позже или свяжитесь с торговцем адрес которого производите оплату",
    1110: "Не удалось произвести оплату.\nПовторите попытку позже или свяжитесь с торговцем адрес которого производите оплату",
    1111: "",
    1112: "Не удалось произвести оплату.\nПовторите попытку позже или свяжитесь с торговцем адрес которого производите оплату",
    1113: "Не удалось произвести оплату.\nПовторите попытку позже или свяжитесь с торговцем адрес которого производите оплату",
    1114: "Не удалось произвести оплату.\nПовторите попытку позже или свяжитесь с торговцем адрес которого производите оплату",
    1115: "Не удалось произвести оплату.\nПовторите попытку позже или свяжитесь с торговцем адрес которого производите оплату",
    1116: "Не удалось произвести оплату.\nПовторите попытку позже или свяжитесь с торговцем адрес которого производите оплату",
    1117: "Не удалось произвести оплату.\nПовторите попытку позже или свяжитесь с торговцем адрес которого производите оплату",
    1118: "Не удалось произвести оплату.\nПовторите попытку позже или свяжитесь с торговцем адрес которого производите оплату",
    1119: "",
    1120: "Не удалось произвести оплату.\nСвяжитесь с вашим банком или воспользуйтесь другой картой",
    1121: "Не удалось произвести оплату.\nСвяжитесь с торговцем адрес которого производите оплату",
    1122: "Не удалось произвести оплату.\nПовторите попытку позже.\nЕсли сообщение выводится снова свяжитесь с нами, мы постараемся Вам помочь.",
    1123: "",
    1124: "Время на проведение платежа истекло, повторите попытку оплаты.",
    1125: "",
    1126: "",
    1127: "",
    1129: "",
    1130: "",
    1131: "Ваш платеж обрабатывается. Как только транзакция будет обработана, Вы получите уведомление о состоянии платежа",
    1132: "",
    1133: "Вами создан заказ .. на сайте … Сделать оплату Вы можете в течении ХХ часов ХХ минут.",
    1134: "Транзакция находится на ручной проверке сотрудника мониторинга.",
    1135: "Не удалось произвести оплату.\nПовторите попытку позже или свяжитесь с торговцем адрес которого производите оплату",
    1136: "",
    1137: "Верификация карты неуспешна",
    1138: "",
    1139: "Отказ в зачислении средств на карту получателя",
    1140: "Превышен лимит при зачислении средств на карту получателя.",
    1141: "Частичная отмена холда не доступна",
    1142: "Не удалось произвести оплату.",
    1143: "Неверный номер телефона",
    1144: "",
    1145: "Не удалось произвести оплату.\nСвяжитесь с вашим банком или воспользуйтесь другой картой",
    1146: "",
    1147: "",
    1148: "",
    1149: "",
    5100: "",
}
