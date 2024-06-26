# 2. Синтаксис языка программирования
Синтаксис языка программирования определяет, что такое "законная" программа, которая может быть успешно скомпилирована.

Грамматика языка определяет, как правильно и допустимо строить "предложения" языка (обычно называемые инструкции или тоже предложения) из "слов" языка (обычно называемых токены).

Программа, которая получает на вход последовательность символов (обычный текстовый файл с кодом программы), и формирует из них последовательность токенов, называется лексический анализатор.

Программа, которая получает на вход последовательность токенов, и возвращает так называемое дерево разбора, отображающее структуру каждой инструкции, называется парсер. Подробнее эта тема разбирается на одном из моих дополнительных бесплатных курсов по алгоритмам.

Одна из наиболее распространённых нотаций для задания грамматик языков называется расширенная форма Бэкуса-Наура (EBNF).

Например, правило EBNF
```
‹digit› ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
задаёт одну цифру digit (любую из указанных девяти), а правило
‹int› ::= ‹digit› { ‹digit› } 
задаёт положительное целое int, которое состоит из одной цифры, за которой может следовать от нуля до любого количества цифр.
```
Грамматики подразделяются на зависящие (контекстно-зависимые) и не зависящие от контекста (контекстно-свободные). Например, во многих языках программирования требуется, чтобы тип переменной был явно объявлен до её первого использования, что подразумевает контекстную зависимость инструкций использования переменной от инструкций объявления переменной; однако на уровне синтаксиса нотация EBNF не умеет учитывать такую связь правил с контекстом. В то же время для описания синтаксиса языков применяются контекстно-свободные грамматики, подобные EBNF, потому что они проще и нагляднее, а на практике дополняются набором дополнительных условий.

Лингвистическая абстракция -- новая конструкция языка, расширяющая его синтаксис (например, новый оператор). Лингвистическая абстракция помогает не только повысить выразительность кода, но и улучшать корректность, безопасность и эффективность языка. Лингвистические абстракции активно применяются при создании новых языков.

Синтаксический сахар -- способ повышения читабельности кода и сокращения его размера через использование сокращённых нотаций (например, более компактная запись различных операторов).