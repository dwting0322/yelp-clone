from flask import Blueprint, redirect, url_for, render_template, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from ..models.business import Business
from ..forms.business_form import BusinessForm
from ..models.db import db

business_routes = Blueprint('business', __name__)



# Get all businesses
@business_routes.route("/")
def all_businesses():
    all_business = Business.query.all()
    all_business_json = [business.to_dict() for business in all_business]
    return {"businesses": all_business_json}


# Get one business by business ID
@business_routes.route("/<int:business_id>")
def get_one_business(id):
    business = Business.query.get(id)
    return business.to_dict()


# Get all busioness of the Current User
@business_routes.route("/current")
@login_required
def get_current_businesses():
    current_business = Business.query.filter(Business.owner_id == current_user.id).all()
    current_business_json = [current_post.to_dict() for current_post in current_business]
    return {"current_business": current_business_json}
    

#Create a new business
@business_routes.route("new-business", methods=["POST"])
@login_required
def create_new_business():
    form = BusinessForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        new_business = Business(
            owner_id=current_user.id,
            phone=form.data['phone'],
            address=form.data['address'],
            name=form.data['name'],
            description=form.data['description'],
            price_range=form.data['price_range'],
            preview_img=form.data['preview_img'],
            # city=form.data['city'],
            # state=form.data['state'],
            # country=form.data['country'],
            # zipcode=form.data['zipcode'],
            # lat=form.data['lat'],
            # lng=form.data['lng'],
        )
        db.session.add(new_business)
        db.session.commit()
        return new_business

    else:
        return jsonify(form.errors)


#Edit a business
@business_routes.route("/<int:business_id>", methods=["PUT"])
@login_required
def edit_business():
    form = BusinessForm()
    business = Business.query.get_or_404(id)

    if current_user.id != business.owner_id:
        return {"message": "You don't have authorization to update", "statusCode": 403}

    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        business = Business(
            owner_id=current_user.id,
            phone=form.data['phone'],
            address=form.data['address'],
            name=form.data['name'],
            description=form.data['description'],
            price_range=form.data['price_range'],
            preview_img=form.data['preview_img'],
            # city=form.data['city'],
            # state=form.data['state'],
            # country=form.data['country'],
            # zipcode=form.data['zipcode'],
            # lat=form.data['lat'],
            # lng=form.data['lng'],
        )
        db.session.add(business)
        db.session.commit()
        return business

    else:
        return jsonify(form.errors)



# Delete Business
@business_routes.route("/<int:business_id>", methods=["DELETE"])
@login_required
def delete_business(business_id):
    business = Business.query.filter(Business.id == business_id).first()
    if current_user.id == business.owner_id:
        db.session.delete(business)
        db.session.commit()
        return {'message': 'Successfully deleted'}
    else:
        return {'message': 'Unauthorized user', "statusCode": 403}