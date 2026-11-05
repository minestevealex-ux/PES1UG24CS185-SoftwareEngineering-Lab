
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# TICKET PRICE BRANCH TESTS

def test_invalid_category():
    with pytest.raises(ValueError):
        ticket_price("invalid", 30, "tuesday", False)

def test_negative_age():
    with pytest.raises(ValueError):
        ticket_price("adult", -1, "tuesday", False)

def test_child_under_five():
    assert ticket_price("child", 4, "tuesday", False) == 0

def test_age_five():
    assert ticket_price("child", 5, "tuesday", False) == 100

def test_monday():
    assert ticket_price("adult", 30, "monday", False) == 150

def test_weekday():
    assert ticket_price("adult", 30, "tuesday", False) == 300

def test_saturday():
    assert ticket_price("adult", 30, "saturday", False) == 350

def test_sunday():
    assert ticket_price("adult", 30, "sunday", False) == 350

def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200

def test_non_student_guided_tour():
    assert ticket_price("adult", 30, "tuesday", True) == 400


# GROUP DISCOUNT BRANCH TESTS

def test_invalid_group():
    with pytest.raises(ValueError):
        group_discount(0, False)

def test_school_group_20():
    assert group_discount(20, True) == 40

def test_school_group_below_20():
    assert group_discount(19, True) == 25

def test_regular_group_15():
    assert group_discount(15, False) == 20

def test_regular_group_8():
    assert group_discount(8, False) == 10

def test_regular_group_below_8():
    assert group_discount(7, False) == 0


# GALLERY ENTRY BRANCH TESTS

def test_gallery_full():
    assert gallery_entry(100, 100, False) == "wait"

def test_gallery_below_capacity():
    assert gallery_entry(50, 100, False) == "enter"

def test_gallery_at_90_percent():
    assert gallery_entry(90, 100, False) == "queue"

def test_gallery_above_90_percent():
    assert gallery_entry(95, 100, False) == "queue"

def test_gallery_timed_slot():
    assert gallery_entry(95, 100, True) == "enter"

def test_gallery_below_90_with_timed_slot():
    assert gallery_entry(50, 100, True) == "enter"

