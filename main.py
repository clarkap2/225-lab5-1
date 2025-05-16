from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Use a local SQLite database file for portability
DATABASE = 'shopping.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS shopping_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                status TEXT DEFAULT 'Needed'
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    db = get_db()

    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            item_id = request.form.get('item_id')
            db.execute('DELETE FROM shopping_list WHERE id = ?', (item_id,))
            db.commit()
            message = 'Item deleted.'
        elif request.form.get('action') == 'update':
            item_id = request.form.get('item_id')
            new_status = request.form.get('status')
            db.execute('UPDATE shopping_list SET status = ? WHERE id = ?', (new_status, item_id))
            db.commit()
            message = 'Item status updated.'
        else:
            item_name = request.form.get('item')
            if item_name:
                db.execute('INSERT INTO shopping_list (item) VALUES (?)', (item_name,))
                db.commit()
                message = 'Item added.'
            else:
                message = 'Please enter an item name.'

    items = db.execute('SELECT * FROM shopping_list').fetchall()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Shopping List</title></head>
        <body>
            <h2>Add Item</h2>
            <form method="POST" action="/">
                <input type="text" name="item" placeholder="Enter an item" required>
                <input type="submit" value="Add Item">
            </form>
            <p>{{ message }}</p>
            <h3>Shopping List</h3>
            {% if items %}
                <table border="1">
                    <tr><th>Item</th><th>Status</th><th>Update</th><th>Delete</th></tr>
                    {% for item in items %}
                    <tr>
                        <td>{{ item['item'] }}</td>
                        <td>{{ item['status'] }}</td>
                        <td>
                            <form method="POST" action="/">
                                <input type="hidden" name="item_id" value="{{ item['id'] }}">
                                <select name="status">
                                    <option value="Needed" {% if item['status'] == 'Needed' %}selected{% endif %}>Needed</option>
                                    <option value="Purchased" {% if item['status'] == 'Purchased' %}selected{% endif %}>Purchased</option>
                                </select>
                                <input type="hidden" name="action" value="update">
                                <input type="submit" value="Update">
                            </form>
                        </td>
                        <td>
                            <form method="POST" action="/">
                                <input type="hidden" name="item_id" value="{{ item['id'] }}">
                                <input type="hidden" name="action" value="delete">
                                <input type="submit" value="Delete">
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>No items in your shopping list.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, items=items)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)
