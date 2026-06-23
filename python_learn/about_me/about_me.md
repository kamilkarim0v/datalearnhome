Запрос 1:
Купил себе пк 13400f rx 6600 xt 32 ddr4, несколько ssd 512 m2, 512 sata, 240 sata. Работаю bi аналитиком Jin+ в компании, переведся недавно 2 месяца назад, до этого был специалистом по анализу данных в аналитическом отделе в этой же компании. Стек gp, clickhouse, superset, zeppelin, jira, confluence. Знаю как оптимизировать запросы. До этой компании был аналитиком в одной небольшой химической компании, там был скудный стек из postgres, ms sql, excel. Запросы почти не писал, в основном работал в excel, но было много свободного времени, там я успел пройти курс по python (база, + функциональное программирование - писал декораторы/обертки функций, решал простые задачи и тд). Когда еще был в той компании понял что хочу больше работать дата инженером, так как не очень люблю заказчиков и решать какие-то адхуки постоянные, это как будто люди не умеют писать запросы в бд, и просят меня, сам данные я не анализирую а просто выгружаю им в необходимых разрезах. В нынешней компании все получше с этим, есть спринты и планирование задач, ты что-то хоть анализируешь и ищешь какие-то проблемы, но в основном эти проблемы с качеством конечных данных, а 80% задач это добавить что-то новенькое в отчет superset, либо разработать новый, так же есть регулярные задачи по расчеты выплат для сотрудников ГПД - что я считаю не совсем аналитической задачей, а больше бухгалтерской. Однако там есть множество сложных логик мотиваций, которые надо прописать в sql, что неплохо поднимает скилл. Но из-за частных изменений в мотивации сложно придумать какую-то единую структуру, которую можно будет изменять - меняются как и условия мотиваций сотрудников, так и сами проекты живут относительно не долго и приходиться что то писать новое. Если честно это очень надоедает со временем и кажется что ты не особо этим хотел заниматься когда шел в аналитики. В аналитику я попал достаточно недавно. Прошел курс за 9 месяцев по одной из программ онлайн школ, сам имею высшее техническое образование совсем из другой области. Честно говоря шел в IT из-за денег, но потом понял что это совсем не золотая жила, а реальная работа, но все же она меня увлекла. Однако с каждым разом убеждаюсь, что мне хочется стать дата инженером быть более подкованном в техническом плане - как образуются данные, как они переливаются из одного места в другое, как строить модели и как не потерять хороший кусок информации в этом пути бесконечных трансформаций и загрузок выгрузок из одного места в другое. В новой компании я неплохо познакомился с инфраструктурой и примерно понимаю как все устроено: есть множество систем - приложение, система заявок, лендинги, брокеры и тд. Из них данные проливаются 2 основными путями, это батчевая и стриминговая загрузка, в основном там используются топики Kafka и nifi, из разных систем все попадает в dwh на gp в так называемый сырой слой, основным инструментом для построения модели данных из сырого является airflow, но у нас он досрочно сильно переработан и интегрирован в другую систему автоматизированного CI CD/деплоя в прод, далее используются множество аналитических инструментов для работы, что-то похожее на zeppelin - helicopter. Он имеет несколько видов параграфов (sql, python, markdown). Сам sql параграф вызывает множество разных движков типо gp, clickhouse statist(что-то типо данных из amplitude), clickhouse proteus (данные из superset), dlh - появился недавно, так как сейчас активно переезжаем с dwh на dlh(данные будут храниться в parquet на s3, и будет 2 движка - trino и sparksql) и тд. Короче что-то да я знаю и в целом могу представить картину чем должны заниматься DE, но все же что мне нужно учить, как нужно учить, какой уровень python нужен, насколько хорошо нужно знать docker и Linux чтобы развернуть пет проект у себя на новом компьютере и пощупать все инструменты самому, насколько нужно знать git чтобы из петпроекта сделать портфолио для работодателей, Kafka nifi airflow clickhouse dbt. А возможно ты просто даш совет не идти в DE , а стать кем-то другим?

Мне приходилось работать с api - я делал отчет который просил сообщения из одного из каналов нашего корпоративного мессенджера - в нем писались обращения по созданию маркировок рекламы для блоггеров, если сообщение помещалось реакцией :eyes: - то означало что обращение взято в работу, далее оно помещалось :checkmark: - это означало что оно выполнено, далее я собрал такие сообщения, по тексту разбил их на категории и посчитал среднее время выполнения по командам, логинам; общее количество запросов в динамике по юнитам команд и тд. Все данные я получал в json и приходилось работать и с ним. Собрал удобную структуру в df pandas и рассчитывал метрики. Так же был опыт работы с докером, в принципе я понимаю что такое volume, как его прописывать, знаю что такое build и прописывал networks, но все это было на домашнем пк старом, в котором я просто игрался, работал в терминале линукса на уровне ls -a, пытался научиться писать конфиги на vim(но запутался :) ), git вот вообще не изучал, но у меня есть GitHub портфолио и там я как-то залил свою первые аналитические расчеты в ipynb, пытался поднять airflow и написать свой первый даг, но безуспешно, потом отложил все на поздний срок, так как не было на это времени, но сейчас я купил новый компьютер и обещал себе что за год я стану middle data engineer


То что нужно для junior DE.

Список (только заголовки):

- Linux (базовая работа в терминале, права, процессы, cron)

- Git (commit, push, pull, branch, merge, conflict resolution)

- Docker (Dockerfile, docker-compose, volumes, networks)

- Python для DE (не для DS: работа с API, базами, файлами, логами, исключениями)

- SQL (оконные функции, CTE, индексы, планировщик, транзакции)

- PostgreSQL (настройка, пользователи, схемы, бэкапы)

- Airflow (DAG, операторы, сенсоры, XCom, Connections, Variables)

- ClickHouse (отличия от PostgreSQL, движки таблиц, партиционирование)

- Kafka (топики, продюсеры, консьюмеры, consumer groups)

- dbt (модели, materializations, тесты, документация)

- Spark (DataFrame, SQL, lazy evaluation, простые трансформации)

- Хранилища данных (DWH, DLH, медленно меняющиеся измерения, слои raw/ods/dm)

- Форматы данных (JSON, Parquet, Avro, CSV)

- Orchestration & мониторинг (логи, алерты, retry, backfill)


Уровень владения скиллами:

1. Linux.

Где-то в 2024 году, когда работал на заводе. Я на отдельный диск поставил себе ubuntu и начинал что-то изучать. Что-то пытался настроить себе графический интерфейс чтоб было похоже на macOs, чтобы окно было с красным/желтым/зеленым круглешками (развернуть, свернуть, закрыть). Потом копался с дизайном терминала (пытался поставить красивый zsh.
научился перемещаться в терминале, ls cd mkdir - это все что я сейчас помню.
После я все это удалил и когда купил ПК поставил чистую убунту.

2. Git. 
С гитом я познакомился когда учился на аналитика данных на курсах, причем взаимодействовал я с ним чисто через веб гитхаб, загрузил туда чистые ноутбуки (.ipynb) причем все описания писал в них же в md параграфах.
На этом у меня с ним знакомство и закончилось.
Я знаю что он помогает контролировать версии и подключать кучу разработчиков к одному проекту, к каждой ветке пишутся тесты и проверяются доработки и потом только это merge joinтся с основным проектом.

3. Docker

С докером я познакомился когда в 2024 году изучал линукс, причем я даже пытался пройти курс, но тоже не до конца.
Помню что у докера есть сущность демона, имаджи разных версий (латест и др), знаю что между всеми контейнерами нужно прописывать сети от текущей локальной машины к машине в которой развернуто приложение - порт 1111:2222, что сам докер разворачивает приложение на виртуальной машине с необходимыми для развертки компонентами, чтобы избежать несовместимости версий/компонент. Знаю про докер компосе файл в котором все это прописывается - volume это указывает какая деректория на локальной машине = дериктории на виртуальной машине.
Сам компос никогда не писал, либо забирал готовый, либо просил gpt/deepseek написать за себя.
Знаю команды docker run docker ps -a и больше вроде ничего (ну и docker-compose up|docker compose down)

4. Python.

Ну тут дела достаточно сложные, вроде много чего знал, иногда кажется что вообще ничего не знаю.

Много работал с pandas даже задач 20 на leetcode решил.
Много курсов проходил 
Решал задачи на leetcode на python3
задачи на hash таблицы, на хэш-списки (set), на словари - в основном все изи задачи (их уже наверное около 50 накопилось).
Работал с matplotlib, pandas, seaborn.
И все это было так давно, что кажется это все не правдой.
Сейчас работа с питоном происходит на готовых библиотеках в компании (функции gp_to_df, df_to_gp) - причем в основном это просто скачать excel из облака, немного преобразовать, переименовать, и загрузить в gp и вся работа с ним продолжается уже в sql.
есть конечно всякие исключения, например мне надо было обернуть таблицу из gp в json и отправлять в s3 но и там я попросил просто gpt сделать все это за меня. (Иногда надо отдать быстро и ты делаешь ничего не понимая). Просто создал 2 ключа и по готовой функции загрузил json(который собирается тоже по готовому коду от gpt) в s3.
Я например понимаю как работать со строками, как написать цикл, даже list comprehention (надеюсь правильно написал) знаю.
Лямбда функции +- map, просто функции.
Есть курс где я проходил Обертки для готовых функций, докстринг и аннотации.
typing и тд.
И как бы это что-то, но мне кажется что это вообще ничего.
Python забывается и я ничего не могу с этим сделать, так как это не работает.
Можешь даже не просить писать на работе на python потому что я работаю с большими данными и sql там просто напросто мощнее(144 кластера).

5. SQL 

По началу я его не очень любил, так как считал что это не язык программирования, а обычный декларативный язык. Было не понятно как писать вообще на нем и тд. На первой работе вообще на нем ничего не писал, только фильтры какие-то менял и все, выгружал, вставлял данные в excel - отчет готов.

После перехода в другую компанию sql стал для меня основным рабочим инструментом.
В основном я пишу запросы в БД по такой схеме:
drop table if exists appls;
create table appls as 
select application_rk,
    crm_income_dt,
    product_rk,
    ...
from prod_v_emart.applicarion -- бизнес слой ви выполняешь запросы, а в DWH - выполняешь запросы в DWH.трин

Так же там использую окнные функции, cte, вложенные запросы union union all 
Большие сложные витрины собираю по своему направлению и через инкремент
Например 
когда-то создал витрину через drop|create в песочнице и убираю этот параграф с расписания.

Далее делю темп витрину:
drop table if exists temp_transaction;
create table tamp_transaction as 
select transaction_rk,
    application_rk,
    transaction_dttm,
    transaction_dttm::date as transaction_dt,
    crm_income_dt,
from prod_v_emart.transaction t
inner join appls a on a.account_rk = t.account_rk and a.account_rk is not null
where t.transaction_dttm >= current_date - interval '7 days';

drop table if exists temp_transaction_filtered; выполняешь запросы, а в DWH - выполняешь запросы в DWH.
create table temp_transaction_filtered as 
select *
from temp_transaction
where crm_income_dt < transaction_dt;

begin;

delete
from usr_wrk.retail_transaction
where transaction_rk in (
    select transaction_rk
    from temp_transaction_filtered
);

insert into usr_wrk.retail_transaction
select *
from temp_transaction_filtered;

commit;

Тут первый запрос я дулю на 2 так как если я в первом запросе укажу в фильтре или в джойне crm_income_dt < transaction_dt, то он начнет смотреть на транзакции за ранней период, и читает все партиции а не только за последний месяц.

Дальше по этим транзакциям я считаю нарастающий итог через оконки и дату наструпления транзакций на 500, 1000, 1500р и тд и считаю всякие метрики по картам.

Понятия как индексы и что-то еще я не трогаю, так как это настраивают инженеры на своем уровне, а меня как аналитика это не трогает и если я захочу, мне никто не даст этого сделать.

Надеюсь тут по sql понятен уровень.


6. PostgreSQL.

Тут касался этой темы очень мало. Был у меня как-то PgAdmin в то время как я учился на домашнем ПК, в котором я что-то там создавал.
Помню даже через терминал заходил, там даже что-то делал, но это было 1 день увлечения и я уже ничего не помню.

7. Airflow

С аирфлоу такая же ситуация. Я как бы понимаю что такое акциклический граф - что он направленный и состоит из задач, что его нельзя обернуть в цикл какой-то, он должен быть с началом и концом, что его можно распараллелить на не трогающие друг друга таски в одном даге. Знаю что аирфлоу имеет в себе web UI, что есть папочка dags, что есть библеотека которую нужно импортировать чтобы писать даг, нужно определить даг, потом в тасках указывать даг (таски причем офомляются через фукнцию), каждая таска несет в себе какой-то оператор (не обязательно) - PythonOperator, SQLOperator, BashOperator (знаю только 3).
Даги сам никогда не писал, знаю только что направление тасок рисуется в конце через ">>"

8. ClickHouse

С кликом не сталкивался прям часто. У меня на работе он используется под BI-системой. Знаю что клик это такая БД которая хранит не построчно, а по колоночно. Что его слабые места это джойны, что сильные это огромные витрины с 100+ столбцами, что обращаться через select * лучше не стоит (хотя это для всех БД правило, но для клика особенное). Не нравится из-за своеобразного синтаксиса через Camel Case, хотя это не обязательно.

9. Kafka

Никогда не касался с этой технологией. Знаю только что это брокер сообщений, который используют для стриминга, что есть топик в который записывают данные и потом их перекидывают как-то на БД, для меня это вообще пока темный лес, но очень хочу с этим поработать(так сказать данные в реалтайм). Слышал еще про NiFi, не знаю связано это как-то с кафка, но это тоже используют для стриминга.

10. dbt

Много слышал и все по разному - но никогда не работал с этим. Сначала был слух что это что-то похожее на airflow, потом говорят что это вообще строить трансформации данных на лету, короче не знаю.

11. Spark

Не работал с ним напрямую. Сейчас у нас в компании идет переезд с DWH(GP) на DLH из-за сложности масштабирования DWH из-за простоты DLH. У нас в DLH реализованы движки (воркеры). Оба они  SQL - Trino, SparkSQL. То есть ты в самом интерпретаторе (мы работаем в инструменте на подобии Jupter Notebook) выбираешь либо Trino, либо SparkSQL.
Сам PySpark я как бы не трогаю, но в домашних условиях я его вызывал, но очень мало. Создавал спарк сессию, игрался с dataframe, что-то пытался, через sparksql типо селект, фильтр, групбай.
На этом знакомство закончилось.
В принципе понимаю что это мастхэв в большим распределенных системах, таких как hdfs, s3 и тд. Что он сам знает на каких кластерах лежат части данных, что он очень отказоустойчивый, хранит промежутки расчетов в темпфайлах и тд.

12. Хранилища данных

Тут тоже что-то есть, чего-то нет. Как и рассказывал у нас есть 4 слоя (+между каждыми есть технические слои), есть реплики (к ним обращаюсь редко), bissness слой, интерпрайз слой.

Знаю что есть Инмон (star schema), Кимбалл(dimension modeling), DV 1, DV2, Anchor. Таить не буду, много путаюсь, что есть что. Знаю что DV1 это dimension modeling с 3NF.
Что якорь это очень сложная для построения сущность и ее редко используют, хотя они все сложные. Знаю про scd только то, чем пользуюсь на работе. у нас такие витрины записываются в dds припиской и имеют поля valid_from, valid_to. Например это клиент у которого там возраст поменялся, или номер его телефона, или поменялась фамилия.

13. Форматы данных

Работал только в json, csv. Знаю что есть parquet(тоже хранит инфу по столбцам), avro, iceberg(по моему для хранения метаинфы), xml (не знаю, работают ли с ним еще кто-то)

14. Orchestration & мониторинг

С этим вообще не работал. Слышал и видел только библеотеку logging.


Оцени пожалуйста мой уровень, только без лжи, расскажи реально, на что я могу рассчитывать.

А потом поговорим о дальнейшем развитии.


Чем я сейчас занимаюсь:

2026-06-21.
Я 5 тый день работаю над проектом. Начал им заниматься, так как распылялся на много новых инструментов - где-то поучил python, где-то почитал про spark, потом зачем-то начал решать алгоритмы. Проект дал мне какую-то идею, например я взял над собой челлендж пушить каждый день в проект хоть что-то. Буквально вчера я осмыслял свой проект, вот промты которые я писал:
"Привет я сегодня сильно переосмыслил свой проект) Я проанализировал свой проект и многое для себя решил сегодня. Начну про себя.
Я аналитик BI - который очень хочет перейти в DE, но многого не понимает, как в части разработки, так и в части моделирования баз, так и в инструментах DE.
Сейчас я активно пишу свой сервис дома (я начал этим заниматься только потому что я сильно распылялся в обучении DE - один день смотрел видео по какому-либо инстументу, потом пытался решать задачи на leetcode, потом изучал алгоритмы, потом изучал spark и никаких результатов это само собой не дало).
Я пошел к ИИ за советом и он дал один простой совет, просто писать и пушить git каждый день.
Но чтоб было что запушить, надо что-то сделать. Вот и делаю
Изначально я просто нашел API T-Invest и пытался что-то выгрузить, просил ИИ сделать это за меня. Но SDK Python не хочет работать, так как толи санкции, толи сертификаты.
И я начал писать напрямую через API, тоже попросил ИИ написать за меня. Он написал, скрипт запускается, но я в нем ничего не понимаю. И я начал писать сам, как умею, без функций но с полным пониманием.
Первый скрипт который я выдал был app.py
он выгружал свечи в интервале 15 минут за последние сутки.
Скрипт я доработал, но он сильно не тянет на ООП и стандартные подходы к разработке, но я буду этому учиться.
Далее я делал всякие доработки (занимаюсь этим 5 дней уже и каждый день пушу). Вот хотел бы Readme переделать.
Хочу добавить что проект тестовый или учебный.
Вот то что я переосмыслил:
"За сегодня я решил, что надо предать своему проекту смысл, как с точки зрения разработки, так и с точки зрения DE.
Я решил описать себе на листке что я хочу от этого проекта.
1) Это научится загружать данные из API в БД батчами, научиться работать с json, научиться работать с API.
2) Научиться работать со стримом, загружать данные стримом (возможно научиться работать с Kafka и тд)
3) Писать реально продукт как разраб, сейчас у меня обычный аналитический скрипт. А я хочу if __name__ == __main__ (или как там они пишут на ООП, ахахах)
4) я хочу получить продукт, который реально работает:
- для начала я определяю инструмент, на котором хочу заработать.
- потом я выгружаю с помощью своего приложения статистику по инструменту.
- далее скрипт готовит аналитику или какой-то предикт, возможно сам покупает и выставляет стоп лос тейк профит
- оценивает риски
- читает новости в месте с ИИ."

То есть сам app.py - теперь это будущий метод какой-то большой программы и теперь он называется get_candles.py
вот. Как это все красиво описать, чтобы если ко мне и придут смотреть что-то.

И меня еще смущает что это все похоже на то, что я пишу какой-то SDK который и так уже есть)"

Сейчас у меня новые мысли о проекте, так как сейчас главная цель не стать же каким-то супер разработчиком, сейчас главное это получить навыки DE. Основные это Airflow и DBT. Тогда я смогу перейти уже на какую-то грань BI-инженер.

Помимо этого у меня есть мысли на релокацию. Возможно не прям скорую, но помимо профессии мне нужен английский.

ЧТО Я ОТ ТЕБЯ ХОЧУ, ХОЧУ ЧТОБЫ ТЫ БЫЛ МОИМ СОВЕТНИКОМ, МОИМ АССИСТЕНТОМ ПО РАЗВИТИЮ И КАКИМ-ТО МЕНТОРОМ. Я БУДУ ВЕСТИ С ТОБОЙ ЧАТ ПОЧТИ КАЖДЫЙ ДЕНЬ. У МЕНЯ ЕСТЬ АССИСТЕНТЫ ПО README, ПО ПРОЕКТУ И ТД.








Сейчас я расскажу тебе про свой проект, покажу свой основной скрипт, docker-compose и readme.md. Я работал над ним 5 дней и вот что получил.


readme:

# T-Invest API to Postgres ETL Pipeline

Учебный ETL-пайплайн для загрузки биржевых свечей из API T-Invest в PostgreSQL.

## Текущий статус
Проект в активной разработке. Сейчас — этап исследования API и подготовки модулей для загрузки данных. Код пока простой (без ООП), но с полным пониманием каждого действия.

## Что делает
Стягивает свечи по заданному тикеру и сохраняет в БД. Если запустить повторно — новые данные добавятся, старые не перезатрутся (инкрементальная загрузка).

## Технологии
- Python (requests, pandas, sqlalchemy)
- PostgreSQL (в Docker)
- API T-Invest

## Структура
```
├── get_candles.py         # модуль загрузки свечей (бывший app.py)
├── docker-compose.yml     # подъем PostgreSQL
├── .env.example           # шаблон для .env
├── .env                   # твои личные данные (не в репозитории)
├── sql.ipynb              # Jupyter-ноутбук для работы с БД
└── dev/                   # директория для экспериментов
    ├── get_assets.ipynb   # тестовый ноутбук: получение списка акций
    └── get_currencies.ipynb # тестовый ноутбук: получение списка валют
```

## Как запустить

1. Скопируй и заполни `.env`:
```bash
cp .env.example .env
# открой .env и впиши свой T_TOKEN
```

2. Подними базу:
```bash
docker-compose up -d
```

3. Запусти скрипт:
```bash
python get_candles.py
```

---

## О проекте

Проект родился из желания каждый день делать коммиты и учиться на практике, а не просто смотреть видео. Постепенно он обрастает смыслом: от простого скрипта к полноценному приложению.

Пока это учебный pet-проект, но в планах:
- Переписать код в ООП-стиле
- Добавить потоковую загрузку (WebSocket / Kafka)
- Настроить аналитику по инструментам
- И в перспективе — торговые сигналы

---

## Roadmap (план развития)

**Короткий срок (ближайшие дни):**
- [x] Написать get_candles.py (загрузка свечей)
- [x] Исследовать API: получить список валют и акций
- [ ] Научиться парсить акции
- [ ] Добавить обработку ошибок и retry-механизмы

**Средний срок (недели):**
- [ ] Рефакторинг: переход на ООП
- [ ] Инкрементальная загрузка с учетом пропусков
- [ ] Собрать из модулей (get_candles, get_assets, get_currencies) единое приложение

**Долгосрочно:**
- [ ] Потоковая загрузка (WebSocket → Kafka)
- [ ] Аналитические витрины по инструментам
- [ ] Торговые сигналы (Stop Loss / Take Profit)
- [ ] AI-аналитика новостей

---

## 2026-06-19 Что изменилось.

**Теперь подключение к БД идет через переменные из `.env`**, а не зашито в коде:
- было: `postgresql://postgres:postgres@localhost:5432/dwh_data`
- стало: `postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}`

**Плюс** полностью переписан `docker-compose.yml` — теперь он свой, а не скопированный из стороннего репозитория.

**Добавлен вывод статистики** после загрузки — скрипт теперь показывает общее количество свечей, сохраненных в базе. Можно сразу видеть результат работы и контролировать, что данные действительно пополняются.

**Добавлен `sql.ipynb`** — Jupyter-ноутбук с шаблоном для работы с БД через SQLAlchemy. Удобно писать и тестировать запросы, сразу видеть результат в виде DataFrame, не запуская каждый раз основной скрипт. Полезно для анализа данных и отладки.

---

## 2026-06-20 Что изменилось.

**Ренейм app.py >> get_candles.py** — теперь этот скрипт запускается как отдельный модуль, а не как основной скрипт. В будущем он станет частью большого приложения.

**Добавлена директория `dev/`** — сюда складываю экспериментальные ноутбуки. Пока там:
- `get_assets.ipynb` — пробую получать список акций
- `get_currencies.ipynb` — получаю список валют (работает)

**Добавлена утилита** — функция, которая переводит CamelCase в snake_case (подсмотрел у GPT и добавил в `get_candles.py`). Мелочь, но делает данные чище.

**Переосмысление проекта:** решил, что это не просто скрипт, а учебный трек в Data Engineering. Вместо бесконечной теории — практика каждый день. Проект будет расти: от загрузки свечей до аналитики и торговых стратегий. `get_candles.py` — это первый кирпичик.

---

скрипт:
### 1.Работа с API. Извлечение данных изи OpenAPI T-Invest.
import os
import re
import requests
import logging
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

TOKEN = os.getenv('T_TOKEN')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
URL = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"

headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

intervals_dict = {
    "1min": "CANDLE_INTERVAL_1_MIN",
    "5min": "CANDLE_INTERVAL_5_MIN",
    "15min": "CANDLE_INTERVAL_15_MIN",
    "hour": "CANDLE_INTERVAL_HOUR",
    "day": "CANDLE_INTERVAL_DAY"
}

figi = "BBG004730N88" # FIGI Сбербанк
interval = '15min'
from_dt = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
to_dt = datetime.now(timezone.utc).isoformat()

data = {
    "figi": figi,
    "from": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
    "to": datetime.now(timezone.utc).isoformat(),
    "interval": intervals_dict[interval]
}

logging.info(f"Запрос к API: figi={figi}, interval={interval}, from={from_dt}")

response = requests.post(url = URL, headers=headers, json=data)

if response.status_code == 200:
    # return response.json()
    df = pd.json_normalize(response.json()['candles'], sep='_')
    df.head()
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)
    # return None
    print(None)

logging.info(f"Получено {len(df)} свечей из API")

### 2. Обработка DF данных.
df['open'] = df['open_units'].astype(float) + df['open_nano'] / 1000000000
df['close'] = df['close_units'].astype(float) + df['close_nano'] / 1000000000
df['high'] = df['high_units'].astype(float) + df['high_nano'] / 1000000000
df['low'] = df['low_units'].astype(float) + df['low_nano'] / 1000000000
df['interval'] = intervals_dict[interval]
df['figi'] = figi


def camel_to_snake(name):
    """Преобразует camelCase в snake_case"""
    # Вставляем _ перед заглавными буквами (кроме первой)
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)

    return name.lower()

# Применяем ко всем столбцам
df.columns = [camel_to_snake(col) for col in df.columns]

### 3. Подключение к БД Postgres (Docker). Разово создаем витрину (если нужно).

conn = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}') # postgres docker
cursor = conn.connect()

# Создаю витрину если нужно
sql = '''
    CREATE TABLE IF NOT EXISTS candles (
        time TIMESTAMPTZ,
        figi VARCHAR(255),
        interval VARCHAR(255),
        open DECIMAL(12,2),
        close DECIMAL(12,2),
        high DECIMAL(12,2),
        low DECIMAL(12,2),
        is_complete BOOLEAN,
        candle_source VARCHAR(255),
        volume BIGINT,
        volume_buy BIGINT,
        volume_sell BIGINT,
        open_units BIGINT,
        open_nano BIGINT,
        close_units BIGINT,
        close_nano BIGINT,
        high_units BIGINT,
        high_nano BIGINT,
        low_units BIGINT,
        low_nano BIGINT,
        PRIMARY KEY (time, figi, interval)
    )
'''

cursor.execute(text(sql))
cursor.commit()


#создаем temp_candles с нужными типами данных
sql = '''
    DROP TABLE IF EXISTS temp_candles;
    CREATE TABLE IF NOT EXISTS temp_candles (
        time TIMESTAMPTZ,
        figi VARCHAR(255),
        interval VARCHAR(255),
        open DECIMAL(12,2),
        close DECIMAL(12,2),
        high DECIMAL(12,2),
        low DECIMAL(12,2),
        is_complete BOOLEAN,
        candle_source VARCHAR(255),
        volume BIGINT,
        volume_buy BIGINT,
        volume_sell BIGINT,
        open_units BIGINT,
        open_nano BIGINT,
        close_units BIGINT,
        close_nano BIGINT,
        high_units BIGINT,
        high_nano BIGINT,
        low_units BIGINT,
        low_nano BIGINT,
        PRIMARY KEY (time, figi, interval)
    )
'''

cursor.execute(text(sql))
cursor.commit()

#загружаю данные в temp_candles
df.to_sql(
    'temp_candles', 
    conn, 
    if_exists='append', 
    index=False,
    method='multi'
)

logging.info(f"Загружено {len(df)} строк в temp_candles")

#делаю инкрементальную загрузку
sql = '''
    DELETE FROM candles
    WHERE (time, figi, interval) IN (
        SELECT time, figi, interval 
        FROM temp_candles
    );
    INSERT INTO candles
    SELECT * FROM temp_candles;
'''
cursor.execute(text(sql))
cursor.commit()
cursor.close()

logging.info("Инкрементальная загрузка завершена")

#Проверка на дубликаты
sql = '''
    select figi, interval, time, count(*) as cnt_rows
    FROM candles 
    GROUP BY figi, interval, time
    HAVING COUNT(*) > 1;
'''
df_test_db = pd.read_sql(sql, conn)

if df_test_db.empty:
    logging.info("Нет дубликатов")
else:
    logging.error("Есть дубликаты")
    logging.error(df_test_db.to_string())

#Общее кол-во сохраненных свечей
sql = '''
    SELECT COUNT(*) FROM candles;
'''
df_test_db = pd.read_sql(sql, conn)
logging.info(f"Общее кол-во сохраненных свечей: {df_test_db.iloc[0, 0]}")

docker-compose:
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: postgres_db
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - '5432:5432'
    
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:



Тут я тебе в кратце даю со своим ассистентом по проекту (он тоже deepseek как и ты, и он со мной 7 дней):
Ну привет) Вчера вечером выделил время, поработал над гитом и над созданием и настройкой venv.

Не очень сложно как оказалось.
Работал с командами git status
git add .
echo ".env" >> .gitignore

добавил имя и емейл
пока не коммитил ничего

Сегодня сел в 8:00
Начал разбираться с api
решил что самый простой путь это sdk, но оказалось нет.
Мучался с документацией, полез на гитхаб, там ничего не понятно. Пошел к deepseek, но и он мне не помог.
Как оказалось есть через команду устанавливается актуальный пакет sdk: $ pip install t-tech-investments --index-url https://opensource.tbank.ru/api/v4/projects/238/packages/pypi/simple

но pip его не пропускает из-за сертификата и код не запускался.
Потом мы пошли в обход на старые библиотеки tinkoff.invest и tinkoff.investments, у них проблема в том что они старые и последние версии недоступны в pip (толи они из-за санкций заблочены, толи не понятно).

В итоге deepseek предложил собрать данные напрямую через openapi
Я зарегал токен, сохранил его как нужно в .env, и вызвал его через dotenv
было интересно поработать.

В целях чтобы что-то заработало, я тестил каждый код который мне давал ИИ, в итоге в некоторых местах поправлял сам и код заработал.
Скажу честно, я сам мало что там написал, но вроде читаю код и понимаю все.
Отдельно попросил код для сохранения сразу в БД sqlite3 и в отдельном ноуте написал сам скрипт по вытаскиванию данных оттуда.
import sqlite3
import pandas as pd

conn = sqlite3.connect('candles.db')
cursor = conn.cursor()

sql = '''
select *
from candles
'''

df = pd.read_sql(sql, conn)

print(df.head(15))
(venv) kam@kam-MS-7D48:~/datalearnhome$ /home/kam/datalearnhome/venv/bin/python /home/kam/datalearnhome/SQL.py
    id          figi                  time    open    high     low   close  volume  is_complete           created_at
0    1  BBG004730N88  2026-06-14T06:45:00Z  322.67  322.67  322.67  322.67    1600            1  2026-06-15 06:57:49
1    2  BBG004730N88  2026-06-14T07:00:00Z  322.66  322.66  322.27  322.50   26729            1  2026-06-15 06:57:49
2    3  BBG004730N88  2026-06-14T07:15:00Z  322.50  322.59  322.43  322.53   20020            1  2026-06-15 06:57:49
3    4  BBG004730N88  2026-06-14T07:30:00Z  322.53  322.60  322.48  322.58   31322            1  2026-06-15 06:57:49
4    5  BBG004730N88  2026-06-14T07:45:00Z  322.58  322.60  322.48  322.57   13411            1  2026-06-15 06:57:49
5    6  BBG004730N88  2026-06-14T08:00:00Z  322.59  322.59  322.37  322.40   41272            1  2026-06-15 06:57:49
6    7  BBG004730N88  2026-06-14T08:15:00Z  322.45  322.54  322.40  322.50   11231            1  2026-06-15 06:57:49
7    8  BBG004730N88  2026-06-14T08:30:00Z  322.50  322.50  322.40  322.48   12513            1  2026-06-15 06:57:49
8    9  BBG004730N88  2026-06-14T08:45:00Z  322.48  322.48  322.41  322.43    4924            1  2026-06-15 06:57:49
9   10  BBG004730N88  2026-06-14T09:00:00Z  322.43  322.50  322.40  322.49   25359            1  2026-06-15 06:57:49
10  11  BBG004730N88  2026-06-14T09:15:00Z  322.49  322.50  322.42  322.43   18646            1  2026-06-15 06:57:49
11  12  BBG004730N88  2026-06-14T09:30:00Z  322.44  322.44  322.04  322.04   72959            1  2026-06-15 06:57:49
12  13  BBG004730N88  2026-06-14T09:45:00Z  322.09  322.20  322.05  322.19   24093            1  2026-06-15 06:57:49
13  14  BBG004730N88  2026-06-14T10:00:00Z  322.19  322.22  322.07  322.08   37968            1  2026-06-15 06:57:49
14  15  BBG004730N88  2026-06-14T10:15:00Z  322.08  322.08  322.03  322.04   22434            1  2026-06-15 06:57:49

Сам скрипт загрузки:
import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('T_TOKEN')

def get_candles(figi, from_date, to_date, interval):
    """Прямой запрос к REST API Tinkoff"""
    url = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "figi": figi,
        "from": from_date.isoformat(),
        "to": to_date.isoformat(),
        "interval": interval
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)
        return None

def parse_candle(candle):
    """Преобразует свечу из формата Tinkoff в обычные числа"""
    return {
        'time': candle['time'],
        'open': float(candle['open']['units']) + candle['open']['nano'] / 1e9,
        'high': float(candle['high']['units']) + candle['high']['nano'] / 1e9,
        'low': float(candle['low']['units']) + candle['low']['nano'] / 1e9,
        'close': float(candle['close']['units']) + candle['close']['nano'] / 1e9,
        'volume': int(candle['volume']),
        'is_complete': candle['isComplete']
    }

# Константы интервалов
INTERVALS = {
    "1min": "CANDLE_INTERVAL_1_MIN",
    "5min": "CANDLE_INTERVAL_5_MIN",
    "15min": "CANDLE_INTERVAL_15_MIN",
    "hour": "CANDLE_INTERVAL_HOUR",
    "day": "CANDLE_INTERVAL_DAY"
}

# Получаем свечи
candles_data = get_candles(
    figi="BBG004730N88",
    from_date=datetime.now(timezone.utc) - timedelta(days=1),  # за последние сутки
    to_date=datetime.now(timezone.utc),
    interval=INTERVALS["15min"]
)

if candles_data:
    print("Время | Открытие | Максимум | Минимум | Закрытие | Объем")
    print("-" * 70)
    for candle in candles_data.get("candles", []):
        parsed = parse_candle(candle)
        print(f"{parsed['time']} | {parsed['open']:.2f} | {parsed['high']:.2f} | {parsed['low']:.2f} | {parsed['close']:.2f} | {parsed['volume']}")






###########################################
# Сохраняем в базу
###########################################

import sqlite3

def save_candles_to_db(candles_data, figi, db_name="candles.db"):
    """Сохраняет свечи в SQLite"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            figi TEXT,
            time TIMESTAMP,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            is_complete BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    for candle in candles_data.get("candles", []):
        parsed = parse_candle(candle)
        cursor.execute("""
            INSERT INTO candles (figi, time, open, high, low, close, volume, is_complete)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (figi, parsed['time'], parsed['open'], parsed['high'], 
              parsed['low'], parsed['close'], parsed['volume'], parsed['is_complete']))
    
    conn.commit()
    conn.close()
    print(f"Сохранено {len(candles_data.get('candles', []))} свечей в {db_name}")

# Сохраняем в базу
if candles_data:
    save_candles_to_db(candles_data, "BBG004730N88")



Сегодня занимался по такому плану:
Я решил полностью переписать код в ipynb и переделать его на свой уровень знаний (без функций, без всяких обработок, которые я не знаю и не понимаю). Пока этим занимался время прошло незаметно, + смотрел методы как сразу писать в бд без каких либо сохранений в переменную data_candles и так далее, но пока не разобрался.
Пока просто переписывал код столкнулся с ошибкой 400 код 3 (нашел в документации это "interval is invalid"), пока с этим тоже не разобрался, видимо это ошибка в генерации даты (я хотел взять данных чуть глубже - хотя бы с начала июня).
Короче, есть чувство что сегодня ничего не сделал, хотя упорно сидел все 2 часа (даже начал пораньше).

Вот что успел написать:

import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('T_TOKEN')
URL = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"

headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

intervals_dict = {
    "1min": "CANDLE_INTERVAL_1_MIN",
    "5min": "CANDLE_INTERVAL_5_MIN",
    "15min": "CANDLE_INTERVAL_15_MIN",
    "hour": "CANDLE_INTERVAL_HOUR",
    "day": "CANDLE_INTERVAL_DAY"
}

figi = "BBG004730N88"
from_date = '2026-06-16'
to_date = datetime.today().strftime('%Y-%m-%d')
interval = '15min'

data = {
    "figi": figi,
    "from": datetime.fromisoformat(from_date).isoformat(),
    "to": datetime.fromisoformat(to_date).isoformat(),
    "interval": intervals_dict[interval]
}
response = requests.post(url = URL, headers=headers, json=data)

if response.status_code == 200:
    # return response.json()
    df = pd.DataFrame(response.json()['candles'])
    df.head()
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)
    # return None
    print(None)

В гит ничего не грузил пока вокруг только сплошные черновики


Привет, сегодня с утра не получилось посидеть, так как пришлось поработать, но вечером вместо 2х часов работы я поучился.
Все что сделал:
### 1.Работа с API. Извлечение данных изи OpenAPI T-Invest.
import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('T_TOKEN')
URL = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.MarketDataService/GetCandles"

headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

intervals_dict = {
    "1min": "CANDLE_INTERVAL_1_MIN",
    "5min": "CANDLE_INTERVAL_5_MIN",
    "15min": "CANDLE_INTERVAL_15_MIN",
    "hour": "CANDLE_INTERVAL_HOUR",
    "day": "CANDLE_INTERVAL_DAY"
}

figi = "BBG004730N88" # FIGI Сбербанк
interval = '15min'
from_dt = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
to_dt = datetime.now(timezone.utc).isoformat()

data = {
    "figi": figi,
    "from": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
    "to": datetime.now(timezone.utc).isoformat(),
    "interval": intervals_dict[interval]
}
response = requests.post(url = URL, headers=headers, json=data)

if response.status_code == 200:
    # return response.json()
    df = pd.json_normalize(response.json()['candles'], sep='_')
    df.head()
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)
    # return None
    print(None)


### 2. Обработка DF данных.
df['open'] = df['open_units'].astype(float) + df['open_nano'] / 1000000000
df['close'] = df['close_units'].astype(float) + df['close_nano'] / 1000000000
df['high'] = df['high_units'].astype(float) + df['high_nano'] / 1000000000
df['low'] = df['low_units'].astype(float) + df['low_nano'] / 1000000000
df['interval'] = intervals_dict[interval]
df['figi'] = figi


ren_col = {
    'isComplete': 'is_complete',
    'candleSource': 'candle_source',
    'volumeBuy': 'volume_buy',
    'volumeSell': 'volume_sell'
}

df = df.rename(columns=ren_col)

### 3. Подключение к БД Postgres (Docker). Разово создаем витрину (если нужно).
from sqlalchemy import create_engine, text

conn = create_engine('postgresql://postgres:postgres@localhost:5051/postgres') # 5051 это бд под клиентом Airflow
cursor = conn.connect()

# Создаю витрину если нужно
sql = '''
    CREATE TABLE IF NOT EXISTS candles (
        time TIMESTAMPTZ,
        figi VARCHAR(255),
        interval VARCHAR(255),
        open DECIMAL(12,2),
        close DECIMAL(12,2),
        high DECIMAL(12,2),
        low DECIMAL(12,2),
        is_complete BOOLEAN,
        candle_source VARCHAR(255),
        volume BIGINT,
        volume_buy BIGINT,
        volume_sell BIGINT,
        open_units BIGINT,
        open_nano BIGINT,
        close_units BIGINT,
        close_nano BIGINT,
        high_units BIGINT,
        high_nano BIGINT,
        low_units BIGINT,
        low_nano BIGINT,
        PRIMARY KEY (time, figi, interval)
    )
'''

cursor.execute(text(sql))
cursor.commit()


#создаем temp_candles с нужными типами данных
sql = '''
    DROP TABLE IF EXISTS temp_candles;
    CREATE TABLE IF NOT EXISTS temp_candles (
        time TIMESTAMPTZ,
        figi VARCHAR(255),
        interval VARCHAR(255),
        open DECIMAL(12,2),
        close DECIMAL(12,2),
        high DECIMAL(12,2),
        low DECIMAL(12,2),
        is_complete BOOLEAN,
        candle_source VARCHAR(255),
        volume BIGINT,
        volume_buy BIGINT,
        volume_sell BIGINT,
        open_units BIGINT,
        open_nano BIGINT,
        close_units BIGINT,
        close_nano BIGINT,
        high_units BIGINT,
        high_nano BIGINT,
        low_units BIGINT,
        low_nano BIGINT,
        PRIMARY KEY (time, figi, interval)
    )
'''

cursor.execute(text(sql))
cursor.commit()

#загружаю данные в temp_candles
df.to_sql(
    'temp_candles', 
    conn, 
    if_exists='append', 
    index=False,
    method='multi'
)

#делаю инкрементальную загрузку
sql = '''
    DELETE FROM candles
    WHERE (time, figi, interval) IN (
        SELECT time, figi, interval 
        FROM temp_candles
    );
    INSERT INTO candles
    SELECT * FROM temp_candles;
'''
cursor.execute(text(sql))
cursor.commit()
cursor.close()

#Проверка на дубликаты
sql = '''
    select figi, interval, time, count(*) as cnt_rows
    FROM candles 
    GROUP BY figi, interval, time
    HAVING COUNT(*) > 1;
'''
df_test_db = pd.read_sql(sql, conn)
print(df_test_db)

Как тебе?
Знаю что это не код датаинженера, но задача выполнена!)

по поводу гит вот что-то словил не понимаю что это
(venv) kam@kam-MS-7D48:~/datalearnhome$ git add .
git commit -m "feat: first working API call, still debugging date format"
git push
[master (корневой коммит) 4685fc9] feat: first working API call, still debugging date format
 2 files changed, 369 insertions(+)
 create mode 100644 app.py
 create mode 100644 test.ipynb
fatal: Не настроена точка назначения для отправки.
Либо укажите URL с помощью командной строки, либо настройте внешний репозиторий с помощью

    git remote add <имя> <адрес>

а затем отправьте изменения с помощью имени внешнего репозитория

    git push <имя>


залил в Git. классное чувство, буду стараться делать коммит каждый день
добавил логгирование? что еще предложешь поделать? я потратил пока только 20 минут

что сделал за сегодня:
logging, readme, залил в гит обновление (с логами).
так как я писал в реадми про docker-compose я решил его приложить в проект (но суть в том что он не мой, я указал его в readmi с ссылкой откуда взял)
Дальше пошли тормоза, так как пришлось объединять проекты где сборка докера и мои скрипты.
Перенес сборку в свою папку откуда пушу в гит. подтянул вроде все git add и запушил.

Что не сделал, так это параметизацию, и не могу быть в ответе за этот docker-compose, хочется научиться собирать его самостоятельно


Привет, я сегодня создал свой docker-compose.yml
создал в базе юзера и добавил ему права.
сделал env.example.
удалил старые зависимости от старого образа, который собирал не я.
добавил sql.ipynb в котором шаблон для работы с базой (для аналитики и отладки)
Добавил сноску в readme.md где описал обновления и тд.
вот мой компосе:
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: postgres_db
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - '5432:5432'
    
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:

это как это работает в скрипте:
load_dotenv()

TOKEN = os.getenv('T_TOKEN')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

Это мой readme.md:

# T-Invest API to Postgres ETL Pipeline

Простой ETL-пайплайн для загрузки биржевых свечей из API T-Invest в PostgreSQL.

## Что делает
Стягивает свечи по заданному тикеру и сохраняет в БД. Если запустить повторно — новые данные добавятся, старые не перезатрутся (инкрементальная загрузка).

## Технологии
- Python (requests, pandas, sqlalchemy)
- PostgreSQL (в Docker)
- API T-Invest

## Структура
```
app.py                 # основной скрипт
docker-compose.yml     # подъем PostgreSQL
.env.example           # шаблон для .env
.env                   # твои личные данные (не в репозитории)
requirements.txt       # зависимости
```

## Как запустить

1. Скопируй и заполни `.env`:
```bash
cp .env.example .env
# открой .env и впиши свой T_TOKEN
```

2. Подними базу:
```bash
docker-compose up -d
```

3. Запусти скрипт:
```bash
python app.py
```

## Что изменилось в последней версии

**Теперь подключение к БД идет через переменные из `.env`**, а не зашито в коде:
- было: `postgresql://postgres:postgres@localhost:5432/dwh_data`
- стало: `postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}`

**Плюс** полностью переписан `docker-compose.yml` — теперь он свой, а не скопированный из стороннего репозитория.

**Добавлен вывод статистики** после загрузки — скрипт теперь показывает общее количество свечей, сохраненных в базе. Можно сразу видеть результат работы и контролировать, что данные действительно пополняются.

**Добавлен `sql.ipynb`** — Jupyter-ноутбук с шаблоном для работы с БД через SQLAlchemy. Удобно писать и тестировать запросы, сразу видеть результат в виде DataFrame, не запуская каждый раз основной скрипт. Полезно для анализа данных и отладки.

это шаблон sql.ipynb:
# Импортируем алхимию и создаем соединение
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

conn = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}')

sql = '''
    SELECT 
        min(time)::date as min_date,
        max(time)::date as max_date 
    FROM candles
'''

df = pd.read_sql(sql, conn)
df

вот еще я добавил в скрипт вывод статистики:
#Общее кол-во сохраненных свечей
sql = '''
    SELECT COUNT(*) FROM candles;
'''
df_test_db = pd.read_sql(sql, conn)
logging.info(f"Общее кол-во сохраненных свечей: {df_test_db.iloc[0, 0]}")


я решил пока не создавать свои dockerfile, так как пока не думаю что мне это нужно.
За сегодня я решил, что надо предать своему проекту смысл, как с точки зрения разработки, так и с точки зрения DE.
Я решил описать себе на листке что я хочу от этого проекта.
1) Это научится загружать данные из API в БД батчами, научиться работать с json, научиться работать с API.
2) Научиться работать со стримом, загружать данные стримом (возможно научиться работать с Kafka и тд)
3) Писать реально продукт как разраб, сейчас у меня обычный аналитический скрипт. А я хочу if __name__ == __main__ (или как там они пишут на ООП, ахахах)
4) я хочу получить продукт, который реально работает:
- для начала я определяю инструмент, на котором хочу заработать.
- потом я выгружаю с помощью своего приложения статистику по инструменту.
- далее скрипт готовит аналитику или какой-то предикт, возможно сам покупает и выставляет стоп лос тейк профит
- оценивает риски
- читает новости в месте с ИИ.

Короче что-то такое.
Сегодня я занимался этим анализом и решил посмотреть что есть в API и подготовил 2 файла в виде тестовых .ipynb
это получение валют, и получение акций. Акции пока не научился парсить нормально, но буду учиться.
Еще с помощью GPT я подсмотрел функцию которая из CamelCase делает SnakeCase. добавил ее в свой изначальный app.py и переименовал его в get_candles.py

Оцени мою сегодняшнюю работу, и еще расскажи, стоит ли брать себе выходные от учебы или это должен быть каждодневный ритуал.
Стоит ли опасаться ИИ агентов, которые сейчас творят невероятные вещи (как Claude Code и др) - вопрос в плане не обесценят ли они то, что я сейчас изучаю? Меня это очень сильно беспокоит.
Стоит ли пушить git свои черновики и тд? Стоит ли пушить каждый день?
Не получается ли что я строю что-то похожее на SDK Python который работает с T-Invest напрямую?)
Есть ли смысл строить какой-то SDK, если он есть, но не импортируется нормально) по факту у меня он будет свой и будет работать непосредственно с БД и Агентами