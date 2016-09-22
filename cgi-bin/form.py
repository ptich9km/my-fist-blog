#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf8 -*- 
from __future__ import division
from docx import Document
from docx.shared import Inches

import os, sys
import cgi
import html
import codecs



ZERO = "ноль"

L_1_HE = HE = [ZERO, "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять", "десять",
    "одинадцать", "двенадцать", "тринадцать", "четырнадцать", "пятнадцать", 
    "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"]
    
L_1_SHE = SHE = [ZERO, "одна", "две"] + L_1_HE[3:]
    
L_10 = [ZERO, "десять", "двадцать", "тридцать", "сорок", "пятьдесят", 
    "шестьдесят", "семьдесят", "восемьдесят", "девяносто"]
    
L_100 = [ZERO, "сто", "двести", "триста", "четыреста", "пятьсот", 
    "шестьсот", "семьсот", "восемьсот", "девятьсот"]
    
N_ROUBLE = "рубл"
N_COP = "копе"
RUR = (N_ROUBLE, N_COP)

N_DOLLAR = "доллар"
N_CENT = "цент"
USD = (N_DOLLAR, N_CENT)

GENDER = {
    N_ROUBLE: HE,
    N_COP: SHE,
    N_DOLLAR: HE,
    N_CENT: HE,
}

N_1000 = "тысяч"
N_MILLION = "миллион"
N_BILLION = "миллиард"

ENDINGS = {
    N_ROUBLE:     ["ей", "ь", "я", "я", "я"] + 30 * ["ей"],
    N_COP:    ["ек", "йка", "йки", "йки", "йки"] + 30 * ["ек"],
    N_DOLLAR:    ["ов", "", "а", "а", "а"] + 30 * ["ов"],
    N_CENT:    ["ов", "", "а", "а", "а"] + 30 * ["ов"],
    N_1000:    ["", "а", "и", "и", "и"] + 30 * [""],
    N_MILLION:    ["ов", "", "а", "а", "а"] + 30 * ["ов"],
    N_BILLION:    ["ов", "", "а", "а", "а"] + 30 * ["ов"],
}

def write_1_to_999(n, gender_digits=HE):
    assert n<=999
    
    if n==0:
        return ZERO
    
    n_100 = n // 100
    n_10 = n % 100 // 10 
    n_1 = n % 10
    
    res = []
    res.append(L_100[n_100])
    
    if n_10 == 1:
        res.append(gender_digits[10*n_10 + n_1])
    else:
        res.append(L_10[n_10])
        res.append(gender_digits[n_1])
    return " ".join([s for s in res if s != ZERO])

def ending_index(n):
    n_2 = n % 100
    return n_2 if n_2 < 20 else n_2 % 10

def form_group_name(group, n):
    return group + ENDINGS[group][ending_index(n)]
    
def form_group(group, n, gender_digits=HE):
    return ("%s %s" % (write_1_to_999(n, gender_digits), form_group_name(group, n))) if n else ZERO

def write_number(n, gender_digits=HE):
    assert type(n) in (int, float)
    if n==0:
        return ZERO
    
    n_3 = n % 10**3
    n_6 = n % 10**6 // 10**3
    n_9 = n % 10**9 // 10**6
    n_12 = n % 10**12 // 10**9
    
    #print n_12, n_9, n_6, n_3
    res = []
    
    res.append(form_group(N_BILLION, n_12))
    res.append(form_group(N_MILLION, n_9))
    res.append(form_group(N_1000, n_6, SHE))
    res.append(write_1_to_999(n_3, gender_digits))
    
    return ", ".join([s for s in res if s != ZERO])

def write_price(n_rub, n_cop=0, currency=RUR):
    rub_id, cop_id = currency
    n = int(n_rub)
    res = []
    res.append("%s %s" % (write_number(n, GENDER[rub_id]), form_group_name(rub_id, n)))
    res.append(form_group(cop_id, n_cop, GENDER[cop_id]))
    
    return " и ".join([s for s in res if s != ZERO])
    

if __name__ == "__main__":
    print (write_price (1111082))

    form = cgi.FieldStorage()
    text1 = form.getfirst("TEXT_1", "not")
    text2 = form.getfirst("TEXT_2", "not")
    investor = form.getfirst("investor", "not")
    investpoluch = form.getfirst("investpoluch", "not")
    works1 = form.getfirst("works1", "not")
    works2 = form.getfirst("works2", "not")
    works3 = form.getfirst("works3", "not")
    text1 = html.escape(text1)
    text2 = html.escape(text2)
    
    
    def str_to_float(str):
        # попробуем воспользоваться самым простым методом преобразования из str в float
        try:
            return float(str)
        except:
            # других вариантов не осталось. скорее всего функция приняла на входе мусор
            return 0
    
    texttoflaoat = str_to_float(text2)
    
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    
    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Data use</title>
            </head>
            <body>""")
    
    print("<h1>Договор</h1>")
    print("<p>Номер: {}</p>".format(text1))
    print("<p>Инвестор: {}</p>".format(investor))
    print("<p>Инвест получатель: {}</p>".format(investpoluch))
    print("<p>Строительство: {}</p>".format(works1))
    print("<p>Отделка: {}</p>".format(works2))
    print("<p>Устройство территории: {}</p>".format(works3))
    
    print("<h1>Сумма</h1>")
    print("<p>Сумма по договору: {}</p>".format(write_price(texttoflaoat)))
    
    print("""</body>
            </html>""")
    print("<p><input type=submit value=Toggle id=toggle1 /></p>")
    

    

