import enum

GRIZZLY_TEMPLATE_NAME='grizzly'
MONARCH_TEMPLATE_NAME='monarch'
THREEMUSHROOMS_TEMPLATE_NAME='threemushrooms'

class Company(enum.Enum): 
    GRIZZLY = 0
    MONARCH = 1
    THREEMUSHROOMS=2

    def get_company(name:str):
        if GRIZZLY_TEMPLATE_NAME in name.lower():
            return Company.GRIZZLY
        elif MONARCH_TEMPLATE_NAME in name.lower():
            return Company.MONARCH
        elif THREEMUSHROOMS_TEMPLATE_NAME in name.lower():
            return Company.THREEMUSHROOMS

    def determine_template(option:str)->str:
        if Company.get_company(option.lower()) == Company.GRIZZLY:
            return GRIZZLY_TEMPLATE_NAME
        elif Company.get_company(option.lower()) == Company.MONARCH:
            return MONARCH_TEMPLATE_NAME
        elif Company.get_company(option.lower()) == Company.THREEMUSHROOMS:
            return THREEMUSHROOMS_TEMPLATE_NAME
        