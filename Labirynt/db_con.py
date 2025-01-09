import psycopg2
from psycopg2.extras import DictCursor
import json
import ast
from Escapee import Escapee


def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",  # lub "localhost"
            port=5432,
            dbname="postgres",
            user="root",
            password="minotaur"
        )
        print("Połączenie udane!")
        return conn
    except Exception as e:
        print("Błąd połączenia: {}\n".format(type(e).__name__))


def load_q_table(conn, id):
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT * FROM escapees WHERE id=%s", (id,))
        rows = cursor.fetchall()

        if not rows:
            print(f"Nie znaleziono uciekiniera o ID {id}")
            return None

        q_table = {}
        for row in rows:
            try:
                state = ast.literal_eval(row['state'])  # Deserializacja krotek
            except (ValueError, SyntaxError):
                print(f"Błąd przy deserializacji stanu dla escapee ID {id}")
                continue

            # Zakładamy, że q_val jest teraz w formacie JSON
            try:
                q_val = json.loads(row['q_val']) if isinstance(row['q_val'], str) else row['q_val']
            except json.JSONDecodeError:
                print(f"Błąd w deserializacji q_val dla escapee ID {id}")
                continue

            q_table[state] = q_val

        cursor.close()

        # Tworzymy obiekt Escapee i przypisujemy załadowaną q_table
        escapee = Escapee(escapee_id=id, environment=None)
        escapee.q_table = q_table
        return escapee

    except Exception as e:
        print(f"Błąd w ładowaniu Q-tabeli dla escapee o ID {id}: {type(e).__name__} - {str(e)}")
        return None



def save_q_table(conn, q_table, id):
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)

        for state, actions in q_table.items():
            # Serializujemy tylko akcje
            q_val_json = json.dumps(actions)  # Q-values dla danego stanu
            state_str = str(state)  # Przechowuj state jako tekst (np. "(0, 0)")

            cursor.execute("""
                INSERT INTO escapees (id, state, q_val)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) 
                DO UPDATE SET q_val = EXCLUDED.q_val
            """, (id, state_str, q_val_json))  # Używamy state_str i q_val_json

        conn.commit()
        return True

    except Exception as e:
        print(f"Błąd w zapisie danych: {type(e).__name__} - {str(e)}")
        conn.rollback()
        return False

def exists_escapee(conn, id):
    try:
        cursor = conn.cursor()
        query = "SELECT 1 FROM escapees WHERE id=%s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"Błąd w szukaniu uciekiniera w bazie: {type(e).__name__}\n")
        return False

def insert_escapee(conn,id):
    try:
        cursor = conn.cursor(cursor_factory=DictCursor)
        state="(0,0)"
        q_val_json=json.dumps({"0": 0, "1": 0, "2": 0, "3": 0})
        id=int(id)

        cursor.execute("INSERT INTO escapees (id,state, q_val) VALUES (%s,%s,%s)",(id,state,q_val_json))
        conn.commit()
        return True
    except Exception as e:
        print(f"Błąd w zapisie danych: {type(e).__name__} - {str(e)}")
        conn.rollback()
        return False
