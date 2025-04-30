from dataclasses import dataclass, field
import datetime
from os import getenv
import random
from typing import Union
from fastapi import FastAPI, HTTPException, Request
from pymssql import connect
import pymssql

from uc_repository3 import uc_repository3

# MAC
# >wrk -t 10 -c 10  http://localhost:8000/employees_random
# Running 10s test @ http://localhost:8000/employees_random
#   10 threads and 10 connections
#   Thread Stats   Avg      Stdev     Max   +/- Stdev
#     Latency     8.77ms   10.65ms 138.17ms   95.48%
#     Req/Sec   140.49     40.55   280.00     84.40%
#   14041 requests in 10.06s, 4.40MB read
# Requests/sec:   1395.24
# Transfer/sec:    447.67KB
#
#>wrk -t 10 -c 10 http://localhost:8000/employees/11 
# Running 10s test @ http://localhost:8000/employees/11
#   10 threads and 10 connections
#   Thread Stats   Avg      Stdev     Max   +/- Stdev
#     Latency     9.11ms   12.75ms 171.40ms   95.21%
#     Req/Sec   139.88     42.75   191.00     79.40%
#   13991 requests in 10.06s, 4.31MB read
# Requests/sec:   1390.29
# Transfer/sec:    438.59KB
#
# WINDOWS
# learniken@059b480963b8:~/source$ wrk -t 10 -c 10  http://localhost:8000/employees/11
# Running 10s test @ http://localhost:8000/employees/11
#   10 threads and 10 connections
#   Thread Stats   Avg      Stdev     Max   +/- Stdev
#     Latency    12.95ms    1.40ms  22.65ms   83.49%
#     Req/Sec    77.21      7.32    90.00     83.30%
#   7721 requests in 10.01s, 2.41MB read
# Requests/sec:    771.28
# Transfer/sec:    246.30KB
# learniken@059b480963b8:~/source$ wrk -t 10 -c 10  http://localhost:8000/employees
# Running 10s test @ http://localhost:8000/employees
#   10 threads and 10 connections
#   Thread Stats   Avg      Stdev     Max   +/- Stdev
#     Latency    79.54ms    4.17ms 103.13ms   86.01%
#     Req/Sec    12.52      4.35    20.00     74.72%
#   1251 requests in 10.01s, 24.01MB read
# Requests/sec:    124.93
# Transfer/sec:      2.40MB

@dataclass(order=True)
class Hallo:
    melding: str = field(default="Hello")
    til: str = field(default="Learniken")
    
@dataclass(order=True)
class Employees:
    id: int = field(default=0)
    etternavn: str = field(default=None)
    fornavn: str = field(default=None)
    gatenavn: str = field(default=None)
    husnummer: str = field(default=None)
    postnummer: str = field(default=None)
    poststed: str = field(default=None)
    fdato: datetime.datetime = field(default=None)
    ansattdato: datetime.datetime = field(default=None)
    
class Database():
    async def create_pool(self):
        self.conn = pymssql.connect(
            server=getenv("DOCKER_MSSQLSERVER"), 
            user=getenv("DOCKER_MSSQLUSER"), 
            password=getenv("DOCKER_MSSQLPW"), 
            database=getenv("DOCKER_MSSQLDB"),
            charset="ISO-8859-1" # Fiks ØÆÅ problemer
        )
        print("pool created")


# wrk -t 10 -c 10  http://localhost:8000

def create_app():

    app = FastAPI()
    db = Database()

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        request.state.conn = db.conn
        response = await call_next(request)
        return response

    @app.on_event("startup")
    async def startup():
        print("Starting up")
        await db.create_pool()

    @app.on_event("shutdown")
    async def shutdown():
        # cleanup
        print("Shutting down")
        pass

    @app.get("/")
    def read_root():
        result = Hallo()
        return result

    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "name": "Python"}
    
    @app.get("/employees")
    async def get_all_employees(request: Request):   
        cursor = request.state.conn.cursor()
        ansatt_repo = uc_repository3(Employees, cursor)     
        result = ansatt_repo.get_all()
        return result
    
    @app.get("/employees/{id}")
    async def get_employee_by_id(request: Request, id: int):   
        cursor = request.state.conn.cursor()
        emp_repo = uc_repository3(Employees, cursor)     
        result = emp_repo.get_by_field("id", id)
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return result
    
    @app.get("/employees/byid/{id}")
    async def get_employee_by_id(request: Request, id: int):   
        cursor = request.state.conn.cursor()
        emp_repo = uc_repository3(Employees, cursor)     
        result = emp_repo.get_by_field("id", id)
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return result
    
    @app.get("/employees_random")
    async def get_employee_by_id(request: Request):   
        cursor = request.state.conn.cursor()
        emp_repo = uc_repository3(Employees, cursor)   
        id = random.randint(1, 1999) 
        #print(f"Random id: {id}") 
        #return {"item_id": id, "name": "Python"}
        result = emp_repo.get_by_field("id", id)
        return result
    
    @app.post("/employees")
    async def create_item(request: Request, item: Employees):
        cursor = request.state.conn.cursor()
        emp_repo = uc_repository3(Employees, cursor)   
        emp_repo.insert(item)
        request.state.conn.commit()
        return item
    
    @app.put("/employees")
    async def create_item(request: Request, item: Employees):
        cursor = request.state.conn.cursor()
        emp_repo = uc_repository3(Employees, cursor)   
        res = emp_repo.update(item)
        request.state.conn.commit()
        return res
    
    @app.delete("/employees")
    async def create_item(request: Request, item: Employees):
        cursor = request.state.conn.cursor()
        emp_repo = uc_repository3(Employees, cursor)   
        res = emp_repo.delete(item)
        request.state.conn.commit()
        return res

    
    return app

app = create_app()

# To debug this server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)