
import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# Coupon discount tests

def test_invalid_cart():
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_welcome_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend20_large_cart():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == 120


def test_weekend20_small_cart():
    assert coupon_discount("WEEKEND20", 200, True, "sun") == 50


def test_weekend20_weekday():
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0


def test_flat100_eligible_cart():
    assert coupon_discount("FLAT100", 400, False, "mon") == 100


def test_flat100_ineligible_cart():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


def test_unknown_coupon():
    assert coupon_discount("INVALID", 400, False, "mon") == 0


# Best discount tests

def test_best_discount_without_cap():
    assert best_discount(["WELCOME10"], 200, True, "mon") == 20


def test_best_discount_with_cap():
    assert best_discount(["WEEKEND20"], 100, False, "sat") == 40


# Expiry tests

def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True


def test_coupon_expired_after_validity():
    assert is_expired(10, 4, 5) is True
