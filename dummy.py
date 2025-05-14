import http.client

conn = http.client.HTTPSConnection("latest-mutual-fund-nav.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "63e83a5882msh61beeb4a639a93fp116a01jsn396d1d8f4900",
    'x-rapidapi-host': "latest-mutual-fund-nav.p.rapidapi.com"
}

conn.request("GET", "/fetch_all_funds", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))