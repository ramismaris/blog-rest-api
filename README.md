# Installation

---

1. Create .env file and fill it
   ```bash
   cp .env.dist .env && nano .env
   ```

2. ```bash
   docker-compose build
   ```
   
3. ```bash
   docker-compose up -d
   ```

4. To fill the database, run
   ```bash
   python3 tests/fill_database.py
   ```