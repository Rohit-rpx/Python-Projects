import project
import pytest

def test_authenticate(monkeypatch):
    monkeypatch.setattr("builtins.input",lambda _:'124632' if _ =='User id: ' else 'admin@632')
    id, name = project.authenticate()
    assert id == 124632
    assert name == 'abcd'

def test_authenticate_strid(monkeypatch):
    monkeypatch.setattr("builtins.input",lambda _:'hello' if _ =='User id: ' else 'admin@632')
    with pytest.raises(SystemExit):
        project.authenticate()

def test_authenticate_wrong_password(monkeypatch):
    monkeypatch.setattr("builtins.input",lambda _:'124632' if _ =='User id: ' else 'admin@631')
    with pytest.raises(SystemExit):
        project.authenticate()
        
def test_get_isbn_wrong(monkeypatch):
    monkeypatch.setattr("builtins.input",lambda _:'6247136747')
    assert project.get_isbn() == None

def test_get_isbn(monkeypatch):
    monkeypatch.setattr("builtins.input",lambda _:'9781449302757')
    assert project.get_isbn() == '9781449302757'

def test_search_book():
    assert project.search_book('9781449302757') == {'isbn':'9781449302757',
                                             'title':'Programming Python',
                                             'authors':"'Mark Lutz'",
                                             'quantity':10,
                                             'published date':'2010-12-14'}
    
def test_search_book_not_available(capsys):
    project.search_book('1860920225')
    message = capsys.readouterr()
    assert message.out.strip() == "Book Not found in Catalougue"

def test_search_online():
    assert project.search_online('9780596527402') == {'isbn':'9780596527402',
                                                      'title':'Dynamic HTML',
                                                      'authors':'Danny Goodman',
                                                      'published date':'2007-06-26',
                                                      'language':'en'}
    
def test_search_online_invalid():
    assert project.search_online('88242676172') == None

