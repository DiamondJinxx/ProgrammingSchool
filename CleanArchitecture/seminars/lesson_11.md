# 11. Функциональная инъекция зависимостей-2

Пожалуй, главный недостаток последнего подхода в том, что мы передавали в качестве параметров пять разных функций. Но строго говоря, когда у функции много параметров, это верный признак плохого дизайна (при использовании функционального стиля разработки). Никогда не требуется столь много параметров, если главная функция действительно независима. Конечно, можно передавать список функций одним параметром, однако всё равно в нём нам потребуется ровно пять функций, что не очень здорово.

Сейчас мы организуем инъекцию зависимостей, в которой обойдёмся всего одной функцией вместо пяти.

Реализуйте схему функциональной инъекции с одной функцией вместо пяти -- так, как вы это понимаете.