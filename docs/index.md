# 3615 GPT

[English version](index.en.md)

Aller directement à la [démo](#demo)

<p align="center"><img src="./minitel.jpg" width="600" alt="photo d'un minitel"/></p>

J'ai récemment récupéré un minitel et je me suis dit que j'allais essayer d'en
faire un petit terminal rétro pour afficher la météo, ou les news, etc. Quand
j'ai commencé, ça ne m'a pas étonné de découvrir que beaucoup de hackers se
sont déjà intéressés à la question, et pour le plus gros de ce projet il m'a
suffi de suivre diverses instructions sur le net.

D'abord, l'adaptateur USB, copié de: [Un minitel comme terminal linux
USB. Partie 1 : Hardware](https://pila.fr/wordpress/?p=361). Je suis loin
d'avoir le talent de soudeur de pila, donc mon adaptateur est légèrement plus
gros...


<p align="center"><img src="./cable.jpg" width="600" alt="photo d'un cable usb-minitel"/></p>


Ensuite le logiciel. Je ne voulais pas utiliser un simple terminal ASCII, mais
vraiment pouvoir utiliser l'interface graphique typique du minitel: les
caractères semi-graphiques, la double taille horizontale et verticale, etc., que
l'on ne peut recréer avec un VT100 de base. J'ai trouvé
[PyMinitel](https://github.com/Zigazou/PyMinitel), une impressionnante librairie
Python qui permet de controller un minitel, avec entrée, sortie, couleurs, et
tout ce dont j'avais envie.

Histoire d'écrire mon code sans avoir à sortir et brancher le minitel à chaque
fois, j'ai écrit une petite librairie qui permet d'émuler l'écran, compatible
avec PyMinitel.  Grace à pygame, la [fonte minitel](https://github.com/Zigazou/Minitel-Canvas), une [fonte
semi-graphique compatible](https://github.com/Zigazou/Minitel-Canvas), ca peut afficher ca:


<p align="center"><img src="./emulator.png" width="600" alt="capture d'écran de l'émulateur"/></p>


Pour la connection à ChatGPT, j'utilise la librairie python fournie par OpenAI et c'est vraiment très simple.

## Demo

Et voilà ce que ca donne:

<p align="center"><iframe width="600" height="1067" src="https://www.youtube.com/embed/4mqJF_qJgYU" title="3615 GPT" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></p>
