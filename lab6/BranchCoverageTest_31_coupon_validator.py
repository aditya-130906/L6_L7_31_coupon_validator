
import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# Coupon discount branches

def test_invalid_cart():
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_welcome_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend_large_cart():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == 120


def test_weekend_small_cart():
    assert coupon_discount("WEEKEND20", 200, True, "sun") == 50


def test_weekend_coupon_on_weekday():
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0


def test_flat100_eligible():
    assert coupon_discount("FLAT100", 400, False, "mon") == 100


def test_flat100_at_threshold():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


def test_unknown_coupon():
    assert coupon_discount("INVALID", 400, False, "mon") == 0


# Best discount branches

def test_best_discount_selects_highest():
    assert best_discount(
        ["FLAT100", "WELCOME10"], 400, True, "mon"
    ) == 100


def test_best_discount_empty_list():
    assert best_discount([], 200, True, "mon") == 0


def test_best_discount_applies_cap():
    assert best_discount(["WEEKEND20"], 100, False, "sat") == 40


def test_best_discount_below_cap():
    assert best_discount(["WELCOME10"], 200, True, "mon") == 20


# Expiry branches

def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True


def test_coupon_expired():
    assert is_expired(11, 5, 5) is True


def test_coupon_not_expired_at_boundary():
    assert is_expired(10, 5, 5) is False
