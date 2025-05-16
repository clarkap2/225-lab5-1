import sqlite3

DATABASE = 'shopping.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def generate_test_items(num_items):
    db = connect_db()
    for i in range(num_items):
        item = f'Test Item {i}'
        db.execute('INSERT INTO shopping_list (item, status) VALUES (?, ?)', (item, 'Needed'))
    db.commit()
    print(f'{num_items} test items added to the shopping list.')
    db.close()

if __name__ == '__main__':
    generate_test_items(10)
