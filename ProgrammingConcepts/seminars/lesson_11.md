# 11. Поток данных Dataflow

Что произойдет, если операция попытается использовать переменную, которая еще не определена (идентификатор не связан с конкретным значением)? Даже с эстетической точки зрения было бы неплохо, если бы операция просто подождала, когда в эту переменную загрузится некоторое первичное значение. Например, переменную инициализирует какая-нибудь другая нить, и затем данная операция сможет продолжить работу. Такая парадигма называется dataflow (поток данных).

Её наивная реализация потенциально даже не требует поддержки работы с неопределёнными переменными. Можно просто использовать некоторые значения как флажки, показывающие, может ли операция продолжаться, как и реализовано в различных распространённых языках программирования. Опасность такой ситуации как раз в том, что мы явно привязываемся к конкретным состояниям (а не к их отсутствию), что всегда чревато ошибками, ну и выразительность и простота кода существенно снижается. А ведь именно качественное различие в выразительности кода и формирует различные парадигмы.

В документации Julia приводится такой пример:

Thread 1:
```
global b = false
global a = rand()
global b = true
```

Thread 2:
```
while !b; end
use(a)
```

Вторая нить ждёт, когда флажок "b" станет истинным (а это произойдёт, только когда в первой нити переменная "a" получит некоторое случайное значение), и лишь после этого начинает обработку переменной "a".

# 11. Dataflow (2)

В Julia при желании можно смоделировать и схему с неопределённой переменной, так как формально переменные до их первой инициализации действительно остаются в неопределённом состоянии. Обращение к неопределённой переменной вызовет ошибку времени выполнения UndefValError.
Имеется макро @isdefined, которое проверяет, определена ли некоторая переменная x: 

```
println(@isdefined z) # false
z = 32
println(@isdefined z) # true
```
Таким образом, факт определения значения некоторой переменной, которая ранее была не определена, может служить флагом для продолжения работы процесса, контролирующего эту переменную.

Thread 3:
```
while ! @isdefined(a); end
use(a)
```
Тут надо учитывать потенциальную опасность memory unsafe в конкретном языке, когда например значение переменной "a" может непредсказуемо меняться в разных нитях. Обычно для этого применяется паттерн lock(a)/unlock(a), который блокирует возможность изменения некоторой глобальной переменной другими нитями до окончания её использования.


В целом, парадигма Dataflow отличается, во-первых, независимыми корректными вычислениями -- независимо от того, как они распределяются по параллельным процессам.
Например, имеются три функции, первая из которых возводит глобальную переменную X в квадрат, как только она будет определена. Вторая функция задаёт переменной X значение 9, и третья функция выполняет задержку работы всей программы на 10 секунд. В каком бы порядке мы не стали вызывать эти функции, как бы мы не распределили их по нитям, в парадигме Dataflow итог всегда будет один и тот же: программа замирает на 10 секунд и выдаёт значение 81.
И во-вторых, сами вычисления скромны и терпеливы: они не посылают никаких сигналов, а просто ждут, когда активизируются нужные им данные.
Добавление нитей и временных задержек в программу может кардинально изменить форму её работы, но до тех пор, пока одни и те же операции вызываются с одними и теми же аргументами, результаты программы всегда будут одними и теми же. Это ключевое свойство dataflow-параллелизма. Поэтому данная парадигма предоставляет множество преимуществ параллелизма без излишних сложностей, обычно ему присущих.