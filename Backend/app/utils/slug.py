import re
def generate_slug(value:str)->str:
    value = value.strip().lower()
    value =re.sub(r"[^a-z0-9\s-]","",value)
    value=re.sub(r"[\s_-]+","-",value)
    value=re.sub(r"^-+|-+$","",value)

    return value

# re python ka regex module hai jo text pattern find ya replace karne ke liye use hota hai
