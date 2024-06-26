# 16. Классификация декларативных программ по степени выразительности кода
Рассмотрим классификацию декларативных программ по их выразительности, чтобы определиться, какой подход на практике будет наиболее практичен.

1. Дескриптивная декларативщина (менее выразительная): декларативная программа просто определяет структуру данных. Это, например, языки HTML или XML, которые конечно слишком слабы, чтобы на них разрабатывать универсальные программы. Однако они удобны, когда требуются вычисления с соответствующими структурами данных (например, задать структуру документа, не указывая, как конкретно выполнять форматирование).

2. Программируемая декларативность (более выразительная). Это, например, язык, основанный на изученной декларативной вычислительной модели. Тут в свою очередь существуют два фундаментально отличных подхода:
2.1. дефиниционная форма, когда декларативщина есть свойство реализации компонента. Например, компонент, реализованный в декларативной модели, по определению будет гарантированно декларативным.
2.2. наблюдаемая форма, когда декларативщина есть свойство интерфейса компонента. Тут мы придерживаемся принципа абстракции: чтобы использовать компонент, достаточно знать его интерфейс, и не нужно знать реализацию. Компонент должен вести себя декларативно: быть независимым, stateless и детерминистичным, но необязательно реализованным в декларативной модели.

Для дефиниционной формы в свою очередь характерны два популярных стиля программирования: логический и функциональный. В функциональном стиле компонент -- это математическая функция, в логическом -- логическая взаимосвязь. Формально манипулировать функциями или логическим кодом труднее, нежели в случае дескриптивных программ, однако к ним по прежнему хорошо применимы алгебраические правила.

В наблюдаемой форме компоненты могут быть реализованы в любой вычислительной модели: главное, что в нашей декларативной программе они ведут себя декларативно, и доступны только через свои публичные декларативные интерфейсы (в частности, в парадигме абстрактных типов данных, которые мы изучали на курсе по ООАП).