# 22. Корректность с инвариантами состояния

Как уже говорилось, в декларативной модели многие важные вещи реализуются достаточно легко (в частности, доказательство формальной корректности кода). Рассмотрим общую технику такого доказательства на примере функции IterLen -- эта техника легко применяется и к IterRev, и к другим итеративным вычислениям.

Идея этой техники, что мы определяем некоторое свойство P(S-i) состояния (свойство P для i-го состояния S), о котором мы всегда можем сказать (доказать), что оно истинно. Такое свойство называется инвариант состояния. Для простоты можно считать, что это свойство -- предикат (некоторая аксиома тождественности).

Если P выбрано удачно, то корректность всего вычисления будет автоматически получено из истинности P(S-final).

Какое состояние мы выбрали для IterLen? Напомню, это пара {длина уже обработанного списка, оставшийся список} -- (i,Ys). На основе этого состояния и исходного списка Xs введём такое свойство:

P( (i,Ys) ) : length(Xs) = i + length(Ys)
Оно утверждает, что длина всего списка Xs для любого состояния равна текущему значению длины i из этого состояния плюс длина оставшегося списка Ys (второй элемент состояния).

1. Докажем истинность P(S-0). Исходное состояние будет (0, Xs), из чего следует, что length(Xs) = 0 + length(Xs).

2. Из P(S-i), где S-i ещё не заключительное состояние, должно следовать S-i+1. Это будет следовать из семантики оператора if и вызова функции. Пусть S-i = (i,Ys). Так как это ещё не заключительное состояние, длина Ys будет ненулевой. Из семантики, i+1 в коде увеличит i в состоянии на один, а Ys в следующем состоянии станет нынешний Ys без первого элемента. Отсюда доказана истинность P(S-i).

3. Так как Ys будет постоянно уменьшаться на один элемент, мы гарантированно придём к заключительному состоянию S-final, в котором Ys будет пустым списком: (i, []), а функция возвращает i. Так как length([]) = 0, из P(S-final) следует, что i = length(Xs).

Мы доказали это "вручную", но сегодня уже существует немало пруф-ассистантов, которые способны выполнять подобные доказательства корректности автоматичски.

Понятно, что наиболее трудный шаг в таком процессе -- это выбор инварианта, свойства P, подразумевающий определённое мастерство. В этом поможет, в частности, такое ограничение, накладываемое на P: свойство должно комбинировать аргументы итерационных вычислений так, чтобы результат не менялся по ходу этих вычислений. Другими словами, мы подбираем, например, некоторый предикат, который задаёт какую-то наглядную и явно истинную характеристику состояния.

Например, в случае функции обращения списка Xs, где состояние -- это пара {уже обращённая часть списка Rs, оставшаяся необработанная часть списка Ys}, в состоянии S-i можно потребовать, чтобы элемент Rs[end] был равен Xs[end - i + 1] (при индексации с единицы), а необработанная часть списка на каждом шаге сокращалась.

Другими словами, в уже обращённой части списка на i-м шаге её последний элемент всегда будет end-i+1 -м элементом в исходном списке (отсчитываем i с конца исходного списка).

Xs = [1,2,3,4,5]
S[1] = 5 + 1,2,3,4
S[2] = 5,4 + 1,2,3
S[3] = 5,4,3 + 1,2
...