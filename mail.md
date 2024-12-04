# mail

## /User/GetMailList

```
{'connection': 'close', 'content-length': '24', 'content-type': 'application/json; charset=utf-8'}
b'{"user_index":"<会員番号>"}'
/User/GetMailList
Headers([('content-length', '359'), ('connection', 'close'), ('content-type', 'application/json; charset=utf-8'), ('date', 'Tue, 03 Dec 2024 12:04:27 GMT'), ('server', 'Microsoft-IIS/10.0'), ('cache-control', 'private'), ('content-encoding', 'gzip'), ('set-cookie', 'ARRAffinity=5f541a4de72b982990a3263e16c919ccf758f7822c00c9bf1244fc7813fcc18e;Path=/;HttpOnly;Secure;Domain=iceonline.azurewebsites.net'), ('set-cookie', 'ARRAffinitySameSite=5f541a4de72b982990a3263e16c919ccf758f7822c00c9bf1244fc7813fcc18e;Path=/;HttpOnly;SameSite=None;Secure;Domain=iceonline.azurewebsites.net'), ('vary', 'Accept-Encoding'), ('x-aspnetmvc-version', '5.2'), ('x-aspnet-version', '4.0.30319'), ('x-powered-by', 'ASP.NET')])
b'{"msg":"OK","getMailResultData":{"mail_list_data":[{"mail_index":1068757,"bosang_type":1,"bosang_value":250,"end_date":"Jan  2 2025  8:04PM","bosang_text":"\xe3\x83\x95\xe3\x83\xaa\xe3\x83\xbc\xe3\x82\xba\xc2\xb7\xe3\x83\x91\xe3\x82\xb9\xc2\xb7\xe3\x82\xb7\xe3\x83\xbc\xe3\x82\xba\xe3\x83\xb338 6\xe7\x95\xaa \xe8\xa3\x9c\xe5\x84\x9f\xe6\x94\xaf\xe7\xb5\xa6(0)"},{"mail_index":1068755,"bosang_type":50,"bosang_value":2,"end_date":"Jan  2 2025  8:04PM","bosang_text":"\xe3\x83\x95\xe3\x83\xaa\xe3\x83\xbc\xe3\x82\xba\xc2\xb7\xe3\x83\x91\xe3\x82\xb9\xc2\xb7\xe3\x82\xb7\xe3\x83\xbc\xe3\x82\xba\xe3\x83\xb338 5\xe7\x95\xaa \xe8\xa3\x9c\xe5\x84\x9f\xe6\x94\xaf\xe7\xb5\xa6(0)"}],"mail_count":0}}'
INFO:     172.21.32.1:0 - "POST /User/GetMailList HTTP/1.1" 200 OK
```

## bosang_type

- 0: gold(たぶん)
- 1: ice
- 2: マイレージ
- 3: キューブ(たぶん)
- 50: 高級箱

## /User/GetMailBosang

##　財貨

```
{'connection': 'close', 'content-length': '47', 'content-type': 'application/json; charset=utf-8'}
b'{"user_index":"<会員番号>","mail_index":"<メール番号>"}'
/User/GetMailBosang
Headers([('content-length', '160'), ('connection', 'close'), ('content-type', 'application/json; charset=utf-8'), ('date', 'Tue, 03 Dec 2024 12:06:50 GMT'), ('server', 'Microsoft-IIS/10.0'), ('cache-control', 'private'), ('content-encoding', 'gzip'), ('set-cookie', 'ARRAffinity=5f541a4de72b982990a3263e16c919ccf758f7822c00c9bf1244fc7813fcc18e;Path=/;HttpOnly;Secure;Domain=iceonline.azurewebsites.net'), ('set-cookie', 'ARRAffinitySameSite=5f541a4de72b982990a3263e16c919ccf758f7822c00c9bf1244fc7813fcc18e;Path=/;HttpOnly;SameSite=None;Secure;Domain=iceonline.azurewebsites.net'), ('vary', 'Accept-Encoding'), ('x-aspnetmvc-version', '5.2'), ('x-aspnet-version', '4.0.30319'), ('x-powered-by', 'ASP.NET')])
b'{"msg":"OK","bosang_type":1,"bosang_value":250}'
INFO:     172.21.32.1:0 - "POST /User/GetMailBosang HTTP/1.1" 200 OK
```

`bosang_type` には財貨の種別、`bosang_value` にはもらった量

## ガチャ

```
{'connection': 'close', 'content-length': '47', 'content-type': 'application/json; charset=utf-8'}
b'{"user_index":"<会員番号>","mail_index":"<メール番号>"}'
/User/GetMailBosang
Headers([('content-length', '160'), ('connection', 'close'), ('content-type', 'application/json; charset=utf-8'), ('date', 'Tue, 03 Dec 2024 12:07:38 GMT'), ('server', 'Microsoft-IIS/10.0'), ('cache-control', 'private'), ('content-encoding', 'gzip'), ('set-cookie', 'ARRAffinity=5f541a4de72b982990a3263e16c919ccf758f7822c00c9bf1244fc7813fcc18e;Path=/;HttpOnly;Secure;Domain=iceonline.azurewebsites.net'), ('set-cookie', 'ARRAffinitySameSite=5f541a4de72b982990a3263e16c919ccf758f7822c00c9bf1244fc7813fcc18e;Path=/;HttpOnly;SameSite=None;Secure;Domain=iceonline.azurewebsites.net'), ('vary', 'Accept-Encoding'), ('x-aspnetmvc-version', '5.2'), ('x-aspnet-version', '4.0.30319'), ('x-powered-by', 'ASP.NET')])
b'{"msg":"OK","bosang_type":5,"bosang_value":896}'
```

`bosang_type` にはレアリティ、`bosang_value` には内容がはいってるかもしれない
