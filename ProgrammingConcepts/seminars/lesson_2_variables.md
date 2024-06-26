# 2.1. Переменные и присваивание
Переменные в Julia вводятся автоматически, когда впервые указываются в левой части оператора присваивания "=" .

```
x = 2
println(3.14 + x)
```
В классическом понятии "переменная" традиционно объединяются две концепции: идентификатор (символьное имя переменной в исходном коде) и физическая ячейка в памяти, связанная с этим идентификатором и непосредственно хранящая значение переменной.

В массовых языках программирования, а также в Julia, по умолчанию подразумевается, что значение переменной может меняться в ходе работы программы. Однако существует фундаментальная концепция однократного присваивания, распространённая например в функциональном программировании: после того, как переменная в программе получила первое значение, она становится неизменяемой (своеобразный аналог константы времени выполнения).
Как правило, эта концепция дополняется механизмом явного объявления переменной, позволяющего повторно вводить в программу переменную с тем же идентификатором, задавая ей новое значение. В некотором смысле классическое присваивание переменной разных значений есть некоторая форма такого однократного присваивания с последующим автоматическим переопределением идентификатора в следующих операциях присваивания.

# 2.2. Строки
Строки в Julia заключаются в двойные кавычки, символьные литералы -- в одинарные кавычки.
К элементам строк можно обращаться по индексам (индексация в строках, массивах и списках в Julia начинается с 1):

```
println("Hello")
println("Hello"[2])
```
Внутрь строк можно включать выражения Julia (например, имена переменных), перед которыми ставится знак $ -- в таком случае вместо подобной конструкции с префиксом $ подставится значение выражения, вычисленное динамически.

```
n = 123
x = 23
println("n = $n ;") # n = 123 ;
println(" $(n*n-x)") # 15106

```
