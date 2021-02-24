# BrewBubbles_cbpi
A CraftBeerPi Plugin for the BrewBubbles Device (https://docs.brewbubbles.com/en/latest/index.html)

NOTE : You need to modify the /etc/apache2/sites-available/000-default.conf file and add a VirtualHost
```
<VirtualHost *:80>
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
        ProxyPass /api/brewbubbles/v1/data/ http://127.0.0.1:5000/api/brewbubbles/v1/data
        ProxyPassReverse /api/brewbubbles/v1/data/ http://127.0.0.1:5000/api/brewbubbles/v1/data
</VirtualHost>
```

 You then set up your BrewBubbles to point to IP_To_CBPi/api/brewbubbles/v1/data / (WITH the final /)

