
# To-Do App

## Popis projektu
Jednoduchá aplikace pro správu úkolů, vytvořená pomocí Django frameworku.

---

## Nastavení projektu

1. **Klonování repozitáře**:
    ```bash
    git clone https://github.com/Montikks/To_Do_app.git
    cd To_Do_app
    ```

2. **Vytvoření virtuálního prostředí**:
    - Pro Windows:
      ```bash
      python -m venv .venv
      .venv\Scripts\activate
      ```
    - Pro Linux/Mac:
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```

3. **Instalace závislostí**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Migrace databáze**:
    - Vytvoření migrací:
      ```bash
      python manage.py makemigrations
      ```
    - Aplikace migrací:
      ```bash
      python manage.py migrate
      ```

5. **Spuštění serveru**:
    ```bash
    python manage.py runserver
    ```

6. **Otevření aplikace v prohlížeči**:
    ```text
    http://127.0.0.1:8000
    ```

---

## Funkce aplikace
- Vytváření, editace a mazání úkolů
- Označování úkolů jako dokončené/rozpracované
- Přihlášení a registrace uživatelů

---

## Technologie
- **Django**: Framework pro backend
- **SQLite**: Použitá databáze
- **HTML/CSS**: Frontend technologie
- **Bootstrap**: Stylování

---

## Autoři
- Pavel Mrazek 
- Lucia Poľaková
