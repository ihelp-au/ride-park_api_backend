# Park&Ride Backend API (工地)

## 1. 项目介绍
IHELP Project

获取NSW政府停车场数据，并维护API接口，供IHELP项目前端使用

/stations 提供所有车站信息，包括空余车位数，车站名称，车站位置，车站ID等； **测设中**

/stations/id/annouce 提供某一车站的详细信息，包括空余车位数，车站名称，车站位置，车站ID等; **未完成**

## 2. 项目结构

```
Park&Ride Backend API
├── app
│ ├── routers
│ │ └── stations.py
│ ├── test
│ │ └── test_main.py
│ └── main.py
├── data_backend
│ └── create_parkinglot.py
| └── create_station_geocoord.py
| └── create_location.py
| └── read_carpark_api.py
├── data
│ ├── 486.json
│ ├── 487.json
│ ├── ...
│ ├── parking_lots.parquet
│ ├── station.parquet
│ └── station_geo.parquet
├── test
│ └── test_stations.py
|── conftest.md
├── pyproject.toml
|── README.md
└── requirements.txt
```

## 3. 项目依赖
请见requirements.txt



## 4. 项目运行
当前在app文件夹下使用`python -m fastapi dev main.py`启动fastapi web api服务。
本地浏览器使用http://127.0.0.1:8000/docs 访问API文档。


## 5. TODO List
1. 会出现某个车站的空余车位数为负数的情况，例如 facility_id 486
![alt text](image.png)；暂时不太像数据问题
2. 各车站Zone信息会提供更精确的停车位信息，可以进一步利用
3. 增加停车位json数据读取函数，同时保留读取parquet文件能力
4. Timestap使用原始数据中的时间戳会更用户友好
5. 使用ttl cache减少后台IO及计算


