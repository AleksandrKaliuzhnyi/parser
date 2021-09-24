from urllib.parse import unquote

url = "https://spb.zoon.ru/redirect/?to=https%3A%2F%2Fvk.com%2Fcmt_clinics&hash=916ab6047f7021bc23cd0608ce23c7ad&from=5024c24f3c72ddf110000011.fbe8&ext_site=ext_vk&backurl=https%3A%2F%2Fspb.zoon.ru%2Fmedical%2Fklinika_smt_poliklinicheskij_kompleks_na_moskovskom_prospekte_22%2F"

url = unquote(url.split("?to=")[1].split("&")[0])

print(url)