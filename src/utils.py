def validate_cep(cep):
    return len(cep) == 8 and cep.isdigit()