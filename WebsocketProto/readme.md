
### Run Server
Untuk menghidupkan server, cukup dengan command
```powershell
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```
host dan port dapat diganti sesuai keinginan

### API Meminta Status dengan websocat
```powershell
C:\Users\virsh>websocat ws://<Ip_address>:<port>/ws/<user>/lock/status                                                  
```
Dengan ini, websocket akan return string biner, berupa 1 atau 0
>1 #artinya terkunci
>0 #artinya terbuka

### API Mengunci atau membuka
User dapat membuka atau mengunci dengan meluncurkan request ke API berikut, lalu menginputkan nilai 1 atau 0
```powershell
C:\Users\virsh>websocat ws://<Ip_address>:<port>/ws/<user>/lock/locking                                                  
1
```
Websocket akan return string, namun string ini dapat diabaikan
```powershell
Lock state changed to: LOCKED
```
