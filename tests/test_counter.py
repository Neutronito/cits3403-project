import pytest
from flask_app.models.count import AbstractCountModel, UserCountAlreadyExistException, UserCountNotFoundException


def test_add_user(count_model: AbstractCountModel):
    count_model.add_user("banana")


def test_add_remove_user(count_model: AbstractCountModel):
    count_model.add_user("cat")
    count_model.remove_user("cat")


def test_add_get_count_zero(count_model: AbstractCountModel):
    count_model.add_user("gogo")
    assert count_model.get_count("gogo") == 0


def test_increment_count(count_model: AbstractCountModel):
    count_model.add_user("baba")
    count_model.increment_count("baba")
    assert count_model.get_count("baba") == 1


def test_decrement_count(count_model: AbstractCountModel):
    count_model.add_user("lolo")
    count_model.decrement_count("lolo")
    assert count_model.get_count("lolo") == -1


def test_reset_count(count_model: AbstractCountModel):
    count_model.add_user("dodo")
    count_model.increment_count("dodo")
    count_model.increment_count("dodo")
    count_model.reset_count("dodo")
    assert count_model.get_count("dodo") == 0


def test_add_user_exception(count_model: AbstractCountModel):
    count_model.add_user("gege")
    with pytest.raises(UserCountAlreadyExistException):
        count_model.add_user("gege")


def test_remove_user_exception(count_model: AbstractCountModel):
    with pytest.raises(UserCountNotFoundException):
        count_model.remove_user("pop")


def test_increment_count_exception(count_model: AbstractCountModel):
    with pytest.raises(UserCountNotFoundException):
        count_model.increment_count("qwqw")


def test_decrement_count_exception(count_model: AbstractCountModel):
    with pytest.raises(UserCountNotFoundException):
        count_model.decrement_count("sgsg")


def test_reset_count_exception(count_model: AbstractCountModel):
    with pytest.raises(UserCountNotFoundException):
        count_model.reset_count("sgsg")


def test_get_count_exception(count_model: AbstractCountModel):
    with pytest.raises(UserCountNotFoundException):
        count_model.get_count("gdgd")
