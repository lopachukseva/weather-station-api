<h1>API для сети метеостанций</h1>
<h2>Создан по тех. заданию:</h2>
<p>
Существует сеть метеостанций. С одной стороны необходимо круглосуточно принимать от них информацию о текущей погодной обстановке и сохранять ее в базу данных, а с другой - по запросу отдавать информацию.</p>

<p>Входные данные (один запрос):</p>
<ol>
<li>id метеостанции</li>
<li>температура</li>
<li>направление ветра</li>
<li>скорость ветра</li>
<li>влажность воздуха</li>
</ol>

<p>
Также по запросу должны быть получены средние дневные показатели данных параметров (вместе с запросом передается id метеостанции и дата).
В дальнейшем необходимо быть готовым к тому, что список входных параметров и запросов будет сильно расширяться (к примеру, будет добавлена широта и долгота каждой точки).
Все запросы должны происходить с использованием секретного ключа, который передается при каждом запросе (причем ключ для метеостанции должен позволять только записывать данные, а ключ пользователя - только получать). Секретный ключ един для всех станций и пользователей.
</p>

<p>
Температура измеряется в градусах цельсия. Диапазон - от -37 до +51.
Направление ветра выражается в градусах (°). Север обозначается как 0°, восток — как 90°, юг — как 180°, запад — как 270°. Общий диапазон значений - от 0 до 360.
Скорость ветра выражается в м/с. Минимальное значение - 0, максимальное - 86.
Влажность воздуха выражается в процентах - от 0 до 100.
</p>


<h2>Реализация:</h2>

<p>Для реализации был выбран фреймворк FastAPI. В качестве базы данных используется PostgreSQL с подключением через
асинхронный драйвер asyncpg. Взаимодействие с базой данных происходит через ORM (библиотека SQLAlchemy). Так как в 
будущем планируется расширение базы данных, была внедрена система миграций (с помощью библиотеки Alembic) для контроля
версий базы данных. Также в проект внедрены unit тесты.</p>

<h2>Настройка и запуск:</h2>
<ul>
<li>Создание файла .env, который содержит в себе параметры для подключение к основной и тестовой базе данных (см. ниже)</li>
<li>Установка зависимостей: pip install -r requirements.txt</li>
<li>Создание миграций: alembic revision --autogenerate -m "initial"</li>
<li>Применение миграций: alembic upgrade head</li>
<li>Запуск uvicorn (из папки src): uvicorn main:app</li>
</ul>

<p>Документация openapi доступна по адресу: localhost:8000/docs</p>

<h4> Файл .env должен находиться в директории src включать в себя следующие параметры: </h4>
<ul>
<li>DB_USER - имя пользователя БД</li> 
<li>DB_PASS - пароль от БД</li>
<li>DB_HOST - адрес БД</li>
<li>DB_PORT - порт БД</li>
<li>DB_NAME - имя БД</li>
</ul>

<p>Аналогично с DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST, но уже для тестовой БД</p>

<ul>
<li>STATION_ACCESS_KEY - секретный ключ для станции</li>
<li>USER_ACCESS_KEY - секретный ключ для пользователей</li>
</ul>




