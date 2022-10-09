# Utilizar ProtonMail con Tor y no con ProtonVPN

## Contenidos

- [Introducción](#introducción)
- [Investigación](#investigación)
- [Conclusión](#conclusión)
- [Nota final](#nota-final)
- [Recursos](#recursos)

## Introducción

Esta semana, la noticia sobre que ProtonMail facilitó la dirección IP de un usuario a las autoridades Suizas ha provocado comentarios en las redes sociales, ya que es un servicio enfocado a la privacidad.

Desde sus cuentas oficiales, la empresa Proton respondió a estos comentarios explicando [qué ha sucedido y porqué actuaron de este modo](https://protonmail.com/blog/climate-activist-arrest/). En resumen, bajo orden judicial, debido a las leyes Suizas tuvieron que dar la dirección IP del usuario investigado.

En las respuestas explican que están enfocados a la privacidad (que los archivos, mails, etc. que almacenamos solo pueden ser accedidos por nosotros) pero, para ser anónimo (evitar que se sepan datos como por ejemplo nuestra IP) [recomiendan usar la red Tor y no una VPN](https://protonmail.com/blog/climate-activist-arrest/). Me pregunté porqué ProtonVPN no sería suficiente y estas son las conclusiones que he sacado.

## Investigación

Hay que señalar dos puntos:

- Recolección de dirección IP: [ProtonMail almacena temporalmente la dirección IP de quién accede a su servicio](https://protonmail.com/privacy-policy), mientras que [ProtonVPN no guarda información sobre la dirección IP](https://protonvpn.com/privacy-policy).
- Solicitud de información por parte de las autoridades: en algunas [respuestas que han dado en redes sociales](https://twitter.com/ProtonMail/status/1435530623087792133) y en su [blog](https://protonmail.com/blog/climate-activist-arrest/) indican diferencias entre ProtonMail y ProtonVPN:

  > VPN and email are treated differently within the current Swiss legal framework. We can be legally compelled to provide logs for email, but not for VPN.

Es decir, con ProtonVPN la compañía no guarda la dirección IP y tampoco las autoridades pueden solicitar que se haga, parece lógico pensar que recomienden ProtonVPN para acceder a su servicio de email y leer nuestro correo. ¿Cuál es el motivo de que no lo hagan?

Creo que la respuesta está en [este detalle](https://protonvpn.com/support/tor-browser-vs-tor-vpn/):

> Note: When you connect to ProtonVPN, we will be able to see your IP address, like any VPN service. This may be an issue if you trust ProtonVPN less than the Tor network.

Como los servicios de VPN sí conocen la dirección IP de quién los utiliza, aunque en el caso de Proton no la almacenen ni las autoridades puedan solicitarlo, seguramente bajo ciertas circunstancias se termine sabiendo la dirección IP original. 

Para resolver esto, recomiendan [utilizar Tor](https://protonmail.com/tor), porque Tor se encargará de ocultar nuestra IP y la empresa Proton no podrá aportarla a las autoridades al no disponer de ella.

## Conclusión

La idea que he sacado es que, para conseguir el anonimato no se puede depender solamente de la compañía Proton o utilizar VPN de otra empresa. Son curiosos los detalles del funcionamiento de cada servicio.

## Nota final

En un comentario a esta entrada del blog, el equipo de [Proton señaló](https://www.linkedin.com/feed/update/urn:li:activity:6842781257714159616?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A6842781257714159616%2C6843100674788491265%29) (muchas gracias) que Tor es una mejor alternativa en algunos threat models, para otros recomiendan ProtonVPN:

> Hi! Please note that our blogpost you quoted in your article simply indicates that, for certain threat models, Tor network may be a better approach to using a VPN. However, if your threat model is covered by VPN technology, we recommend ProtonVPN.

## Recursos

IP de un usuario facilitada por ProtonMail a las autoridades Suizas y privacidad VS anonimato

<https://protonmail.com/blog/climate-activist-arrest/>

Noticia en The Hackers News

<https://thehackernews.com/2021/09/protonmail-shares-activists-ip-address.html>

Recolección información ProtonMail

<https://protonmail.com/privacy-policy>

Recolección información ProtonVPN

<https://protonvpn.com/privacy-policy>

<https://protonvpn.com/support/tor-browser-vs-tor-vpn/>

Recolección información ProtonMail VS ProtonVPN

<https://twitter.com/ProtonMail/status/1435530623087792133>

ProtonMail con Tor

<https://protonmail.com/tor>

Comentario de Proton en LinkedIn

<https://www.linkedin.com/feed/update/urn:li:activity:6842781257714159616?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A6842781257714159616%2C6843100674788491265%29>

