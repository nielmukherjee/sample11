import os
import tablib
from flask import Flask, render_template, redirect, url_for, session, request
from flask.json import jsonify
import subprocess
import database
import utils as ut

app = Flask(__name__)
app.secret_key = "major project secret key"


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('new_dashboard.html')


@app.route('/profile',methods=['POST','GET'])
def profile():
    db = database.Database()
    try:
        db.preference_table()
    except:
        pass
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    data = db.view_preference(session.get('id'));
    if data:
        pref = data[0]
        return render_template('Profile.html',pref=pref)
    if request.method == 'POST':
        preference = request.form.get('prefer')
        review = request.form.get('review')
        rating = request.form.get('rating')
        if preference and review and rating:
            db.add_preference(preference, review, rating,session.get('id'))
            return redirect(url_for('profile'))            
    return render_template('Profile.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    errors = ''
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('password')
        if username and password:
            db = database.Database()
            userlist = db.view_user()
            for row in userlist:
                if username in row and password in row:
                    print(row)
                    session['id'] = row[0]
                    session['username'] = row[1]
                    session['logged_in'] = True
                    message = "successful logged in"
                    return redirect(url_for('dashboard', data=message))
            errors = "invalid credential"
        else:
            errors = "please fill details"
    return render_template('login.html', errors=errors)


@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = ""
    if request.method == 'POST':
        db = database.Database()
        try:
            db.user_table()
        except:
            pass
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('pwd')
        cpassword = request.form.get('cpwd')
        print(username, email, cpassword, password)

        if password == cpassword and len(username) > 2 and len(
                password) >= 6 and '@' in email and '.com' in email and len(email) >= 11:
            db.add_user(username, email, password)

            return redirect(url_for('login', data=errors))
        else:
            errors = "invalid details"

    return render_template('register.html', errors=errors)


@app.route('/analysis', methods=['GET', 'POST'])
def analysis():

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    recommends_prefer =""
    recommends_reviews=""
    recommends_rating=""
    details = None
    filename = request.args.get('filename')
    folder = "scraper/datasets"
    imagefolder = os.path.join("static", "graph")
    if filename:
        details = {}
        dataset = tablib.Dataset()
        # with open(os.path.join(os.path.dirname(__file__), folder, filename)) as f:
        # dataset.csv = f.read().replace('\n\n', '\n')
        # details = dataset.html

        df = ut.cleaning_columns(os.path.join(folder, filename))
        reviewImage = filename.replace('.csv', '') + '_reviews.jpg'
        ratingImage = filename.replace('.csv', '') + '_rating.jpg'
        priceImage = filename.replace('.csv', '') + '_price.jpg'
        maxPriceImage = filename.replace('.csv', '') + '_max_price.jpg'
        maxReviewImage = filename.replace('.csv', '') + '_max_review.jpg'
        maxRatingImage = filename.replace('.csv', '') + '_max_rating.jpg'
        ut.totalreviews(df, os.path.join(imagefolder, reviewImage))
        ut.rating(df, os.path.join(imagefolder, ratingImage))
        ut.price(df, os.path.join(imagefolder, priceImage))
        ut.pie_price(df, os.path.join(imagefolder, maxPriceImage))
        ut.pie_rating(df, os.path.join(imagefolder, maxRatingImage))
        ut.pie_reviews(df, os.path.join(imagefolder, maxReviewImage))

        details.update({
            'rating': os.path.join(imagefolder, ratingImage),
            'review': os.path.join(imagefolder, reviewImage),
            'price': os.path.join(imagefolder, priceImage),
            'max_rating': os.path.join(imagefolder, maxRatingImage),
            'max_price': os.path.join(imagefolder, maxPriceImage),
            'max_reviews': os.path.join(imagefolder, maxReviewImage)
        })
        # recommendation
    
        db = database.Database()
        db.preference_table()
        pref = db.view_preference(session.get('id'));
        if len(pref) < 1:
            redirect(url_for('profile'))
        else:
            prefers = pref[0][1]
            reviews = pref[0][2]
            rating = pref[0][3]
            df = ut.cleaning_columns(os.path.join(folder, filename))
            recommends_prefer = ut.recommend_on_prefs(df,prefers)
            recommends_reviews = ut.recommend_on_reviews(df,reviews)
            recommends_rating = ut.recommend_on_rating(df,rating)
        
    folder_content = os.listdir(folder)
    datasets = [item for item in folder_content if item.endswith('.csv')]
    return render_template('analyse.html', data=datasets, details=details,rcp=recommends_prefer,rcr=recommends_reviews,rcrt=recommends_rating)


@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login', status="logged_out"))


@app.route('/display')
def display():
    
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    details = None
    filename = request.args.get('filename')
    folder = "scraper/datasets"
    if filename:
        dataset = tablib.Dataset()
        with open(os.path.join(os.path.dirname(__file__), folder, filename)) as f:
            dataset.csv = f.read().replace('\n\n', '\n')
            details = dataset.html
    folder_content = os.listdir(folder)
    datasets = [item for item in folder_content if item.endswith('.csv')]
    return render_template('display.html', data=datasets, details=details)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/fetch_request')
def fetch_request():
    
    search_item = request.args.get('content')
    os.chdir('scraper')
    print(os.getcwd())
    # command = f"scrapy crawl amazon_search -o datasets/{search_item}.csv -a search_term={search_item}"
    command = f"scrapy crawl amazon_search -o datasets/{search_item}.csv -a search_term={search_item}"
    print("command ", command)
    try:
        request_status = subprocess.check_output(command.split(), shell=False)
        print(request_status)
        os.chdir('..')
        return jsonify({'success': "done"})
    except subprocess.CalledProcessError as e:
        print(e)
        os.chdir('..')
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
