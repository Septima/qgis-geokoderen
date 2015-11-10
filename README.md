Geokoderen
==============

QGIS plugin som tillader brugeren at åbne et punkt fra QGIS i
[Geokoderen.dk](http://geokoderen.dk).

Pluginet er udviklet af [Septima](http://www.septima.dk), og er frigivet under
Open Source licensen [GPL3](http://www.gnu.org/licenses/gpl.html).

Installation
--------------
Den nemmeste måde at installere pluginet på, er at tilføje Septima's repository
til QGIS. På den måde finder QGIS selv en kompatibel version af pluginet, og du
får automatisk besked, når der kommer nye versioner af pluginet.

Pluginet installerer en knap, som kan aktiveres og derefter kan der trykkes i kortet, hvorved det punkt der er trykket på vil blive åbnet i [Geokoderen.dk](http://geokoderen.dk).

###QGIS 2.x
 - 1) Åbn Plugin Manageren (Klik Plugins -> Manage and Install Plugins)
 - 2) Vælg Settings
 - 3) Klik Add under Plugin Repositories
 - 4) Indtast et selvvalgt navn (feks Septima) og under URL indtastes http://qgis.septima.dk/plugins
 - 5) I Plugin Manageren vil pluginet nu være listet under Get more

![Add repository](http://septima.github.io/qgis-geosearch/img/qgis2-addrepo.PNG)

Opdatering
--------------
Nye versioner af pluginet udstilles via Septimas plugin repository, som
installeret ovenfor. I Plugin Manageren vil opdateringer fremgå under punktet
Upgradeable. Automatisk advisering om opgraderbare plugins kan aktiveres under
Settings i Plugin Manageren.
