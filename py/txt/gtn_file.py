import requests

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

def toto(file_name):
    is_web = file_name.startswith("http://") or file_name.startswith("https://")
    if is_web:
        f = open_web(file_name)
    else:
        f = open(file_name, "r", encoding="utf-8")
    dico = {}
    for i in f if not is_web else f.strip().split("\n"):
        a = i.split()
        # print(a)
        if len(a) >= 3:
            dico[a[0]] = {"borne1": transform_to_int(a[1]), "borne2": transform_to_int(a[2])}
    if not is_web:
        f.close()
    return dico
# print(toto(str(path_name).replace("\\", "/") + "/gtn_data.txt"))
# print(toto("http://thesevendeadlysinsds.github.io/py/txt/gtn-data1.txt"))
