# Arqui_Software
Comandos para Probar los Clientes
Ejecuta el bus de servicios en Docker:
docker run -d -p 5000:5000 jrgiadach/soabus:v1

Inicia el servicio de Gestión de Usuarios (USR01):
python usr01_service.py

Inicia el servicio de Gestión de Productos (PRD02):
python prd02_service.py

Inicia el servicio de Acceso a la Base de Datos (DBS07):
python dbs07_service.py

Ejecuta el cliente normal:
python cliente_normal.py

Ejecuta el cliente administrador:
python cliente_administrador.py