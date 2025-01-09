To-Do Aplikace
==============

Popis Projektu
--------------

**To-Do Aplikace** je webová aplikace vyvinutá pomocí frameworku Django v jazyce Python, která umožňuje uživatelům efektivně spravovat své úkoly a to-do listy. Aplikace nabízí robustní systém autentizace a autorizace, podporuje různé uživatelské role a zahrnuje moderní uživatelské rozhraní s funkcí přepínání mezi světlým a tmavým režimem.

Hlavní Funkce
-------------

### Registrace a Přihlášení Uživatelů

*   Uživatelé mohou vytvářet své účty, přihlašovat se a odhlašovat.
    
*   Systém podporuje různé uživatelské role s odlišnými oprávněními.
    

### Správa Úkolů

*   Vytváření, úprava, označování jako dokončené a odstraňování úkolů.
    
*   Detailní zobrazení jednotlivých úkolů s možností správy podúkolů.
    

### Uživatelské Role

*   Různí uživatelé mohou mít různá práva a přístup k určitým funkcím aplikace.
    

### Dark Mode

*   Možnost přepínání mezi světlým a tmavým režimem pro lepší uživatelský komfort.
    

### Stylizace a Uživatelské Rozhraní

*   Použití moderního CSS pro přehledné a responzivní rozhraní.
    
*   Implementace toast notifikací pro informování uživatelů o akcích.
    

### Validace Formulářů

*   Zajištění správného zadávání dat prostřednictvím validace na frontendu i backendu.
    

### Testování

*   Implementace testů pro modely, formuláře a uživatelské rozhraní, aby byla zajištěna kvalita a stabilita aplikace.
    

Technologie a Nástroje
----------------------

*   **Backend:**
    
    *   Python
        
    *   Django
        
*   **Frontend:**
    
    *   HTML5
        
    *   CSS3
        
    *   JavaScript (pro validaci a interaktivní prvky)
        
*   **Databáze:**
    
    *   SQLite (použité v rámci vývoje)
        
*   **Verzovací Systém:**
    
    *   Git
        
    *   GitHub pro správu repozitáře
        

Architektura Aplikace
---------------------

### Modely

Definice modelů pro uživatele, úkoly a podúkoly s odpovídajícími vztahy.

### Šablony

*   Použití dědičnosti šablon pro konzistentní vzhled a strukturu webových stránek.
    
*   Organizace šablon do samostatných adresářů podle aplikací.
    

### Styly

*   Použití CSS proměnných pro snadnou správu barev a témat (světlý/tmavý režim).
    
*   Specifické třídy pro různé typy tlačítek (Detail, Edit, Complete) s odpovídajícími styly.
    

ER Diagram
----------

_Poznámka: Vygenerujte ER diagram a nahraďte cestu k obrázku._

Autentizace a Autorizace
------------------------

### Registrace Uživatelských Účtů

Uživatelé mohou vytvářet nové účty s unikátními přihlašovacími údaji.

### Přihlašování/Odhlášení

Bezpečný systém přihlašování a odhlašování uživatelů.

### Uživatelské Role

Definice různých rolí (např. administrátor, běžný uživatel) s odlišnými oprávněními a přístupem k funkcím aplikace.

Instalace a Spuštění
--------------------

### Předpoklady

*   Python 3.8+
    
*   Git
    

### Klonování Repozitáře

```bash
git clone https://github.com/Montikks/To_Do_app.git
cd To_Do_app
```


### Vytvoření a Aktivace Virtuálního Prostředí

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Instalace Závislostí

```bash
pip install -r requirements.txt
```

### Nastavení Databáze


```bash
Zkopírovat kódpython manage.py migrate
```

### Vytvoření Superuživatele

```bash
python manage.py createsuperuser
```
### Spuštění Vývojového Serveru


```bash
python manage.py runserver
```
Přejděte na [http://127.0.0.1:8000/](http://127.0.0.1:8000/) ve vašem prohlížeči.



Testování
---------

### Spuštění Testů

```bash
python manage.py test
```

Zajištění, že všechny testy proběhnou úspěšně bez chyb.

Použití
-------

### Přihlášení a Správa Úkolů

*   Registrujte si účet nebo se přihlaste.
    
*   Vytvářejte nové úkoly, upravujte je, označujte jako dokončené nebo je odstraňujte.
    
*   Spravujte podúkoly pro jednotlivé úkoly.
    

### Přepínání Dark Mode

*   Klikněte na tlačítko "Dark Mode" v hlavičce pro přepnutí mezi světlým a tmavým režimem.
    

Validace Vstupních Dat
----------------------

*   Formuláře v aplikaci obsahují validaci na frontendu (JavaScript) i backendu (Python), aby bylo zajištěno správné zadávání dat.
    

Struktura Kódu
--------------

*   **Models:** Definice databázových modelů.
    
*   **Views:** Logika zpracování požadavků a odpovědí.
    
*   **Templates:** HTML šablony pro uživatelské rozhraní.
    
*   **Static:** Statické soubory jako CSS a JavaScript.
    

GIT Repozitář
-------------

### Branching Strategie

*   Hlavní větev: main
    
*   Větve pro nové funkce: feature/nazev-funkce
    

### Commit Zprávy

```bash
git commit -m "Přidání funkce přepínání Dark Mode"
 ```   

### .gitignore

Soubor .gitignore obsahuje všechny nepotřebné soubory a složky, které by neměly být sledovány Git repozitářem, např.:

```bash
arduinoZkopírovat kódvenv/
__pycache__/
*.pyc
db.sqlite3
/static/
```
### README

Tento soubor README.md slouží jako úvodní stránka repozitáře, poskytuje přehled o projektu, jeho funkcích, instalaci a použití.

Pokrývání Testů a Kvalita
-------------------------

*   **Testy:** Implementace unit testů pro modely, formuláře a funkce aplikace.
    
*   **Kvalita Kódu:** Dodržení PEP8 specifikace, čitelnost kódu a správná struktura souborů.
    

Autorizace a Autentizace
------------------------

*   **Vytváření Uživatelských Účtů:** Možnost registrace nových uživatelů.
    
*   **Přihlašování/Odhlášení:** Bezpečné přihlašování a odhlašování uživatelů.
    
*   **Uživatelské Role:** Různé role s odlišnými právy a přístupem k funkcím aplikace.
    

Specifické Části Projektu
-------------------------

*   **Uživatelské Role:** Administrátoři mohou spravovat uživatele a úkoly, běžní uživatelé mohou spravovat pouze své vlastní úkoly.
    
*   **Dark Mode:** Uživatelské rozhraní podporuje světlý a tmavý režim.
    
*   **Validace Formulářů:** Zajištění správného zadávání dat pomocí validace na frontendu a backendu.