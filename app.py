from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import Seller, Buyer, Deal, Term, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pranavsonawane@localhost/Negotiation_Engine'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy without associating it with the app for now
db.init_app(app)

# Create database tables within application context
with app.app_context():
    db.create_all()

# Define database models in models.py

@app.route('/', methods=['GET'])
def index():
    # Extract data from request
    # Validate and process data
    # Save new product to the database
    return jsonify({'message': 'hello'}), 200

# Placeholder lists for database
sellers = []
buyer = []
deals = []
term = []
# Placeholder data
seller_deals = []
all_deals = []

# Create instances of Seller
seller1 = Seller(
    name='John Doe',
    gstno='123456789',
    businessregno='ABC123',
    rating=4.5,
    phoneno='1234567890',
    email='john@example.com',
    address='123 Main Street, City, Country',
    password='password123'
)

seller2 = Seller(
    name='Alice Smith',
    gstno='987654321',
    businessregno='XYZ456',
    rating=4.2,
    phoneno='9876543210',
    email='alice@example.com',
    address='456 Elm Street, City, Country',
    password='password456'
)

# Create instances of Buyer
buyer1 = Buyer(
    name='Jane Doe',
    phoneno='1112223333',
    email='jane@example.com',
    address='789 Oak Avenue, City, Country',
    password='password789'
)

buyer2 = Buyer(
    name='Bob Johnson',
    phoneno='4445556666',
    email='bob@example.com',
    address='101 Pine Street, City, Country',
    password='password101'
)

# Create instances of Deal
deal1 = Deal(
    name='Deal 1',
    seller=seller1  # Assuming seller1 is the seller for this deal
)

deal2 = Deal(
    name='Deal 2',
    seller=seller2  # Assuming seller2 is the seller for this deal
)

# Create instances of Term
term1 = Term(
    content='Term 1 content',
    is_accepted=True,
    deal=deal1  # Assuming deal1 is the deal for this term
)

term2 = Term(
    content='Term 2 content',
    is_accepted=False,
    is_declined=True,
    counter_term='Counter term content',
    deal=deal2  # Assuming deal2 is the deal for this term
)

# Add instances to lists
sellers = [seller1, seller2]
buyers = [buyer1, buyer2]
deals = [deal1, deal2]
terms = [term1, term2]



# Authentication Endpoints
@app.route('/login/seller', methods=['POST'])
def login_seller():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Find the seller with the given email
    seller = Seller.query.filter_by(email=email).first()
    
    if seller and seller.password == password:
        # Authentication successful
        return jsonify({'message': 'Seller login successful', 'seller': seller.id}), 200
    else:
        # Authentication failed
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/login/buyer', methods=['POST'])
def login_buyer():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Find the buyer with the given email
    buyer = Buyer.query.filter_by(email=email).first()
    
    if buyer and buyer.password == password:
        # Authentication successful
        return jsonify({'message': 'Buyer login successful', 'buyer': buyer.id}), 200
    else:
        # Authentication failed
        return jsonify({'error': 'Invalid email or password'}), 401

# Endpoint for seller registration
@app.route('/seller/register', methods=['POST'])
def seller_register():
    data = request.json
    new_seller = Seller(
        name=data['name'],
        gstno=data['gstno'],
        businessregno=data['businessregno'],
        rating=data['rating'],
        phoneno=data['phoneno'],
        email=data['email'],
        address=data['address'],
        password=data['password']
    )
    db.session.add(new_seller)
    db.session.commit()
    return jsonify({'message': 'Seller registration successful'}), 201

# Endpoint for buyer registration
@app.route('/buyer/register', methods=['POST'])
def buyer_register():
    data = request.json
    new_buyer = Buyer(
        name=data['name'],
        phoneno=data['phoneno'],
        email=data['email'],
        address=data['address'],
        password=data['password']
    )
    db.session.add(new_buyer)
    db.session.commit()
    return jsonify({'message': 'Buyer registration successful'}), 201


# Seller Deal Management Endpoints
@app.route('/seller/deals', methods=['GET'])
def get_seller_deals():
    return jsonify(seller_deals)

@app.route('/seller/deals', methods=['POST'])
def create_seller_deal():
    data = request.json
    seller_deals.append(data)
    return jsonify({'message': 'Seller deal created successfully'}), 201

@app.route('/seller/deals/<int:deal_id>', methods=['GET', 'PUT', 'DELETE'])
def seller_deal(deal_id):
    if request.method == 'GET':
        return jsonify(seller_deals[deal_id])
    elif request.method == 'PUT':
        data = request.json
        seller_deals[deal_id] = data
        return jsonify({'message': 'Seller deal updated successfully'}), 200
    elif request.method == 'DELETE':
        seller_deals.pop(deal_id)
        return jsonify({'message': 'Seller deal deleted successfully'}), 200

# Customer Deal Management Endpoints
@app.route('/deals', methods=['GET'])
def get_all_deals():
    return jsonify(all_deals)

@app.route('/deals/<int:deal_id>', methods=['GET'])
def get_deal(deal_id):
    return jsonify(all_deals[deal_id])

# Search and Filtering Endpoints
@app.route('/deals/search', methods=['POST'])
def search_deals():
    criteria = request.json
    filtered_deals = []

    # Iterate over all deals and filter based on criteria
    for deal in all_deals:
        # Filtering based on category
        if 'category' in criteria and criteria['category'] != deal['category']:
            continue  # Skip if category does not match

        # Filtering based on price range
        if 'price_range' in criteria:
            min_price, max_price = map(float, criteria['price_range'].split('-'))
            if not min_price <= deal['price'] <= max_price:
                continue  # Skip if price is not in range

        # Add the deal to filtered deals if all criteria match
        filtered_deals.append(deal)

    return jsonify(filtered_deals)

# Deal Acceptance and Counteroffer Endpoints
@app.route('/deals/<int:deal_id>/accept', methods=['PUT'])
def accept_deal(deal_id):
    # Placeholder code to accept all terms of a deal
    deal = Deal.query.get_or_404(deal_id)
    deal.accepted = True
    db.session.commit()
    return jsonify({'message': 'Deal accepted successfully'}), 200

@app.route('/deals/<int:deal_id>/counteroffer', methods=['PUT'])
def counteroffer_deal(deal_id):
    # Placeholder code to submit counteroffer terms for a deal
    data = request.json
    deal = Deal.query.get_or_404(deal_id)
    deal.counteroffer_terms = data.get('counteroffer_terms')
    db.session.commit()
    return jsonify({'message': 'Counteroffer submitted successfully'}), 200

@app.route('/deals/<int:deal_id>/accept_counteroffer', methods=['PUT'])
def accept_counteroffer(deal_id):
    # Placeholder code to accept counteroffer terms for a deal
    deal = Deal.query.get_or_404(deal_id)
    deal.accepted_counteroffer = True
    db.session.commit()
    return jsonify({'message': 'Counteroffer accepted successfully'}), 200

if __name__ == '__main__':
    
    app.run(debug=True)
