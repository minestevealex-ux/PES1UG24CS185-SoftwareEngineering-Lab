
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# Ticket Price Tests

def test_invalid_category():
    with pytest.raises(ValueError):
        ticket_price("invalid", 30, "tuesday", False)

def test_negative_age():
    with pytest.raises(ValueError):
        ticket_price("adult", -1, "tuesday", False)

def test_child_under_five():
    assert ticket_price("child", 4, "tuesday", False) == 0

def test_monday_discount():
    assert ticket_price("adult", 30, "monday", False) == 150

def test_weekend_price():
    assert ticket_price("adult", 30, "saturday", False) == 350

def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200

def test_adult_guided_tour():
    assert ticket_price("adult", 30, "tuesday", True) == 400


# Group Discount Tests

def test_invalid_group_size():
    with pytest.raises(ValueError):
        group_discount(0, False)

def test_school_large_group():
    assert group_discount(20, True) == 40

def test_school_small_group():
    assert group_discount(5, True) == 25

def test_regular_large_group():
    assert group_discount(15, False) == 20

def test_regular_medium_group():
    assert group_discount(8, False) == 10

def test_regular_small_group():
    assert group_discount(4, False) == 0


# Gallery Entry Tests

def test_gallery_full():
    assert gallery_entry(100, 100, False) == "wait"

def test_gallery_queue():
    assert gallery_entry(91, 100, False) == "queue"

def test_gallery_timed_slot():
    assert gallery_entry(95, 100, True) == "enter"

def test_gallery_normal_entry():
    assert gallery_entry(50, 100, False) == "enter"

