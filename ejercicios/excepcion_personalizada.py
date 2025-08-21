# Excepción personalizada
class EmailInvalido(Exception):
    def __str__(self):
        return "Email inválido"

def verificar_email(e):
    if "@" not in e:
        raise EmailInvalido()

try:
    verificar_email("usuario#dominio.com")
except EmailInvalido as ex:
    print(ex)
