import datetime
import json
import random


class UcFaker:
    
    fornavn = None
    etternavn = None
    postnummer_register = None
    pnr_dict = None
    postnumre = None
    
    def __init__(self):
        
        with open('/home/learniken/source/datafiles/ordliste_ssb_norske_etternavn.txt', 'r') as file:
            self.etternavn = file.read().splitlines()            
            
        with open('/home/learniken/source/datafiles/ordliste_ssb_norske_fornavn.txt', 'r') as file:
            self.fornavn = file.read().splitlines()                 
        
        with open('/home/learniken/source/datafiles/GateNavnBg.txt', 'r') as file:
            self.gatenavn = file.read().splitlines()                
        
        with open('/home/learniken/source/datafiles/postnummer.json', 'r') as file:
            data = file.read()    
            self.postnummer_register = json.loads(data)   
            self.pnr_dict = {key: value["poststed"] for key, value in self.postnummer_register.items()}
            
            #my_dictionary = dict(map(lambda kv: (kv[0], f(kv[1])), my_dictionary.items()))
            #my_dictionary = {k: f(v) for k, v in self.postnummer_register.items()}
            self.postnumre = sorted(list(self.postnummer_register.keys()))   
             
    def get_random_firstname(self):
        return random.choice(self.fornavn).capitalize()

    def get_random_lastname(self):
        return  random.choice(self.etternavn)
    
    def get_random_fullname(self):
        return random.choice(self.etternavn) + ', ' + random.choice(self.fornavn).capitalize()
    
    def get_random_poststed(self):
        (postnr, pstedict) = random.choice(list(self.postnummer_register.items()))    
        return (postnr, pstedict["poststed"])    
   
    def get_poststed(self, postnr):  
        pstedict = self.pnr_dict[postnr]
        return pstedict["poststed"]
    
    def get_random_fdato(self):
        return  datetime.datetime(random.randint(1940, 2001), random.randint(1, 12), random.randint(1, 28))
    
    def get_random_ansattdato(self):
        return  datetime.datetime(random.randint(2001, 2024), random.randint(1, 12), random.randint(1, 28))
    
    def get_random_gatenavn(self):       
        return random.choice(self.gatenavn)
    
    def get_random_gatenummer(self):
        gatenumre = ['1', '2', '3', '4', '5', '6' ]
        gatebokstav = ['', '', '', 'A', 'B']
        return random.choice(gatenumre) + random.choice(gatebokstav)
    
    def get_gateadresse(self):
        return f'{self.get_random_gatenavn()} {self.get_random_gatenummer()}'
    