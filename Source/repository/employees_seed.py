# Koble oss mot databasen med PyMSSQL via miljÃ¸variabler
from dataclasses import astuple, dataclass, field, fields
import datetime
from os import getenv
import pymssql
from uc_faker import UcFaker
from uc_repository3 import uc_repository3

# =============================================================================
# Koble oss mot databasen med PyMSSQL via miljÃ¸variabler
# =============================================================================
conn = pymssql.connect(
    server=getenv("DOCKER_MSSQLSERVER"), 
    user=getenv("DOCKER_MSSQLUSER"), 
    password=getenv("DOCKER_MSSQLPW"), 
    database=getenv("DOCKER_MSSQLDB"),
    charset="ISO-8859-1" # Fiks Ã˜Ã†Ã… problemer
)
cursor = conn.cursor()

# =============================================================================
# Component dataclass
# =============================================================================
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
    
    
uc_faker = UcFaker()
ansatt_repo = uc_repository3(Employees, cursor)

ansatt_liste = []
for _ in range(2000):                
    new_emp = Employees()
    new_emp.id = 0
    new_emp.etternavn = uc_faker.get_random_lastname()
    new_emp.fornavn = uc_faker.get_random_firstname()
    new_emp.gatenavn = uc_faker.get_random_gatenavn()
    new_emp.husnummer = uc_faker.get_random_gatenummer()
    (new_emp.postnummer, new_emp.poststed) = uc_faker.get_random_poststed()     
    new_emp.fdato = uc_faker.get_random_fdato()
    new_emp.ansattdato = uc_faker.get_random_ansattdato()
    ansatt_liste.append(astuple(new_emp))
    
print(ansatt_liste)
ansatt_repo.create_table(True)
ansatt_repo.bulk_insert(ansatt_liste)
conn.commit()