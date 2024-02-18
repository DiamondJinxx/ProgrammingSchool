# 6. Типовая хипстерская архитектура: ошибочный паттерн
Клиенту мы предоставим совершенно оригинальный API, который инкапсулирует (полностью скроет) нашу реализацию.

Серверный API:
```
import pure_robot

# класс Чистильщик API
class CleanerApi:

    # конструктор 
    def __init__(self):
        self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

    # взаимодействие с роботом вынесено в отдельную функцию
    def transfer_to_cleaner(self,message):
        print (message)

    def get_x(self):
        return self.cleaner_state.x

    def get_y(self):
        return self.cleaner_state.y

    def get_angle(self):
        return self.cleaner_state.angle

    def get_state(self):
        return self.cleaner_state.state

    def activate_cleaner(self,code):
        for command in code:
            cmd = command.split(' ')
            if cmd[0]=='move':
                self.cleaner_state = pure_robot.move(self.transfer_to_cleaner,
                    int(cmd[1]),self.cleaner_state) 
            elif cmd[0]=='turn':
                self.cleaner_state = pure_robot.turn(self.transfer_to_cleaner,
                    int(cmd[1]),self.cleaner_state)
            elif cmd[0]=='set':
                self.cleaner_state = pure_robot.set_state(self.transfer_to_cleaner,
                    cmd[1],self.cleaner_state) 
            elif cmd[0]=='start':
                self.cleaner_state = pure_robot.start(self.transfer_to_cleaner,
                    self.cleaner_state)
            elif cmd[0]=='stop':
                self.cleaner_state = pure_robot.stop(self.transfer_to_cleaner,
                    self.cleaner_state)
```
Клиентская часть:
```
from client_cleaner_api import ClientCleanerApi

# главная программа
cleaner_api = ClientCleanerApi()

cleaner_api.activate_cleaner((
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
    ))

print (cleaner_api.get_x(), 
    cleaner_api.get_y(), 
    cleaner_api.get_angle(), 
    cleaner_api.get_state())
```

Клиенту код реализации API будет недоступен -- ему лишь известно, что имеется класс ClientCleanerApi с пустым конструктором и методами activate_cleaner() и get_*(). На самом деле в этом классе API могут быть и другие методы, но в нашем игрушечном примере мы не рассматриваем способы сокрытия кода в Python и предоставления клиенту интерфейсной информации (практика, распространённая в С++ или Java).

Фактически и наш интерфейсный API, и код pure_robot.py размещаются и выполняются на сервере, и каким способом клиентам представляется доступ к этому API, мы не рассматриваем (взаимодействие клиента с сервером скрыто в классе ClientCleanerApi клиентской библиотеки). Например, это может быть набор обычных HTTP-вызовов, никоим образом с питоновским форматом не связанных.

Клиентов, понятно, может быть множество, и для каждого из них на сервере будет создан отдельный экземпляр класса CleanerAPI, который будет хранить внутри себя текущее состояние взаимодействия. Контроль за созданием и удалением таких серверных объектов CleanerAPI и идентификация клиента на протяжении сессии возлагаются на серверный фреймворк.

Плюсы.

Реализация Чистильщика полностью скрыта от клиента и тем самым неплохо защищена.

Способ взаимодействия клиента и сервера скрывается внутри классов ClientCleanerAPI и CleanerAPI. Мы можем использовать HTTP, SOAP или что угодно другое, свободно заменять эти схемы, клиенту подобные модификации будут совершенно незаметны.

Добавление промежуточного уровня CleanerAPI позволяет включать в него сервисы дополнительной валидации результатов оригинальных вычислений, а также добавлять всевозможные схемы балансировки нагрузки, внутреннего роутинга на сервере и т. п.

Минусы.

Хотя реализация CleanerAPI недоступна клиенту, на неё тем не менее полностью ориентирован клиентский интерфейс ClientCleanerAPI.

Вся система мутабельна и завязана на текущие состояния внутренних серверных объектов, что существенно усложняет отладку.

Хоть клиент и не знает конкретную реализацию, ему косвенно доступны расшаренные значения серверных полей.
