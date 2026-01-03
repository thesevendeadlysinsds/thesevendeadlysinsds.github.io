def transform_to_int(tifsec):
    autorises = "".join([chr(i) for i in range(ord("0"), ord("9")+1)]) + "+-*/%(). "
    # print(tifsec)
    for i in str(tifsec):
        if i not in autorises:
            return None
    try:
        return int(eval(str(tifsec), {"__builtins__": {}}, {}))
    except:
        return None
# print(transform_to_int("print('coucou')"))

def open_web(url):
    try:
        reponse = requests.get(url)
        reponse.raise_for_status()
        return reponse.text
    except:
        return f"Erreur lors de la récupération : {e}"
# print(open_web("https://thesevendeadlysinsds.github.io/py/txt/gtn-data1.txt"))
