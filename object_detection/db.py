""" db functions """


def get_or_create_user(db, effective_user, chat_id):
    """get or create user("""
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "chat_id": chat_id
        }
        db.users.insert_one(user)
    return user


def save_car_counts(db, user_id, car_count, ratio_in_img, img_name = ""):
    """save car counts"""
    data = {
        "image": img_name,
        "car_count": car_count,
        "ratio": ratio_in_img,
        "user_id": user_id
    }
    db.car_counts.insert_one(data)


def save_detected_defects(db, user_id, object_class, label, img_name = ""):
    """save detected defects"""
    data = {
        "image": img_name,
        "object_class": object_class,
        "object_label": label,
        "user_id": user_id
    }
    db.detected_defects.insert_one(data)


def defects_stat(db):
    """defects stat"""
    no_results = db.detected_defects.find({"object_class": 0})
    defect_results = db.detected_defects.find({"object_class": 1})
    latch_results = db.detected_defects.find({"object_class": 2})
    return (no_results.count(), defect_results.count(), latch_results.count())


def cars_stat(db):
    """cars stat"""
    query = [{"$group" : {"_id" : 0,
              "total" : {"$sum" : "$car_count"}
             }}]
    test = list(db.car_counts.aggregate(query))
    return test[0]['total']
