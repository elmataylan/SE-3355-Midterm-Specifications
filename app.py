from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import base64


app = Flask(__name__)

def b64encode(data):
    return base64.b64encode(data).decode('utf-8')

app.jinja_env.filters['b64encode'] = b64encode

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '00000000'
app.config['MYSQL_DB'] = 'products'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('query')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products_1 WHERE urunismi LIKE %s", ('%' + query + '%',))
    products = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT urunkategori FROM products_1")
    categories = cur.fetchall()
    cur.close()


    category_counts = {}
    for category in categories:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM products_1 WHERE urunkategori = %s AND urunismi LIKE %s", (category[0], '%' + query + '%'))
        count = cur.fetchone()[0]
        category_counts[category[0]] = count
        cur.close()


    matched_categories = []
    for category in categories:
        if query.lower() in category[0].lower():
            matched_categories.append((category[0], True, category_counts.get(category[0], 0)))
        else:
            matched_categories.append((category[0], False, category_counts.get(category[0], 0)))

    num_results = len(products)
    return render_template('search_results.html', products=products, categories=matched_categories, category_counts=category_counts, search_term=query, num_results=num_results)

@app.route('/category/<category>')
def category(category):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products_1 WHERE urunkategori = %s", (category,))
    products = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT DISTINCT urunkategori FROM products_1")
    categories = cur.fetchall()
    cur.close()


    category_counts = {}
    for cat in categories:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM products_1 WHERE urunkategori = %s", (cat[0],))
        count = cur.fetchone()[0]
        category_counts[cat[0]] = count
        cur.close()

    num_results = len(products)

    return render_template('category_results.html', products=products, categories=categories, category_counts=category_counts, selected_category=category, num_results=num_results)

@app.route('/product/<int:product_id>')
def product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products_1 WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()

    if not product:
        return "Product not found", 404

    return render_template('product_details.html', product=product)

if __name__ == '__main__':
    app.run()
