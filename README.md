#### Gradio App en un Droplet de Digital Ocean 🐬

1.- Clona éste repositorio en la dropplet en donde quieres otra app de gradio corriendo.<br>

**git clone git@github.com:Moibe/gradio-standalone-do.git astro-blend**

2.- Crea en Github un nuevo repositorio de producción desde donde manejarás ésta app.
La nomenclatura será ocean- como prefijo, con lo que indicas que es el fornt de Digital Ocean para determinada app, en éste caso Astro-Blend.

3.- Cambia el remoto del directorio recién clonado para que ahora manejes ésta nueva app desde el repositorio que acabas de crear en Github.<br>
**git remote set-url origin git@github.com:Moibe/ocean-astro-blend.git**

4.- Haz git push origin main, para probar y subir el repositorio a su nuevo lugar en Github. 

5.- Agrega las variables en settings: MAIN_BRANCH, SSH_HOST, SSH_PRIVATE_KEY, SSH_USER, WORK_DIR.<br>
Para las referencias a ésto consulta: https://www.youtube.com/watch?v=llUzfOCeLH0<br>
- SSH_PRIVATE_KEY fue creado dentro de la droplet y la encuentras en: cat /root/.ssh/id_rsa
- SSH_USER es root.
- SSH_HOST es la IP de tu server.
- WORK_DIR es la ubicación de tu repositorio, por ejemplo en éste caso: code/ocean-astro-blend
- MAIN_BRANCH main

6.- Ahora necesitas agregar el nuevo sitio a la configuración de nginx, hay dos formas de hacerlo:

**Importante: Antes de agregar el path a las configuraciones de nginx, recuerda que ese path esté especificado en 

**a) agregarlo como un path así: tudominio.com/path**

Para agregarlo como un path, debes de agregar la parte correspondiente al archivo de nginx de tu dominio ya existente que se encuentra en /etc/ngingx/sites-available.<br>
Una vez agregado debes hacer reload así: **systemctl reload nginx**

**b) agregarlo como otro dominio: otrodominio.com**

Para agregarlo como otro dominio, en cambio, debes de copiar el archivo de dominio de nginx que se encuentra en /etc/nginx/sites-available y crear uno nuevo. 
Una vez hecho ésto debes de crear el link simbólico hacia sites-enabled así: **ln -s /etc/nginx/sites-available/otro dominio.com /etc/nginx/sites-enabled/**
Una vez agregado debes hacer reload así: **systemctl reload nginx**

Finalmente requerimos activar los certificados SSL. 🔒
**sudo certbot --nginx -d example.com -d www.example.com**
El proceso de renovación es automático y lo puedes checar aquí así: <br>
**sudo systemctl status certbot.timer**
Para probar si está funcionando correctamente puedes hacer una simulación de la renovación así:<br> 
**sudo certbot renew --dry-run**

Éste repositorio cuenta con github actions para autodesplegarlo cada que hay cambios.<br>
Sin embargo, para que corre la app de gradio lo que se usa es un cron dentro del servidor.<br>
Éste cron activa a deploy.sh que apaga el proceso anterior y reactiva el nuevo.<br>
Todo ésto se guarda dentro de logs/deploy.log.
